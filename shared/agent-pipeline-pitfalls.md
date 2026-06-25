# Carusel — типичные сбои пайплайна

Читать **Директору и всем субагентам** перед run. Fixic дополняет после инцидентов.

## 1. Instagram MCP — только HTTPS URL

- **Симптом:** `BundleValidationError` на Windows paths; `OAuthException 9004` на `file://`
- **Решение:** `carusel-upload` → Kie File Upload API → `publish-urls.json`
- **Кто:** upload → publish

## 2. MCP param `File3` (capital F)

- **Симптом:** slide 3 не попадает в карусель
- **Решение:** в MCP args ключ **`File3`**, не `file3`
- **Кто:** publish

## 2.1 Publish MCP — 9 файлов и один вызов

- **Симптом:** `BundleValidationError: Validation failed for 3 parameter(s)` на payload `file1`–`file6`
- **Root cause:** Make-сценарий ждёт `file7`, `file8`, `file9`
- **Решение:** всегда отправлять `file1`, `file2`, `File3`, `file4`…`file9`, `caption`
- **Важно:** publish не idempotent — **не делать blind retry**. Один MCP call, ждать до 5 минут; если no completion/post URL — `pending-confirmation` и ручная проверка Instagram/Make.
- **Кто:** publish

## 3. Kie API — один ключ

- **Симптом:** 401 на image/video/upload
- **Решение:** `KIE_API_KEY` в `Carusel/.env` (workspace root)
- **Кто:** slice, animate, upload

## 4. Grok video — нужен HTTPS на slide-01 для motion

- **Симптом:** motion-director blocker «нет URL»
- **Решение:** после slice — Kie upload slide-01 **или** URL из цепочки generation; для motion до upload — URL из Kie image task / brief reference
- **Кто:** motion-director, upload

## 5. Kie File Upload — файлы временные (~24ч)

- **Симптом:** Instagram не открывает media через сутки
- **Решение:** publish **сразу** после upload
- **Кто:** Director, publish

## 6. Wide master 6480×1350 (legacy)

Устарело — default **grid_3x3** (`shared/carousel-grid-design.md`).

## 7. Промпты на русском

- image-prompter, motion-director — промпты для Kie/Grok **на русском**
- **Кто:** copywriter/designer не путают с caption

## 8. Grid 3×3 — один Kie 3:4 @ 4K

- **Формат:** `generation_mode: grid_3x3`, `aspect_ratio: 3:4`, `resolution: 4K`
- **Нарезка:** `slice_grid.py --cols 3 --rows 3`
- **Анимация:** только `slide-01`
- **MCP:** для publish нужны все 9 файлов (`file1`, `file2`, `File3`, `file4`…`file9`)
- **Важно:** все 9 PNG и video slide-01 должны иметь один aspect `3:4`; не смешивать `3:4` и `4:5`.

## 8.1 Windows stdout

- **Симптом:** `UnicodeEncodeError: 'charmap' codec can't encode...` на Windows PowerShell/cp1251
- **Решение:** в скриптовых `print()` только ASCII (`->`, `...`) или запуск с `PYTHONIOENCODING=utf-8`
- **Кто:** slice, upload, common polling

## 8.2 Grok transient 500

- **Симптом:** `Task failed: 500 — Server exception, please try again later`
- **Решение:** `grok_video_gen.py` делает auto-retry (`--max-retries 2`) без смены prompt
- **Кто:** animate

## 9. Vertical slice bleed (grid 3×3)

- **Симптом:** orphan-текст в верхней полосе slides 04–09 («хвост» ячейки сверху)
- **Prevention:** image-prompter — safe margin 10–12% от всех gutters и краёв ячейки
- **Recovery:** regenerate master с усиленным prompt; **не** делать post-crop отдельных слайдов в publish assets
- **Кто:** slice, design-guardian

## 10. Grok video source mismatch

- **Симптом:** frame 0 mp4 показывает **чужой** hook (другой run / Fixic test)
- **Root cause:** stale `slide-01-url.txt` или fallback на `publish-urls.json` file1 (video URL)
- **Решение:** перед animate — fresh Kie upload `slide-01.png`; post-animate MAE check (`video_frame_qa.py`, threshold 35)
- **Кто:** animate, design-guardian

## 11. Publish blocked — duplicate Kie URLs

- **Симптом:** новый run не может publish — те же 9 HTTPS URL в `publish-log.md` от prior run
- **Root cause:** upload без run-scoped path (`carusel/instagram` shared)
- **Решение:** `upload_carousel_assets.py --run-id {run_id}`; pre-flight `publish_preflight.py`
- **Кто:** upload, publish

## 11.1 Kie 400 на длинном image prompt

- **Симптом:** Kie i2i task на валидном `grid_3x3`, `3:4 @ 4K` падает `failCode: 400`, `Internal Error, Please try again later`
- **Root cause:** слишком длинный/сложный активный prompt или payload complexity; fresh reference URL сам по себе не лечит
- **Решение:** compact retry: `prompt` ≤4500 chars (target 2800–4200), подробности в `style_lock`, `reference_contract`, `typography_rules`, `panel_visual_brief`
- **Важно:** сначала compact prompt retry в том же `3:4 @ 4K`; не менять aspect/resolution до этого без явного разрешения
- **Кто:** image-prompter, slice, design-guardian

## 11.2 MP4 geometry mismatch before publish

- **Симптом:** Guardian OK, но предупреждает MP4 `816x1104` против PNG slides `816x1088`
- **Root cause:** Grok video result может иметь высоту/размер, отличающийся от slice PNG
- **Решение:** перед upload/publish нормализовать file1 к PNG slide size через fit+pad без crop и stream upload локального mp4: `upload_carousel_assets.py --normalize-video-to-slides --reupload-video-stream`
- **Важно:** regenerated `publish-urls.json` должен указывать `video_source: kie_stream_upload_local_video` и `video_normalization`
- **Кто:** upload, publish, design-guardian

## 11.3 White gutters / edge hairlines after grid slice

- **Симптом:** первые slides выглядят OK, но на 04-09 или отдельных edges остаются белые 1-3px рамки/hairlines
- **Root cause:** Kie рисует visible gutters/outer frame в master или оставляет near-white pixels на будущих cut-lines; strict slice честно переносит их в PNG
- **Решение:** canonical no-frame pipeline в `kie_carousel_gen.py`: `remove_grid_gutters.py` -> strict `slice_grid.py` -> `clean_slide_edges.py` -> `grid_gutter_qa.py`
- **Важно:** не crop отдельных slides и не менять размеры; cleanup заменяет только near-white pixels на exact cut-lines/edge strips
- **BLOCKER:** `grid-gutter-qa-clean.json` не `status: ok`
- **Кто:** image-prompter, slice, design-guardian

## 12. Incident memory

- Проблема не в списке → **incident** в `carusel-memory/pipeline-fix-queue.md`
- После run → **carusel-fixic**

---

Файл: `carusel/shared/agent-pipeline-pitfalls.md`. Fixic обновляет после `status: fixed`.
