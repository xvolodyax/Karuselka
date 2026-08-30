#!/usr/bin/env python3
"""ТАРО СЕЙЧАС pack gate — meaning + visual family lock.

PASS only if:
  (a) new packs: no host portrait (face_lock=none). Live 27–30.08 keep historical face lock.
  (b) >=3 slides use animals as metaphor
  (c) >=2 save slides have a real framework or questions
  (d) hook is a scene
  (e) no platinum
  (f) no empty vibe-only slides
  (g) prompts do not copy sheet clothes (white cami + jeans) or ivory blazer
  (i) CTA = app_audio (not 3 free bot readings as the comment prize)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import cta_canon
from face_gate import (
    FACE_FILE_RE,
    LIVE_HOST_FACE_PACKS,
    NO_FACE,
    check_face,
    is_live_host_face_pack,
    pack_has_real_pixels,
)

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

ALLOWED_PRODUCTS = {cta_canon.REQUIRED_PRODUCT}
TRIGGERS = {"ru": "ПАУЗА", "en": "PAUSE"}
HANDLES = {"ru": "@todaytaro_ru", "en": "@todaytaro_bot"}
FACE_LOCK = NO_FACE
FACE_LOCK_UPLOAD = NO_FACE
LEGACY_FACE = "Виктория.png"
LEGACY_PACKS = LIVE_HOST_FACE_PACKS
RETIRED_FACE_RE = re.compile(
    r"viktoriaref\.png|victoria-sheet\.png|victoria-sheet-front\.png|victoria-face\.png",
    re.I,
)
ALENA_BINARIES = (
    Path("/workspace/cover-refs/victoria.png"),
    Path("/workspace/cover-refs/victoria_ref.jpg"),
    Path("/workspace/cover-refs/alena.png"),
    Path("/workspace/cover-refs/alena_ref.jpg"),
    Path("/workspace/assets/victoria.png"),
    Path("/workspace/assets/alena.png"),
    Path("/workspace/assets/victoria_ref.jpg"),
    Path("/workspace/assets/alena_ref.jpg"),
)
PROMPT_MAX_CHARS = 2200
STYLE_LOCK_RE = re.compile(r"animals-viktoria-style-lock|style-lock", re.I)
ALENA_RE = re.compile(
    r"alena|cover-refs/victoria\.png|assets/victoria\.png|victoria-hair-lock",
    re.I,
)
SHEET_CLOTHES_RE = re.compile(
    r"white cami|white camisole|spaghetti-strap|ivory blazer|white blazer|"
    r"light-wash jeans|white cami \+ jeans",
    re.I,
)
STICKER_HALO_RE = re.compile(
    r"\b(cutout|die-cut|sticker outline|white outline|white halo|crooked halo|"
    r"вырезк|стикер-контур|белый контур|белый ореол)\b",
    re.I,
)
SEAM_RE = re.compile(
    r"thin white gutter|white seam|бел(ые|ых) (желоб|шов|gutter)|seam_slice|slice_method.: .seam",
    re.I,
)
FORBIDDEN_INPUT_RE = re.compile(
    r"cover-refs/victoria\.png|victoria-hair-lock|cover-old\.png|karusel-old/cover-old",
    re.I,
)


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
    pack_id = str(manifest.get("pack_id") or pack.name)
    live_face = is_live_host_face_pack(pack_id)
    want_face = LEGACY_FACE if live_face else FACE_LOCK
    face = str(manifest.get("face_lock") or "")
    if live_face:
        if want_face not in face:
            errors.append(f"PACK.json face_lock must be {want_face}")
    elif face not in {NO_FACE, "no_host", "absent", ""}:
        errors.append(f"PACK.json face_lock must be {NO_FACE} (no host portrait)")
    if ALENA_RE.search(json.dumps(manifest, ensure_ascii=False)):
        errors.append("PACK.json points at Alena / retired hair-lock")

    refs = Path(__file__).resolve().parent.parent / "carusel-memory" / "references"
    if live_face:
        repo_face = refs / LEGACY_FACE
        if not repo_face.is_file() or repo_face.stat().st_size < 100_000:
            errors.append(
                f"missing historical face binary carusel-memory/references/{LEGACY_FACE} "
                "(live 27–30.08 only; new packs must not i2i it)"
            )
    for retired in (
        refs / "viktoriaref.png",
        refs / "victoria-sheet.png",
        refs / "victoria-sheet-front.png",
        refs / "victoria-face.png",
        refs / "виктория.png",
        refs / "victoria.png",
    ):
        if retired.is_file() and retired.stat().st_size > 1000:
            errors.append(f"retired face file still present: {retired.name}. Delete it.")
    for banned in ALENA_BINARIES:
        if banned.is_file() and banned.stat().st_size > 1000:
            errors.append(
                f"Alena binary still present: {banned}. Delete it. "
                "Carousel does not i2i any host face."
            )

    for lang in langs:
        errors.extend(check_lang(pack / lang, lang, manifest, pack_id))
    if pack_has_real_pixels(pack):
        errors.extend(check_face(pack))
    return errors


def check_lang(root: Path, lang: str, manifest: dict[str, Any], pack_id: str = "") -> list[str]:
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
        s.get("index")
        for s in slides
        if s.get("victoria") or re.search(r"\bvictoria\b", slide_text(s), re.I)
    ]
    live_face = is_live_host_face_pack(pack_id or str(manifest.get("pack_id") or ""))
    if live_face:
        if 1 not in victoria_slides or 9 not in victoria_slides:
            errors.append(f"{lang}: Victoria must be on slides 1 and 9")
    elif victoria_slides:
        errors.append(
            f"{lang}: host portrait / Victoria on slides {victoria_slides} is forbidden"
        )

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
        if lang == "en" and re.search(r"academy", blob, re.I):
            errors.append("en: Academy is forbidden")
        handle = HANDLES[lang]
        if handle not in blob:
            errors.append(f"{lang}: caption must mention {handle}")
        slide9 = next((s for s in slides if s.get("index") == 9), {})
        if not cta_canon.is_legacy_bot_pack(manifest):
            errors.extend(
                cta_canon.check_cta_offer(
                    lang=lang,
                    product=product,
                    caption_blob=blob,
                    slide9_blob=slide_text(slide9),
                )
            )
        elif product not in {cta_canon.REQUIRED_PRODUCT, "bot_three_spreads"}:
            errors.append(f"{lang}: product must be app_audio or legacy bot_three_spreads")
    else:
        errors.append(f"{lang}: missing CAROUSEL_CAPTION.json")

    if prompt_path.is_file():
        prompt = load_json(prompt_path)
        blob = json.dumps(prompt, ensure_ascii=False)
        if "PLACEHOLDER" in blob:
            errors.append(f"{lang}: image prompt still has PLACEHOLDER")
        if prompt.get("visual_family") not in {None, "animals_viktoria_collage"}:
            errors.append(f"{lang}: prompt visual_family wrong")
        pack_id = pack_id or str(manifest.get("pack_id") or "")
        live_face = is_live_host_face_pack(pack_id)
        want_face = LEGACY_FACE if live_face else FACE_LOCK
        lock = str(prompt.get("face_lock") or "")
        if live_face:
            if want_face not in lock:
                errors.append(f"{lang}: prompt face_lock must be {want_face}")
        elif lock not in {NO_FACE, "no_host", "absent", ""}:
            errors.append(f"{lang}: prompt face_lock must be {NO_FACE}")
        inputs = " ".join(
            str(x)
            for x in (
                prompt.get("input_files_in_repo")
                or prompt.get("input_files_on_box")
                or prompt.get("input_urls")
                or []
            )
        )
        if FORBIDDEN_INPUT_RE.search(inputs) or ALENA_RE.search(inputs):
            errors.append(f"{lang}: Alena / victoria.png / hair-lock / cover-old used as i2i input")
        if FACE_FILE_RE.search(inputs) or FACE_FILE_RE.search(str(prompt.get("i2i_source") or "")):
            if not live_face:
                errors.append(f"{lang}: do not put a face ref in generation (Виктория.png / sheet)")
        if live_face and want_face not in inputs and want_face not in blob:
            errors.append(f"{lang}: i2i must use {want_face}")
        urls = prompt.get("input_urls") or []
        url0 = str(urls[0]) if urls else ""
        if live_face and urls and want_face not in url0 and not (
            want_face == LEGACY_FACE and LEGACY_FACE in url0
        ):
            errors.append(f"{lang}: input_urls[0] must be {want_face} (Excalibur i2i order)")
        if not live_face:
            active = str(prompt.get("prompt") or "")
            count = int(prompt.get("prompt_char_count") or len(active))
            if len(active) > PROMPT_MAX_CHARS or count > PROMPT_MAX_CHARS:
                errors.append(
                    f"{lang}: prompt_char_count {max(count, len(active))} > {PROMPT_MAX_CHARS}"
                )
            if any(FACE_FILE_RE.search(str(u)) for u in urls):
                errors.append(f"{lang}: input_urls must not include a host face file")
            if any(RETIRED_FACE_RE.search(str(u)) for u in urls) or RETIRED_FACE_RE.search(
                str(prompt.get("i2i_source") or "")
            ):
                errors.append(f"{lang}: i2i of viktoriaref / victoria-sheet / victoria.png is forbidden")
            head = active[:500]
            if not re.search(
                r"no host|no woman|no (face|portrait)|без (лица|портрет)|без Вик",
                head,
                re.I,
            ):
                errors.append(f"{lang}: prompt must start with no host portrait / no Vika")
            if re.search(r"same woman as Виктория|one woman, same face", head, re.I):
                errors.append(f"{lang}: prompt must not lock a host face")
        else:
            active = str(prompt.get("prompt") or "")
            count = int(prompt.get("prompt_char_count") or len(active))
            if len(active) > PROMPT_MAX_CHARS or count > PROMPT_MAX_CHARS:
                errors.append(
                    f"{lang}: prompt_char_count {max(count, len(active))} > {PROMPT_MAX_CHARS} "
                    "(long collage essay starves face lock)"
                )
            if urls and len(urls) != 1:
                errors.append(f"{lang}: exactly one input_url — {LEGACY_FACE} only")
            if any(STYLE_LOCK_RE.search(str(u)) for u in urls):
                errors.append(f"{lang}: do not send animals-viktoria-style-lock as i2i")
            if any(RETIRED_FACE_RE.search(str(u)) for u in urls) or RETIRED_FACE_RE.search(
                str(prompt.get("i2i_source") or "")
            ):
                errors.append(f"{lang}: i2i of viktoriaref / victoria-sheet / victoria.png is forbidden")
            head = active[:500]
            if LEGACY_FACE not in head or not re.search(
                r"зелён.*карим|green.*hazel|green.*light-brown|green.*hazel-brown",
                head,
                re.I,
            ):
                errors.append(
                    f"{lang}: prompt must start with {LEGACY_FACE} + "
                    "green/hazel / зелёные с лёгким карим"
                )
            if not re.search(r"one woman|одна женщин|same face|Виктория", head, re.I):
                errors.append(f"{lang}: prompt must lock one woman / same face as Виктория.png")
        if str(prompt.get("slice_method") or "") != "seam":
            errors.append(f"{lang}: slice_method must be seam (Excalibur white-gutter cut)")
        visual_positive = " ".join(
            [str(prompt.get("prompt") or "")]
            + [str(b.get("visual_only") or "") for b in (prompt.get("panel_visual_brief") or [])]
        )
        if SHEET_CLOTHES_RE.search(visual_positive):
            errors.append(
                f"{lang}: prompt copies sheet clothes/pose (white cami+jeans or ivory blazer). "
                "Clothes must change. Ban those looks in negative_prompt only."
            )
        if STICKER_HALO_RE.search(visual_positive):
            errors.append(
                f"{lang}: prompt asks for sticker/cutout/white halo. "
                "Use a seamed canvas (Excalibur). Ban stickers in negative_prompt only."
            )
        if not SEAM_RE.search(blob):
            errors.append(f"{lang}: prompt must request thin white gutters / seam slice")
        if PLATINUM_RE.search(visual_positive) and not re.search(
            r"fail|forbidden|not |не |ban|avoid|запрет|избегать", visual_positive, re.I
        ):
            errors.append(f"{lang}: platinum / white-blonde in positive prompt")
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

- (a) no host portrait; face_lock=none; do not i2i Виктория.png (live 27–30.08 historical face packs grandfathered)
- (b) >=3 slides use animals as metaphor
- (c) >=2 save slides have a real framework or questions
- (d) hook is a scene
- (e) no platinum
- (f) no empty vibe-only slides
- (g) no sheet cami+jeans / ivory blazer
- (h) seam slice (Excalibur white gutters), no sticker halo
- (i) CTA = app_audio (аудиоразбор in the APP); bot as comment prize = FAIL
- (j) FACE_CHECK.md verdict ABSENT — GATE FAIL if Vika / any host portrait. FACE MATCH vs Виктория.png is retired
- caption: one trigger word, no raw URLs, links in profile, no Academy on EN
"""
    report.write_text(body, encoding="utf-8")
    print("✅ CANON GATE PASS")
    print(f"wrote {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
