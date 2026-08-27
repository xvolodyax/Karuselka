#!/usr/bin/env python3
"""Seam slice finds Excalibur-style white gutters and fails a crooked canvas."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

import seam_slice_grid as seam


def _seamed_canvas(w: int = 300, h: int = 400, gutter: int = 8) -> Image.Image:
    img = Image.new("RGB", (w, h), (20, 20, 20))
    draw = ImageDraw.Draw(img)
    # 3x3 cells with white seams at 1/3 and 2/3
    xs = [w // 3, 2 * w // 3]
    ys = [h // 3, 2 * h // 3]
    half = gutter // 2
    for x in xs:
        draw.rectangle((x - half, 0, x + half, h - 1), fill=(255, 255, 255))
    for y in ys:
        draw.rectangle((0, y - half, w - 1, y + half), fill=(255, 255, 255))
    return img


class SeamSliceTest(unittest.TestCase):
    def test_detects_white_seams(self) -> None:
        img = _seamed_canvas()
        boxes, meta = seam.detect_grid_boxes(img, split_mode="gutter")
        self.assertEqual(len(boxes), 9)
        self.assertEqual(meta["split_mode"], "gutter_detect")
        self.assertEqual(len(meta["v_gutters_px"]), 2)
        self.assertEqual(len(meta["h_gutters_px"]), 2)

    def test_crooked_canvas_fails_gutter_mode(self) -> None:
        img = Image.new("RGB", (300, 400), (20, 20, 20))
        with self.assertRaises(SystemExit):
            seam.detect_grid_boxes(img, split_mode="gutter")

    def test_writes_nine_equal_pngs(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="seam-"))
        src = tmp / "master.png"
        _seamed_canvas().save(src)
        out = tmp / "slides"
        written = seam.slice_seamed(src, out, split_mode="gutter", manifest_path=tmp / "m.json")
        self.assertEqual(len(written), 9)
        sizes = {Image.open(p).size for p in written}
        self.assertEqual(len(sizes), 1)
        w, h = next(iter(sizes))
        self.assertAlmostEqual(w / h, 0.75, places=2)


if __name__ == "__main__":
    unittest.main()
