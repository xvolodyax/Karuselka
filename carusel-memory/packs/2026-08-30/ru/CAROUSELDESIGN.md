---
name: ТАРО СЕЙЧАС / Today Tarot — Weekend Vacuum
pack_id: 2026-08-30
run_id: 2026-08-30-1110
slot: 11:10 MSK
lang_pair: ru+en
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: b10a4a88db134fc38e2cc9d5838339c3
format:
  generation_mode: "grid_3x3"
  slide_count: 9
  grid:
    cols: 3
    rows: 3
    order: "row-major"
  master_aspect: "3:4"
  resolution: "4K"
  panel_aspect: "3:4"
  output: "static_png"
  skip_motion: true
  skip_animate: true
colors:
  primary: "#ff006e"
  background: "#111111"
  on-background: "#ffffff"
  accent: "#ff006e"
  surface: "#1a1a1a"
  outline: "#d4af37"
  metal: "soft gold"
typography:
  slide-headline: "heavy sans, white, #ffffff"
  slide-body: "medium sans, white 85–92%"
  slide-cta: "huge thin script / handwritten, magenta #ff006e"
  slide-number: "small white or gold pill, bottom-right, never on seam"
  slide-script: "thin magenta script for secondary words only"
  slide-pill: "magenta torn-tape / pill blocks for short labels"
grid:
  cols: 3
  rows: 3
  order: "row-major"
  gutters: "thin white seams at 1/3 and 2/3 (horizontal + vertical)"
  gutters_px: 3
  cell_is_self_contained: true
  slice_method: "seam"
  safe_area_pct: 12
  animate_slide: 0
carousel_system:
  carousel_family: "animals_viktoria_collage"
  narrative: "hook-pain-mistake-mechanism-save-save-save-recap-cta"
  product: "app_audio"
  trigger_ru: "СУББОТА"
  trigger_en: "WEEKEND"
  face_lock: "Виктория.png"
  victoria_slides: [1, 9]
  slide_roles:
    - hook
    - problem
    - mistake
    - mechanism
    - save_decoder
    - save_checklist
    - save_rule
    - recap
    - cta
wardrobe_lock:
  carousel_date: "2026-08-30"
  rule: "new clothes + pose this carousel; never copy sheet or 29.08"
  slide_1:
    garment: "rumpled weekend-at-home oatmeal knit (heather wheat-oat, NOT white cami)"
    bottom: "soft charcoal lounge knit pants (NOT jeans)"
    pose: "sitting 3/4 on dark sofa, phone face-down on thigh, looking off-camera; NOT hand-on-chin"
  slide_9:
    garment: "midnight-blue silk slip + open charcoal cardigan"
    pose: "standing 3/4, weight on back hip, one hand on cardigan edge; NOT hand-on-chin"
  do_not_repeat:
    - "sheet white cami + jeans + hand-on-chin"
    - "29.08 graphite pajama"
    - "29.08 petrol-teal + espresso jacket"
identity:
  face_file: "carusel-memory/references/Виктория.png"
  box_copy: "/workspace/cover-refs/Виктория.png"
  eyes: "green with slight hazel, same every slide"
  hair: "warm honey/wheat blonde, darker roots, NOT platinum"
  forbidden_face_files:
    - "viktoriaref.png"
    - "victoria-sheet.png"
    - "victoria.png"
    - "victoria_ref.jpg"
    - "alena*.png"
---

# CAROUSELDESIGN — 2026-08-30 Weekend Vacuum

Design contract only. No Kie prompt JSON. No pixels. No publish.

`carousel_family`: **animals_viktoria_collage**
`slice_method`: **seam** (thin white gutters at 1/3 and 2/3)
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG
`product`: **app_audio** · slide 9 huge magenta **СУББОТА** / **WEEKEND**

## Source Replication Doctrine

User reference = law. Style lock is the animals-Victoria collage family
(`animals-viktoria-style-lock.png` / `image-851e.png` for palette + collage
rhythm only). Face lock is **Виктория.png only**. Never i2i the style lock
as a face. Never restore deleted files.

Decompose first, then adapt topic objects and Sunday wardrobe.

- **preserve**: dark charcoal field, magenta + white type mix, torn-paper
  pills, animals-as-metaphor, Victoria in-scene on 1+9 (no sticker halo),
  seam slice, 3:4 cells, soft gold metal accents.
- **change**: weekend-vacuum topic objects, verbatim copy, which animal on
  which slide, NEW Sunday wardrobe and poses.
- **do_not_borrow**: Portuguese text, foreign faces, Alena, sheet outfit,
  29.08 graphite pajama / petrol-teal + espresso jacket, horror table,
  bot-offer, watermarks, Victoria signature.

## Composition Lock

Fixed on all 9 panels:

1. Matte charcoal / black `#111111`–`#1a1a1a` full-bleed per cell.
2. Heavy white sans headlines; magenta script / torn-tape accents.
3. Soft gold only as foil (medallion, buttons, thin highlight) — never as
   a pastel wash.
4. Thin **white** gutters on the master at 1/3 and 2/3. Cells do not bleed
   type or faces across seams.
5. Safe area ≥10–12% from every cell edge and gutter.
6. Verbatim copy from `CAROUSEL_SLIDE_COPY.json` (RU) / `design/en/` (EN).
   No extra labels. No watermarks. No Victoria signature.
7. One woman. Twelve angles of ONE face. Eyes green + slight hazel. Hair
   warm honey/wheat with darker roots.
8. Animals are metaphors, not cute pets. Minimum 3 slides (this pack uses
   cat/dog/owl on 8 of 9).
9. Victoria **in-scene** on slides 1 and 9 only. No die-cut halo.

## Philosophy & Vibe

Sunday-morning emptiness after a warm weekday chat. Not horror. Not beige
lifestyle. Not a pajama hangover from 29.08.

The room is dark and lived-in. The phone is quiet. The cat already knows.
The dog waits. The owl reads the excuses. Victoria is at home, rumpled
oatmeal knit on the hook, then standing in midnight-blue silk + charcoal
cardigan for the CTA — one woman, two Sunday looks, neither from the
character sheet.

Tone: adult, tender, clear. Contrast is structural (5 warm days / 48 hours
of vacuum), not theatrical.

## Grid Rules

- One master canvas, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: prompt thin white gutters on the 1/3 and 2/3 lines.
  Code-cut with `scripts/seam_slice_grid.py --split-mode gutter`.
- If a seam is missing or crooked → rebuild the whole canvas. Never patch
  one cell.
- Each cell is a self-contained 3:4 Instagram portrait. Not 4:5. Not 1:1.
- Hook (01) = large scene line + Victoria + one animal (cat).
- Internal (02–08) = 50–60% type, smaller animal at bottom or side.
- CTA (09) = Victoria + **huge magenta script** trigger word.
- Static PNG only this run. Slide 01 is not video.

## Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed charcoal |
| accent | `#ff006e` | script, pills, tape, lips, trigger word |
| type | `#ffffff` | heavy sans headlines + body |
| metal | soft gold `#d4af37` | medallion, buttons, light foil |

No pastel rainbow. No beige lifestyle wash. No horror red/black candle table.
WCAG: white on `#111111` and magenta on `#111111` both pass for large type.

## Typography & Readability

- Hook must read in **2 seconds** at thumbnail (~200 px).
- Headline: heavy white sans. One idea per panel.
- Body: 1–3 short lines. Decoder (05) and checklist (06) may use stacked
  lines; keep inside the safe area.
- CTA: **huge** magenta handwritten **СУББОТА** (RU) / **WEEKEND** (EN).
  This is the largest word on the canvas.
- Layer type behind and in front of subjects, but never across a gutter.
- Verbatim copy only. No «Сцена» label. No extra watermarks.

## Slide Rhythm

```text
01 hook scene     Victoria + cat + Friday 18:00 silence
02 problem        dog waits at the silent screen
03 mistake        dog loyalty trap / excuses
04 mechanism      cat sees the weekday-slot boundary
05 save decoder   owl: says vs means
06 save checklist owl: 3 waiting-zone signs
07 save rule      cat reclaims Saturday
08 recap          owl: free time is the proof
09 CTA            Victoria + huge magenta СУББОТА / WEEKEND
```

Product lock on 09: аудиоразбор **в моём приложении** / audio reading in
my app. Суть – Тень – Вектор / Essence–Shadow–Vector. Not the bot.

## Sunday Wardrobe (30.08) — NEW

**Slide 1.** Rumpled weekend-at-home knit, oatmeal / heather wheat-oat.
Slightly oversized waffle or slouchy crew. Soft charcoal lounge pants.
Sitting 3/4 on a dark sofa. Phone face-down on the thigh. Tender, knowing.
Cat alert beside her. **Not** white cami. **Not** jeans. **Not**
hand-on-chin.

**Slide 9.** Standing 3/4. Midnight-blue silk slip. Open charcoal cardigan
(soft merino, slouchy — not a structured jacket). Soft gold hoop or small
medallion. One hand on the cardigan edge or a cup held low. Huge magenta
trigger word. **Not** graphite pajama. **Not** petrol-teal. **Not**
espresso jacket.

Same woman. New clothes. New poses. Eyes and hair locked.

## Do's and Don'ts

**Do**

- Face lock `Виктория.png` only. Eyes green + slight hazel. Honey/wheat
  hair with darker roots.
- Animals as emotion on every slide that names an animal in copy.
- Thin white seams. Self-contained cells. Verbatim copy.
- Huge magenta **СУББОТА** / **WEEKEND** on slide 9.
- In-scene Victoria on 1 and 9, no sticker halo.

**Don't**

- i2i `viktoriaref.png` / `victoria-sheet.png` / `victoria.png` / Alena /
  style-lock as a face.
- Platinum / white-blonde hair. Brown-only, grey, or blue eyes.
- Copy sheet white cami + jeans + hand-on-chin.
- Copy 29.08 graphite pajama or petrol-teal + espresso jacket.
- White halo / die-cut around Victoria or animals.
- Horror, skulls, blood, dripping candles, ouija, demon faces.
- Portuguese text, foreign faces, other brands, Victoria signature.
- Bot prize, «3 бесплатных расклада», Academy (EN), raw URLs.
- Write Kie prompt JSON (image-prompter) or generate pixels (slice).
