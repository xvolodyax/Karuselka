# PIXELS — 2026-08-29 Labels / Статус

status: sliced + edge-cleaned
mode: grid_3x3 seam
aspect: 3:4 @ 4K
slice: seam / gutter_detect (`scripts/seam_slice_grid.py --split-mode gutter`)
cell: 1080×1440 (all 18 PNG)
master: 2448×3264
edge_cleanup: strip=10 (no crop)
gutter_qa: ok (mode=seam)
this_run_slide_01: static_png
publish_requested: false
face_i2i: carusel-memory/references/viktoriaref.png only
regen: 1 whole-master rebuild per lang after CROOKED CANVAS exit 2 (never patched a cell)

## RU

taskId: 9835d862b26219d8a3449e1970f3505c
failed_then_retry: e1f9caf0e407ca0a57cd6aa60596b1ec (CROOKED CANVAS: white seams missing at 1/3 or 2/3; whole master regenerated)
slides:
- carusel-memory/packs/2026-08-29/ru/slides/slide-01.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-02.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-03.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-04.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-05.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-06.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-07.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-08.png 1080×1440
- carusel-memory/packs/2026-08-29/ru/slides/slide-09.png 1080×1440
master: carusel-memory/packs/2026-08-29/ru/master.png 2448×3264
source: carusel-memory/packs/2026-08-29/ru/source.png 2448×3264
qa: carusel-memory/packs/2026-08-29/ru/grid-gutter-qa-clean.json status=ok
seam: gutter_detect max_center_offset_px=7.0 (limit 73.44)
pipeline_copy: carusel-memory/output/slides/slide-01.png … slide-09.png (lang=ru)

## EN

taskId: 9e770d1e5945a132f7a5df44b6420c5e
failed_then_retry: d29cb7c951146d4001d05dca06fc6b34 (CROOKED CANVAS: white seams missing at 1/3 or 2/3; whole master regenerated)
slides:
- carusel-memory/packs/2026-08-29/en/slides/slide-01.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-02.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-03.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-04.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-05.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-06.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-07.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-08.png 1080×1440
- carusel-memory/packs/2026-08-29/en/slides/slide-09.png 1080×1440
master: carusel-memory/packs/2026-08-29/en/master.png 2448×3264
source: carusel-memory/packs/2026-08-29/en/source.png 2448×3264
qa: carusel-memory/packs/2026-08-29/en/grid-gutter-qa-clean.json status=ok
seam: gutter_detect max_center_offset_px=8.5 (limit 73.44)
