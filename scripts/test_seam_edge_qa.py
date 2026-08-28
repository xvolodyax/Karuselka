#!/usr/bin/env python3
"""Seam leftover strip + 4K remainder WARN (INC-20260828-0948)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

import grid_gutter_qa as qa
import kie_carousel_gen as gen


class LeftoverStripTest(unittest.TestCase):
    def test_kie_4k_remainder_is_2(self) -> None:
        self.assertEqual(gen.leftover_gutter_px(2480, 3312), 2)
        self.assertEqual(gen.leftover_gutter_px(2478, 3312), 0)

    def test_seam_strip_at_least_default_10(self) -> None:
        self.assertEqual(gen.seam_edge_strip_px(2480, 3312), 10)
        self.assertEqual(gen.seam_edge_strip_px(2478, 3312), 10)
        self.assertEqual(gen.seam_edge_strip_px(2480, 3312, default=1), 2)

    def test_known_4k_remainder_helper(self) -> None:
        self.assertTrue(
            qa.is_known_kie_4k_seam_remainder(
                {"width": 2480, "height": 3312},
                {"width": 2, "height": 0},
                3,
                3,
            )
        )
        self.assertFalse(
            qa.is_known_kie_4k_seam_remainder(
                {"width": 2478, "height": 3312},
                {"width": 0, "height": 0},
                3,
                3,
            )
        )
        self.assertFalse(
            qa.is_known_kie_4k_seam_remainder(
                {"width": 11, "height": 12},
                {"width": 2, "height": 0},
                3,
                3,
            )
        )


class SeamQaModeTest(unittest.TestCase):
    def _seamed(self, w: int, h: int, gutter: int = 8) -> Image.Image:
        img = Image.new("RGB", (w, h), (20, 20, 20))
        draw = ImageDraw.Draw(img)
        half = gutter // 2
        for x in (w // 3, 2 * w // 3):
            draw.rectangle((x - half, 0, x + half, h - 1), fill=(255, 255, 255))
        for y in (h // 3, 2 * h // 3):
            draw.rectangle((0, y - half, w - 1, y + half), fill=(255, 255, 255))
        return img

    def _slides(self, folder: Path, n: int = 9, size: tuple[int, int] = (36, 48)) -> None:
        folder.mkdir(parents=True, exist_ok=True)
        for i in range(1, n + 1):
            Image.new("RGB", size, (30, 30, 30)).save(folder / f"slide-{i:02d}.png")

    def test_crop_remainder_drops_kie_style_leftover(self) -> None:
        img = Image.new("RGB", (11, 12), (20, 20, 20))
        cropped = qa.crop_remainder(img, 3, 3)
        self.assertEqual(cropped.size, (9, 12))

    def test_equal_mode_fails_nonzero_remainder(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="seam-qa-eq-"))
        master = tmp / "master.png"
        Image.new("RGB", (11, 12), (20, 20, 20)).save(master)
        slides = tmp / "slides"
        self._slides(slides, size=(12, 16))
        out = tmp / "report.json"
        old = sys.argv
        sys.argv = [
            "grid_gutter_qa.py",
            "--master",
            str(master),
            "--slides-dir",
            str(slides),
            "--mode",
            "equal",
            "--output",
            str(out),
        ]
        try:
            code = qa.main()
        finally:
            sys.argv = old
        self.assertEqual(code, 2)
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "fail")
        self.assertTrue(any("not divisible" in f for f in data["failures"]))

    def test_seam_mode_scrubs_internal_lines_on_copy(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="seam-qa-"))
        master = tmp / "master.png"
        self._seamed(300, 399, gutter=8).save(master)
        slides = tmp / "slides"
        self._slides(slides)
        raw = qa.analyze_master(master, 3, 3, 8, 235)
        self.assertGreater(float(raw["internal_lines"]["v1"]["white_ratio"]), 0.20)
        internal, note = qa.prepare_seam_internal_master(master, 3, 3, 8, 235)
        self.assertEqual(note["qa_size"], {"width": 300, "height": 399})
        self.assertLessEqual(float(internal["internal_lines"]["v1"]["white_ratio"]), 0.20)

        out = tmp / "report.json"
        old = sys.argv
        sys.argv = [
            "grid_gutter_qa.py",
            "--master",
            str(master),
            "--slides-dir",
            str(slides),
            "--mode",
            "seam",
            "--max-internal-white",
            "0.20",
            "--max-edge-white",
            "0.35",
            "--output",
            str(out),
        ]
        try:
            code = qa.main()
        finally:
            sys.argv = old
        self.assertEqual(code, 0, out.read_text(encoding="utf-8")[:1500])
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["mode"], "seam")
        self.assertEqual(data["failures"], [])

    def test_seam_mode_warns_kie_4k_remainder_width_2(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="seam-qa-4k-"))
        master = tmp / "master.png"
        Image.new("RGB", (2480, 3312), (20, 20, 20)).save(master)
        slides = tmp / "slides"
        self._slides(slides)
        out = tmp / "report.json"
        old = sys.argv
        sys.argv = [
            "grid_gutter_qa.py",
            "--master",
            str(master),
            "--slides-dir",
            str(slides),
            "--mode",
            "seam",
            "--max-internal-white",
            "0.20",
            "--max-edge-white",
            "0.35",
            "--output",
            str(out),
        ]
        try:
            code = qa.main()
        finally:
            sys.argv = old
        self.assertEqual(code, 0, out.read_text(encoding="utf-8")[:1500])
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["master"]["remainders"], {"width": 2, "height": 0})
        self.assertTrue(any("2480" in w or "remainder" in w or "not divisible" in w for w in data["warnings"]))
        self.assertEqual(data["failures"], [])
        self.assertEqual(data["seam_internal_qa"]["qa_size"], {"width": 2478, "height": 3312})


if __name__ == "__main__":
    unittest.main()
