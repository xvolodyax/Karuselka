#!/usr/bin/env python3
"""CTA canon: app audio reading, not 3 free bot spreads."""

from __future__ import annotations

import unittest

import cta_canon


RU_OK = (
    "Напиши ПАУЗА @todaytaro_ru. В Direct пришлём аудиоразбор в приложении: "
    "Суть – Тень – Вектор. Ссылки в профиле."
)
EN_OK = (
    "Comment PAUSE @todaytaro_bot. We'll DM an audio reading in the app: "
    "Essence–Shadow–Vector. Links are in the profile."
)
RU_SLIDE9 = "Напиши ПАУЗА. Аудиоразбор в приложении. Суть – Тень – Вектор."
EN_SLIDE9 = "Comment PAUSE. Audio reading in the app. Essence–Shadow–Vector."


class CtaCanonTest(unittest.TestCase):
    def test_ru_app_audio_passes(self) -> None:
        self.assertEqual(
            cta_canon.check_cta_offer(
                lang="ru",
                product="app_audio",
                caption_blob=RU_OK,
                slide9_blob=RU_SLIDE9,
            ),
            [],
        )

    def test_en_app_audio_passes(self) -> None:
        self.assertEqual(
            cta_canon.check_cta_offer(
                lang="en",
                product="app_audio",
                caption_blob=EN_OK,
                slide9_blob=EN_SLIDE9,
            ),
            [],
        )

    def test_bot_product_fails(self) -> None:
        errors = " ".join(
            cta_canon.check_cta_offer(
                lang="en",
                product="bot_three_spreads",
                caption_blob=EN_OK,
                slide9_blob=EN_SLIDE9,
            )
        )
        self.assertIn("product must be app_audio", errors)

    def test_en_bot_prize_fails(self) -> None:
        errors = " ".join(
            cta_canon.check_cta_offer(
                lang="en",
                product="app_audio",
                caption_blob=(
                    "Comment PAUSE @todaytaro_bot. We'll DM you 3 free spreads "
                    "in our bot. Links are in the profile."
                ),
                slide9_blob="Comment PAUSE. 3 free readings in the bot.",
            )
        )
        self.assertIn("comment prize cannot be the bot", errors)
        self.assertIn("3 free readings", errors)

    def test_ru_bot_prize_fails(self) -> None:
        errors = " ".join(
            cta_canon.check_cta_offer(
                lang="ru",
                product="app_audio",
                caption_blob=(
                    "Напиши ПАУЗА @todaytaro_ru. В Direct — три бесплатных расклада "
                    "в боте. Ссылки в профиле."
                ),
                slide9_blob="Напиши ПАУЗА. 3 расклада в боте.",
            )
        )
        self.assertIn("comment prize cannot be the bot", errors)
        self.assertIn("три бесплатных расклада", errors)

    def test_missing_audio_and_frame_fails(self) -> None:
        errors = " ".join(
            cta_canon.check_cta_offer(
                lang="en",
                product="app_audio",
                caption_blob="Comment PAUSE @todaytaro_bot. Links are in the profile.",
                slide9_blob="Comment PAUSE",
            )
        )
        self.assertIn("audio reading", errors)
        self.assertIn("Essence", errors)

    def test_missing_profile_links_fails(self) -> None:
        errors = " ".join(
            cta_canon.check_cta_offer(
                lang="en",
                product="app_audio",
                caption_blob=(
                    "Comment PAUSE. We'll DM an audio reading in the app: "
                    "Essence–Shadow–Vector."
                ),
                slide9_blob=EN_SLIDE9,
            )
        )
        self.assertIn("links are in the profile", errors)

    def test_lichny_audio_fails(self) -> None:
        errors = " ".join(
            cta_canon.check_cta_offer(
                lang="ru",
                product="app_audio",
                caption_blob=(
                    "Напиши ПАУЗА. В Direct — личный аудиоразбор в приложении: "
                    "Суть – Тень – Вектор. Ссылки в профиле."
                ),
                slide9_blob=RU_SLIDE9,
            )
        )
        self.assertIn("личный аудиоразбор", errors)

    def test_legacy_bot_pack_ids(self) -> None:
        self.assertTrue(cta_canon.is_legacy_bot_pack({"pack_id": "2026-08-27-swarm"}))
        self.assertTrue(cta_canon.is_legacy_bot_pack({"pack_id": "2026-08-27-v2"}))
        self.assertFalse(cta_canon.is_legacy_bot_pack({"pack_id": "2026-08-28-cta"}))


if __name__ == "__main__":
    unittest.main()
