"""Kie.ai Grok Imagine Video 1.5 Preview — image to video."""

from __future__ import annotations

from typing import Any

from kie_common import KieTaskClient

MODEL = "grok-imagine-video-1-5-preview"

# Kie grok-imagine-video-1-5-preview createTask enum. No 3:4.
KIE_GROK_ASPECT_RATIOS = ("1:1", "16:9", "9:16", "3:2", "2:3", "auto")
CONTRACT_ASPECT_TO_KIE = {
    "3:4": "auto",  # carousel contract; auto follows the source PNG
}

DEFAULT_LOOP_PROMPT_RU = (
    "Сохрани референс-кадр один в один. "
    "Создай тонкое бесшовное зацикленное видео 5 секунд. "
    "Лёгкий parallax, пульс света, микродвижение без смены сцены. "
    "Первый и последний кадр совпадают для бесконечного loop. "
    "Без новых объектов, без искажения лиц, без hard cuts. "
    "Hook-слайд Instagram-карусели."
)


def map_aspect_ratio_for_kie(aspect_ratio: str) -> str:
    """Map carousel contract aspect to a Kie grok-imagine-video enum value."""
    if aspect_ratio in KIE_GROK_ASPECT_RATIOS:
        return aspect_ratio
    return CONTRACT_ASPECT_TO_KIE.get(aspect_ratio, "auto")


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

        kie_aspect = map_aspect_ratio_for_kie(aspect_ratio)
        payload: dict[str, Any] = {
            "model": MODEL,
            "input": {
                "image_urls": image_urls,
                "aspect_ratio": kie_aspect,
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
