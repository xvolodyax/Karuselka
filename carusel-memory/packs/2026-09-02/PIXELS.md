# PIXELS — 2026-09-02

Static PNG only. Face lock: none. No host portrait.
Command: `python scripts/kie_run_prompt.py --workspace /workspace --prompt-json carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json` (RU) then `design/en/CAROUSEL_IMAGE_PROMPT.json` (EN).
Mode: `grid_3x3` + `slice_method: seam` + `seam_slice_grid.py --split-mode gutter`. No `kie_render_pack.py`. No `remove_grid_gutters.py` primary path. No publish. No animate. No mp4.

## Kie taskIds

| lang | attempt | taskId | result | notes |
|------|---------|--------|--------|-------|
| ru | 0 | `9b7bcafcfb787eefb0ee21409777ea3d` | kept | seam detect ok, offset 9.0px / limit 73.44, gutter QA ok |
| en | 0 | `c0cc9e7198ba41e3bd74d570f4b8c175` | discarded | gutter QA fail: white outer edges (white_ratio=1.0). Whole master regen. Never patched a cell. |
| en | 1 | `360f309bc5d1b4fe278013f56b67f132` | discarded | Kie 400 content-policy flag. Whole master regen. |
| en | 2 | `047661b00f8b934014542a1c5f0aa277` | discarded | Kie 500 Internal Error. Whole master regen. |
| en | 3 | `8383b24a197f3fc61fb6e88fc84cf2f2` | discarded | gutter QA fail: white outer frame. Whole master regen. |
| en | 4 | `24c3e93ad19f1eaa62e67ca276132bf1` | discarded | seam ok; QA fail leftover white on internal v2/h2 after scrub. Whole master regen. |
| en | 5 | `d8a8caaca7cf9e7692ef1968ebd749b0` | discarded | Kie 500 Internal Error. Whole master regen. |
| en | 6 | `0f45adfb5c9cb231b023d43d4fab17b1` | kept | seam detect ok, offset 3.5px / limit 73.44, gutter QA ok |

Regen: RU 0 whole-master. EN 6 whole-master (3 QA / 1×400 / 2×500). Max unused: RU 7, EN 1. Never patched a cell.

Result URLs:
- RU kept: https://tempfile.aiquickdraw.com/p/9b7bcafcfb787eefb0ee21409777ea3d_1_1788339162_9013.png
- EN kept: https://tempfile.aiquickdraw.com/a2/0f45adfb5c9cb231b023d43d4fab17b1_1788340301740.png

i2i: style lock only `https://tempfile.redpandaai.co/kieai/378019/carusel-style-lock/animals-viktoria-style-lock.png`. No host face ref.

## Masters

- `/workspace/carusel-memory/packs/2026-09-02/ru/master.png` 2448×3264 PNG 9644873 bytes (taskId 9b7bcafcfb787eefb0ee21409777ea3d)
- `/workspace/carusel-memory/packs/2026-09-02/en/master.png` 2448×3264 PNG 10074534 bytes (taskId 0f45adfb5c9cb231b023d43d4fab17b1)
- Gate master: `/workspace/carusel-memory/output/master/master.png` (RU copy)

## 18 PNG slides (all 1080×1440, PNG, no mp4)

### RU (also restored to `carusel-memory/output/slides/`)

- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-01.png` 1080×1440 1588590 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-02.png` 1080×1440 1534361 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-03.png` 1080×1440 1758158 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-04.png` 1080×1440 1658822 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-05.png` 1080×1440 1557174 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-06.png` 1080×1440 1840487 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-07.png` 1080×1440 1594760 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-08.png` 1080×1440 1780288 bytes
- `/workspace/carusel-memory/packs/2026-09-02/ru/slides/slide-09.png` 1080×1440 1416184 bytes

### EN

- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-01.png` 1080×1440 1686755 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-02.png` 1080×1440 1754401 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-03.png` 1080×1440 1657243 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-04.png` 1080×1440 1844624 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-05.png` 1080×1440 1705688 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-06.png` 1080×1440 1910216 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-07.png` 1080×1440 1681894 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-08.png` 1080×1440 1696629 bytes
- `/workspace/carusel-memory/packs/2026-09-02/en/slides/slide-09.png` 1080×1440 1536066 bytes
