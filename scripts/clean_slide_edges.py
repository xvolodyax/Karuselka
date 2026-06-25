#!/usr/bin/env python3
"""Clean 1-3px edge artifacts from sliced slides without cropping or resizing."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image


def clean_edges(path: Path, strip: int, edges: set[str]) -> dict[str, object]:
    with Image.open(path) as raw:
        img = raw.convert("RGB")

    width, height = img.size
    px = img.load()
    changed = 0

    if "left" in edges:
        src_x = min(strip, width - 1)
        for x in range(min(strip, width)):
            for y in range(height):
                if px[x, y] != px[src_x, y]:
                    px[x, y] = px[src_x, y]
                    changed += 1

    if "right" in edges:
        src_x = max(0, width - strip - 1)
        for x in range(max(0, width - strip), width):
            for y in range(height):
                if px[x, y] != px[src_x, y]:
                    px[x, y] = px[src_x, y]
                    changed += 1

    if "top" in edges:
        src_y = min(strip, height - 1)
        for y in range(min(strip, height)):
            for x in range(width):
                if px[x, y] != px[x, src_y]:
                    px[x, y] = px[x, src_y]
                    changed += 1

    if "bottom" in edges:
        src_y = max(0, height - strip - 1)
        for y in range(max(0, height - strip), height):
            for x in range(width):
                if px[x, y] != px[x, src_y]:
                    px[x, y] = px[x, src_y]
                    changed += 1

    img.save(path, "PNG", optimize=True)
    return {"file": path.name, "size": {"width": width, "height": height}, "changed_pixels": changed}


def parse_slide_range(raw: str) -> set[int]:
    slides: set[int] = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            slides.update(range(int(start), int(end) + 1))
        else:
            slides.add(int(part))
    return slides


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean edge artifacts on sliced carousel PNGs")
    parser.add_argument("--slides-dir", required=True)
    parser.add_argument("--slides", default="1-9", help="Comma/range list, e.g. 4-9 or 4,5,6,8")
    parser.add_argument("--strip", type=int, default=2, help="Pixels to replace from each outer edge")
    parser.add_argument("--edges", default="top,right,bottom,left", help="Comma list of top,right,bottom,left")
    parser.add_argument("--backup-dir", help="Optional backup directory before overwrite")
    parser.add_argument("--report", help="Optional JSON report")
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    slide_numbers = parse_slide_range(args.slides)
    edges = {e.strip().lower() for e in args.edges.split(",") if e.strip()}
    invalid = edges - {"top", "right", "bottom", "left"}
    if invalid:
        raise SystemExit(f"Invalid edges: {sorted(invalid)}")

    if args.backup_dir:
        backup_dir = Path(args.backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)
    else:
        backup_dir = None

    results: list[dict[str, object]] = []
    for number in sorted(slide_numbers):
        path = slides_dir / f"slide-{number:02d}.png"
        if not path.exists():
            raise FileNotFoundError(path)
        if backup_dir:
            shutil.copy2(path, backup_dir / path.name)
        results.append(clean_edges(path, max(1, args.strip), edges))

    report = {
        "method": "copy interior pixels over outer edge strips; no crop, no resize",
        "slides_dir": str(slides_dir),
        "slides": sorted(slide_numbers),
        "strip": max(1, args.strip),
        "edges": sorted(edges),
        "results": results,
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
