# PIXELS — 2026-09-03

Static PNG only. Face lock: none. No host / no Vika / no Виктория.png i2i.
Command: `python3 /workspace/scripts/kie_carousel_gen.py` (default seam path).
Mode: `grid_3x3` + `slice_method: seam`. No `--legacy-zero-gutter`. No `remove_grid_gutters.py` primary. No publish. No animate. No mp4. No Grok.

Style lock i2i: `carusel-memory/references/animals-viktoria-style-lock.png` (palette only).

## Kie taskIds

| lang | attempt | taskId | result | notes |
|------|---------|--------|--------|-------|
| ru | 0 | `68bf1d71a6d42974985235cc78de822a` | discarded | CROOKED CANVAS: white seams missing at 1/3 or 2/3. Whole master regen. Never patched a cell. No face. |
| ru | 1 (regen 1) | `6d1f7ea93d376c8ac9a2ee74217a2705` | discarded | Kie 500 Internal Error while generating. Same prompt retry. |
| ru | 2 (regen 2, kept) | `a6a96b6f6dca07b2a6f67d48164589e2` | kept | seam detect ok, offset 3.5px / limit 74.4, gutter QA ok. Animals only. |
| en | 0 | `a6812e537dc8b306cf5be2af401dc116` | discarded | Seam cut ok; gutter QA FAIL (white right edge on 03/06/09 — outer canvas border). Whole master regen. Never patched a cell. No face. |
| en | 1 (regen 1, kept) | `cfa9188ac6c7de8b70331288de3c34d1` | kept | seam detect ok, offset 3.5px / limit 74.4, gutter QA ok. Animals only. |

Regen: RU 2 whole-master (1 crooked + 1 Kie 500). EN 1 whole-master (gutter QA / outer white). Max crooked unused: 0 leftover on RU after 2 extras used (500 counted as extra). No cell patches.

Result URLs:
- RU kept: https://tempfile.aiquickdraw.com/h/a6a96b6f6dca07b2a6f67d48164589e2_1788425384.png
- EN kept: https://tempfile.aiquickdraw.com/h/cfa9188ac6c7de8b70331288de3c34d1_1788425856.png

Face on any generated canvas (kept or discarded): **none**. No woman / host / Vika.

Prompt compacted: no (no Kie 400). Active prompt RU 2157 / EN 2207 assembled; JSON fields 1879 / 1929.

## Masters

- `/workspace/carusel-memory/packs/2026-09-03/ru/master/master.png` 2480×3312 PNG 8195997 bytes (taskId a6a96b6f6dca07b2a6f67d48164589e2)
- `/workspace/carusel-memory/packs/2026-09-03/ru/master/source.png` 2480×3312 PNG 9296561 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/master/master.png` 2480×3312 PNG 7988970 bytes (taskId cfa9188ac6c7de8b70331288de3c34d1)
- `/workspace/carusel-memory/packs/2026-09-03/en/master/source.png` 2480×3312 PNG 9177303 bytes
- Gate master: `/workspace/carusel-memory/output/master/master.png` (RU copy)

## 18 PNG slides (all 1080×1440, PNG, no mp4)

### RU (also restored to `carusel-memory/output/slides/`)

- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-01.png` 1080×1440 1451848 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-02.png` 1080×1440 1205487 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-03.png` 1080×1440 1325060 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-04.png` 1080×1440 1338097 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-05.png` 1080×1440 1424796 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-06.png` 1080×1440 1399049 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-07.png` 1080×1440 1223645 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-08.png` 1080×1440 1373418 bytes
- `/workspace/carusel-memory/packs/2026-09-03/ru/slides/slide-09.png` 1080×1440 1279346 bytes

### EN

- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-01.png` 1080×1440 1313765 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-02.png` 1080×1440 1289431 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-03.png` 1080×1440 1229170 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-04.png` 1080×1440 1328132 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-05.png` 1080×1440 1415085 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-06.png` 1080×1440 1148193 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-07.png` 1080×1440 1348784 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-08.png` 1080×1440 1386182 bytes
- `/workspace/carusel-memory/packs/2026-09-03/en/slides/slide-09.png` 1080×1440 1173049 bytes
