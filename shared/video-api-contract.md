# Carusel — Grok Video API (slide-01)

> **Модель:** `grok-imagine-video-1-5-preview` (Kie.ai)  
> **Ключ:** тот же `KIE_API_KEY` в `Carusel/.env`

## Цель

Slide-01 (hook) → **5 секунд** зацикленного видео → Instagram `file1`.

## Endpoints

| Шаг | Method | URL |
|-----|--------|-----|
| Create | POST | `https://api.kie.ai/api/v1/jobs/createTask` |
| Poll | GET | `https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...` |

## Параметры по умолчанию

| Param | Value |
|-------|-------|
| model | `grok-imagine-video-1-5-preview` |
| duration | **5** |
| aspect_ratio | `3:4` (должен совпадать с PNG slide-01 и всеми слайдами) |
| resolution | `720p` |
| image_urls | HTTPS URL **slide-01.png** |

## Скрипты

| Файл | Назначение |
|------|------------|
| `grok_video_client.py` | API client |
| `grok_video_gen.py` | CLI generate + ffmpeg trim |
| `grok_run_video_prompt.py` | Run from `CAROUSEL_VIDEO_PROMPT.json` |

## Pipeline

```text
carusel-slice → carusel-animate → carusel-design-guardian → carusel-publish
```

## Publish

```json
{
  "file1": "https://.../slide-01.mp4",
  "file2": "https://.../slide-02.png",
  "File3": "https://.../slide-03.png",
  "file4": "...",
  "file5": "...",
  "file6": "..."
}
```

## ffmpeg (опционально)

Если установлен — обрезка/зацикливание до ровно 5s, `yuv420p` для Instagram.

## Агенты

| Агент | Решение | Исполнение |
|-------|---------|------------|
| **carusel-motion-director** | Смотрит slide-01, решает motion/речь/атмосферу, пишет RU-промпт | — |
| **carusel-animate** | — | Запускает Grok по JSON |
