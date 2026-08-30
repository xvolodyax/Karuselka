#!/usr/bin/env python3
"""Host-portrait gate.

New packs (after the live 30.08 pair): FAIL if a host face is required,
FACE-MATCH'd, or fed into generation. Live weekend/weekday packs keep
their historical MATCH notes and are not rebuilt.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHEET = REPO / "carusel-memory" / "references" / "Виктория.png"
LIVE_HOST_FACE_PACKS = frozenset(
    {
        "2026-08-27-swarm",
        "2026-08-27-v2",
        "2026-08-28",
        "2026-08-29",
        "2026-08-30",
    }
)
LEGACY_PACKS = LIVE_HOST_FACE_PACKS
NO_FACE = "none"
FACE_FILE_RE = re.compile(
    r"Виктория\.png|viktoriaref\.png|victoria-sheet(?:-front)?\.png|"
    r"victoria-face\.png|victoria\.png",
    re.I,
)

VERDICT_RE = re.compile(r"^verdict:\s*(MATCH|FAIL|ABSENT)\s*$", re.I | re.M)
COMPARED_RE = re.compile(r"Виктория\.png", re.I)
HAIR_ONLY = re.compile(r"honey|wheat|пшенич|медов", re.I)
GREEN_RE = re.compile(r"green|зелён|зелен", re.I)
HAZEL_RE = re.compile(r"hazel|орех|карим|light-?brown|светло-?корич", re.I)
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
ABSENT_RULE_RE = re.compile(
    r"no host|без (лица|портрет)|no (face|portrait)|absent|портрет ведущ",
    re.I,
)
MATCH_OLD_RE = re.compile(r"FACE MATCH|похож.*Виктор|same woman as Виктор", re.I)


def is_live_host_face_pack(pack_id: str) -> bool:
    return pack_id in LIVE_HOST_FACE_PACKS


def pack_has_real_pixels(pack: Path) -> bool:
    candidates = [
        pack / "ru" / "slides" / "slide-01.png",
        pack / "slides" / "slide-01.png",
    ]
    return any(p.is_file() and p.stat().st_size > 10_000 for p in candidates)


def check_face_live(pack: Path, text: str) -> list[str]:
    errors: list[str] = []
    verd = VERDICT_RE.search(text)
    if not verd:
        errors.append("FACE_CHECK.md needs a line: verdict: MATCH|FAIL")
    elif verd.group(1).upper() != "MATCH":
        errors.append("FACE_CHECK.md verdict is not MATCH")
    if not COMPARED_RE.search(text):
        errors.append("FACE_CHECK.md must name Виктория.png as the compared face")
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
        crop_dir / "Виктория.png",
        crop_dir / "ru-slide-01-face.png",
        crop_dir / "ru-slide-09-face.png",
        crop_dir / "en-slide-01-face.png",
        crop_dir / "en-slide-09-face.png",
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size < 1000:
            errors.append(f"missing pixel crop {path.relative_to(pack)}")
    if not SHEET.is_file() or SHEET.stat().st_size < 10_000:
        errors.append("missing official face carusel-memory/references/Виктория.png")
    return errors


def check_face_absent(pack: Path, text: str) -> list[str]:
    errors: list[str] = []
    verd = VERDICT_RE.search(text)
    if not verd:
        errors.append("FACE_CHECK.md needs a line: verdict: ABSENT")
    elif verd.group(1).upper() == "MATCH":
        errors.append(
            "FACE_CHECK.md verdict MATCH is retired — host portrait must be ABSENT, "
            "not FACE MATCH vs Виктория.png"
        )
    elif verd.group(1).upper() != "ABSENT":
        errors.append("FACE_CHECK.md verdict is not ABSENT")
    if MATCH_OLD_RE.search(text) and not ABSENT_RULE_RE.search(text):
        errors.append("do not FACE MATCH «похожа на Виктория.png» — face must be absent")
    if not ABSENT_RULE_RE.search(text):
        errors.append(
            "FACE_CHECK.md must state no host portrait / no Vika face "
            "(not a likeness check)"
        )
    if FACE_FILE_RE.search(text) and "not" not in text.lower() and "не " not in text.lower():
        if "forbidden" not in text.lower() and "не класть" not in text.lower():
            errors.append(
                "FACE_CHECK.md must not treat Виктория.png as a generation ref"
            )
    return errors


def check_face(pack: Path) -> list[str]:
    errors: list[str] = []
    manifest = pack / "PACK.json"
    if not manifest.is_file():
        return [f"missing {manifest}"]
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        pack_id = str(data.get("pack_id") or "")
    except json.JSONDecodeError as exc:
        return [f"PACK.json invalid: {exc}"]
    if not pack_has_real_pixels(pack):
        return []

    note = pack / "FACE_CHECK.md"
    if not note.is_file():
        if is_live_host_face_pack(pack_id):
            return [
                "missing FACE_CHECK.md — compare slide 01/09 faces to "
                "Виктория.png pixel-side before DESIGN OK"
            ]
        return [
            "missing FACE_CHECK.md — confirm every slide has no host portrait "
            "(verdict: ABSENT). FACE MATCH vs Виктория.png is retired."
        ]
    text = note.read_text(encoding="utf-8")
    if is_live_host_face_pack(pack_id):
        return check_face_live(pack, text)
    return check_face_absent(pack, text)


def main() -> int:
    p = argparse.ArgumentParser(description="Host-portrait pixel gate")
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
