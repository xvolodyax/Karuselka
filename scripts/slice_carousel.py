#!/usr/bin/env python3
"""Prepare and slice a seamless Instagram carousel.

Workflow:
  1. You provide one wide image (e.g. API 2K export — any size).
  2. Script fits it to master 6480x1350 (6 x 1080 x 1350).
  3. Script cuts 6 slides for Instagram.

Default: 6480x1350 master -> 6 slides of 1080x1350 each.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow required. Install: pip install Pillow", file=sys.stderr)
    sys.exit(1)

MASTER_WIDTH = 6480
MASTER_HEIGHT = 1350
SLIDE_COUNT = 6
SLIDE_WIDTH = 1080
SLIDE_HEIGHT = 1350


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fit source image to 6480x1350 master and slice into 6 Instagram slides"
    )
    parser.add_argument("--input", "-i", required=True, help="Source image (e.g. 2K API file)")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory for slides")
    parser.add_argument("--master-out", "-m", help="Save normalized master PNG path (optional)")
    parser.add_argument("--slides", "-n", type=int, default=SLIDE_COUNT, help="Number of slides")
    parser.add_argument("--slide-width", type=int, default=SLIDE_WIDTH, help="Slide width in px")
    parser.add_argument("--slide-height", type=int, default=SLIDE_HEIGHT, help="Slide height in px")
    parser.add_argument(
        "--fit",
        choices=("cover", "contain"),
        default="cover",
        help="cover = fill 6480x1350 and crop edges (default, best for seamless). "
        "contain = fit inside with letterbox.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if input is not exactly master size (skip auto-resize)",
    )
    parser.add_argument("--manifest", help="Optional manifest JSON path")
    return parser.parse_args()


def target_master_size(slides: int, slide_width: int, slide_height: int) -> tuple[int, int]:
    return slides * slide_width, slide_height


def fit_to_master(
    img: Image.Image,
    target_w: int,
    target_h: int,
    fit: str = "cover",
    fill_rgb: tuple[int, int, int] = (15, 23, 42),
) -> Image.Image:
    """Resize arbitrary source (e.g. 2K) to exact master dimensions."""
    src_w, src_h = img.size
    if src_w == target_w and src_h == target_h:
        return img

    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if fit == "cover":
        if src_ratio > target_ratio:
            # Wider than target: match height, crop width
            new_h = target_h
            new_w = round(src_w * (target_h / src_h))
        else:
            # Taller than target: match width, crop height
            new_w = target_w
            new_h = round(src_h * (target_w / src_w))
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        return resized.crop((left, top, left + target_w, top + target_h))

    # contain + letterbox
    if src_ratio > target_ratio:
        new_w = target_w
        new_h = round(src_h * (target_w / src_w))
    else:
        new_h = target_h
        new_w = round(src_w * (target_h / src_h))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), fill_rgb)
    paste_x = (target_w - new_w) // 2
    paste_y = (target_h - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y))
    return canvas


def slice_master(
    img: Image.Image,
    output_dir: Path,
    slides: int,
    slide_width: int,
    slide_height: int,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i in range(slides):
        left = i * slide_width
        box = (left, 0, left + slide_width, slide_height)
        crop = img.crop(box)
        out_path = output_dir / f"slide-{i + 1:02d}.png"
        crop.save(out_path, "PNG", optimize=True)
        written.append(out_path)
        print(f"Wrote {out_path} ({crop.size[0]}x{crop.size[1]})")
    return written


def process_carousel(
    input_path: Path,
    output_dir: Path,
    slides: int = SLIDE_COUNT,
    slide_width: int = SLIDE_WIDTH,
    slide_height: int = SLIDE_HEIGHT,
    fit: str = "cover",
    strict: bool = False,
    master_out: Path | None = None,
    manifest_path: Path | None = None,
) -> list[Path]:
    target_w, target_h = target_master_size(slides, slide_width, slide_height)

    with Image.open(input_path) as raw:
        img = raw.convert("RGB")
        source_size = img.size
        print(f"Source: {input_path} ({source_size[0]}x{source_size[1]})")

        if strict and source_size != (target_w, target_h):
            raise ValueError(
                f"Strict mode: expected {target_w}x{target_h}, got {source_size[0]}x{source_size[1]}"
            )

        if source_size != (target_w, target_h):
            print(f"Preparing master: {source_size[0]}x{source_size[1]} -> {target_w}x{target_h} (fit={fit})")
            img = fit_to_master(img, target_w, target_h, fit=fit)

        if master_out:
            master_out.parent.mkdir(parents=True, exist_ok=True)
            img.save(master_out, "PNG", optimize=True)
            print(f"Master: {master_out} ({target_w}x{target_h})")

        written = slice_master(img, output_dir, slides, slide_width, slide_height)

    if manifest_path:
        manifest = {
            "source": str(input_path.resolve()),
            "source_size": {"width": source_size[0], "height": source_size[1]},
            "master_size": {"width": target_w, "height": target_h},
            "fit": fit,
            "slides": slides,
            "slide_width": slide_width,
            "slide_height": slide_height,
            "master_out": str(master_out.resolve()) if master_out else None,
            "files": [str(p.resolve()) for p in written],
        }
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Manifest: {manifest_path}")

    return written


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    manifest_path = Path(args.manifest) if args.manifest else None
    master_out = Path(args.master_out) if args.master_out else None

    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}", file=sys.stderr)
        return 1

    try:
        process_carousel(
            input_path=input_path,
            output_dir=output_dir,
            slides=args.slides,
            slide_width=args.slide_width,
            slide_height=args.slide_height,
            fit=args.fit,
            strict=args.strict,
            master_out=master_out,
            manifest_path=manifest_path,
        )
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
