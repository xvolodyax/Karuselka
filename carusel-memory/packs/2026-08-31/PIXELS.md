# PIXELS — 2026-08-31

Static PNG only. Host portrait: **NONE**. Do not upload or i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` / `victoria.png`.
Style lock only: `carusel-memory/references/animals-viktoria-style-lock.png` (palette).
Command: `python3 scripts/kie_run_prompt.py --workspace …` (not `kie_render_pack.py --langs ru,en` — that hard-skips EN).
Mode: `grid_3x3` + `slice_method: seam` + `seam_slice_grid.py --split-mode gutter`.
No publish. No animate. No mp4. Slide-01 is still PNG.

## Kie taskIds

| lang | attempt | taskId | result | notes |
|------|---------|--------|--------|-------|
| ru | 0 | `565bbf247f17ab71add5808a39cb3159` | discarded | Kie 500 Internal Error. Whole master retry. |
| ru | 1 | `3713e837a84f01d3608fc476b82fb562` | discarded | Kie 500 Internal Error. Whole master retry. |
| ru | 2 | `5e5c11cf5608e08e110e9c8d8fa11315` | kept | seam detect ok, offset 6.0px / limit 74.4, gutter QA ok |
| en | 0 | `85ed182a29dea0f26c2d6adcebb53f77` | discarded | CROOKED CANVAS. Whole master regen. Never patched a cell. |
| en | 1 | `c8ae700bc7978c50fc2a21333aa5f349` | discarded | CROOKED CANVAS. Whole master regen. |
| en | 2 | `a558ff7365395d7ec6c4d87a98232c5f` | discarded | CROOKED CANVAS. Whole master regen. |
| en | 3 | `e643225dc52901bde1c6dd1e2539ef5e` | discarded | CROOKED / leftover-gutter QA fail. Whole master regen. |
| en | 4 | `4eb0baba702c82c2600355174b325192` | discarded | CROOKED CANVAS. Whole master regen. |
| en | 5 | `7a7153d0f0e84c1ee3fb7bf8849ea2f7` | discarded | CROOKED CANVAS. Whole master regen. |
| en | 6 | `cc15258962747291d650e8cdb6f384f7` | discarded | CROOKED CANVAS. Whole master regen. |
| en | 7 | `b89d1a0c1d2a57167963d6195c0e3441` | kept | seam detect ok, offset 19.0px / limit 73.44, gutter QA ok |

Regen: RU 0 crooked-canvas (2 API-500 whole-master retries). EN 7 crooked-canvas whole-master. No cell patches.

Result URLs:
- RU kept: https://tempfile.aiquickdraw.com/h/5e5c11cf5608e08e110e9c8d8fa11315_1788166948.png
- EN kept: https://tempfile.aiquickdraw.com/a2/b89d1a0c1d2a57167963d6195c0e3441_1788168306465.png

i2i source: `animals-viktoria-style-lock.png` uploaded as style lock only.
`https://tempfile.redpandaai.co/kieai/378019/carusel-style-lock/animals-viktoria-style-lock.png`
No host face file uploaded.

## Masters

- `/workspace/carusel-memory/packs/2026-08-31/ru/master.png` 2480×3312 PNG 6757182 bytes (taskId 5e5c11cf5608e08e110e9c8d8fa11315)
- `/workspace/carusel-memory/packs/2026-08-31/en/master.png` 2448×3264 PNG 7556035 bytes (taskId b89d1a0c1d2a57167963d6195c0e3441)
- Gate master: `/workspace/carusel-memory/output/master/master.png` (RU copy)

## 18 PNG slides (all 1080×1440, PNG, no mp4)

No people / no host on any slide.

### RU (also copied to `carusel-memory/output/slides/`)

- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-01.png` 1080×1440 1319037 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-02.png` 1080×1440 1195037 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-03.png` 1080×1440 973920 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-04.png` 1080×1440 1077528 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-05.png` 1080×1440 1236073 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-06.png` 1080×1440 901820 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-07.png` 1080×1440 1008738 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-08.png` 1080×1440 1354086 bytes
- `/workspace/carusel-memory/packs/2026-08-31/ru/slides/slide-09.png` 1080×1440 801172 bytes

### EN

- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-01.png` 1080×1440 1292241 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-02.png` 1080×1440 1388838 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-03.png` 1080×1440 1417143 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-04.png` 1080×1440 1255104 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-05.png` 1080×1440 1268261 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-06.png` 1080×1440 961256 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-07.png` 1080×1440 1198630 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-08.png` 1080×1440 1504362 bytes
- `/workspace/carusel-memory/packs/2026-08-31/en/slides/slide-09.png` 1080×1440 1039738 bytes
