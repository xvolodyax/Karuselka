#!/usr/bin/env python3
"""Unit tests for scripts/pipeline_gate.py — no extra deps."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline_gate as gate  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class PipelineGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="carusel-gate-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))
        self.repo = ROOT

    def run_cmd(self, *argv: str) -> int:
        return gate.main(["--workspace", str(self.tmp), "--repo-root", str(self.repo), *argv])

    def test_init_requires_lang_and_writes_brief(self) -> None:
        rc = self.run_cmd("init", "--lang", "ru", "--topic", "ТАРО СЕЙЧАС", "--run-id", "test-ru")
        self.assertEqual(rc, 0)
        brief = (self.tmp / "carusel-memory" / "00-brief.md").read_text(encoding="utf-8")
        self.assertIn("lang: ru", brief)
        self.assertIn("handle: @todaytaro_ru", brief)
        ledger = json.loads((self.tmp / "carusel-memory" / "pipeline-ledger.json").read_text())
        self.assertEqual(ledger["steps"]["director"]["status"], "ok")
        self.assertEqual(ledger["handle"], "@todaytaro_ru")

    def test_init_en_uses_bot_handle(self) -> None:
        self.run_cmd("init", "--lang", "en", "--topic", "Today Tarot", "--run-id", "test-en")
        brief = (self.tmp / "carusel-memory" / "00-brief.md").read_text(encoding="utf-8")
        self.assertIn("lang: en", brief)
        self.assertIn("handle: @todaytaro_bot", brief)
        self.assertIn("product: app_audio", brief)
        self.assertIn("APP audio reading", brief)

    def test_next_after_init_is_researcher(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        # capture via ledger
        ledger = gate.load_ledger(self.tmp)
        self.assertEqual(gate.first_pending(ledger), "researcher")

    def test_cannot_verify_without_dispatch(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        write(
            self.tmp / "carusel-memory" / "research" / "carousel-research-dossier.md",
            "# dossier\n",
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "researcher.md",
            "=== CARUSEL-RESEARCHER ===\nincident_report: none\n",
        )
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd("verify", "--step", "researcher")
        self.assertIn("not dispatched", str(ctx.exception))

    def test_inline_via_rejected(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd("record-dispatch", "--step", "researcher", "--via", "inline")
        self.assertIn("illegal", str(ctx.exception))

    def test_cannot_skip_researcher(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        with self.assertRaises(SystemExit):
            self.run_cmd("skip", "--step", "researcher", "--reason", "fast")

    def test_happy_researcher_then_blocks_copywriter_skip(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["researcher"]["dispatch_id"]
        write(
            self.tmp / "carusel-memory" / "research" / "carousel-research-dossier.md",
            "# dossier\nwritten_by: gemini\n## Topic\nHook lab\n## Client pain\nwait\n",
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "researcher.md",
            "\n".join(
                [
                    "=== CARUSEL-RESEARCHER ===",
                    "Статус: ✅ OK",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "written_by: gemini",
                    "incident_report: none",
                    "HANDOFF_NEXT: copywriter",
                    "",
                ]
            ),
        )
        self.assertEqual(self.run_cmd("verify", "--step", "researcher"), 0)
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd("verify", "--step", "copywriter")
        self.assertIn("not dispatched", str(ctx.exception))

    def test_copywriter_rejects_raw_url_and_wrong_handle(self) -> None:
        self.run_cmd("init", "--lang", "en", "--topic", "Today Tarot")
        self._complete_researcher()
        self.run_cmd("record-dispatch", "--step", "copywriter", "--via", "Task(carusel-copywriter)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["copywriter"]["dispatch_id"]
        slides = {
            "hook_options": [{"framework": "pain", "headline": "x", "why_it_swipes": "y"}],
            "hook_rationale": "gap",
            "slide_count": 9,
            "slides": [{"index": i, "role": "x", "headline": "h"} for i in range(1, 10)],
        }
        write(
            self.tmp / "carusel-memory" / "design" / "CAROUSEL_SLIDE_COPY.json",
            json.dumps(slides),
        )
        write(
            self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.md",
            "caption",
        )
        write(
            self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.json",
            json.dumps(
                {
                    "full_caption": "Read more https://t.me/todaytaro_bot",
                    "mentions": ["@todaytaro_ru"],
                }
            ),
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "copywriter.md",
            "\n".join(
                [
                    "=== CARUSEL-COPYWRITER ===",
                    "dispatched_via: Task(carusel-copywriter)",
                    f"dispatch_id: {dispatch_id}",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        rc = self.run_cmd("verify", "--step", "copywriter")
        self.assertEqual(rc, 2)

    def test_copywriter_rejects_bot_prize(self) -> None:
        self.run_cmd("init", "--lang", "en", "--topic", "Today Tarot")
        self._complete_researcher()
        self.run_cmd("record-dispatch", "--step", "copywriter", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["copywriter"]["dispatch_id"]
        slides = {
            "hook_options": [{"framework": "pain", "headline": "x", "why_it_swipes": "y"}],
            "hook_rationale": "gap",
            "slide_count": 9,
            "written_by": "gemini",
            "product": "bot_three_spreads",
            "slides": [{"index": i, "role": "x", "headline": "h"} for i in range(1, 9)]
            + [
                {
                    "index": 9,
                    "role": "cta",
                    "headline": "Comment PAUSE",
                    "body": "We'll DM you 3 free spreads in our bot.",
                }
            ],
        }
        write(self.tmp / "carusel-memory" / "design" / "CAROUSEL_SLIDE_COPY.json", json.dumps(slides))
        write(self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.md", "written_by: gemini\n")
        write(
            self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.json",
            json.dumps(
                {
                    "full_caption": (
                        "Comment PAUSE @todaytaro_bot. We'll DM you 3 free readings "
                        "in the bot. Links are in the profile."
                    ),
                    "mentions": ["@todaytaro_bot"],
                    "cta": "Comment PAUSE for 3 free spreads in our bot",
                    "trigger_word": "PAUSE",
                    "product": "bot_three_spreads",
                    "written_by": "gemini",
                }
            ),
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "copywriter.md",
            "\n".join(
                [
                    "=== CARUSEL-COPYWRITER ===",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "written_by: gemini",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        self.assertEqual(self.run_cmd("verify", "--step", "copywriter"), 2)

    def test_copywriter_en_ok(self) -> None:
        self.run_cmd("init", "--lang", "en", "--topic", "Today Tarot")
        self._complete_researcher()
        self.run_cmd("record-dispatch", "--step", "copywriter", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["copywriter"]["dispatch_id"]
        slides = {
            "hook_options": [{"framework": "pain", "headline": "x", "why_it_swipes": "y"}],
            "hook_rationale": "gap",
            "slide_count": 9,
            "product": "app_audio",
            "slides": [{"index": i, "role": "x", "headline": "h"} for i in range(1, 9)]
            + [
                {
                    "index": 9,
                    "role": "cta",
                    "headline": "Comment PAUSE",
                    "body": "Audio reading in the app. Essence–Shadow–Vector.",
                }
            ],
        }
        slides["written_by"] = "gemini"
        write(self.tmp / "carusel-memory" / "design" / "CAROUSEL_SLIDE_COPY.json", json.dumps(slides))
        write(self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.md", "written_by: gemini\ncaption\n")
        write(
            self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.json",
            json.dumps(
                {
                    "full_caption": (
                        "Today Tarot. Comment PAUSE @todaytaro_bot. "
                        "We'll DM an audio reading in the app: Essence–Shadow–Vector. "
                        "Links are in the profile."
                    ),
                    "mentions": ["@todaytaro_bot"],
                    "cta": (
                        "Comment PAUSE. We'll DM an audio reading in the app: "
                        "Essence–Shadow–Vector. Links are in the profile."
                    ),
                    "trigger_word": "PAUSE",
                    "product": "app_audio",
                    "written_by": "gemini",
                }
            ),
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "copywriter.md",
            "\n".join(
                [
                    "=== CARUSEL-COPYWRITER ===",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "written_by: gemini",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        self.assertEqual(self.run_cmd("verify", "--step", "copywriter"), 0)

    def test_cannot_skip_ahead_to_publish(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd("skip", "--step", "publish", "--reason", "publish-not-requested")
        self.assertIn("previous step", str(ctx.exception))

    def test_legal_skip_publish_and_fixic_after_full_prefix(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        self._force_done_until("upload")
        self.assertEqual(
            self.run_cmd("skip", "--step", "publish", "--reason", "publish-not-requested"),
            0,
        )
        self.assertEqual(
            self.run_cmd("skip", "--step", "fixic", "--reason", "no-open-incidents"),
            0,
        )
        self.assertEqual(self.run_cmd("assert-complete"), 0)

    def test_open_incident_blocks_fixic_skip(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        self._force_done_until("upload")
        self.run_cmd("skip", "--step", "publish", "--reason", "publish-not-requested")
        write(
            self.tmp / "carusel-memory" / "pipeline-fix-queue.md",
            "## INC-1\nstatus: open\n",
        )
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd("skip", "--step", "fixic", "--reason", "no-open-incidents")
        self.assertIn("open incidents", str(ctx.exception))

    def test_dispatch_prompt_contains_skill_and_nonce(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        rc = self.run_cmd("dispatch-prompt", "--step", "researcher")
        self.assertEqual(rc, 0)
        packet = (self.tmp / "carusel-memory" / "dispatches" / "researcher.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("You are carusel-researcher", packet)
        self.assertIn("skills/carusel-researcher/SKILL.md", packet)
        self.assertIn("dispatch_id:", packet)
        self.assertIn("Do only this step", packet)
        self.assertIn("shared/swarm-spawn-contract.md", packet)
        self.assertIn("required_model: gemini-3.7-flash-high", packet)
        self.assertIn("Task(generalPurpose, model=gemini-3.7-flash-high)", packet)

    def test_wrong_plugin_task_name_rejected(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        with self.assertRaises(SystemExit):
            self.run_cmd("record-dispatch", "--step", "slice", "--via", "Task(carusel-publish)")

    def _complete_researcher(self) -> None:
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["researcher"]["dispatch_id"]
        write(
            self.tmp / "carusel-memory" / "research" / "carousel-research-dossier.md",
            "# d\nwritten_by: gemini\n## Topic\npain and meaning\n",
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "researcher.md",
            "\n".join(
                [
                    "=== CARUSEL-RESEARCHER ===",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "written_by: gemini",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        self.assertEqual(self.run_cmd("verify", "--step", "researcher"), 0)

    def _force_done_until(self, last: str) -> None:
        """Mark prefix steps ok in ledger only — used to test legal skip order."""
        ledger = gate.load_ledger(self.tmp)
        for step_id in gate.STEP_IDS:
            if step_id == "director":
                continue
            ledger["steps"][step_id]["status"] = "ok"
            ledger["steps"][step_id]["dispatched_via"] = f"Task({gate.PLUGIN_TASK[step_id]})"
            if step_id == last:
                break
        gate.save_ledger(self.tmp, ledger)


class GeminiAndDryRunTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="carusel-gate-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))
        self.repo = ROOT

    def run_cmd(self, *argv: str) -> int:
        return gate.main(["--workspace", str(self.tmp), "--repo-root", str(self.repo), *argv])

    def test_researcher_defaults_to_gemini(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        self.assertEqual(
            self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)"),
            0,
        )
        ledger = gate.load_ledger(self.tmp)
        self.assertEqual(ledger["steps"]["researcher"]["model"], gate.GEMINI_MODEL)

    def test_wrong_gemini_model_rejected(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd(
                "record-dispatch",
                "--step",
                "researcher",
                "--via",
                "Task(generalPurpose)",
                "--model",
                "inherit",
            )
        self.assertIn("gemini-3.7-flash-high", str(ctx.exception))

    def test_copywriter_wrong_model_rejected(self) -> None:
        self.run_cmd("init", "--lang", "en")
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        ledger["steps"]["researcher"]["status"] = "ok"
        gate.save_ledger(self.tmp, ledger)
        with self.assertRaises(SystemExit) as ctx:
            self.run_cmd(
                "record-dispatch",
                "--step",
                "copywriter",
                "--via",
                "Task(generalPurpose)",
                "--model",
                "composer-2.5",
            )
        self.assertIn("gemini-3.7-flash-high", str(ctx.exception))

    def test_dry_run_records_eleven_workers_without_pixels(self) -> None:
        rc = self.run_cmd("dry-run", "--lang", "ru", "--topic", "ТАРО СЕЙЧАС")
        self.assertEqual(rc, 0)
        ledger = gate.load_ledger(self.tmp)
        self.assertEqual(ledger["mode"], "dry-run")
        self.assertEqual(ledger["pixels"], "forbidden")
        self.assertEqual(ledger["steps"]["director"]["status"], "ok")
        for step_id in gate.DRY_RUN_WORKERS:
            state = ledger["steps"][step_id]
            self.assertEqual(state["status"], "ok", step_id)
            self.assertEqual(state["dispatched_via"], "Task(generalPurpose)", step_id)
            self.assertTrue(state.get("dispatch_id"), step_id)
        self.assertEqual(ledger["steps"]["publish"]["status"], "skipped")
        self.assertEqual(ledger["steps"]["publish"]["skip_reason"], "publish-not-requested")
        self.assertEqual(ledger["steps"]["fixic"]["status"], "skipped")
        self.assertEqual(ledger["steps"]["fixic"]["skip_reason"], "no-open-incidents")
        self.assertEqual(ledger["steps"]["researcher"]["model"], gate.GEMINI_MODEL)
        self.assertEqual(ledger["steps"]["copywriter"]["model"], gate.GEMINI_MODEL)
        pixels = [
            p
            for p in self.tmp.rglob("*")
            if p.is_file() and p.suffix.lower() in gate.PIXEL_SUFFIXES
        ]
        self.assertEqual(pixels, [])
        caption = json.loads(
            (self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.json").read_text()
        )
        self.assertEqual(caption["trigger_word"], "ПАУЗА")
        self.assertEqual(caption["product"], "app_audio")
        self.assertIn("аудиоразбор", caption["full_caption"])
        self.assertNotIn("3 free", caption["full_caption"].lower())
        self.assertEqual(self.run_cmd("assert-complete"), 0)

    def test_copywriter_dispatch_prompt_owns_caption(self) -> None:
        self.run_cmd("init", "--lang", "en")
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        ledger["steps"]["researcher"]["status"] = "ok"
        gate.save_ledger(self.tmp, ledger)
        self.run_cmd("record-dispatch", "--step", "copywriter", "--via", "Task(generalPurpose)")
        self.assertEqual(self.run_cmd("dispatch-prompt", "--step", "copywriter"), 0)
        packet = (self.tmp / "carusel-memory" / "dispatches" / "copywriter.md").read_text()
        self.assertIn("Caption is THIS step", packet)
        self.assertIn("required_model: gemini-3.7-flash-high", packet)
        self.assertIn("written_by: gemini", packet)
        self.assertIn("cta-app-audio-contract.md", packet)
        self.assertIn("app_audio", packet)
        self.assertNotIn("Telegram bot, not an app", packet)

    def _complete_researcher(self) -> None:
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["researcher"]["dispatch_id"]
        write(
            self.tmp / "carusel-memory" / "research" / "carousel-research-dossier.md",
            "# d\nwritten_by: gemini\n## Topic\npain and meaning\n",
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "researcher.md",
            "\n".join(
                [
                    "=== CARUSEL-RESEARCHER ===",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "written_by: gemini",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        self.assertEqual(self.run_cmd("verify", "--step", "researcher"), 0)

    def test_copy_rejected_without_written_by_gemini(self) -> None:
        self.run_cmd("init", "--lang", "en")
        self._complete_researcher()
        self.run_cmd("record-dispatch", "--step", "copywriter", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["copywriter"]["dispatch_id"]
        slides = {
            "written_by": "opus",
            "hook_options": [{"framework": "pain", "headline": "x", "why_it_swipes": "y"}],
            "hook_rationale": "gap",
            "slide_count": 9,
            "slides": [{"index": i, "role": "x", "headline": "h"} for i in range(1, 10)],
        }
        write(self.tmp / "carusel-memory" / "design" / "CAROUSEL_SLIDE_COPY.json", json.dumps(slides))
        write(self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.md", "written_by: sonnet\n")
        write(
            self.tmp / "carusel-memory" / "design" / "CAROUSEL_CAPTION.json",
            json.dumps(
                {
                    "full_caption": "Comment PAUSE @todaytaro_bot",
                    "mentions": ["@todaytaro_bot"],
                    "trigger_word": "PAUSE",
                    "product": "bot_three_spreads",
                    "written_by": "composer",
                }
            ),
        )
        write(
            self.tmp / "carusel-memory" / "fragments" / "copywriter.md",
            "\n".join(
                [
                    "=== CARUSEL-COPYWRITER ===",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "written_by: opus",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        rc = self.run_cmd("verify", "--step", "copywriter")
        self.assertEqual(rc, 2)

    def test_researcher_rejected_without_written_by(self) -> None:
        self.run_cmd("init", "--lang", "ru")
        self.run_cmd("record-dispatch", "--step", "researcher", "--via", "Task(generalPurpose)")
        ledger = gate.load_ledger(self.tmp)
        dispatch_id = ledger["steps"]["researcher"]["dispatch_id"]
        write(self.tmp / "carusel-memory" / "research" / "carousel-research-dossier.md", "# only caption\n")
        write(
            self.tmp / "carusel-memory" / "fragments" / "researcher.md",
            "\n".join(
                [
                    "=== CARUSEL-RESEARCHER ===",
                    "dispatched_via: Task(generalPurpose)",
                    f"dispatch_id: {dispatch_id}",
                    "incident_report: none",
                    "",
                ]
            ),
        )
        self.assertEqual(self.run_cmd("verify", "--step", "researcher"), 2)


if __name__ == "__main__":
    unittest.main()
