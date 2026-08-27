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
| aspect_ratio | contract `3:4` (PNG slides); Kie createTask sends **`auto`** |
| resolution | `720p` |
| image_urls | HTTPS URL **slide-01.png** |

### Kie `aspect_ratio` enum (grok-imagine-video-1-5-preview)

Allowed: `1:1`, `16:9`, `9:16`, `3:2`, `2:3`, `auto`. **No `3:4`.**

Carousel contract stays `3:4` (same as PNG slide-01). Before `createTask`,
`grok_video_client.py` maps `3:4` → `auto` so Kie follows the source PNG.
Docs note aspect is ignored for a single image; `auto` is the durable send value.
Do not rewrite `CAROUSEL_VIDEO_PROMPT.json` just to change this field.

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
