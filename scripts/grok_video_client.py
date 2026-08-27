"""Kie.ai Grok Imagine Video 1.5 Preview — image to video."""

from __future__ import annotations

from typing import Any

from kie_common import KieTaskClient

MODEL = "grok-imagine-video-1-5-preview"

# Kie grok-imagine-video-1-5-preview rejects 3:4 / 4:5.
# Allowed: auto, 1:1, 16:9, 9:16, 3:2, 2:3. Default auto.
# For a single image, aspect_ratio is ignored and the video follows the source PNG.
_GROK_ASPECT_ALLOWED = {"auto", "1:1", "16:9", "9:16", "3:2", "2:3"}
_GROK_ASPECT_ALIASES = {"3:4": "auto", "4:5": "auto"}


def normalize_grok_aspect_ratio(aspect_ratio: str) -> str:
    value = (aspect_ratio or "auto").strip()
    if value in _GROK_ASPECT_ALLOWED:
        return value
    return _GROK_ASPECT_ALIASES.get(value, "auto")


DEFAULT_LOOP_PROMPT_RU = (
    "Сохрани референс-кадр один в один. "
    "Создай тонкое бесшовное зацикленное видео 5 секунд. "
    "Лёгкий parallax, пульс света, микродвижение без смены сцены. "
    "Первый и последний кадр совпадают для бесконечного loop. "
    "Без новых объектов, без искажения лиц, без hard cuts. "
    "Hook-слайд Instagram-карусели."
)


class GrokVideoClient(KieTaskClient):
    def create_task(
        self,
        image_urls: list[str],
        prompt: str | None = None,
        aspect_ratio: str = "3:4",
        resolution: str = "720p",
        duration: int = 5,
        nsfw_checker: bool = True,
        callback_url: str | None = None,
    ) -> str:
        if not image_urls:
            raise ValueError("image_urls required (HTTPS URL of slide-01)")

        payload: dict[str, Any] = {
            "model": MODEL,
            "input": {
                "image_urls": image_urls,
                "aspect_ratio": normalize_grok_aspect_ratio(aspect_ratio),
                "resolution": resolution,
                "duration": duration,
                "nsfw_checker": nsfw_checker,
            },
        }
        if prompt:
            payload["input"]["prompt"] = prompt
        if callback_url:
            payload["callBackUrl"] = callback_url
        return self.create_task_raw(payload)
