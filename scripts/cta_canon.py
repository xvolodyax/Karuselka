#!/usr/bin/env python3
"""Instagram carousel CTA canon — app audio reading, not the bot.

Vladimir 27.08.2026: last slide + caption sell the APP audio reading.
Comment a topic-tied code word. Direct = аудиоразбор / audio reading in the app
(RU: Суть – Тень – Вектор; EN: Essence–Shadow–Vector).
No raw URLs; links live in the profile.
"""

from __future__ import annotations

import re
from typing import Any

REQUIRED_PRODUCT = "app_audio"
# Already-live / already-shipped 27.08 packs. Do not restyle their copy.
LEGACY_BOT_PACK_IDS = frozenset({"2026-08-27-swarm", "2026-08-27-v2"})

BOT_PRIZE_RE = re.compile(
    r"3 free (bot )?spreads|3 free readings|"
    r"три бесплатных расклад|"
    r"бесплатн\w{0,8} расклад|"
    r"spreads in (our |the )?bot|"
    r"readings in (our |the )?bot|"
    r"расклад\w{0,8} в боте|"
    r"in the bot to|"
    r"в боте\.|в боте,",
    re.I,
)
AUDIO_RE = {
    "ru": re.compile(r"аудиоразбор", re.I),
    "en": re.compile(r"audio reading", re.I),
}
FRAMEWORK = {
    "ru": (("Суть", re.compile(r"суть", re.I)), ("Тень", re.compile(r"тень", re.I)), ("Вектор", re.compile(r"вектор", re.I))),
    "en": (
        ("Essence", re.compile(r"essence", re.I)),
        ("Shadow", re.compile(r"shadow", re.I)),
        ("Vector", re.compile(r"vector", re.I)),
    ),
}
PROFILE_LINKS_RE = re.compile(
    r"ссылк\w* в (шапк|профил)|в профиле|в шапке|"
    r"link in (bio|profile)|links? (are )?in the profile",
    re.I,
)
LICHNY_AUDIO_RE = re.compile(r"личный аудиоразбор", re.I)
NASH_APP_RE = re.compile(r"в нашем приложении", re.I)
SCENA_LABEL_RE = re.compile(r"(^|\s)Сцена(\s|$|[.:,])")


def is_legacy_bot_pack(manifest: dict[str, Any] | None) -> bool:
    if not manifest:
        return False
    return str(manifest.get("pack_id") or "") in LEGACY_BOT_PACK_IDS


def check_cta_offer(
    *,
    lang: str,
    product: str | None,
    caption_blob: str,
    slide9_blob: str = "",
    prefix: str = "",
) -> list[str]:
    """FAIL if the comment prize is the bot, or the app-audio offer is missing."""
    label = prefix or lang
    errors: list[str] = []
    combined = f"{caption_blob}\n{slide9_blob}"
    if (product or "") != REQUIRED_PRODUCT:
        errors.append(
            f"{label}: product must be {REQUIRED_PRODUCT} (app audio reading), got {product!r}"
        )
    if BOT_PRIZE_RE.search(combined):
        errors.append(
            f"{label}: comment prize cannot be the bot "
            "(3 free readings / три бесплатных расклада). Sell the app audio reading."
        )
    audio = AUDIO_RE.get(lang) or AUDIO_RE["en"]
    if not audio.search(combined):
        need = "аудиоразбор" if lang == "ru" else "audio reading"
        errors.append(f"{label}: CTA must promise {need} in the APP")
    if not re.search(r"приложен|в приложении|\bapp\b", combined, re.I):
        errors.append(f"{label}: CTA must say the audio reading is in the APP")
    for name, rx in FRAMEWORK.get(lang) or FRAMEWORK["en"]:
        if not rx.search(combined):
            errors.append(f"{label}: CTA must name the topic frame {name}")
    if not PROFILE_LINKS_RE.search(caption_blob):
        errors.append(
            f"{label}: caption must say links are in the profile / ссылка в шапке (no raw URLs)"
        )
    if slide9_blob and BOT_PRIZE_RE.search(slide9_blob):
        errors.append(f"{label}: slide 9 sells the bot as the comment prize")
    if slide9_blob and not audio.search(slide9_blob) and not re.search(
        r"приложен|\bapp\b", slide9_blob, re.I
    ):
        errors.append(f"{label}: slide 9 hook must sell the app audio reading, not the bot")
    if LICHNY_AUDIO_RE.search(combined):
        errors.append(f"{label}: forbidden phrase личный аудиоразбор (write аудиоразбор)")
    if NASH_APP_RE.search(combined):
        errors.append(f"{label}: write «в моём приложении», not «в нашем приложении»")
    if SCENA_LABEL_RE.search(combined):
        errors.append(f"{label}: do not write the word «Сцена»")
    return errors
