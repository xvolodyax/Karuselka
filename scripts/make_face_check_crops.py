#!/usr/bin/env python3
"""Copy viktoriaref.png + crop pack slides 01/09 for FACE_CHECK.

Does not invent a face. Does not crop a 12-up sheet. Does not publish.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
FACE = REPO / "carusel-memory" / "references" / "виктория.png"


def _slide_face(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    box = (int(w * 0.18), int(h * 0.06), int(w * 0.82), int(h * 0.48))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.crop(box).save(dest)


def make_crops(pack: Path) -> list[Path]:
    if not FACE.is_file() or FACE.stat().st_size < 100_000:
        raise SystemExit("missing carusel-memory/references/виктория.png")
    out = pack / "face-check"
    out.mkdir(parents=True, exist_ok=True)
    dest_face = out / "виктория.png"
    shutil.copy2(FACE, dest_face)
    written = [dest_face]
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
