#!/usr/bin/env python3
"""Post-slice bleed crop — remove orphan text from row above in grid panels.

Grid 3x3 row-major: rows 2-3 (slides 04-09) often show vertical bleed from
cells above when Kie typography sits near cell bottom edge.

Usage:
  python slice_bleed_crop.py --slides-dir output/slides --crop-top 40
  python slice_bleed_crop.py --slides 05,06,08 --crop-top 30
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow required. pip install Pillow", file=sys.stderr)
    sys.exit(1)


def parse_slide_list(raw: str | None) -> list[int] | None:
    if not raw:
        return None
    return [int(part.strip()) for part in raw.split(",") if part.strip()]


def crop_slide_top(path: Path, top_px: int) -> tuple[int, int, int]:
    """Crop top_px from slide PNG. Returns (top_px, old_h, new_h)."""
    with Image.open(path) as raw:
        img = raw.convert("RGB")
        w, h = img.size
        if top_px <= 0:
            return 0, h, h
        if top_px >= h - 8:
            raise ValueError(f"{path.name}: crop {top_px}px too large for height {h}")
        cropped = img.crop((0, top_px, w, h))
        cropped.save(path, "PNG", optimize=True)
        return top_px, h, h - top_px


def default_row2plus_slides(cols: int = 3, rows: int = 3) -> list[int]:
    """Slides in rows 2+ (1-based): 04..09 for 3x3."""
    slides: list[int] = []
    index = 1
    for row in range(rows):
        for _col in range(cols):
            if row >= 1:
                slides.append(index)
            index += 1
    return slides


def main() -> int:
    p = argparse.ArgumentParser(description="Crop vertical bleed from grid slice PNGs")
    p.add_argument("--slides-dir", default="carusel-memory/output/slides")
    p.add_argument("--workspace", default=".")
    p.add_argument(
        "--slides",
        help="Comma list of slide numbers (e.g. 05,06,08). Default: rows 2+ in 3x3",
    )
    p.add_argument("--crop-top", type=int, default=40, help="Pixels to remove from top")
    p.add_argument(
        "--per-slide",
        help="Overrides: 05:28,06:32,08:30 (crop px per slide)",
    )
    p.add_argument("--manifest", help="Append bleed_crop record to slice-manifest.json")
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    slides_dir = Path(args.slides_dir)
    if not slides_dir.is_absolute():
        slides_dir = workspace / slides_dir

    per_slide: dict[int, int] = {}
    if args.per_slide:
        for part in args.per_slide.split(","):
            num_str, _, px_str = part.partition(":")
            if px_str:
                per_slide[int(num_str.strip())] = int(px_str.strip())

    slide_nums = parse_slide_list(args.slides) or default_row2plus_slides()
    report: list[dict] = []

    for num in slide_nums:
        path = slides_dir / f"slide-{num:02d}.png"
        if not path.exists():
            print(f"WARN: missing {path}", file=sys.stderr)
            continue
        top_px = per_slide.get(num, args.crop_top)
        try:
            applied, old_h, new_h = crop_slide_top(path, top_px)
            report.append(
                {
                    "slide": num,
                    "path": str(path.resolve()),
                    "crop_top_px": applied,
                    "height_before": old_h,
                    "height_after": new_h,
                }
            )
            print(f"slide-{num:02d}: crop top {applied}px -> {new_h}px height")
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

    if args.manifest:
        manifest_path = Path(args.manifest)
        if not manifest_path.is_absolute():
            manifest_path = workspace / manifest_path
        if manifest_path.exists():
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        else:
            data = {}
        data["bleed_crop"] = {
            "crop_top_default": args.crop_top,
            "per_slide": per_slide or None,
            "slides": report,
        }
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Manifest updated: {manifest_path}")

    if not report:
        print("WARN: no slides cropped", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
