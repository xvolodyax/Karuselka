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
        pack = Path(__file__).resolve().parent.parent / "carusel-memory/packs/2026-08-27-v2"
        if not pack.is_dir():
            self.skipTest("pack not in workspace")
        errors = gate.check_pack(pack)
        sheet = Path(__file__).resolve().parent.parent / "carusel-memory/references/victoria-sheet.png"
        if not sheet.is_file():
            self.assertTrue(
                any("victoria-sheet.png" in e for e in errors),
                errors,
            )
            errors = [e for e in errors if "victoria-sheet.png" not in e]
        self.assertEqual(errors, [])

    def test_alena_and_sheet_clothes_fail(self) -> None:
        pack = self.tmp / "pack"
        write(
            pack / "PACK.json",
            {
                "visual_family": "animals_viktoria_collage",
                "face_lock": "victoria-sheet.png",
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


if __name__ == "__main__":
    unittest.main()
