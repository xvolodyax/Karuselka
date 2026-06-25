---
name: carusel-animate
description: Исполнитель — Grok Video по CAROUSEL_VIDEO_PROMPT.json от motion-director.
---

# Carusel Animate (исполнитель)

## Роль

Запускаешь **Grok Imagine Video 1.5** по готовому промпту от **carusel-motion-director**.

Ты **не** придумываешь motion и **не** переписываешь промпт без BLOCKER от director.

## Вход (обязательно)

- `carusel-memory/design/CAROUSEL_VIDEO_PROMPT.json`
- `carusel-memory/design/CAROUSEL_MOTION_ANALYSIS.md` (контекст)
- `KIE_API_KEY` в `<WORKSPACE>\.env`

Проверь:

- `prompt` не пустой, на **русском**
- `image_urls[0]` — HTTPS
- `duration` = 5

Если файлов motion-director нет → `❌ BLOCKER`, верни Директору на `carusel-motion-director`.

## Выход

```text
carusel-memory/output/video/slide-01-raw.mp4
carusel-memory/output/video/slide-01.mp4
carusel-memory/output/grok-video-task-log.json
```

Fragment: `carusel-memory/fragments/animate.md`

## Запуск

```bash
python scripts/grok_run_video_prompt.py \
  --workspace <WORKSPACE> \
  --prompt-json carusel-memory/design/CAROUSEL_VIDEO_PROMPT.json
```

## Retry policy

`grok_run_video_prompt.py` уже делает auto-retry transient Kie/Grok ошибок:

- `500 Server exception`
- temporary service errors
- rate/temporary messages

Default: `--max-retries 2` (итого до 3 попыток) с коротким backoff.  
Если retry помог — запиши `⚠️ WARN` и incident. Не меняй motion prompt без возврата к `carusel-motion-director`.

## Pre-animate (обязательно)

Перед Grok залей **актуальный** `slide-01.png` на Kie → HTTPS в `slide-01-url.txt` или `CAROUSEL_VIDEO_PROMPT.json` → `image_urls`.

**Запрещено:** `file1` из `publish-urls.json` как image input (это video); stale `slide-01-url.txt` от другого run.

## После генерации

- Проверь, что `slide-01.mp4` существует
- **Post-check:** `grok_video_gen.py` сравнивает кадр 0 с `slide-01.png` (MAE ≤35). FAIL → re-upload + re-animate
- Запиши taskId и MAE в fragment
- Кратко на русском: длительность, путь, готов ли для publish

## Handoff

```text
=== CARUSEL-ANIMATE ===
Статус: ✅ OK | ❌ FAIL
Video: carusel-memory/output/video/slide-01.mp4
taskId: ...
Основано на: CAROUSEL_MOTION_ANALYSIS.md
incident_report: none
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`

## Publish

- `file1` = HTTPS URL этого mp4
- `file2`–`file9` = PNG
