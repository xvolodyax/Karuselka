---
name: carusel-publish
description: Публикация 9-slide carousel (grid 3×3) в Instagram через MCP t4528_carrusel_instagram.
---

# Carusel Publish

## Вызов

Только отдельный Task. Director не вызывает Instagram MCP сам.  
Если `publish_requested: false` в brief — **не публикуй**, fragment ❌ BLOCKER.

Caption без сырых URL. Handle по `lang`. `@todaytaro_bot` — бот, не приложение.  
Fragment: `dispatched_via`, `dispatch_id`, `HANDOFF_NEXT: fixic`.

## Preconditions

- Guardian: `✅ DESIGN OK` or score ≥ 90
- `CAROUSEL_CAPTION.json` → `full_caption`
- **`carusel-memory/output/publish-urls.json`** — от агента `carusel-upload`

## Шаг 0 — upload (если ещё не сделан)

`Task(carusel-upload)` → `upload_carousel_assets.py` → `publish-urls.json`

## MCP contract

Читай `shared/instagram-publish-contract.md`.

```text
server: user-instagram carusel
toolName: t4528_carrusel_instagram
```

**Critical:** slide 3 param is `File3` (capital F).
**Critical:** Make-сценарий ожидает **9 файлов**: `file1`, `file2`, `File3`, `file4` … `file9`.

## Anti-duplicate rule

Публикация — side-effect. **Один run = один MCP call.**

Запрещено:

- **blind retry** — второй MCP call с тем же payload без явного OK пользователя;
- "тестировать" тем же MCP tool с picsum/short caption после production payload;
- отправлять 6-file payload для 9-slide grid.

Разрешено и ожидаемо:

- **один** MCP call на run после успешного `publish_preflight.py`;
- если preflight BLOCK из‑за URL overlap → **сначала** `upload_carousel_assets.py --run-id {run_id}`, затем publish (не останавливаться без MCP);
- если пользователь подтвердил «поста нет / Make не вызывался» → fresh upload + один MCP call.

**Не блокируй MCP** только по совпадению имён файлов (`slide-05.png`) — сравнивай **полные HTTPS URL** через `publish_preflight.py`.

## MCP async — ждать ответ

Make публикует **~3–5 минут**. Ответ MCP часто:

```text
Tool execution has started, but did not complete yet
```

Это **не ошибка** и **не повод для retry**.

После **единственного** `CallMcpTool`:

1. **Подожди 3–5 минут** (не завершай задачу сразу).
2. Если клиент вернул async — зафиксируй `pending-confirmation`, но **не вызывай MCP повторно**.
3. Статус `✅ OK` ставь, если пользователь или Make подтвердили успех; иначе `⏳ PENDING` + попроси проверить Instagram/Make.

Запрещено: интерпретировать async как fail и сразу слать второй call.

Старый сценарий (устарел): «если нет post URL за 5 мин → incident и стоп без call» — заменён на «один call + wait + pending».

## Arguments (из publish-urls.json)

```json
{
  "file1": "<video slide-01>",
  "file2": "<slide-02>",
  "File3": "<slide-03>",
  "file4": "...",
  "file5": "...",
  "file6": "...",
  "file7": "<slide-07>",
  "file8": "<slide-08>",
  "file9": "<slide-09>",
  "caption": "<из CAROUSEL_CAPTION.json>"
}
```

Читай ключи из `publish-urls.json`. MCP schema может иметь только file1–file6 — см. contract.

## Pre-flight

1. Есть `publish-urls.json` от `carusel-upload` (Kie File Upload API).
2. Caption из `CAROUSEL_CAPTION.json`.
3. В `publish-urls.json` есть `file1`, `file2`, `File3`, `file4`, `file5`, `file6`, `file7`, `file8`, `file9`.
4. **Обязательно запусти:** `python scripts/publish_preflight.py --workspace .`
   - exit 0 → **вызови MCP** (не пропускай шаг);
   - exit 2 → re-upload `--run-id`, preflight снова, затем MCP;
   - **не** блокируй вручную по `publish-log.md` без preflight.
5. Log в `publish-log.md` **перед** MCP.

### Verified MCP (2026-06-25)
- Args must be **HTTPS URLs**, not `C:\...` paths or `file://`.
- `BundleValidationError` на 3 параметра при 6-file payload означает: отсутствуют `file7`, `file8`, `file9`.

## Post-call

Append to `carusel-memory/output/publish-log.md`:

- timestamp
- MCP response
- errors if any
- post URL if returned
- if async/no URL after wait: `pending-confirmation`, no retry

## Connection test mode

For `verify_mcp_connection.py` or first run:

- Use test slides from `output/slides/`
- Caption: `[TEST] Carusel MCP connection check`
- Document result in `output/mcp-connection-report.md`

## Phase 3 — video slide 1 (активно)

`file1` = HTTPS URL `slide-01.mp4` (Grok, 5s loop)  
`file2`–`file9` = HTTPS PNG (slides 2–9)  
Первый файл задаёт aspect ratio всей карусели.

## Fragment

```text
=== CARUSEL-PUBLISH ===
Статус: ✅ OK | ❌ FAIL | ⏳ PENDING
dispatched_via: Task(carusel-publish) | Task(generalPurpose)
dispatch_id: <from pipeline_gate>
Log: carusel-memory/output/publish-log.md
incident_report: none
HANDOFF_NEXT: fixic
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
