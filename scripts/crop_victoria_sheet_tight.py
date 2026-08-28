#!/usr/bin/env python3
"""Crop ONE left frontal close-up from victoria-sheet.png for i2i.

The full 12-up sheet averages Vika into a generic blonde. This does not
invent a face. It only cuts the large front portrait on the left of the
official sheet (top-left cell of the 4×3 contact grid).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SHEET = REPO / "carusel-memory" / "references" / "victoria-sheet.png"
DEFAULT_OUT = REPO / "carusel-memory" / "references" / "victoria-sheet-front.png"


def crop_front_closeup(sheet: Path, out: Path, cols: int = 4, rows: int = 3) -> Path:
    im = Image.open(sheet).convert("RGB")
    w, h = im.size
    cw, ch = w // cols, h // rows
    # Inset past the white gutter so we send only the face, not the grid.
    inset = 8
    box = (inset, inset, max(inset + 1, cw - inset), max(inset + 1, ch - inset))
    tight = im.crop(box)
    if tight.size[0] > 500 or tight.size[1] > 400:
        raise SystemExit(f"crop still looks like a grid: {tight.size} from {im.size}")
    out.parent.mkdir(parents=True, exist_ok=True)
    tight.save(out)
    return out


def crop_tight(sheet: Path, out: Path, cols: int = 4, rows: int = 3) -> Path:
    """Back-compat alias used by kie_render_pack."""
    return crop_front_closeup(sheet, out, cols=cols, rows=rows)


def main() -> int:
    p = argparse.ArgumentParser(description="Crop one frontal close-up from victoria-sheet.png")
    p.add_argument("--sheet", default=str(SHEET))
    p.add_argument("--output", default=str(DEFAULT_OUT))
    args = p.parse_args()
    sheet = Path(args.sheet)
    if not sheet.is_file() or sheet.stat().st_size < 10_000:
        raise SystemExit(f"missing official sheet: {sheet}")
    if "victoria.png" in sheet.name and "sheet" not in sheet.name:
        raise SystemExit("refusing Alena file victoria.png")
    out = crop_front_closeup(sheet, Path(args.output))
    im = Image.open(out)
    print(f"wrote {out} {im.size} from {sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
