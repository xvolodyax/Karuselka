# CAROUSEL IMAGE PROMPT (EN) — 2026-08-31

## Kie i2i Generation Spec

- **Model:** `gpt-image-2-image-to-image`
- **Mode:** `grid_3x3` (single master canvas 3:4 @ 4K)
- **Slice Method:** `seam` (thin white gutters exactly at 1/3 and 2/3, Excalibur seam_slice)
- **Face Lock:** `none` (host_portrait: false, no woman, no Victoria, no Виктория.png)
- **Style Reference:** `animals-viktoria-style-lock.png` (palette, type mix, collage rhythm only — never a face)
- **Output:** Static PNG (static PNG only, no video / motion)
- **Prompt Length:** 1965 characters (limit ≤ 2200)

## Style and Visual Contract

1. **Host Lock (No Face):**
   - No female portraits, no host, no presenter, no Victoria.
   - `face_lock: none`, `host_portrait: false`.
   - `input_urls` contains only style lock: `animals-viktoria-style-lock.png`.
   - Slide 01 and Slide 09: Monday objects, animal metaphors, and bold typography only.

2. **Grid and Typography:**
   - 9 equal 3:4 vertical panels in a 3×3 row-major grid.
   - Thin white seam guides at 1/3 and 2/3 for subsequent slicing with `seam_slice_grid.py`.
   - Safe margin ≥ 12% from all edges and seam lines.
   - Verbatim English copy in quotes matching `carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json`.
   - Slide 09: huge magenta handwritten script trigger "MONDAY" (largest word on canvas).

3. **Animal Metaphors and Monday Objects:**
   - Slide 01: Sleek alert cat + voice-note waveform + 09:11 clock.
   - Slide 02: Loyal dog waiting at closed office door + muted smartphone.
   - Slide 03: Muted phone + magenta torn-tape pause pills.
   - Slide 04: Open laptop + paper calendar "In a meeting" + toggle switch.
   - Slide 05: Wise owl perched above says vs means decoder table.
   - Slide 06: Three numbered meeting pills 1-2-3 for diagnostic checklist.
   - Slide 07: Takeaway office coffee cup (reclaiming Monday morning focus).
   - Slide 08: Soft gold Today Tarot medallion + August 31 calendar leaf.
   - Slide 09: Huge magenta trigger MONDAY + coffee / muted phone, app audio reading offer.

4. **Negative Constraints:**
   - No human faces, no host, no woman, no Victoria (`Виктория.png`, `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`, `alena`).
   - No weekend sofa-vacuum hero (dark sofa + face-down Friday phone, СУББОТА, WEEKEND).
   - No sticker outlines or white die-cut halos around animals/objects.
   - No horror elements, skulls, blood, dripping candles.
   - No bot offers, no 3 free spreads, no Academy, no raw URLs.
