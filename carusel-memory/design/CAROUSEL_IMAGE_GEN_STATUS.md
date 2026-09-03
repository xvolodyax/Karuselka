# Image gen status — designer step

**No pixels. No Kie. No GenerateImage.**

Designer wrote `prompt_hints` only. `carusel-image-prompter` writes
`CAROUSEL_IMAGE_PROMPT.json`. `carusel-slice` runs Kie + seam cut.

| Item | Status |
|------|--------|
| Master 3:4 4K | not generated |
| input_urls | style lock palette only if used — **no face file** |
| face_lock | none |
| slice_method | seam (contracted) |
| slide-01..09 PNG | pending slice |
| slide-01 | static PNG (not MP4) |
| motion / video | skipped this run (static PNG) |
