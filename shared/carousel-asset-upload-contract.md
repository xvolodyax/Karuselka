# Carusel — загрузка через Kie.ai File Upload API

Instagram MCP требует **HTTPS URL**. Используем **тот же KIE_API_KEY**, без catbox/FTP.

Документация: https://docs.kie.ai/file-upload-api/quickstart

## Выбранные методы

| Файл | Метод Kie | Почему |
|------|-----------|--------|
| **file1** (видео Grok) | **URL File Upload** | Grok уже отдал HTTPS → Kie копирует на свой CDN |
| **file2–file9** (PNG) | **File Stream Upload** | Локальные слайды, эффективно |
| reference image | Stream, fallback Base64 | Если локальный референс нужен как HTTPS `input_urls` |
| fallback | Base64 | Только если stream не проходит и файл ≤10 MB |

Base URL: `https://kieai.redpandaai.co`

## Скрипт

```bash
python scripts/upload_carousel_assets.py \
  --workspace <WORKSPACE> \
  --run-id cursor-bomba-grid-2026-06-25
```

`--run-id` (auto from brief/caption if omitted) scopes Kie path to `carusel/instagram/{run_id}` — unique URLs per run.
`--upload-path-suffix final-YYYYMMDD-HHMMSS` appends a unique final suffix to the run-scoped path.

If local Grok MP4 geometry differs from PNG slides, normalize file1 before publish:

```bash
python scripts/upload_carousel_assets.py \
  --workspace <WORKSPACE> \
  --run-id cursor-bomba-grid-2026-06-25 \
  --upload-path-suffix final-YYYYMMDD-HHMMSS \
  --normalize-video-to-slides \
  --reupload-video-stream
```

Выход: `carusel-memory/output/publish-urls.json`

```json
{
  "run_id": "cursor-bomba-grid-2026-06-25",
  "upload_path": "carusel/instagram/cursor-bomba-grid-2026-06-25",
  "file1": "https://...",
  ...
}
```

## Важно

- Загрузка на Kie **бесплатна**
- Файлы **временные** (~24 часа) — публикуй карусель в Instagram **сразу** после upload
- Тот же `KIE_API_KEY` в `Carusel/.env`
- Для multipart stream upload клиент **снимает** inherited `Content-Type: application/json`, иначе requests не ставит boundary и Kie отвечает `Please use multipart/form-data`.
- Base64 fallback использовать только для малых файлов (≤10MB), чаще для референса.
- file1 video и PNG slides должны сохранять один publish geometry contract. Если MP4 отличается от PNG по размеру/aspect, `upload_carousel_assets.py --normalize-video-to-slides` делает fit+pad без crop и stream-upload нормализованного mp4.

## Агент

`carusel-upload` → запускает скрипт → `carusel-publish` читает JSON.

## Endpoints

| Метод | Endpoint |
|-------|----------|
| Stream | `POST /api/file-stream-upload` |
| URL | `POST /api/file-url-upload` |
| Base64 | `POST /api/file-base64-upload` |

Код: `scripts/kie_file_upload.py`
