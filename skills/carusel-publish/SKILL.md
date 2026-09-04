---
name: carusel-publish
description: Публикация 9+9 static PNG каруселей RU+EN в Instagram через Composio после GATE PASS.
---

# Carusel Publish

После **GATE PASS** + **FACE_CHECK ABSENT** (нет лица Вики) рой **сам** кладёт карусель.
Холл **не** публикует и слайды **не** пересматривает.

Читай `shared/composio-instagram-publish-contract.md`.

## Preconditions

- `GATE.md` = PASS
- `FACE_CHECK.md` = ABSENT — на слайдах нет лица Вики / портрета ведущей
- Guardian: `✅ DESIGN OK` или score ≥ 90 без P0
- CTA = кодовое слово → аудиоразбор в приложении, не бот
- В подписи нет сырых URL
- 9+9 статичные PNG, `publish-urls.json` с HTTPS

GATE FAIL / лицо Вики на слайде / CTA бота → **не публиковать**.

## Команда

```bash
python scripts/composio_instagram_publish.py --pack carusel-memory/packs/YYYY-MM-DD
```

Env: только `COMPOSIO_API_KEY`. Alias обязателен, не default:

- `instagram-ru` = `@todaytaro_ru`
- `instagram-en` = `@todaytaro_bot`

Telegram не слать. Ключ в git/лог/отчёт/fragment не писать.

## Что без ключа

GATE PASS + нет `COMPOSIO_API_KEY` → **SKIP «нет COMPOSIO_API_KEY»**, exit 0, не падать.

```bash
python scripts/pipeline_gate.py --workspace . skip --step publish --reason 'нет COMPOSIO_API_KEY'
```

## Уже live / anti-stale

`live-posts.json` — архив прошлых дат. SKIP `already-live` только для **того же** `pack_id`.
Чужие permalinks (30.08 `DcqJGCblQqv` / `DcqJS--m0op` и любые URL другой даты) **запрещено** писать как посты этого прогона.
В отчёт — только permalink из API текущего вызова.

## 403 / нет tool_execution

FAIL + `HOLE.md`, exit 2. Не крутить этот skill и не перечитывать `composio_instagram_publish.py`.

## Make MCP (устарел)

`t4528_carrusel_instagram` больше не канон. Не вызывать.

## Fragment

```text
=== CARUSEL-PUBLISH ===
Статус: ✅ OK | ⏭️ SKIP | ❌ FAIL
reason: composio | нет COMPOSIO_API_KEY | already-live
alias: instagram-ru / instagram-en
incident_report: none
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
