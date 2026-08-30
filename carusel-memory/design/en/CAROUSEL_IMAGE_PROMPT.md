# CAROUSEL IMAGE PROMPT (EN) — 2026-08-30

## Kie i2i Generation Spec

- **Model:** `gpt-image-2-image-to-image`
- **Mode:** `grid_3x3` (single master canvas 3:4 @ 4K)
- **Slice Method:** `seam` (thin white gutters exactly at 1/3 and 2/3)
- **Face Lock:** `Виктория.png` (first `input_url`, 12 angles)
- **Style Reference:** `animals-viktoria-style-lock.png` (palette, type mix, collage rhythm only)
- **Output:** Static PNG (no video / motion)
- **Prompt Length:** 2097 characters (limit ≤ 2200, range 1900–2100)

## Style and Visual Contract

1. **Victoria's Identity and Styling:**
   - Same woman as in `Виктория.png`, one face.
   - Eyes: green with a slight hazel-brown tint.
   - Hair: warm honey blonde with darker roots (NOT platinum).
   - Slide 01: rumpled oatmeal knit + charcoal lounge pants, sitting 3/4 on dark sofa, phone face-down on thigh, alert cat beside her.
   - Slide 09: midnight-blue silk slip dress + open charcoal cardigan, standing 3/4, soft tender gaze.

2. **Grid and Typography:**
   - 9 equal 3:4 vertical panels in a 3×3 row-major grid.
   - Thin white seam guides at 1/3 and 2/3.
   - Safe margin ≥ 12% from all edges and seam lines.
   - Verbatim English copy in quotes matching `carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json`.
   - Slide 09: huge magenta handwritten script trigger "WEEKEND".

3. **Animal Metaphors:**
   - Slides 1, 4, 7: Cat (intuition, sensing boundary, sovereignty).
   - Slides 2, 3: Dog (loyal waiting trap).
   - Slides 5, 6, 8: Owl (night clarity, diagnostic checklist, core insight).
   - Slide 9: No animals.

4. **Negative Constraints:**
   - No deleted face references (`viktoriaref.png`, `victoria-sheet.png`, `alena`).
   - No sheet cami, no jeans, no hand-on-chin pose.
   - No sticker outlines or white die-cut halos around subjects.
   - No horror elements, skulls, blood, dripping candles.
   - No bot offers, no 3 free spreads.
