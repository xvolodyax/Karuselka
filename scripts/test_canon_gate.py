#!/usr/bin/env python3
"""canon_gate rejects mechanic hooks and missing animal metaphors."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import canon_gate as gate


def write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, str):
        path.write_text(obj, encoding="utf-8")
    else:
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


class CanonGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="canon-gate-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def test_real_pack_passes(self) -> None:
        pack = Path(__file__).resolve().parent.parent / "carusel-memory/packs/2026-08-27-v2"
        if not pack.is_dir():
            self.skipTest("pack not in workspace")
        self.assertEqual(gate.check_pack(pack), [])

    def test_mechanic_hook_and_vibe_fail(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "visual_family": "brand_collage",
                "langs": ["ru"],
                "trigger_words": {"ru": "ПАУЗА"},
            },
        )
        slides = {
            "slide_count": 9,
            "visual_family": "brand_collage",
            "hook_is_scene": False,
            "slides": [
                {"index": i, "role": "value", "headline": "5 признаков паузы", "body": "vibe"}
                for i in range(1, 10)
            ],
        }
        write(pack / "ru" / "CAROUSEL_SLIDE_COPY.json", slides)
        errors = " ".join(gate.check_pack(pack))
        self.assertIn("animals_viktoria_collage", errors)
        self.assertIn("hook_is_scene", errors)


if __name__ == "__main__":
    unittest.main()
