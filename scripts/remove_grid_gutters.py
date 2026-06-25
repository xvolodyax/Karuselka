#!/usr/bin/env python3
"""Remove thin generated gutters without cropping or changing master geometry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def is_near_white(pixel: tuple[int, int, int], threshold: int) -> bool:
    r, g, b = pixel
    return r >= threshold and g >= threshold and b >= threshold


def blend(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple((x + y) // 2 for x, y in zip(a, b))


def scrub_vertical(img: Image.Image, x: int, strip: int, threshold: int) -> int:
    width, height = img.size
    px = img.load()
    changed = 0
    left = max(0, x - strip)
    right = min(width - 1, x + strip)
    for y in range(height):
        left_src = px[max(0, left - 1), y]
        right_src = px[min(width - 1, right + 1), y]
        fill = blend(left_src, right_src)
        for xx in range(left, right + 1):
            if is_near_white(px[xx, y], threshold):
                px[xx, y] = fill
                changed += 1
    return changed


def scrub_horizontal(img: Image.Image, y: int, strip: int, threshold: int) -> int:
    width, height = img.size
    px = img.load()
    changed = 0
    top = max(0, y - strip)
    bottom = min(height - 1, y + strip)
    for x in range(width):
        top_src = px[x, max(0, top - 1)]
        bottom_src = px[x, min(height - 1, bottom + 1)]
        fill = blend(top_src, bottom_src)
        for yy in range(top, bottom + 1):
            if is_near_white(px[x, yy], threshold):
                px[x, yy] = fill
                changed += 1
    return changed


def scrub_outer_frame(img: Image.Image, strip: int, threshold: int) -> int:
    width, height = img.size
    px = img.load()
    changed = 0

    for y in range(height):
        left_fill = px[min(strip, width - 1), y]
        right_fill = px[max(0, width - strip - 1), y]
        for x in range(min(strip, width)):
            if is_near_white(px[x, y], threshold):
                px[x, y] = left_fill
                changed += 1
        for x in range(max(0, width - strip), width):
            if is_near_white(px[x, y], threshold):
                px[x, y] = right_fill
                changed += 1

    for x in range(width):
        top_fill = px[x, min(strip, height - 1)]
        bottom_fill = px[x, max(0, height - strip - 1)]
        for y in range(min(strip, height)):
            if is_near_white(px[x, y], threshold):
                px[x, y] = top_fill
                changed += 1
        for y in range(max(0, height - strip), height):
            if is_near_white(px[x, y], threshold):
                px[x, y] = bottom_fill
                changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrub generated grid gutters while preserving exact source dimensions")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--strip", type=int, default=4)
    parser.add_argument("--white-threshold", type=int, default=235)
    parser.add_argument("--scrub-outer-frame", action="store_true")
    parser.add_argument("--report", help="Optional JSON report")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    with Image.open(input_path) as raw:
        img = raw.convert("RGB")
    width, height = img.size

    changes: dict[str, int] = {}
    for i in range(1, args.cols):
        x = round(width * i / args.cols)
        changes[f"v{i}@{x}"] = scrub_vertical(img, x, args.strip, args.white_threshold)
    for i in range(1, args.rows):
        y = round(height * i / args.rows)
        changes[f"h{i}@{y}"] = scrub_horizontal(img, y, args.strip, args.white_threshold)
    if args.scrub_outer_frame:
        changes["outer_frame"] = scrub_outer_frame(img, args.strip, args.white_threshold)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)

    report = {
        "input": str(input_path),
        "output": str(output_path),
        "size": {"width": width, "height": height},
        "grid": {"cols": args.cols, "rows": args.rows},
        "method": "replace near-white pixels only on exact grid cut-lines; no crop, no resize",
        "strip": args.strip,
        "white_threshold": args.white_threshold,
        "changes": changes,
        "total_changed": sum(changes.values()),
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
