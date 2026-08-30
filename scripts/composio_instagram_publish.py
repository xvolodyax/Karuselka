#!/usr/bin/env python3
"""Publish a GATE-PASS 9+9 static PNG carousel to Instagram via Composio.

Canon:
- API key only from env COMPOSIO_API_KEY. Never log, print, or write the key.
- Alias is required (never the default account):
    instagram-ru = @todaytaro_ru
    instagram-en = @todaytaro_bot
- Telegram is forbidden.
- No key + GATE PASS → SKIP «нет COMPOSIO_API_KEY», exit 0.
- GATE FAIL / чужое лицо / CTA бота → do not publish, exit 2.
- Already-live today's carousels are not republished.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

import requests

import cta_canon
from face_gate import NO_FACE, check_face, is_live_host_face_pack
from publish_preflight import load_publish_urls

API_KEY_ENV = "COMPOSIO_API_KEY"
API_BASE_ENV = "COMPOSIO_API_BASE"
DEFAULT_API_BASE = "https://backend.composio.dev/api/v3"
SKIP_NO_KEY = "нет COMPOSIO_API_KEY"
SKIP_ALREADY_LIVE = "already-live"
FORBIDDEN_TOOLKITS = ("telegram", "TELEGRAM")

ALIASES = {"ru": "instagram-ru", "en": "instagram-en"}
HANDLES = {"ru": "@todaytaro_ru", "en": "@todaytaro_bot"}
EXPECTED_USERNAME = {"ru": "todaytaro_ru", "en": "todaytaro_bot"}
FACE_LOCK = NO_FACE
LEGACY_FACE_LOCK = "Виктория.png"
RAW_URL_RE = re.compile(r"https?://|instagram\.com/|t\.me/|telegram\.me/", re.I)
GATE_PASS_RE = re.compile(r"^verdict:\s*PASS\s*$", re.I | re.M)
DEFAULT_ACCOUNT_RE = re.compile(r"\bdefault\b", re.I)
SECRET_ENV_NAMES = (API_KEY_ENV, "COMPOSIO_API_KEY")

Transport = Callable[[str, str, dict[str, str], dict[str, Any] | None], dict[str, Any]]


class PublishBlocked(RuntimeError):
    """Hard stop — do not post."""


class PublishSkip(RuntimeError):
    """Legal skip — GATE may be PASS, but do not post."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(detail or reason)
        self.reason = reason
        self.detail = detail or reason


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def read_api_key(env: dict[str, str] | None = None) -> str | None:
    source = env if env is not None else os.environ
    raw = source.get(API_KEY_ENV)
    if raw is None:
        return None
    key = raw.strip()
    return key or None


def redact_secrets(text: str, env: dict[str, str] | None = None) -> str:
    """Strip any known secret values from text that might be logged or written."""
    source = env if env is not None else os.environ
    out = str(text)
    for name in SECRET_ENV_NAMES:
        val = (source.get(name) or "").strip()
        if val:
            out = out.replace(val, "[REDACTED]")
    out = re.sub(r"(?i)(x-api-key|authorization|bearer)\s*[:=]\s*\S+", r"\1: [REDACTED]", out)
    return out


def api_base(env: dict[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    return (source.get(API_BASE_ENV) or DEFAULT_API_BASE).rstrip("/")


def required_alias(lang: str) -> str:
    if lang not in ALIASES:
        raise PublishBlocked(f"lang must be ru|en, got {lang!r}")
    return ALIASES[lang]


def default_headers(api_key: str) -> dict[str, str]:
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def http_transport(
    method: str,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any] | None,
    timeout: int = 180,
) -> dict[str, Any]:
    try:
        resp = requests.request(
            method,
            url,
            headers=headers,
            json=payload,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise PublishBlocked(redact_secrets(f"Composio HTTP error: {exc}")) from exc
    try:
        data = resp.json() if resp.content else {}
    except ValueError:
        data = {"raw": redact_secrets(resp.text[:400])}
    if not isinstance(data, dict):
        data = {"data": data}
    if resp.status_code >= 400:
        raise PublishBlocked(
            redact_secrets(f"Composio HTTP {resp.status_code}: {data}")
        )
    return data


def flatten_accounts(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("items", "connected_accounts", "connectedAccounts", "accounts", "data"):
        if key in payload:
            found = flatten_accounts(payload[key])
            if found:
                return found
    if payload.get("id") or payload.get("alias") or payload.get("nanoid"):
        return [payload]
    return []


def account_alias(account: dict[str, Any]) -> str:
    return str(account.get("alias") or account.get("name") or "").strip()


def account_id(account: dict[str, Any]) -> str:
    return str(
        account.get("id")
        or account.get("nanoid")
        or account.get("connected_account_id")
        or account.get("connectedAccountId")
        or ""
    ).strip()


def account_username(account: dict[str, Any]) -> str:
    info = account.get("user_info") or account.get("userInfo") or {}
    if isinstance(info, dict):
        return str(info.get("username") or info.get("name") or "").lstrip("@")
    return str(account.get("username") or "").lstrip("@")


def is_default_account(account: dict[str, Any]) -> bool:
    if account.get("is_default") is True or account.get("isDefault") is True:
        return True
    return False


def resolve_account_by_alias(
    accounts: list[dict[str, Any]],
    *,
    lang: str,
    allow_default: bool = False,
) -> dict[str, Any]:
    alias = required_alias(lang)
    handle = HANDLES[lang]
    expected_user = EXPECTED_USERNAME[lang]
    matches = [acc for acc in accounts if account_alias(acc) == alias]
    if not matches:
        raise PublishBlocked(
            f"Composio Instagram alias {alias} ({handle}) not found. "
            "Alias is required; default account is forbidden."
        )
    if len(matches) > 1:
        raise PublishBlocked(f"multiple Composio accounts share alias {alias}")
    acc = matches[0]
    if not allow_default and is_default_account(acc) and account_alias(acc) != alias:
        raise PublishBlocked(f"refusing default Instagram account for lang={lang}")
    username = account_username(acc)
    if username and username != expected_user:
        raise PublishBlocked(
            f"alias {alias} is connected to @{username}, expected {handle}"
        )
    if not account_id(acc):
        raise PublishBlocked(f"alias {alias} has no connected account id")
    return acc


def list_instagram_accounts(
    api_key: str,
    *,
    transport: Transport,
    env: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    url = f"{api_base(env)}/connected_accounts"
    data = transport("GET", url, default_headers(api_key), None)
    accounts = flatten_accounts(data)
    instagram = []
    for acc in accounts:
        toolkit = str(
            acc.get("toolkit")
            or acc.get("toolkit_slug")
            or acc.get("appName")
            or acc.get("appUniqueId")
            or ""
        ).lower()
        slug = str(acc.get("slug") or "").lower()
        if toolkit in {"instagram", "instagram_"} or "instagram" in toolkit or slug == "instagram":
            instagram.append(acc)
        elif account_alias(acc).startswith("instagram-"):
            instagram.append(acc)
    return instagram or accounts


def execute_tool(
    api_key: str,
    slug: str,
    arguments: dict[str, Any],
    connected_account_id: str,
    *,
    transport: Transport,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    if any(name.lower() in slug.lower() for name in FORBIDDEN_TOOLKITS):
        raise PublishBlocked("Telegram tools are forbidden")
    if not connected_account_id:
        raise PublishBlocked("connected_account_id is required (alias, not default)")
    url = f"{api_base(env)}/tools/execute/{slug}"
    payload = {
        "arguments": arguments,
        "connected_account_id": connected_account_id,
        "version": "latest",
        "dangerously_skip_version_check": True,
    }
    data = transport("POST", url, default_headers(api_key), payload)
    if data.get("successful") is False or data.get("error"):
        raise PublishBlocked(redact_secrets(f"{slug} failed: {data.get('error') or data}"))
    return data


def load_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_live_posts(repo_root: Path) -> list[dict[str, Any]]:
    path = repo_root / "carusel-memory" / "canon" / "live-posts.json"
    data = load_json_if_exists(path)
    posts = data.get("posts") if isinstance(data, dict) else data
    if isinstance(posts, list):
        return [p for p in posts if isinstance(p, dict)]
    return []


def pack_langs(pack: Path, manifest: dict[str, Any] | None = None) -> list[str]:
    data = manifest if manifest is not None else load_json_if_exists(pack / "PACK.json")
    langs = data.get("langs")
    if isinstance(langs, list) and langs:
        return [str(x) for x in langs]
    found = [lang for lang in ("ru", "en") if (pack / lang).is_dir()]
    return found or ["ru", "en"]


def pack_already_live(pack: Path, repo_root: Path, lang: str | None = None) -> dict[str, Any] | None:
    manifest = load_json_if_exists(pack / "PACK.json")
    pack_id = str(manifest.get("pack_id") or pack.name)
    if manifest.get("publish_as_new_post") is True:
        for post in load_live_posts(repo_root):
            if str(post.get("pack_id") or "") == pack_id:
                if lang is None or post.get("lang") == lang:
                    return post
        return None
    if manifest.get("already_live") is True:
        live = manifest.get("already_live_posts") or manifest.get("live_posts") or {}
        if lang and isinstance(live, dict) and live.get(lang):
            return {"pack_id": pack_id, "lang": lang, "permalink": live.get(lang)}
        if not lang:
            return {"pack_id": pack_id, "reason": "PACK.json already_live"}
    for post in load_live_posts(repo_root):
        if str(post.get("pack_id") or "") == pack_id:
            if lang is None or post.get("lang") == lang:
                return post
        date = str(post.get("date") or "")
        if date and date == str(manifest.get("date") or pack.name):
            if lang is None or post.get("lang") == lang:
                triggers = manifest.get("trigger_words") or {}
                if not lang or post.get("trigger") == triggers.get(lang) or not triggers:
                    return post
    return None


def read_gate_verdict(pack: Path) -> str:
    path = pack / "GATE.md"
    if not path.is_file():
        raise PublishBlocked("GATE.md missing — refuse publish")
    text = path.read_text(encoding="utf-8")
    if GATE_PASS_RE.search(text):
        return "PASS"
    return "FAIL"


def load_caption(lang_dir: Path) -> dict[str, Any]:
    for rel in (
        lang_dir / "CAROUSEL_CAPTION.json",
        lang_dir / "slides" / "CAROUSEL_CAPTION.json",
        lang_dir / "design" / "CAROUSEL_CAPTION.json",
    ):
        if rel.is_file():
            return json.loads(rel.read_text(encoding="utf-8"))
    md = lang_dir / "slides" / "CAROUSEL_CAPTION.md"
    if md.is_file():
        return {"full_caption": md.read_text(encoding="utf-8"), "product": "app_audio"}
    raise PublishBlocked(f"caption missing under {lang_dir}")


def caption_text(data: dict[str, Any]) -> str:
    return str(data.get("full_caption") or data.get("caption") or "").strip()


def slide9_blob(lang_dir: Path) -> str:
    copy_path = lang_dir / "CAROUSEL_SLIDE_COPY.json"
    if not copy_path.is_file():
        return ""
    data = json.loads(copy_path.read_text(encoding="utf-8"))
    slides = data.get("slides") or []
    for slide in slides:
        if int(slide.get("index") or 0) == 9:
            return " ".join(
                str(slide.get(k) or "") for k in ("headline", "body", "cta", "text")
            )
    return json.dumps(data, ensure_ascii=False)


def collect_image_urls(lang_dir: Path) -> list[str]:
    urls_path = lang_dir / "publish-urls.json"
    if not urls_path.is_file():
        raise PublishBlocked(f"missing {urls_path} — upload HTTPS URLs first")
    loaded = load_publish_urls(urls_path)
    order = ("file1", "file2", "File3", "file4", "file5", "file6", "file7", "file8", "file9")
    urls: list[str] = []
    for key in order:
        url = loaded.get(key)
        if not isinstance(url, str) or not url.startswith("http"):
            raise PublishBlocked(f"{urls_path} missing HTTPS {key}")
        urls.append(url)
    if len(urls) != 9:
        raise PublishBlocked(f"expected 9 static PNG URLs, got {len(urls)}")
    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            raise PublishBlocked(f"slide URL must be HTTPS: {url}")
        if url.lower().endswith(".mp4"):
            raise PublishBlocked("static PNG canon: file1 must be PNG, not mp4")
    return urls


def assert_pack_may_publish(pack: Path, repo_root: Path) -> None:
    if read_gate_verdict(pack) != "PASS":
        raise PublishBlocked("GATE FAIL — do not publish")
    face_errors = check_face(pack)
    if face_errors:
        raise PublishBlocked("чужое лицо / FACE_CHECK FAIL — " + "; ".join(face_errors))
    manifest = load_json_if_exists(pack / "PACK.json")
    pack_id = str(manifest.get("pack_id") or pack.name)
    face_lock = str(manifest.get("face_lock") or FACE_LOCK)
    if is_live_host_face_pack(pack_id):
        if face_lock != LEGACY_FACE_LOCK:
            raise PublishBlocked(f"live pack face lock must be {LEGACY_FACE_LOCK}, got {face_lock}")
    elif face_lock not in {NO_FACE, "no_host", "absent"}:
        raise PublishBlocked(f"face lock must be {NO_FACE}, got {face_lock}")
    if str(manifest.get("product") or "") == "bot_three_spreads":
        raise PublishBlocked("CTA бота — do not publish")

    for lang in pack_langs(pack, manifest):
        lang_dir = pack / lang
        if not lang_dir.is_dir():
            raise PublishBlocked(f"pack missing {lang}/")
        caption = load_caption(lang_dir)
        blob = caption_text(caption)
        if not blob:
            raise PublishBlocked(f"{lang} caption empty")
        if RAW_URL_RE.search(blob):
            raise PublishBlocked(f"{lang} caption has raw URL — do not publish")
        cta_errors = cta_canon.check_cta_offer(
            lang=lang,
            product=str(caption.get("product") or manifest.get("product") or ""),
            caption_blob=blob,
            slide9_blob=slide9_blob(lang_dir),
            prefix=lang,
        )
        if cta_errors:
            raise PublishBlocked("CTA бота / CTA FAIL — " + "; ".join(cta_errors))
        collect_image_urls(lang_dir)


def ig_user_id_from_payload(data: dict[str, Any]) -> str:
    blob = data.get("data") if isinstance(data.get("data"), dict) else data
    if not isinstance(blob, dict):
        blob = {}
    inner = blob.get("data") if isinstance(blob.get("data"), dict) else blob
    if not isinstance(inner, dict):
        inner = blob
    for key in ("id", "ig_id", "user_id", "ig_user_id"):
        val = inner.get(key)
        if val:
            return str(val)
    return "me"


def creation_id_from_payload(data: dict[str, Any]) -> str:
    blob = data.get("data") if isinstance(data.get("data"), dict) else data
    if not isinstance(blob, dict):
        raise PublishBlocked("carousel container response missing data")
    inner = blob.get("data") if isinstance(blob.get("data"), dict) else blob
    if not isinstance(inner, dict):
        inner = blob
    for key in ("id", "creation_id", "container_id"):
        val = inner.get(key)
        if val:
            return str(val)
    raise PublishBlocked(redact_secrets(f"no creation_id in {data}"))


def permalink_from_payload(data: dict[str, Any]) -> str | None:
    blob = data.get("data") if isinstance(data.get("data"), dict) else data
    if not isinstance(blob, dict):
        return None
    inner = blob.get("data") if isinstance(blob.get("data"), dict) else blob
    if not isinstance(inner, dict):
        inner = blob
    for key in ("permalink", "url", "post_url"):
        val = inner.get(key)
        if isinstance(val, str) and val.startswith("http"):
            return val
    return None


def publish_lang(
    pack: Path,
    lang: str,
    api_key: str,
    *,
    transport: Transport,
    env: dict[str, str] | None = None,
    execute: bool = True,
) -> dict[str, Any]:
    alias = required_alias(lang)
    accounts = list_instagram_accounts(api_key, transport=transport, env=env)
    acc = resolve_account_by_alias(accounts, lang=lang)
    connected_id = account_id(acc)
    caption = caption_text(load_caption(pack / lang))
    urls = collect_image_urls(pack / lang)
    result: dict[str, Any] = {
        "lang": lang,
        "alias": alias,
        "handle": HANDLES[lang],
        "connected_account_id": connected_id,
        "slide_count": 9,
        "executed": False,
    }
    if not execute:
        result["status"] = "check-only"
        return result

    info = execute_tool(
        api_key,
        "INSTAGRAM_GET_USER_INFO",
        {"ig_user_id": "me"},
        connected_id,
        transport=transport,
        env=env,
    )
    ig_user_id = ig_user_id_from_payload(info)
    container = execute_tool(
        api_key,
        "INSTAGRAM_CREATE_CAROUSEL_CONTAINER",
        {
            "ig_user_id": ig_user_id,
            "caption": caption,
            "child_image_urls": urls,
        },
        connected_id,
        transport=transport,
        env=env,
    )
    creation_id = creation_id_from_payload(container)
    published = execute_tool(
        api_key,
        "INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH",
        {
            "ig_user_id": ig_user_id,
            "creation_id": creation_id,
            "max_wait_seconds": 180,
        },
        connected_id,
        transport=transport,
        env=env,
    )
    result.update(
        {
            "status": "published",
            "executed": True,
            "ig_user_id": ig_user_id,
            "creation_id": creation_id,
            "permalink": permalink_from_payload(published),
            "media_id": creation_id_from_payload(published) if published else None,
        }
    )
    return result


def write_publish_log(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.is_file() else "# publish-log\n\n"
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def format_log(status: str, reason: str, rows: list[dict[str, Any]], extra: str = "") -> str:
    lines = [
        f"## {utc_now()}",
        f"status: {status}",
        f"reason: {reason}",
        "via: composio",
        "telegram: forbidden",
        "api_key_source: env COMPOSIO_API_KEY",
        "alias_required: instagram-ru / instagram-en (never default)",
    ]
    for row in rows:
        lines.append(
            f"- {row.get('lang')}: alias={row.get('alias')} handle={row.get('handle')} "
            f"status={row.get('status')} permalink={row.get('permalink') or '-'}"
        )
    if extra:
        lines.append(redact_secrets(extra))
    return "\n".join(lines)


def run_pack(
    pack: Path,
    repo_root: Path,
    *,
    transport: Transport | None = None,
    env: dict[str, str] | None = None,
    execute: bool = True,
    log_path: Path | None = None,
    langs: list[str] | None = None,
) -> dict[str, Any]:
    pack = pack.resolve()
    repo_root = repo_root.resolve()
    env = dict(env if env is not None else os.environ)
    transport = transport or http_transport
    log_path = log_path or (pack / "publish-log.md")

    assert_pack_may_publish(pack, repo_root)

    live = pack_already_live(pack, repo_root)
    if live:
        payload = {
            "status": "skipped",
            "reason": SKIP_ALREADY_LIVE,
            "langs": [],
            "detail": f"pack already live: {live.get('permalink') or live}",
        }
        write_publish_log(
            log_path,
            format_log("skipped", SKIP_ALREADY_LIVE, [], extra=payload["detail"]),
        )
        raise PublishSkip(SKIP_ALREADY_LIVE, payload["detail"])

    api_key = read_api_key(env)
    if not api_key:
        write_publish_log(
            log_path,
            format_log("skipped", SKIP_NO_KEY, [], extra="GATE PASS; key absent"),
        )
        raise PublishSkip(SKIP_NO_KEY, "GATE PASS; COMPOSIO_API_KEY missing")

    rows: list[dict[str, Any]] = []
    try:
        for lang in langs or pack_langs(pack):
            if lang == "en" and (load_json_if_exists(pack / "PACK.json").get("langs") == ["ru"]):
                continue
            lang_live = pack_already_live(pack, repo_root, lang=lang)
            if lang_live:
                rows.append(
                    {
                        "lang": lang,
                        "alias": required_alias(lang),
                        "handle": HANDLES[lang],
                        "status": "skipped",
                        "reason": SKIP_ALREADY_LIVE,
                        "permalink": lang_live.get("permalink"),
                    }
                )
                continue
            rows.append(
                publish_lang(
                    pack,
                    lang,
                    api_key,
                    transport=transport,
                    env=env,
                    execute=execute,
                )
            )
    except Exception as exc:
        write_publish_log(
            log_path,
            format_log("fail", "composio-error", rows, extra=redact_secrets(str(exc), env)),
        )
        raise

    status = "ok" if execute else "check-only"
    write_publish_log(log_path, format_log(status, "composio", rows))
    if (pack / "ru").is_dir():
        write_publish_log(pack / "ru" / "publish-log.md", format_log(status, "composio", rows))
    if (pack / "en").is_dir():
        write_publish_log(pack / "en" / "publish-log.md", format_log(status, "composio", rows))
    return {"status": status, "reason": "composio", "langs": rows}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Publish RU+EN carousel via Composio Instagram")
    p.add_argument("--pack", help="dated pack dir, e.g. carusel-memory/packs/2026-08-29")
    p.add_argument("--workspace", default=".", help="unused workspace root (Director compatibility)")
    p.add_argument("--repo-root", default=str(repo_root_from_script()))
    p.add_argument(
        "--check-only",
        action="store_true",
        help="GATE + alias checks only; do not call Instagram publish",
    )
    p.add_argument(
        "--lang",
        action="append",
        choices=("ru", "en"),
        help="Publish only these langs (repeatable). Default: PACK.json langs.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not args.pack:
        print("ERROR: --pack is required", file=sys.stderr)
        return 2
    pack = Path(args.pack)
    if not pack.is_absolute():
        pack = (repo_root / pack).resolve()
    try:
        result = run_pack(
            pack,
            repo_root,
            execute=not args.check_only,
            langs=args.lang,
        )
    except PublishSkip as skip:
        print(f"GATE PASS")
        print(f"publish: SKIP {skip.reason}")
        print(redact_secrets(skip.detail))
        return 0
    except PublishBlocked as blocked:
        print(f"publish: REFUSE {redact_secrets(str(blocked))}", file=sys.stderr)
        return 2
    print(f"publish: {result['status']}")
    for row in result.get("langs") or []:
        print(
            f"- {row.get('lang')} alias={row.get('alias')} "
            f"status={row.get('status')} permalink={row.get('permalink') or '-'}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
