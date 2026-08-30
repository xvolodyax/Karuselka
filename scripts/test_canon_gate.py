#!/usr/bin/env python3
"""canon_gate rejects mechanic hooks and missing animal metaphors."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import canon_gate as gate


def write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj, str):
        path.write_text(obj, encoding="utf-8")
    else:
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


class CanonGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="canon-gate-"))
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def test_real_pack_passes(self) -> None:
        pack = Path(__file__).resolve().parent.parent / "carusel-memory/packs/2026-08-29"
        if not pack.is_dir() or not (pack / "ru" / "CAROUSEL_SLIDE_COPY.json").is_file():
            self.skipTest("pack not in workspace")
        errors = gate.check_pack(pack)
        sheet = Path(__file__).resolve().parent.parent / "carusel-memory/references/Виктория.png"
        if not sheet.is_file():
            self.assertTrue(
                any("Виктория.png" in e for e in errors),
                errors,
            )
            errors = [e for e in errors if "Виктория.png" not in e]
        self.assertEqual(errors, [])

    def test_alena_and_sheet_clothes_fail(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "langs": ["ru"],
                "trigger_words": {"ru": "ПАУЗА"},
            },
        )
        slides = {
            "slide_count": 9,
            "visual_family": "animals_viktoria_collage",
            "hook_is_scene": True,
            "trigger_word": "ПАУЗА",
            "product": "bot_three_spreads",
            "slides": [
                {
                    "index": 1,
                    "role": "hook",
                    "hook_type": "scene",
                    "headline": "Он смотрит сторис.",
                    "body": "Третью неделю.",
                    "victoria": True,
                    "animal": "cat",
                    "animal_job": "чуешь",
                },
                {
                    "index": 2,
                    "role": "pain",
                    "headline": "Ты уже решила за него",
                    "body": "Если бы хотел — написал.",
                },
                {
                    "index": 3,
                    "role": "mistake",
                    "headline": "Карты не судят.",
                    "body": "Говорит: пауза.",
                    "has_framework": True,
                    "animal": "dog",
                    "animal_job": "верность",
                },
                {
                    "index": 4,
                    "role": "mechanism",
                    "headline": "Пауза — не ответ",
                    "body": "Это развилка трёх путей.",
                    "has_framework": True,
                },
                {
                    "index": 5,
                    "role": "save",
                    "headline": "Три вопроса",
                    "body": "Он отвечает?",
                    "has_framework": True,
                },
                {
                    "index": 6,
                    "role": "save",
                    "headline": "Что карта говорит",
                    "body": "Слышишь худшее.",
                    "animal": "owl",
                    "animal_job": "ночь",
                    "has_framework": True,
                },
                {
                    "index": 7,
                    "role": "save",
                    "headline": "Три состояния",
                    "body": "Ждёт / боится / вышел",
                    "has_framework": True,
                },
                {
                    "index": 8,
                    "role": "recap",
                    "headline": "Как отличить",
                    "body": "Правило решения.",
                    "has_framework": True,
                },
                {
                    "index": 9,
                    "role": "cta",
                    "headline": "Напиши ПАУЗА",
                    "body": "3 расклада в боте",
                    "victoria": True,
                },
            ],
        }
        write(pack / "ru" / "CAROUSEL_SLIDE_COPY.json", slides)
        write(
            pack / "ru" / "CAROUSEL_CAPTION.json",
            {
                "full_caption": "Напиши ПАУЗА @todaytaro_ru",
                "trigger_word": "ПАУЗА",
                "product": "bot_three_spreads",
                "mentions": ["@todaytaro_ru"],
            },
        )
        write(
            pack / "ru" / "CAROUSEL_IMAGE_PROMPT.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "victoria-hair-lock.png",
                "input_files_in_repo": [
                    "carusel-memory/references/victoria-hair-lock.png",
                    "/workspace/cover-refs/victoria.png",
                ],
                "prompt": "Victoria in white cami and light-wash jeans, ivory blazer.",
                "panel_visual_brief": [{"slide": 1, "visual_only": "ivory blazer"}],
                "negative_prompt": "none",
            },
        )
        for i in range(1, 10):
            write(pack / "ru" / "slides" / f"slide-{i:02d}.png", "x")
        errors = " ".join(gate.check_pack(pack))
        self.assertTrue("Alena" in errors or "victoria.png" in errors or "hair-lock" in errors, errors)
        self.assertTrue(
            "cami" in errors.lower() or "ivory" in errors.lower() or "clothes" in errors.lower(),
            errors,
        )

    def test_sticker_prompt_fails_without_seams(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "langs": ["ru"],
                "trigger_words": {"ru": "ШАГ"},
            },
        )
        slides = {
            "slide_count": 9,
            "visual_family": "animals_viktoria_collage",
            "hook_is_scene": True,
            "trigger_word": "ШАГ",
            "product": "bot_three_spreads",
            "slides": [
                {
                    "index": 1,
                    "role": "hook",
                    "hook_type": "scene",
                    "headline": "Он молчал 24 дня. В 23:42: «Спишь?»",
                    "body": "Ровно в тот вечер.",
                    "victoria": True,
                    "animal": "cat",
                    "animal_job": "чуешь",
                },
                {
                    "index": 2,
                    "role": "pain",
                    "headline": "Сердце колотится",
                    "body": "Снова ночь.",
                    "animal": "dog",
                    "animal_job": "ждёт",
                },
                {
                    "index": 3,
                    "role": "mistake",
                    "headline": "Ловушка импульса",
                    "body": "Это не любовь.",
                    "has_framework": True,
                },
                {
                    "index": 4,
                    "role": "mechanism",
                    "headline": "Это пинг",
                    "body": "Нулевые затраты.",
                    "animal": "owl",
                    "animal_job": "ночь",
                },
                {
                    "index": 5,
                    "role": "save",
                    "headline": "Три вопроса",
                    "body": "Есть действие?",
                    "has_framework": True,
                },
                {
                    "index": 6,
                    "role": "save",
                    "headline": "Что слышишь",
                    "body": "Слышишь худшее.",
                    "has_framework": True,
                },
                {
                    "index": 7,
                    "role": "save",
                    "headline": "Рамка шага",
                    "body": "Звонок днём.",
                    "has_framework": True,
                },
                {
                    "index": 8,
                    "role": "recap",
                    "headline": "Правило",
                    "body": "Шаг или пинг.",
                },
                {
                    "index": 9,
                    "role": "cta",
                    "headline": "Напиши ШАГ",
                    "body": "3 расклада в боте",
                    "victoria": True,
                },
            ],
        }
        write(pack / "ru" / "CAROUSEL_SLIDE_COPY.json", slides)
        write(
            pack / "ru" / "CAROUSEL_CAPTION.json",
            {
                "full_caption": "Напиши ШАГ @todaytaro_ru",
                "trigger_word": "ШАГ",
                "product": "bot_three_spreads",
                "mentions": ["@todaytaro_ru"],
            },
        )
        write(
            pack / "ru" / "CAROUSEL_IMAGE_PROMPT.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "slice_method": "zero-gutter",
                "input_urls": ["https://example.com/other.png"],
                "input_files_in_repo": ["carusel-memory/references/Виктория.png"],
                "prompt": "Zero-gutter cutout collage, white outline sticker around Victoria.",
                "panel_visual_brief": [{"slide": 1, "visual_only": "sticker cutout"}],
            },
        )
        for i in range(1, 10):
            write(pack / "ru" / "slides" / f"slide-{i:02d}.png", "x")
        errors = " ".join(gate.check_pack(pack))
        self.assertTrue("sticker" in errors.lower() or "cutout" in errors.lower() or "halo" in errors.lower(), errors)
        self.assertTrue("seam" in errors.lower() or "gutter" in errors.lower(), errors)

    def test_mechanic_hook_and_vibe_fail(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "visual_family": "brand_collage",
                "langs": ["ru"],
                "trigger_words": {"ru": "ПАУЗА"},
            },
        )
        slides = {
            "slide_count": 9,
            "visual_family": "brand_collage",
            "hook_is_scene": False,
            "slides": [
                {"index": i, "role": "value", "headline": "5 признаков паузы", "body": "vibe"}
                for i in range(1, 10)
            ],
        }
        write(pack / "ru" / "CAROUSEL_SLIDE_COPY.json", slides)
        errors = " ".join(gate.check_pack(pack))
        self.assertIn("animals_viktoria_collage", errors)
        self.assertIn("hook_is_scene", errors)

    def test_bot_prize_fails(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "pack_id": "2026-08-28-cta",
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "langs": ["en"],
                "trigger_words": {"en": "PAUSE"},
            },
        )
        slides = {
            "slide_count": 9,
            "visual_family": "animals_viktoria_collage",
            "hook_is_scene": True,
            "trigger_word": "PAUSE",
            "product": "bot_three_spreads",
            "slides": [
                {
                    "index": 1,
                    "role": "hook",
                    "hook_type": "scene",
                    "headline": "He watched your stories.",
                    "body": "Third week. No text.",
                    "victoria": True,
                    "animal": "cat",
                    "animal_job": "sense",
                },
                {
                    "index": 2,
                    "role": "pain",
                    "headline": "You already decided",
                    "body": "If he wanted to, he would text.",
                    "animal": "dog",
                    "animal_job": "wait",
                },
                {
                    "index": 3,
                    "role": "mistake",
                    "headline": "The cards don't judge.",
                    "body": "You hear a verdict.",
                    "has_framework": True,
                },
                {
                    "index": 4,
                    "role": "mechanism",
                    "headline": "A pause is a fork",
                    "body": "Three paths, not one answer.",
                    "has_framework": True,
                },
                {
                    "index": 5,
                    "role": "save",
                    "headline": "Three questions",
                    "body": "Does he answer?",
                    "has_framework": True,
                },
                {
                    "index": 6,
                    "role": "save",
                    "headline": "What you hear",
                    "body": "You hear the worst.",
                    "animal": "owl",
                    "animal_job": "night",
                    "has_framework": True,
                },
                {
                    "index": 7,
                    "role": "save",
                    "headline": "Three states",
                    "body": "Stuck / afraid / gone",
                    "has_framework": True,
                },
                {
                    "index": 8,
                    "role": "recap",
                    "headline": "Decision rule",
                    "body": "Pause is not over.",
                    "has_framework": True,
                },
                {
                    "index": 9,
                    "role": "cta",
                    "headline": "Comment PAUSE",
                    "body": "We'll DM you 3 free spreads in our bot.",
                    "victoria": True,
                },
            ],
        }
        write(pack / "en" / "CAROUSEL_SLIDE_COPY.json", slides)
        write(
            pack / "en" / "CAROUSEL_CAPTION.json",
            {
                "full_caption": (
                    "Comment PAUSE @todaytaro_bot. We'll DM you 3 free readings "
                    "in the bot."
                ),
                "trigger_word": "PAUSE",
                "product": "bot_three_spreads",
                "mentions": ["@todaytaro_bot"],
            },
        )
        write(
            pack / "en" / "CAROUSEL_IMAGE_PROMPT.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "slice_method": "seam",
                "input_urls": ["https://example.com/Виктория.png"],
                "input_files_in_repo": ["carusel-memory/references/Виктория.png"],
                "prompt": "Thin white gutters at 1/3 and 2/3. Face lock Виктория.png.",
                "panel_visual_brief": [{"slide": i, "visual_only": "scene"} for i in range(1, 10)],
            },
        )
        for i in range(1, 10):
            write(pack / "en" / "slides" / f"slide-{i:02d}.png", "x")
        errors = " ".join(gate.check_pack(pack))
        self.assertIn("comment prize cannot be the bot", errors)
        self.assertIn("3 free readings", errors)

    def test_long_prompt_fails_on_new_pack(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "pack_id": "2026-08-28",
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "langs": ["ru"],
                "trigger_words": {"ru": "ТЕПЛО"},
                "product": "app_audio",
            },
        )
        write(
            pack / "ru" / "CAROUSEL_SLIDE_COPY.json",
            {
                "slide_count": 9,
                "visual_family": "animals_viktoria_collage",
                "hook_is_scene": True,
                "trigger_word": "ТЕПЛО",
                "product": "app_audio",
                "slides": [
                    {
                        "index": 1,
                        "role": "hook",
                        "hook_type": "scene",
                        "headline": "В субботу он смотрел в глаза",
                        "body": "и строил планы.",
                        "victoria": True,
                        "animal": "cat",
                        "animal_job": "чуешь",
                    },
                    *[{"index": i, "role": "save", "headline": "Правило", "body": "Шаг.", "has_framework": True} for i in range(2, 9)],
                    {
                        "index": 9,
                        "role": "cta",
                        "headline": "Напиши ТЕПЛО",
                        "body": "Аудиоразбор в приложении. Суть – Тень – Вектор.",
                    },
                ],
            },
        )
        write(
            pack / "ru" / "CAROUSEL_CAPTION.json",
            {
                "full_caption": "Напиши ТЕПЛО @todaytaro_ru. Аудиоразбор в приложении. Ссылки в шапке профиля.",
                "trigger_word": "ТЕПЛО",
                "product": "app_audio",
                "mentions": ["@todaytaro_ru"],
            },
        )
        write(
            pack / "ru" / "CAROUSEL_IMAGE_PROMPT.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "Виктория.png",
                "slice_method": "seam",
                "input_urls": ["https://example.com/Виктория.png"],
                "prompt": "Thin white gutters at 1/3 and 2/3. " + ("collage cats type wardrobe " * 200),
                "prompt_char_count": 3631,
                "panel_visual_brief": [{"slide": i, "visual_only": "scene"} for i in range(1, 10)],
            },
        )
        errors = " ".join(gate.check_pack(pack))
        self.assertIn("prompt_char_count", errors)


if __name__ == "__main__":
    unittest.main()

