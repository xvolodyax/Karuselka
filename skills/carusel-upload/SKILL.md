---
name: carusel-upload
description: Kie.ai File Upload API — HTTPS URL для Instagram (stream + url upload).
---

# Carusel Upload

## Роль

Заливает медиа на **Kie.ai File Upload API** (тот же `KIE_API_KEY`) и собирает `publish-urls.json`.

**Без** catbox, FTP и стороннего хостинга.

## Методы (авто)

Default Instagram carousel = **9 static PNG** (`--static-all-pngs`). file1 = `slide-01.png`.

| Слайд | Kie метод |
|-------|-----------|
| file1–file9 PNG | **Stream upload** всех `slide-01.png` … `slide-09.png` |
| video (только если Hall просила) | URL/stream mp4 — не default |

Документация: https://docs.kie.ai/file-upload-api/quickstart  
Контракт: `shared/carousel-asset-upload-contract.md`

## Команда

```bash
python scripts/upload_carousel_assets.py \
  --workspace <WORKSPACE> \
  --run-id <run_id> \
  --static-all-pngs
```

`publish-urls.json` обязан нести **этот** `run_id`. Archive permalinks запрещены.

`--run-id` auto из brief/caption если не указан → Kie path `carusel/instagram/{run_id}` — уникальные URL на run.
Если fresh Guardian предупреждает, что MP4 размер отличается от PNG slides, перед publish использовать нормализованный локальный file1:

```bash
python scripts/upload_carousel_assets.py \
  --workspace <WORKSPACE> \
  --run-id <run_id> \
  --upload-path-suffix final-YYYYMMDD-HHMMSS \
  --normalize-video-to-slides \
  --reupload-video-stream
```

Также можно передать уже готовый файл: `--normalized-video-path carusel-memory/output/video/slide-01-publish-816x1088.mp4`.

## Выход

`carusel-memory/output/publish-urls.json`

## Важно

- Файлы на Kie **временные (~24ч)** — сразу после upload → `carusel-publish`
- Static mode: нет mp4 — это норма. Не требовать grok log / `slide-01.mp4`.
- `kie_file_upload.py` stream upload уже снимает inherited `Content-Type: application/json`, чтобы requests поставил multipart boundary.
- Скрипты находятся в plugin: `<CURSOR_PLUGIN_DIR>/carusel\scripts\...`; не предполагай `Carusel/scripts`.
- В логах/print не использовать Unicode arrows на Windows; только ASCII.
- Для publish все 9 assets должны иметь один visual aspect/size contract: если Grok MP4 отличается от PNG (`816x1104` vs `816x1088`), делай fit+pad normalization без crop и stream upload file1.

## Fragment

```text
=== CARUSEL-UPLOAD ===
Статус: ✅ OK | ❌ FAIL
provider: kie_file_upload_api
publish-urls.json: carusel-memory/output/publish-urls.json
incident_report: none
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
