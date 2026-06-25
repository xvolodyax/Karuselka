#!/usr/bin/env python3
"""Detect visible white gutters/frames in a 3x3 carousel master and slides."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageStat


def white_ratio(img: Image.Image, box: tuple[int, int, int, int], threshold: int) -> dict[str, object]:
    crop = img.crop(box).convert("RGB")
    pixels = crop.getdata()
    total = crop.size[0] * crop.size[1]
    white = sum(1 for r, g, b in pixels if r >= threshold and g >= threshold and b >= threshold)
    stat = ImageStat.Stat(crop)
    return {
        "box": box,
        "white_ratio": round(white / total, 4) if total else 0.0,
        "mean_rgb": [round(v, 1) for v in stat.mean],
    }


def analyze_master(path: Path, cols: int, rows: int, strip: int, threshold: int) -> dict[str, object]:
    with Image.open(path) as raw:
        img = raw.convert("RGB")
        width, height = img.size
        result: dict[str, object] = {
            "path": str(path),
            "size": {"width": width, "height": height},
            "grid": {"cols": cols, "rows": rows},
            "remainders": {"width": width % cols, "height": height % rows},
            "internal_lines": {},
        }

        lines: dict[str, object] = {}
        half = max(1, strip // 2)
        for i in range(1, cols):
            x = round(width * i / cols)
            box = (max(0, x - half), 0, min(width, x + half + 1), height)
            lines[f"v{i}"] = white_ratio(img, box, threshold)
        for i in range(1, rows):
            y = round(height * i / rows)
            box = (0, max(0, y - half), width, min(height, y + half + 1))
            lines[f"h{i}"] = white_ratio(img, box, threshold)
        result["internal_lines"] = lines
        return result


def analyze_slides(slides_dir: Path, strip: int, threshold: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(slides_dir.glob("slide-*.png")):
        with Image.open(path) as raw:
            img = raw.convert("RGB")
            width, height = img.size
            regions = {
                "left": (0, 0, min(strip, width), height),
                "right": (max(0, width - strip), 0, width, height),
                "top": (0, 0, width, min(strip, height)),
                "bottom": (0, max(0, height - strip), width, height),
            }
            rows.append(
                {
                    "file": path.name,
                    "size": {"width": width, "height": height},
                    "edges": {name: white_ratio(img, box, threshold) for name, box in regions.items()},
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="QA for generated grid gutters/white frames")
    parser.add_argument("--master", required=True, help="Generated 3x3 master PNG")
    parser.add_argument("--slides-dir", required=True, help="Directory with slide-01.png ... slide-09.png")
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--strip", type=int, default=8, help="Pixel strip width around cut lines/edges")
    parser.add_argument("--white-threshold", type=int, default=235)
    parser.add_argument("--max-internal-white", type=float, default=0.45)
    parser.add_argument("--max-edge-white", type=float, default=0.60)
    parser.add_argument("--output", help="Optional JSON report")
    args = parser.parse_args()

    master = analyze_master(Path(args.master), args.cols, args.rows, args.strip, args.white_threshold)
    slides = analyze_slides(Path(args.slides_dir), args.strip, args.white_threshold)
    failures: list[str] = []

    if master["remainders"] != {"width": 0, "height": 0}:
        failures.append(f"master dimensions are not divisible by {args.cols}x{args.rows}: {master['remainders']}")

    for name, data in (master["internal_lines"] or {}).items():
        ratio = float(data["white_ratio"])
        if ratio > args.max_internal_white:
            failures.append(f"internal cut line {name} has white_ratio={ratio}")

    for slide in slides:
        for edge, data in (slide["edges"] or {}).items():
            ratio = float(data["white_ratio"])
            if ratio > args.max_edge_white:
                failures.append(f"{slide['file']} {edge} edge has white_ratio={ratio}")

    report = {
        "status": "ok" if not failures else "fail",
        "method": "strict equal grid slice; detect visible white gutters/frames before publish",
        "thresholds": {
            "strip": args.strip,
            "white_threshold": args.white_threshold,
            "max_internal_white": args.max_internal_white,
            "max_edge_white": args.max_edge_white,
        },
        "master": master,
        "slides": slides,
        "failures": failures,
    }

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
