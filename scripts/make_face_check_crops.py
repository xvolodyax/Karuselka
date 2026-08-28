#!/usr/bin/env python3
"""Cut face-check crops from the official sheet + pack slides 01/09.

Does not invent a face. Does not publish. Guardian still writes FACE_CHECK.md.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SHEET = REPO / "carusel-memory" / "references" / "victoria-sheet.png"
FRONT = REPO / "carusel-memory" / "references" / "victoria-sheet-front.png"


def _ensure_front() -> Path:
    if FRONT.is_file() and FRONT.stat().st_size > 1000:
        return FRONT
    from crop_victoria_sheet_tight import crop_front_closeup

    return crop_front_closeup(SHEET, FRONT)


def _slide_face(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    box = (int(w * 0.18), int(h * 0.06), int(w * 0.82), int(h * 0.48))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.crop(box).save(dest)


def make_crops(pack: Path) -> list[Path]:
    out = pack / "face-check"
    out.mkdir(parents=True, exist_ok=True)
    front = _ensure_front()
    sheet_front = out / "sheet-front.png"
    shutil.copy2(front, sheet_front)
    written = [sheet_front]
    mapping = {
        "ru-slide-01-face.png": pack / "ru" / "slides" / "slide-01.png",
        "ru-slide-09-face.png": pack / "ru" / "slides" / "slide-09.png",
        "en-slide-01-face.png": pack / "en" / "slides" / "slide-01.png",
        "en-slide-09-face.png": pack / "en" / "slides" / "slide-09.png",
    }
    for name, src in mapping.items():
        if not src.is_file():
            raise SystemExit(f"missing slide {src}")
        dest = out / name
        _slide_face(src, dest)
        written.append(dest)
    return written


def main() -> int:
    p = argparse.ArgumentParser(description="Make FACE_CHECK pixel crops")
    p.add_argument("--pack", required=True)
    args = p.parse_args()
    pack = Path(args.pack).expanduser().resolve()
    paths = make_crops(pack)
    for path in paths:
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
