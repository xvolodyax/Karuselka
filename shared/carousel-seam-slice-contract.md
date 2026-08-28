# Carusel seam slice — copied from taro-excalibur

Excalibur BLOG generates **one** canvas with **thin white gutters**, then
`excalibur_blog_cover_quad_split.py` cuts **on those seams**.

Karuselka uses the same method for a **3×3** Instagram grid.

## Do

1. One Kie i2i job → one master `3:4 @ 4K`.
2. Prompt the model: exact 3×3, **thin white gutters** on the 1/3 and 2/3 lines, no bleed across cells.
3. Face lock is the **first** `input_url`: `виктория.png` (one woman, 12 angles). Eyes green+hazel / зелёные с лёгким карим first. No face essay.
4. Code-cut with `scripts/seam_slice_grid.py` (`--split-mode gutter`).
5. If a seam is missing or crooked → **rebuild the whole canvas**. Never patch one cell.

## Do not

- Zero-gutter “cells touch pixel-to-pixel” prompts (the model then draws **sticker outlines** on people/animals).
- `remove_grid_gutters.py` as the primary path (that scrubs cut-lines; it does not invent seams).
- White halo / die-cut / “вырезка” around Victoria or animals.
- Alena (deleted). Platinum / white-blonde hair. Vika = `виктория.png` only.
- i2i of `viktoriaref.png` or `animals-viktoria-style-lock.png` as a face.
- Copy the reference white cami onto slides.

## Pipeline

```text
Kie master (white seams) → seam_slice_grid.py → clean_slide_edges.py (strip ≥ leftover, default 10) → 9 slides
```

If `seam_slice_grid.py` exits 2 (`CROOKED CANVAS`), regenerate the master.
After a successful cut, strip leftover gutter on every slide (`clean_slide_edges.py`,
default 10). Do not disable `edge_cleanup` on the seam path — row-2 bottoms keep
a white bar. `grid_gutter_qa.py --mode seam` treats Kie 4K 2480×3312 remainder
`width=2` as WARN and checks internals on a scrubbed copy.
