#!/usr/bin/env python3
"""Generate test master canvas and slides for Carusel MCP verification."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow required. Install: pip install Pillow", file=sys.stderr)
    sys.exit(1)

SLIDES = 6
SLIDE_W = 1080
SLIDE_H = 1350
MASTER_W = SLIDES * SLIDE_W
MASTER_H = SLIDE_H

COLORS = [
    (30, 64, 175),
    (37, 99, 235),
    (59, 130, 246),
    (96, 165, 250),
    (147, 197, 253),
    (191, 219, 254),
]


def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arial.ttf", "Arial.ttf", "segoeui.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_seamless_master() -> Image.Image:
    img = Image.new("RGB", (MASTER_W, MASTER_H), (15, 23, 42))
    draw = ImageDraw.Draw(img)

    for i in range(SLIDES):
        x0 = i * SLIDE_W
        draw.rectangle([x0, 0, x0 + SLIDE_W, MASTER_H], fill=COLORS[i])

    gradient = Image.new("RGB", (MASTER_W, MASTER_H))
    gdraw = ImageDraw.Draw(gradient)
    for x in range(MASTER_W):
        alpha = int(40 * (x / MASTER_W))
        gdraw.line([(x, 0), (x, MASTER_H)], fill=(255, 255, 255, alpha))
    img = Image.blend(img, gradient, 0.15)

    draw = ImageDraw.Draw(img)
    font_lg = get_font(72)
    font_md = get_font(36)
    font_sm = get_font(24)

    draw.line([(SLIDE_W, 200), (MASTER_W - SLIDE_W, 200)], fill=(255, 255, 255), width=4)
    draw.ellipse([900, 500, 5700, 1100], outline=(255, 255, 255), width=6)

    for i in range(SLIDES):
        x0 = i * SLIDE_W
        cx = x0 + SLIDE_W // 2
        draw.text((cx - 80, 400), f"Slide {i + 1}", fill=(255, 255, 255), font=font_lg, anchor="mm")
        draw.text((cx, 600), "Carusel MCP Test", fill=(226, 232, 240), font=font_md, anchor="mm")
        draw.text((cx, 1200), f"{i + 1} / {SLIDES}", fill=(255, 255, 255), font=font_sm, anchor="mm")

    if SLIDES >= 2:
        draw.text((SLIDE_W - 20, 800), "seam", fill=(250, 204, 21), font=font_sm, anchor="rm")
        draw.text((SLIDE_W + 20, 800), "less", fill=(250, 204, 21), font=font_sm, anchor="lm")

    return img


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate test carousel master and slides")
    parser.add_argument(
        "--workspace",
        default=".",
        help="Workspace root containing carusel-memory/",
    )
    args = parser.parse_args()
    root = Path(args.workspace).resolve()
    master_dir = root / "carusel-memory" / "output" / "master"
    slides_dir = root / "carusel-memory" / "output" / "slides"
    master_dir.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)

    master_path = master_dir / "master.png"
    master = draw_seamless_master()
    master.save(master_path, "PNG")
    print(f"Master: {master_path} ({MASTER_W}x{MASTER_H})")

    script_dir = Path(__file__).resolve().parent
    slice_script = script_dir / "slice_carousel.py"
    if not slice_script.exists():
        print(f"WARN: slice script not found at {slice_script}", file=sys.stderr)
        return 1

    import subprocess

    manifest = root / "carusel-memory" / "output" / "slice-manifest.json"
    result = subprocess.run(
        [
            sys.executable,
            str(slice_script),
            "--input",
            str(master_path),
            "--output-dir",
            str(slides_dir),
            "--slides",
            str(SLIDES),
            "--manifest",
            str(manifest),
        ],
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
