---
name: carusel-publish
description: Публикация 9+9 static PNG каруселей RU+EN в Instagram через Composio после GATE PASS.
---

# Carusel Publish

После **GATE PASS** + **FACE_CHECK MATCH** vs `viktoriaref.png` рой **сам** кладёт карусели.
Холл **не** публикует и слайды **не** пересматривает.

Читай `shared/composio-instagram-publish-contract.md`.

## Preconditions

- `GATE.md` = PASS
- `FACE_CHECK.md` = MATCH, лицо только `viktoriaref.png`, глаза зелёные с лёгким карим
- Guardian: `✅ DESIGN OK` или score ≥ 90 без P0
- CTA = кодовое слово → аудиоразбор в приложении, не бот
- В подписи нет сырых URL
- 9+9 статичные PNG, `publish-urls.json` с HTTPS

GATE FAIL / чужое лицо / CTA бота → **не публиковать**.

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

## Уже live

Сегодняшние live карусели не перезаливать. Реестр: `carusel-memory/canon/live-posts.json`.
SKIP `already-live`.

29.08 уже в ленте: RU `Dcnrh0nm7pp` / EN `Dcnrht_lVca`.

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
