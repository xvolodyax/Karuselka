# PIXELS — 2026-09-01

Static PNG only. Face lock: **none**. No host portrait. No `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` / `victoria.png` in `input_urls`.
Style lock only: `carusel-memory/references/animals-viktoria-style-lock.png` uploaded as HTTPS palette ref.
Command: `python3 scripts/kie_run_prompt.py` / `kie_carousel_gen.py` with `slice_method: seam`.
Code-cut: `seam_slice_grid.py --split-mode gutter`. Never `kie_render_pack.py --langs ru,en` (hard-skips EN).
No Grok. No mp4. Slide-01 is PNG. No animate. No Instagram publish.

## Kie taskIds

| lang | attempt | taskId | result | notes |
|------|---------|--------|--------|-------|
| ru | 0 | `13791a054de0fe1443a481f4ac4dcbd1` | discarded | Kie `500 — Internal Error` while waiting. Whole-master retry. Never patched a cell. |
| ru | 1 | `d10da2252466cf589bb66257cae96f8e` | discarded | Kie `500 — Internal Error` while waiting. Whole-master retry. |
| ru | 2 (regen 2/8) | `6a57700c48ff77dfc019d355f3fce282` | kept | seam detect ok, offset 4.0px / limit 74.4, gutter QA ok |
| en | 0 | `9997ecd4bc4fa55fac408c49f09fd100` | discarded | Kie `500 — Internal Error` while waiting. Whole-master retry. |
| en | 1 | `44088962c775cdcb5929901b2e0d2cd6` | discarded | Kie `500 — Internal Error` while waiting. Whole-master retry. |
| en | 2 (regen 2/8) | `4511b5050376b8a5b9b2d199e07a63d9` | kept | seam detect ok, offset 7.0px / limit 74.4, gutter QA ok |

Regen: RU 2 whole-master. EN 2 whole-master. Crooked canvas (exit 2): 0 / 0. Max unused: 6 per lang. Monday EN needed 7 crooked retries — this run persisted the same 8-attempt cap; Kie 500s recovered on attempt 3 instead.

Result URLs:
- RU kept: https://tempfile.aiquickdraw.com/h/6a57700c48ff77dfc019d355f3fce282_1788252804.png
- EN kept: https://tempfile.aiquickdraw.com/h/4511b5050376b8a5b9b2d199e07a63d9_1788253100.png

i2i source: `animals-viktoria-style-lock.png` only.
Uploaded: `https://tempfile.redpandaai.co/kieai/378019/carusel/animals-viktoria-style-lock.png`
Face files were not uploaded.

## Masters

- `/workspace/carusel-memory/packs/2026-09-01/ru/master.png` 2480×3312 PNG 9691231 bytes (taskId 6a57700c48ff77dfc019d355f3fce282)
- `/workspace/carusel-memory/packs/2026-09-01/en/master.png` 2480×3312 PNG 8965146 bytes (taskId 4511b5050376b8a5b9b2d199e07a63d9)
- Gate master: `/workspace/carusel-memory/output/master/master.png` (RU copy)

## 18 PNG slides (all 1080×1440, PNG, 3:4, no mp4)

### RU (also copied to `carusel-memory/output/slides/`)

- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-01.png` 1080×1440 1662886 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-02.png` 1080×1440 1731692 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-03.png` 1080×1440 1862775 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-04.png` 1080×1440 1562706 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-05.png` 1080×1440 1299219 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-06.png` 1080×1440 1749676 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-07.png` 1080×1440 1461313 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-08.png` 1080×1440 1824677 bytes
- `/workspace/carusel-memory/packs/2026-09-01/ru/slides/slide-09.png` 1080×1440 1142658 bytes

### EN

- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-01.png` 1080×1440 1538250 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-02.png` 1080×1440 1454360 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-03.png` 1080×1440 1430229 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-04.png` 1080×1440 1511245 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-05.png` 1080×1440 1447299 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-06.png` 1080×1440 1558633 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-07.png` 1080×1440 1526877 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-08.png` 1080×1440 1612763 bytes
- `/workspace/carusel-memory/packs/2026-09-01/en/slides/slide-09.png` 1080×1440 1175366 bytes
