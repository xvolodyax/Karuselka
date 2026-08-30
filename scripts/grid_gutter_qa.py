#!/usr/bin/env python3
"""Detect visible white gutters/frames in a 3x3 carousel master and slides."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageStat

# Kie 4K 3:4 is 2480x3312. 2480 % 3 = 2 leftover columns — not a mis-slice.
KIE_4K_SEAM_SIZE = (2480, 3312)
KIE_4K_SEAM_REMAINDER = {"width": 2, "height": 0}


def is_known_kie_4k_seam_remainder(
    size: dict[str, int],
    remainders: dict[str, int],
    cols: int,
    rows: int,
) -> bool:
    return (
        cols == 3
        and rows == 3
        and (int(size.get("width") or 0), int(size.get("height") or 0)) == KIE_4K_SEAM_SIZE
        and dict(remainders) == KIE_4K_SEAM_REMAINDER
    )


def crop_remainder(img: Image.Image, cols: int, rows: int) -> Image.Image:
    """Drop leftover pixels so width/height divide evenly (QA copy only)."""
    width, height = img.size
    rem_w, rem_h = width % cols, height % rows
    if rem_w == 0 and rem_h == 0:
        return img
    left = rem_w // 2
    top = rem_h // 2
    return img.crop((left, top, width - (rem_w - left), height - (rem_h - top)))


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


def analyze_image(
    img: Image.Image,
    path: Path | None,
    cols: int,
    rows: int,
    strip: int,
    threshold: int,
) -> dict[str, object]:
    width, height = img.size
    result: dict[str, object] = {
        "path": str(path) if path else None,
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


def analyze_master(path: Path, cols: int, rows: int, strip: int, threshold: int) -> dict[str, object]:
    with Image.open(path) as raw:
        img = raw.convert("RGB")
        return analyze_image(img, path, cols, rows, strip, threshold)


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


def prepare_seam_internal_master(
    path: Path,
    cols: int,
    rows: int,
    strip: int,
    threshold: int,
) -> tuple[dict[str, object], dict[str, object]]:
    """QA-only copy: crop leftover remainder, then analyze internal lines.

    Expected Excalibur gutters stay on the original master; leftover 1–2px
    from Kie 4K 2480x3312 is dropped so remainder is 0 for the check.
    """
    from remove_grid_gutters import scrub_horizontal, scrub_vertical

    with Image.open(path) as raw:
        img = raw.convert("RGB")
    source_size = {"width": img.size[0], "height": img.size[1]}
    cropped = crop_remainder(img, cols, rows)
    width, height = cropped.size
    for i in range(1, cols):
        scrub_vertical(cropped, round(width * i / cols), strip, threshold)
    for i in range(1, rows):
        scrub_horizontal(cropped, round(height * i / rows), strip, threshold)
    note = {
        "used": True,
        "source_size": source_size,
        "qa_size": {"width": width, "height": height},
        "method": "crop remainder + scrub cut-lines on a copy; slice input unchanged",
    }
    return analyze_image(cropped, None, cols, rows, strip, threshold), note


def main() -> int:
    parser = argparse.ArgumentParser(description="QA for generated grid gutters/white frames")
    parser.add_argument("--master", required=True, help="Generated 3x3 master PNG")
    parser.add_argument("--slides-dir", required=True, help="Directory with slide-01.png ... slide-09.png")
    parser.add_argument("--cols", type=int, default=3)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument(
        "--mode",
        choices=("equal", "seam"),
        default="equal",
        help="equal: remainder must be 0. seam: Kie 4K remainder width=2 is WARN; internals use a scrubbed copy",
    )
    parser.add_argument("--strip", type=int, default=8, help="Pixel strip width around cut lines/edges")
    parser.add_argument("--white-threshold", type=int, default=235)
    parser.add_argument("--max-internal-white", type=float, default=0.45)
    parser.add_argument("--max-edge-white", type=float, default=0.60)
    parser.add_argument("--output", help="Optional JSON report")
    args = parser.parse_args()

    master_path = Path(args.master)
    master = analyze_master(master_path, args.cols, args.rows, args.strip, args.white_threshold)
    slides = analyze_slides(Path(args.slides_dir), args.strip, args.white_threshold)
    failures: list[str] = []
    warnings: list[str] = []
    seam_qa: dict[str, object] | None = None
    internal_source = master

    if master["remainders"] != {"width": 0, "height": 0}:
        msg = f"master dimensions are not divisible by {args.cols}x{args.rows}: {master['remainders']}"
        if args.mode == "seam" and is_known_kie_4k_seam_remainder(
            master["size"], master["remainders"], args.cols, args.rows
        ):
            warnings.append(msg + " (Kie 4K 3:4 remainder; WARN in seam mode)")
        else:
            failures.append(msg)

    if args.mode == "seam":
        internal_source, seam_qa = prepare_seam_internal_master(
            master_path, args.cols, args.rows, args.strip, args.white_threshold
        )
        master["internal_qa"] = internal_source

    for name, data in (internal_source.get("internal_lines") or {}).items():
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
        "mode": args.mode,
        "method": (
            "seam: remainder width=2 on 2480x3312 is WARN; internal lines checked on a remainder-cropped scrubbed copy"
            if args.mode == "seam"
            else "strict equal grid slice; detect visible white gutters/frames before publish"
        ),
        "thresholds": {
            "strip": args.strip,
            "white_threshold": args.white_threshold,
            "max_internal_white": args.max_internal_white,
            "max_edge_white": args.max_edge_white,
        },
        "master": master,
        "seam_internal_qa": seam_qa,
        "slides": slides,
        "warnings": warnings,
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
