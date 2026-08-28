#!/usr/bin/env python3
"""Pixel-side Victoria face + eyes gate.

FAIL if FACE_CHECK.md is missing, is only hair prose, has no crops,
verdict is not MATCH, or eyes are brown/grey. Does not invent a face.
Does not publish.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHEET = REPO / "carusel-memory" / "references" / "victoria-sheet.png"
LEGACY_PACKS = frozenset({"2026-08-27-swarm", "2026-08-27-v2"})

VERDICT_RE = re.compile(r"^verdict:\s*(MATCH|FAIL)\s*$", re.I | re.M)
COMPARED_RE = re.compile(r"victoria-sheet\.png", re.I)
HAIR_ONLY = re.compile(r"honey|wheat|пшенич|медов", re.I)
GREEN_RE = re.compile(r"green|зелён|зелен", re.I)
HAZEL_RE = re.compile(r"hazel|орех|light-?brown|светло-?корич", re.I)
BROWN_GREY_AS_ACTUAL = re.compile(
    r"(eyes?|iris|глаз)\s+(are|is|:)?\s*(brown|grey|gray|кари|серы)"
    r"|(brown|grey|gray|карие|серые)\s+(eyes|глаз)",
    re.I,
)
NOT_BROWN_GREY = re.compile(
    r"not (brown|grey|gray)|не (кари|серы)|brown/?grey = FAIL|карие/серые = FAIL",
    re.I,
)
LANDMARKS = (
    re.compile(r"eye|глаз|iris|hazel|орех", re.I),
    re.compile(r"bone|cheek|скул|челюст|jaw|chin", re.I),
    re.compile(r"age|лет|young|30|возраст", re.I),
)
ALENA_RE = re.compile(r"cover-refs/victoria\.png|alena", re.I)


def pack_has_real_pixels(pack: Path) -> bool:
    candidates = [
        pack / "ru" / "slides" / "slide-01.png",
        pack / "slides" / "slide-01.png",
    ]
    return any(p.is_file() and p.stat().st_size > 10_000 for p in candidates)


def check_face(pack: Path) -> list[str]:
    errors: list[str] = []
    manifest = pack / "PACK.json"
    if not manifest.is_file():
        return [f"missing {manifest}"]
    try:
        pack_id = str(json.loads(manifest.read_text(encoding="utf-8")).get("pack_id") or "")
    except json.JSONDecodeError as exc:
        return [f"PACK.json invalid: {exc}"]
    if pack_id in LEGACY_PACKS:
        return []
    if not pack_has_real_pixels(pack):
        return []

    note = pack / "FACE_CHECK.md"
    if not note.is_file():
        return [
            "missing FACE_CHECK.md — compare slide 01/09 faces to "
            "victoria-sheet.png close-up pixel-side before DESIGN OK"
        ]
    text = note.read_text(encoding="utf-8")
    verd = VERDICT_RE.search(text)
    if not verd:
        errors.append("FACE_CHECK.md needs a line: verdict: MATCH|FAIL")
    elif verd.group(1).upper() != "MATCH":
        errors.append("FACE_CHECK.md verdict is not MATCH")
    if not COMPARED_RE.search(text):
        errors.append("FACE_CHECK.md must name victoria-sheet.png as the compared sheet")
    if ALENA_RE.search(text) and "forbidden" not in text.lower() and "alena" in text.lower():
        if "not alena" not in text.lower() and "не ален" not in text.lower():
            errors.append("FACE_CHECK.md must not treat Alena / victoria.png as Vika")
    if HAIR_ONLY.search(text) and not all(rx.search(text) for rx in LANDMARKS):
        errors.append(
            "FACE_CHECK.md is hair-prose only. Compare eyes, bone/age, and hair pattern "
            "on the actual crops — not just honey/wheat."
        )
    if not all(rx.search(text) for rx in LANDMARKS):
        errors.append(
            "FACE_CHECK.md must note eyes, bone structure/age, and hair pattern "
            "from the pixel crops"
        )
    if not GREEN_RE.search(text) or not HAZEL_RE.search(text):
        errors.append(
            "FACE_CHECK.md must note green + slight hazel/light-brown eyes "
            "(Excalibur lock). Brown or grey = FAIL, new canvas."
        )
    if BROWN_GREY_AS_ACTUAL.search(text) and not NOT_BROWN_GREY.search(text):
        errors.append("brown/grey eyes = FAIL face-gate, rebuild the whole canvas")

    crop_dir = pack / "face-check"
    required = [
        crop_dir / "sheet-front.png",
        crop_dir / "ru-slide-01-face.png",
        crop_dir / "ru-slide-09-face.png",
        crop_dir / "en-slide-01-face.png",
        crop_dir / "en-slide-09-face.png",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size < 1000:
            errors.append(f"missing pixel crop {path.relative_to(pack)}")
    if not SHEET.is_file() or SHEET.stat().st_size < 10_000:
        errors.append("missing official sheet carusel-memory/references/victoria-sheet.png")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Pixel-side Victoria face + eyes gate")
    p.add_argument("--pack", required=True)
    args = p.parse_args()
    pack = Path(args.pack).expanduser().resolve()
    errors = check_face(pack)
    if errors:
        print("❌ FACE GATE FAIL")
        for err in errors:
            print(f"- {err}")
        return 2
    print("✅ FACE GATE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
