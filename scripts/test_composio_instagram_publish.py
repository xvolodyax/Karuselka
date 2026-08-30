#!/usr/bin/env python3
"""Unit tests for Composio Instagram publish — no live posts, no real key."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import composio_instagram_publish as pub  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


CAPTION = {
    "ru": {
        "full_caption": (
            "Он молчит про статус. Напиши в комментариях слово СТАТУС. "
            "В Direct пришлём аудиоразбор в моём приложении: Суть – Тень – Вектор. "
            "Ссылки в шапке профиля."
        ),
        "product": "app_audio",
        "trigger_word": "СТАТУС",
        "mentions": ["@todaytaro_ru"],
    },
    "en": {
        "full_caption": (
            "He won't define it. Comment the word LABELS below. "
            "We'll DM an audio reading in the app: Essence–Shadow–Vector. "
            "Links are in the profile."
        ),
        "product": "app_audio",
        "trigger_word": "LABELS",
        "mentions": ["@todaytaro_bot"],
    },
}

SLIDE9 = {
    "ru": {
        "index": 9,
        "role": "cta",
        "headline": "Напиши СТАТУС",
        "body": "Аудиоразбор в приложении. Суть – Тень – Вектор.",
    },
    "en": {
        "index": 9,
        "role": "cta",
        "headline": "Comment LABELS",
        "body": "Audio reading in the app. Essence–Shadow–Vector.",
    },
}


class FakeTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def __call__(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any] | None,
    ) -> dict[str, Any]:
        self.calls.append((method, url, payload))
        if "connected_accounts" in url:
            return {
                "items": [
                    {
                        "id": "instagram_inroad-levis",
                        "alias": "instagram-ru",
                        "is_default": False,
                        "toolkit": "instagram",
                        "user_info": {"id": "1", "username": "todaytaro_ru"},
                    },
                    {
                        "id": "instagram_mede-racily",
                        "alias": "instagram-en",
                        "is_default": True,
                        "toolkit": "instagram",
                        "user_info": {"id": "2", "username": "todaytaro_bot"},
                    },
                ]
            }
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        if slug == "INSTAGRAM_GET_USER_INFO":
            return {"successful": True, "data": {"id": "17841472502146787"}}
        if slug == "INSTAGRAM_CREATE_CAROUSEL_CONTAINER":
            return {"successful": True, "data": {"id": "container-1"}}
        if slug == "INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH":
            return {
                "successful": True,
                "data": {
                    "id": "media-1",
                    "permalink": "https://www.instagram.com/p/TESTONLY/",
                },
            }
        raise AssertionError(f"unexpected Composio call {method} {url}")


class ComposioPublishTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="composio-pub-"))
        self.pack = self.tmp / "pack"
        self.repo = self.tmp / "repo"
        (self.repo / "carusel-memory" / "canon").mkdir(parents=True)
        write_json(self.repo / "carusel-memory" / "canon" / "live-posts.json", {"posts": []})
        self._write_valid_pack(self.pack, pack_id="test-pack")

    def _write_valid_pack(self, pack: Path, pack_id: str, already_live: bool = False) -> None:
        write(
            pack / "GATE.md",
            "Verdict: PASS\n- (a) face lock = Виктория.png\n",
        )
        write(
            pack / "FACE_CHECK.md",
            "verdict: MATCH\ncompared: Виктория.png\nnot Alena\n",
        )
        write_json(
            pack / "PACK.json",
            {
                "pack_id": pack_id,
                "date": pack_id,
                "face_lock": "Виктория.png",
                "product": "app_audio",
                "already_live": already_live,
                "already_live_posts": {
                    "ru": "https://www.instagram.com/p/Dcnrh0nm7pp/",
                    "en": "https://www.instagram.com/p/Dcnrht_lVca/",
                }
                if already_live
                else {},
                "trigger_words": {"ru": "СТАТУС", "en": "LABELS"},
            },
        )
        for lang in ("ru", "en"):
            write_json(pack / lang / "CAROUSEL_CAPTION.json", CAPTION[lang])
            write_json(
                pack / lang / "CAROUSEL_SLIDE_COPY.json",
                {
                    "product": "app_audio",
                    "slide_count": 9,
                    "slides": [{"index": i, "headline": f"s{i}"} for i in range(1, 9)]
                    + [SLIDE9[lang]],
                },
            )
            files = {}
            for i, key in enumerate(
                ("file1", "file2", "File3", "file4", "file5", "file6", "file7", "file8", "file9"),
                start=1,
            ):
                files[key] = {
                    "url": f"https://cdn.example.test/{pack_id}/{lang}/slide-{i:02d}.png"
                }
            write_json(pack / lang / "publish-urls.json", {"files": files})

    def test_no_key_gate_pass_skips(self) -> None:
        with self.assertRaises(pub.PublishSkip) as ctx:
            pub.run_pack(
                self.pack,
                self.repo,
                env={},
                execute=True,
                transport=FakeTransport(),
            )
        self.assertEqual(ctx.exception.reason, "нет COMPOSIO_API_KEY")
        log = (self.pack / "publish-log.md").read_text(encoding="utf-8")
        self.assertIn("нет COMPOSIO_API_KEY", log)
        self.assertNotIn("sk-secret", log)

    def test_key_never_written_to_log(self) -> None:
        secret = "cmp_super_secret_key_do_not_leak"
        transport = FakeTransport()
        result = pub.run_pack(
            self.pack,
            self.repo,
            env={"COMPOSIO_API_KEY": secret},
            execute=True,
            transport=transport,
        )
        self.assertEqual(result["status"], "ok")
        log = (self.pack / "publish-log.md").read_text(encoding="utf-8")
        self.assertNotIn(secret, log)
        self.assertNotIn("cmp_super", log)
        dumped = json.dumps(result)
        self.assertNotIn(secret, dumped)

    def test_cli_no_key_exits_zero(self) -> None:
        import os

        old = os.environ.pop("COMPOSIO_API_KEY", None)
        try:
            rc = pub.main(["--pack", str(self.pack), "--repo-root", str(self.repo)])
        finally:
            if old is not None:
                os.environ["COMPOSIO_API_KEY"] = old
        self.assertEqual(rc, 0)

    def test_already_live_skips_without_composio_call(self) -> None:
        self._write_valid_pack(self.pack, pack_id="2026-08-29", already_live=True)
        transport = FakeTransport()
        with self.assertRaises(pub.PublishSkip) as ctx:
            pub.run_pack(
                self.pack,
                self.repo,
                env={"COMPOSIO_API_KEY": "cmp_should_not_be_used"},
                execute=True,
                transport=transport,
            )
        self.assertEqual(ctx.exception.reason, "already-live")
        self.assertEqual(transport.calls, [])

    def test_live_posts_registry_skips(self) -> None:
        write_json(
            self.repo / "carusel-memory" / "canon" / "live-posts.json",
            {
                "posts": [
                    {
                        "pack_id": "test-pack",
                        "lang": "ru",
                        "permalink": "https://www.instagram.com/p/Dcnrh0nm7pp/",
                    }
                ]
            },
        )
        transport = FakeTransport()
        with self.assertRaises(pub.PublishSkip) as ctx:
            pub.run_pack(
                self.pack,
                self.repo,
                env={"COMPOSIO_API_KEY": "cmp_unused"},
                execute=True,
                transport=transport,
            )
        self.assertEqual(ctx.exception.reason, "already-live")
        self.assertEqual(transport.calls, [])

    def test_gate_fail_refuses(self) -> None:
        write(self.pack / "GATE.md", "Verdict: FAIL\n- face is Alena\n")
        with self.assertRaises(pub.PublishBlocked) as ctx:
            pub.run_pack(
                self.pack,
                self.repo,
                env={"COMPOSIO_API_KEY": "cmp_unused"},
                execute=True,
                transport=FakeTransport(),
            )
        self.assertIn("GATE FAIL", str(ctx.exception))

    def test_bot_cta_refuses(self) -> None:
        write_json(
            self.pack / "ru" / "CAROUSEL_CAPTION.json",
            {
                "full_caption": (
                    "Comment PAUSE. We'll DM you 3 free readings in the bot. "
                    "Links are in the profile."
                ),
                "product": "bot_three_spreads",
            },
        )
        with self.assertRaises(pub.PublishBlocked) as ctx:
            pub.run_pack(
                self.pack,
                self.repo,
                env={"COMPOSIO_API_KEY": "cmp_unused"},
                execute=True,
                transport=FakeTransport(),
            )
        self.assertIn("CTA", str(ctx.exception))

    def test_raw_url_in_caption_refuses(self) -> None:
        bad = dict(CAPTION["ru"])
        bad["full_caption"] = (
            CAPTION["ru"]["full_caption"] + " https://t.me/todaytaro_bot"
        )
        write_json(self.pack / "ru" / "CAROUSEL_CAPTION.json", bad)
        with self.assertRaises(pub.PublishBlocked) as ctx:
            pub.run_pack(
                self.pack,
                self.repo,
                env={"COMPOSIO_API_KEY": "cmp_unused"},
                execute=True,
                transport=FakeTransport(),
            )
        self.assertIn("raw URL", str(ctx.exception))

    def test_alias_required_never_default(self) -> None:
        accounts = [
            {
                "id": "instagram_mede-racily",
                "alias": "instagram-en",
                "is_default": True,
                "user_info": {"username": "todaytaro_bot"},
            }
        ]
        with self.assertRaises(pub.PublishBlocked) as ctx:
            pub.resolve_account_by_alias(accounts, lang="ru")
        self.assertIn("instagram-ru", str(ctx.exception))
        self.assertIn("default", str(ctx.exception).lower())

        ru = pub.resolve_account_by_alias(
            accounts
            + [
                {
                    "id": "instagram_inroad-levis",
                    "alias": "instagram-ru",
                    "is_default": False,
                    "user_info": {"username": "todaytaro_ru"},
                }
            ],
            lang="ru",
        )
        self.assertEqual(ru["alias"], "instagram-ru")
        self.assertEqual(pub.required_alias("en"), "instagram-en")

    def test_wrong_username_on_alias_refuses(self) -> None:
        with self.assertRaises(pub.PublishBlocked):
            pub.resolve_account_by_alias(
                [
                    {
                        "id": "x",
                        "alias": "instagram-ru",
                        "user_info": {"username": "todaytaro_bot"},
                    }
                ],
                lang="ru",
            )

    def test_redact_secrets(self) -> None:
        env = {"COMPOSIO_API_KEY": "cmp_leak_me"}
        self.assertEqual(
            pub.redact_secrets("key=cmp_leak_me used", env),
            "key=[REDACTED] used",
        )

    def test_execute_uses_alias_account_not_default(self) -> None:
        transport = FakeTransport()
        pub.run_pack(
            self.pack,
            self.repo,
            env={"COMPOSIO_API_KEY": "cmp_test_key"},
            execute=True,
            transport=transport,
        )
        posts = [c for c in transport.calls if c[0] == "POST"]
        self.assertTrue(posts)
        used_ids = {c[2]["connected_account_id"] for c in posts if c[2]}
        self.assertIn("instagram_inroad-levis", used_ids)
        self.assertIn("instagram_mede-racily", used_ids)
        slugs = [c[1].rsplit("/", 1)[-1] for c in posts]
        self.assertNotIn("TELEGRAM_SEND_MESSAGE", slugs)
        for call in posts:
            self.assertIn(call[2]["connected_account_id"], used_ids)


if __name__ == "__main__":
    unittest.main()
