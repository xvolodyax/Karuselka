# Image gen status — image-prompter step (2026-09-05)

**No pixels. No Kie. No GenerateImage.**

`carusel-image-prompter` has prepared `CAROUSEL_IMAGE_PROMPT.json` (RU + EN) and verified all character constraints. `carusel-slice` runs Kie generation + seam cut.

| Item | Status |
|------|--------|
| Master 3:4 4K | pending slice |
| face_lock | **none** (NO host portrait, NO Victoria face, input_urls: style_lock only) |
| slice_method | seam (thin white gutters at 1/3 and 2/3) |
| prompt RU | ready (`carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json`, 2182 chars) |
| prompt EN | ready (`carusel-memory/design/en/CAROUSEL_IMAGE_PROMPT.json`, 2187 chars) |
| slide-01..09 PNG | pending slice |
| motion / video | skipped this run (9+9 static PNG) |
