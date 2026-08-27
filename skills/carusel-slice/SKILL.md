---
name: carusel-slice
description: Kie.ai one grid master -> 3x3 slice -> 9 slides. slide-01 later animated.
---

# Carusel Slice

## Вызов

Только отдельный Task. Director не запускает Kie/slice сам «заодно».  
9 PNG, 3×3. Fragment: `dispatched_via`, `dispatch_id`, `HANDOFF_NEXT: motion-director`.

## Роль

Одна генерация Kie -> **сетка 3×3** -> **9 PNG**. Слайд 1 потом оживляет `carusel-animate`.

## Вход

- `carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json` (`generation_mode: grid_3x3`)
- `<WORKSPACE>\.env` — `KIE_API_KEY`

## Выход

```text
carusel-memory/output/master/source.png
carusel-memory/output/master/master.png
carusel-memory/output/slides/slide-01.png … slide-09.png
carusel-memory/output/slice-manifest.json
carusel-memory/output/kie-task-log.json
```

## Generate + slice

```bash
python scripts/kie_run_prompt.py \
  --workspace <WORKSPACE> \
  --prompt-json carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json
```

Внутри: `kie_carousel_gen.py` -> Kie `3:4` @ `4K` -> `remove_grid_gutters.py`
-> `slice_grid.py --cols 3 --rows 3` -> `clean_slide_edges.py` -> `grid_gutter_qa.py`.

Это canonical no-frame pipeline для всех новых прогонов. Не обходить его ручным `slice_grid.py`,
если цель — publish-ready slides без белых рамок.

`3:4` — основной формат, не fallback. Grid 3×3 даёт 9 одинаковых панелей `3:4`.
Если Kie возвращает повторный `400 Internal Error` на валидный `3:4 @ 4K` i2i payload,
сначала запросить у image-prompter compact retry (`prompt` ≤4500 chars, детали в structured fields).
Не менять `aspect_ratio` или `resolution` до compact retry и явного разрешения.
`kie-task-log.json` должен содержать:

```json
{
  "aspect_ratio_requested": "3:4",
  "aspect_ratio": "3:4",
  "resolution": "4K",
  "gutter_cleanup": { "enabled": true, "status": "ok" },
  "edge_cleanup": { "enabled": true, "status": "ok" },
  "gutter_qa": { "enabled": true, "status": "ok" },
  "slice_status": "ok"
}
```

## Порядок слайдов

```text
01 02 03
04 05 06
07 08 09
```

slide-01 = верхний левый → motion + video.

## Валидация

- 9 файлов PNG
- `kie-task-log.json` с `generation_mode: grid_3x3`
- manifest: `grid.cols=3`, `grid.rows=3`
- все 9 PNG имеют одинаковый размер и одинаковый aspect ratio
- не делать post-slice crop отдельных файлов
- `remove-grid-gutters-report.json` есть и `total_changed` зафиксирован
- `clean-slide-edges-report.json` есть, размер всех slide остаётся неизменным
- `grid-gutter-qa-clean.json` со `status: ok`
- если был Kie 400 на длинном prompt: fragment должен указать `prompt_compacted`, `prompt_char_count`, taskId retry

## White gutters / edge artifacts (automatic)

Known pitfall: даже при zero-gutter prompt Kie может нарисовать 1-3px светлые
hairline artifacts на будущих линиях реза или внешних краях отдельных PNG.

Recovery is automatic and geometry-safe:

1. `remove_grid_gutters.py` чистит near-white pixels только на точных cut-lines
   1/3 и 2/3 master. No crop, no resize.
2. `slice_grid.py` режет строго равные ячейки.
3. `clean_slide_edges.py` копирует внутренний фон на внешний edge strip 3px.
   No crop, no resize; все PNG остаются одного размера.
4. `grid_gutter_qa.py` проверяет internal cut-lines и edge strips. FAIL = BLOCKER,
   не publish.

## Kie 400 / prompt complexity

Known pitfall: длинный активный prompt/payload может приводить к `failCode: 400`
с generic `Internal Error, Please try again later` даже при валидном reference URL.

Recovery order:

1. Проверить, что `input_urls` HTTPS и свежий.
2. Сжать активный `prompt` до ≤4500 chars, оставив подробности в JSON structured fields.
3. Повторить один Kie task в том же `aspect_ratio: 3:4`, `resolution: 4K`.
4. Только если compact retry не помог — остановиться как BLOCKER или спросить разрешение на другой режим.

## Vertical bleed (BLOCKER → regen)

Kie иногда кладёт body text слишком близко к нижнему краю ячейки → после slice на **rows 2–3**
(slides 04–09) виден orphan-текст из ячейки сверху.

**Prevention:** image-prompter — safe margin 10–12% от всех imaginary cut lines и краёв ячейки (см. GRID RULES).

**Recovery:**

```bash
# Лучше: усилить prompt safe-area и regenerate master.
python scripts/kie_run_prompt.py --workspace . --prompt-json carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json
```

Не использовать точечный crop как publish-asset: разные высоты PNG ломают геометрию карусели.
Если crop нужен для диагностики, сохранять только в debug/backup, не в output/slides.

## Fragment

```text
=== CARUSEL-SLICE ===
Статус: ✅ OK | ⚠️ WARN | ❌ FAIL
dispatched_via: Task(carusel-slice) | Task(generalPurpose)
dispatch_id: <from pipeline_gate>
Mode: grid_3x3
Slides: slide-01.png … slide-09.png
incident_report: none
HANDOFF_NEXT: motion-director
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`

Контракт: `shared/carousel-grid-design.md`
