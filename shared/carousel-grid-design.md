# Carusel — Grid 3×3 (9 slides)

Формат по умолчанию с 2026-06: **одна генерация 3:4 @ 4K → сетка 3×3 → 9 файлов 3:4**.

## Размеры

| Элемент | Значение |
|---------|----------|
| Master Kie | `aspect_ratio: 3:4`, `resolution: 4K` |
| Fallback | none by default — if 4K unavailable, stop or ask; do not silently switch aspect |
| Сетка | **3 cols × 3 rows** |
| Панель | **3:4** (каждая ячейка = master_w/3 × master_h/3) |
| Слайдов | **9** |
| Анимация | **slide-01** (верхний левый) → Grok mp4 → `file1` в Instagram |

## Порядок нумерации (row-major)

```text
slide-01  slide-02  slide-03
slide-04  slide-05  slide-06
slide-07  slide-08  slide-09
```

Читать слева направо, сверху вниз — как превью UNILIBRE.

## Не seamless horizontal

В отличие от `seamless_panorama` (6480×1350), каждая панель — **отдельная композиция** в сетке. Общий только style lock (палитра, типографика, бренд).

## Seam slice (Excalibur)

Master **asks for** thin white gutters on the 1/3 and 2/3 lines. Code cuts ON
those seams. Copied from taro-excalibur `excalibur_blog_cover_quad_split.py`.

Canonical pipeline для новых прогонов:

```text
Kie master (thin white gutters; no bleed) -> seam_slice_grid.py --split-mode gutter
```

If a seam is missing or crooked (`CROOKED CANVAS`, exit 2) → rebuild the whole
canvas. Never patch one cell. Do not prompt zero-gutter / sticker cutouts —
that draws a white halo around people and animals.

Контракт: `shared/carousel-seam-slice-contract.md`.

## Kie generation

```json
{
  "generation_mode": "grid_3x3",
  "aspect_ratio": "3:4",
  "resolution": "4K",
  "grid": { "cols": 3, "rows": 3 },
  "slice_method": "seam",
  "face_lock": "victoria-sheet.png"
}
```

### Почему 3:4

Kie i2i может не давать `4:5` в 4K. Поэтому pipeline больше не просит `4:5`,
а сразу работает в доступном стабильном режиме `3:4 @ 4K`.

Для 3×3 это математически корректно: master `3:4` даёт девять одинаковых
панелей `3:4`. Все PNG и slide-01 video должны оставаться в одном aspect.

### Vertical bleed

Typography near cell bottom may bleed into row below after slice. Mitigations:

- Prompt: safe margin 10–12% from all imaginary cut lines and cell edges
- Slice: only equal grid slice; **do not crop individual slides** because mixed
  heights break carousel geometry

Скрипты:

```bash
python scripts/kie_run_prompt.py --workspace .
# direct slice_grid.py использовать только для диагностики;
# publish-ready runs идут через kie_run_prompt.py canonical pipeline.
```

## Publish

| Файл | Содержимое |
|------|------------|
| `file1` | **video** slide-01 (Grok) |
| `file2`–`file9` | PNG slide-02 … slide-09 |

⚠️ Текущий MCP `t4528_carrusel_instagram` — только **6** слотов. См. `instagram-publish-contract.md`.

## Референс

`carusel-memory/design/reference-grid-9-unilibre.png` — style reference only; final generated grid uses `3:4 @ 4K`.
