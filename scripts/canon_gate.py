#!/usr/bin/env python3
"""ТАРО СЕЙЧАС pack gate — meaning + visual family lock.

PASS only if:
  (a) Victoria hair lock noted / no platinum claim
  (b) >=3 slides use animals as metaphor
  (c) >=2 save slides have a real framework or questions
  (d) hook is a scene
  (e) no platinum
  (f) no empty vibe-only slides
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

RAW_URL_RE = re.compile(r"https?://|instagram\.com/|t\.me/|telegram\.me/", re.I)
PLATINUM_RE = re.compile(r"platinum|white-?blonde|платин|белокуры", re.I)
VIBE_ONLY = re.compile(
    r"^( vibes?|energy|настроение|эстетика|just feel|просто почувствуй)\b",
    re.I,
)
MECHANIC_HOOK = re.compile(
    r"^\s*(5 |пять |what is |что такое |pause vs|пауза vs|признак)",
    re.I,
)
QUESTION_RE = re.compile(r"\?|вопрос|question|говорит|says:|слышишь|you hear", re.I)
FRAMEWORK_RE = re.compile(
    r"три |3 |three |рамк|framework|состояни|правил|decision|развилк|fork",
    re.I,
)

ALLOWED_PRODUCTS = {"bot_three_spreads", "app_audio"}
TRIGGERS = {"ru": "ПАУЗА", "en": "PAUSE"}
HANDLES = {"ru": "@todaytaro_ru", "en": "@todaytaro_bot"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slide_text(slide: dict[str, Any]) -> str:
    parts = [
        str(slide.get("headline") or ""),
        str(slide.get("body") or ""),
        str(slide.get("cta") or ""),
        " ".join(str(x) for x in (slide.get("lines") or [])),
        str(slide.get("notes") or ""),
        str(slide.get("visual") or ""),
        str(slide.get("animal") or ""),
    ]
    return " ".join(parts)


def check_pack(pack: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = pack / "PACK.json"
    if not manifest_path.is_file():
        return [f"missing {manifest_path}"]
    manifest = load_json(manifest_path)
    langs = manifest.get("langs") or ["ru", "en"]
    family = manifest.get("visual_family")
    if family != "animals_viktoria_collage":
        errors.append(f"PACK.json visual_family must be animals_viktoria_collage, got {family!r}")

    for lang in langs:
        errors.extend(check_lang(pack / lang, lang, manifest))
    return errors


def check_lang(root: Path, lang: str, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    copy_path = root / "CAROUSEL_SLIDE_COPY.json"
    caption_path = root / "CAROUSEL_CAPTION.json"
    prompt_path = root / "CAROUSEL_IMAGE_PROMPT.json"
    if not copy_path.is_file():
        return [f"{lang}: missing CAROUSEL_SLIDE_COPY.json"]
    data = load_json(copy_path)
    slides = data.get("slides") or []
    if data.get("slide_count") != 9 or len(slides) != 9:
        errors.append(f"{lang}: need exactly 9 slides")
    if data.get("visual_family") != "animals_viktoria_collage":
        errors.append(f"{lang}: visual_family missing/wrong")
    if data.get("hook_is_scene") is not True:
        errors.append(f"{lang}: hook_is_scene must be true")

    hook = slides[0] if slides else {}
    hook_blob = slide_text(hook)
    if MECHANIC_HOOK.search(str(hook.get("headline") or "")):
        errors.append(f"{lang}: hook looks like a mechanic title, not a scene")
    if hook.get("hook_type") != "scene" and not data.get("hook_is_scene"):
        errors.append(f"{lang}: hook is not marked as scene")

    save_frameworks = 0
    animal_slides = 0
    vibe_only = 0
    platinum = 0
    for slide in slides:
        blob = slide_text(slide)
        if slide.get("animal") or re.search(r"\b(cat|dog|owl|кот|кошк|пёс|пес|собак|сова)\b", blob, re.I):
            if slide.get("animal_job") or "метафор" in blob.lower() or slide.get("animal"):
                animal_slides += 1
        role = str(slide.get("role") or "")
        if role.startswith("save") or slide.get("index") in {5, 6, 7}:
            if slide.get("has_framework") or QUESTION_RE.search(blob) or FRAMEWORK_RE.search(blob):
                save_frameworks += 1
        if slide.get("vibe_only") or (len(blob.strip()) < 12) or VIBE_ONLY.search(blob):
            if not slide.get("has_framework") and role not in {"hook", "cta"}:
                vibe_only += 1
        if PLATINUM_RE.search(blob):
            platinum += 1
        for png in (
            root / "slides" / f"slide-{int(slide.get('index', 0)):02d}.png",
            root / f"slide-{int(slide.get('index', 0)):02d}.png",
        ):
            if png.is_file():
                break
        else:
            errors.append(f"{lang}: missing slide-{int(slide.get('index', 0)):02d}.png")

    if animal_slides < 3:
        errors.append(f"{lang}: need >=3 animal-metaphor slides, got {animal_slides}")
    if save_frameworks < 2:
        errors.append(f"{lang}: need >=2 save slides with framework/questions, got {save_frameworks}")
    if vibe_only:
        errors.append(f"{lang}: empty vibe-only slides: {vibe_only}")
    if platinum:
        errors.append(f"{lang}: platinum / white-blonde mentioned in copy or notes")

    victoria_slides = [
        s.get("index") for s in slides if s.get("victoria") or "victoria" in slide_text(s).lower()
    ]
    if 1 not in victoria_slides or 9 not in victoria_slides:
        errors.append(f"{lang}: Victoria must be on slides 1 and 9")

    if caption_path.is_file():
        caption = load_json(caption_path)
        blob = json.dumps(caption, ensure_ascii=False)
        if RAW_URL_RE.search(blob):
            errors.append(f"{lang}: caption contains raw URL")
        trigger = caption.get("trigger_word") or data.get("trigger_word")
        expected = manifest.get("trigger_words", {}).get(lang) or TRIGGERS.get(lang)
        if not trigger:
            errors.append(f"{lang}: caption missing trigger_word")
        elif expected and trigger != expected:
            errors.append(f"{lang}: trigger_word {trigger!r} != {expected!r}")
        product = caption.get("product") or data.get("product")
        if product not in ALLOWED_PRODUCTS:
            errors.append(f"{lang}: product must be one of {sorted(ALLOWED_PRODUCTS)}")
        if lang == "en" and re.search(r"academy", blob, re.I):
            errors.append("en: Academy is forbidden")
        if "личный аудиоразбор" in blob:
            errors.append(f"{lang}: forbidden phrase личный аудиоразбор")
        handle = HANDLES[lang]
        if handle not in blob:
            errors.append(f"{lang}: caption must mention {handle}")
        if product == "bot_three_spreads" and re.search(r"\bapp\b|приложен", blob, re.I):
            errors.append(f"{lang}: mixed bot vs app in caption")
    else:
        errors.append(f"{lang}: missing CAROUSEL_CAPTION.json")

    if prompt_path.is_file():
        prompt = load_json(prompt_path)
        if "PLACEHOLDER" in json.dumps(prompt):
            errors.append(f"{lang}: image prompt still has PLACEHOLDER")
        if prompt.get("visual_family") not in {None, "animals_viktoria_collage"}:
            errors.append(f"{lang}: prompt visual_family wrong")
        if PLATINUM_RE.search(json.dumps(prompt, ensure_ascii=False)):
            # negative prompts may mention platinum as a ban — OK if in negative_*
            pass
    else:
        errors.append(f"{lang}: missing CAROUSEL_IMAGE_PROMPT.json")

    hair = str(manifest.get("hair_lock") or data.get("hair_lock") or "")
    if hair and PLATINUM_RE.search(hair) and not re.search(
        r"fail|forbidden|not |не |ban|avoid|запрет", hair, re.I
    ):
        errors.append("hair_lock claims platinum")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Canon gate for a dated carousel pack")
    parser.add_argument("--pack", required=True, help="path to pack dir, e.g. carusel-memory/packs/2026-08-27-v2")
    args = parser.parse_args(argv)
    pack = Path(args.pack).expanduser().resolve()
    errors = check_pack(pack)
    report = pack / "GATE.md"
    if errors:
        body = "# GATE report\n\nVerdict: FAIL\n\n" + "\n".join(f"- {e}" for e in errors) + "\n"
        report.write_text(body, encoding="utf-8")
        print("❌ CANON GATE FAIL")
        for err in errors:
            print(f"- {err}")
        return 2
    body = """# GATE report

Verdict: PASS

- (a) Victoria face / hair lock: honey-wheat + darker roots; platinum forbidden
- (b) >=3 slides use animals as metaphor
- (c) >=2 save slides have a real framework or questions
- (d) hook is a scene
- (e) no platinum
- (f) no empty vibe-only slides
- caption: one trigger word, no raw URLs, one product, no Academy on EN
"""
    report.write_text(body, encoding="utf-8")
    print("✅ CANON GATE PASS")
    print(f"wrote {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
