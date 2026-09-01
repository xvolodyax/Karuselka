# Image gen status — designer step

**No pixels. No Kie. No GenerateImage.**

Designer wrote `prompt_hints` only. `carusel-image-prompter` writes
`CAROUSEL_IMAGE_PROMPT.json`. `carusel-slice` runs Kie + seam cut.

| Item | Status |
|------|--------|
| Master 3:4 4K | not generated |
| input_urls | style lock palette only if used; **never** Виктория.png |
| face_lock | none |
| host_portrait | false |
| slice_method | seam (contracted) |
| slide-01..09 PNG | pending slice |
| motion / video | skipped this run (static PNG) |
