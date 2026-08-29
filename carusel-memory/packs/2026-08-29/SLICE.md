# SLICE — 2026-08-29 Labels / Статус

status: ok
mode: grid_3x3
slice_method: seam
split_mode: gutter
static_png_only: true
slide_01: static_png (not MP4, no Grok, no ANIMATE.md)
face_lock: Виктория.png
i2i: carusel-memory/references/Виктория.png uploaded as Виктория.png
do_not_i2i: viktoriaref.png, victoria-sheet.png, victoria.png, alena*, style-lock collage

## Cut path

```
Kie 3:4 @ 4K i2i
→ scripts/seam_slice_grid.py --split-mode gutter
→ scripts/clean_slide_edges.py (strip=10)
→ scripts/grid_gutter_qa.py --mode seam
```

CROOKED CANVAS (exit 2) = regenerate the whole master. Never patch one cell.

## TaskIds

| lang | success taskId | failed (CROOKED, rebuilt) | seam QA | edge |
|------|----------------|---------------------------|---------|------|
| ru | 9835d862b26219d8a3449e1970f3505c | e1f9caf0e407ca0a57cd6aa60596b1ec | ok | ok strip=10 |
| en | 9e770d1e5945a132f7a5df44b6420c5e | d29cb7c951146d4001d05dca06fc6b34 | ok | ok strip=10 |

Regen used: 1/2 per lang. No BLOCKER.

## Sizes

- master / source: 2448×3264 (both langs)
- every slide: 1080×1440 3:4
- 18 PNG, no video

## Captions

Already in pack (not rewritten):
- carusel-memory/packs/2026-08-29/ru/slides/CAROUSEL_CAPTION.md
- carusel-memory/packs/2026-08-29/en/slides/CAROUSEL_CAPTION.md

## Pipeline (lang=ru)

- carusel-memory/output/slides/slide-01.png … slide-09.png
- carusel-memory/output/master/master.png
- carusel-memory/output/slice-manifest.json (grid 3x3, slice_method seam, langs ru+en)

Publish: not this step. Do not post Instagram.
