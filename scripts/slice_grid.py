#!/usr/bin/env python3
"""Slice one master image into a cols×rows grid (default 3×3 = 9 slides).

Reading order (row-major, left→right, top→bottom):
  1  2  3
  4  5  6
  7  8  9

Each cell keeps native pixel size from the master (no forced 1080×1350).
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

DEFAULT_COLS = 3
DEFAULT_ROWS = 3


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Slice master into grid panels for Instagram carousel")
    p.add_argument("--input", "-i", required=True)
    p.add_argument("--output-dir", "-o", required=True)
    p.add_argument("--cols", type=int, default=DEFAULT_COLS)
    p.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    p.add_argument("--master-out", "-m", help="Optional copy of full master PNG")
    p.add_argument("--manifest", help="JSON manifest path")
    p.add_argument(
        "--order",
        choices=("row-major",),
        default="row-major",
        help="Panel numbering order",
    )
    p.add_argument(
        "--bleed-crop-top",
        type=int,
        default=0,
        help="Crop N px from top of panels in rows 2+ (slides 04-09 in 3x3)",
    )
    return p.parse_args()


def slice_grid(
    input_path: Path,
    output_dir: Path,
    cols: int = DEFAULT_COLS,
    rows: int = DEFAULT_ROWS,
    master_out: Path | None = None,
    manifest_path: Path | None = None,
    bleed_crop_top: int = 0,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    with Image.open(input_path) as raw:
        img = raw.convert("RGB")
        w, h = img.size
        print(f"Source: {input_path} ({w}x{h})")

        if master_out:
            master_out.parent.mkdir(parents=True, exist_ok=True)
            img.save(master_out, "PNG", optimize=True)
            print(f"Master copy: {master_out}")

        cell_w = w // cols
        cell_h = h // rows
        if cell_w < 1 or cell_h < 1:
            raise ValueError(f"Grid too fine for image {w}x{h} with {cols}x{rows}")

        panel_aspect = round((cell_w / cell_h), 4)
        print(f"Grid: {cols}x{rows} -> cell {cell_w}x{cell_h} (aspect {panel_aspect})")

        index = 1
        for row in range(rows):
            for col in range(cols):
                box = (col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h)
                crop = img.crop(box)
                if bleed_crop_top > 0 and row >= 1:
                    cw, ch = crop.size
                    if bleed_crop_top < ch - 8:
                        crop = crop.crop((0, bleed_crop_top, cw, ch))
                out_path = output_dir / f"slide-{index:02d}.png"
                crop.save(out_path, "PNG", optimize=True)
                written.append(out_path)
                print(f"slide-{index:02d} grid[{row},{col}] -> {out_path} ({crop.size[0]}x{crop.size[1]})")
                index += 1

    if manifest_path:
        manifest = {
            "mode": "grid",
            "source": str(input_path.resolve()),
            "source_size": {"width": w, "height": h},
            "grid": {"cols": cols, "rows": rows, "order": "row-major"},
            "cell_size": {"width": cell_w, "height": cell_h},
            "cell_aspect_ratio": panel_aspect,
            "slide_count": cols * rows,
            "master_out": str(master_out.resolve()) if master_out else None,
            "bleed_crop_top": bleed_crop_top if bleed_crop_top > 0 else None,
            "files": [str(p.resolve()) for p in written],
        }
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Manifest: {manifest_path}")

    return written


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: not found: {input_path}", file=sys.stderr)
        return 1
    try:
        slice_grid(
            input_path=input_path,
            output_dir=Path(args.output_dir),
            cols=args.cols,
            rows=args.rows,
            master_out=Path(args.master_out) if args.master_out else None,
            manifest_path=Path(args.manifest) if args.manifest else None,
            bleed_crop_top=max(0, args.bleed_crop_top),
        )
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
