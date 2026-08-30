#!/usr/bin/env python3
"""face_gate requires pixel FACE_CHECK, not honey/wheat prose."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import face_gate


def write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, bytes):
        path.write_bytes(obj)
    elif isinstance(obj, str):
        path.write_text(obj, encoding="utf-8")
    else:
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


class FaceGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="face-gate-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def test_legacy_pack_skips(self) -> None:
        pack = self.tmp / "pack"
        write(pack / "PACK.json", {"pack_id": "2026-08-27-swarm"})
        self.assertEqual(face_gate.check_face(pack), [])

    def test_missing_face_check_fails_when_pixels_exist(self) -> None:
        pack = self.tmp / "pack"
        write(pack / "PACK.json", {"pack_id": "2026-08-28"})
        write(pack / "ru" / "slides" / "slide-01.png", b"\x00" * 12_000)
        errors = " ".join(face_gate.check_face(pack))
        self.assertIn("FACE_CHECK.md", errors)

    def test_hair_prose_and_brown_eyes_fail(self) -> None:
        pack = self.tmp / "pack"
        write(pack / "PACK.json", {"pack_id": "2026-08-28"})
        write(pack / "ru" / "slides" / "slide-01.png", b"\x00" * 12_000)
        write(
            pack / "FACE_CHECK.md",
            "verdict: MATCH\ncompared Виктория.png\nhoney/wheat blonde\neyes are brown\n",
        )
        for name in (
            "Виктория.png",
            "ru-slide-01-face.png",
            "ru-slide-09-face.png",
            "en-slide-01-face.png",
            "en-slide-09-face.png",
        ):
            write(pack / "face-check" / name, b"\x00" * 1500)
        errors = " ".join(face_gate.check_face(pack))
        self.assertIn("hair-prose", errors.lower() + errors)
        self.assertTrue(
            "brown/grey" in errors or "green" in errors or "hazel" in errors,
            errors,
        )


if __name__ == "__main__":
    unittest.main()
