# Carusel Visual Assets Policy (Kie.ai scripts)

**MCP KV для картинок не используем.** Только скрипты + `.env`.

## Инструменты

```text
scripts/kie_run_prompt.py    # main generation entrypoint
scripts/kie_carousel_gen.py  # grid_3x3 generation
scripts/kie_client.py        # API
scripts/slice_grid.py        # 3x3 slice
```

Контракт: `shared/kie-image-api-contract.md`

## API Key

`<WORKSPACE>\.env` → `KIE_API_KEY=...`

## Когда генерировать

- grid 3×3 master карусели по промпту + референс (`input_urls`)
- style anchor серии
- cutout/объекты — через prompt + reference (без отдельного remove-bg MCP, если не нужен)

## Pipeline

1. `carusel-designer` собирает prompt hints из `CAROUSEL_SERIES_CONCEPT.json`
2. `carusel-image-prompter` пишет `CAROUSEL_IMAGE_PROMPT.json`
3. Запуск `kie_run_prompt.py`
4. Результат: `source.png` -> `master.png` -> `slide-01..09.png`
5. Registry: `CAROUSEL_ASSET_REGISTRY.json` с `local_path` и `kie_task_id`

## Progress

Обновлять `carusel-memory/design/CAROUSEL_PROGRESS.md` во время poll.

## Publish

Instagram MCP только для **публикации** готовых HTTPS URL — не для генерации.
