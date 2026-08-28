---
name: carusel-slice
description: Kie.ai one grid master -> 3x3 slice -> 9 slides. slide-01 later animated.
---

# Carusel Slice

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

Внутри: `kie_carousel_gen.py` -> Kie `3:4` @ `4K` (thin white gutters) ->
`seam_slice_grid.py --split-mode gutter` -> `clean_slide_edges.py`
(strip ≥ leftover gutter, default 10).

После seam-нарезки **нельзя** оставлять `edge_cleanup` выключенным: leftover
белый шов (~9px) остаётся на низе ряда 2 (slides 04–06) и уходит в publish.
`grid_gutter_qa.py --mode seam`: remainder `{width: 2}` на 2480×3312 — WARN;
internal lines проверяются на scrubbed-копии, не на сыром seam-master.

Это canonical Excalibur seam-slice pipeline. Если швы кривые или отсутствуют —
exit 2 `CROOKED CANVAS`: пересобрать **весь** master, не патчить одну ячейку.
Не использовать `remove_grid_gutters.py` как основной путь (только QA-копия).

`3:4` — основной формат, не fallback. Grid 3×3 даёт 9 одинаковых панелей `3:4`.
i2i `input_urls[0]` = **cropped left frontal close-up** uploaded as `victoria-sheet.png`.
Do not send the full 12-up sheet. Do not send `animals-viktoria-style-lock.png`.
Wrong face, brown/grey eyes, or platinum → rebuild the **whole** canvas.

Если Kie возвращает повторный `400 Internal Error` на валидный `3:4 @ 4K` i2i payload,
сначала запросить у image-prompter compact retry (`prompt` ≤2200 chars, детали в structured fields).
Не менять `aspect_ratio` или `resolution` до compact retry и явного разрешения.
`kie-task-log.json` должен содержать:

```json
{
  "aspect_ratio_requested": "3:4",
  "aspect_ratio": "3:4",
  "resolution": "4K",
  "slice_method": "seam",
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
- `slice-manifest.json` с `slice_method: excalibur_white_seams` и `split_meta.split_mode: gutter_detect`
- все 9 PNG одинакового размера
- если `seam_slice_grid.py` exit 2 — BLOCKER, regen master
- если был Kie 400 на длинном prompt: fragment должен указать `prompt_compacted`, `prompt_char_count`, taskId retry

## White seams (Excalibur method)

Prompt asks for **thin white gutters** on the 1/3 and 2/3 lines. Code cuts ON
those seams (`seam_slice_grid.py --split-mode gutter`). Subjects must not have
a sticker / die-cut halo — that was the old zero-gutter bug.

If a seam is missing or crooked → rebuild the whole canvas. Never patch one cell.

After the cut, `kie_carousel_gen.py` must run `clean_slide_edges.py` with
`--strip` ≥ leftover gutter (default **10**, no crop). Do not ship the seam
path with `edge_cleanup: false`.

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
Mode: grid_3x3
Slides: slide-01.png … slide-09.png
incident_report: none
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`

Контракт: `shared/carousel-grid-design.md`, `shared/carousel-seam-slice-contract.md`.
