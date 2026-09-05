---
name: ТАРО СЕЙЧАС / Today Tarot — Зеркальный холод
pack_id: 2026-09-05
run_id: 2026-09-05-1110
slot: 11:10 MSK
date: 2026-09-05
lang_pair: ru+en
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: 710bbd98dea442e294a26d7365f0cdc1
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
  surface: "#18181b"
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
  trigger_ru: "ЗЕРКАЛО"
  trigger_en: "MIRROR"
  face_lock: "none"
  victoria_slides: []
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
identity:
  face_lock: "none"
  host_portrait: "absent"
  rule: "NO host portrait on any slide. NO Victoria face, NO presenter, NO female model, NO Alena."
  forbidden_face_files:
    - "Виктория.png"
    - "viktoriaref.png"
    - "victoria-sheet.png"
    - "victoria.png"
    - "victoria_ref.jpg"
    - "alena*.png"
---

# CAROUSELDESIGN — 2026-09-05 Зеркальный холод

Design contract only. No Kie prompt JSON. No pixels. No publish.

`carousel_family`: **animals_viktoria_collage**
`face_lock`: **none** (NO host portrait, NO Victoria face on any slide)
`slice_method`: **seam** (thin white gutters at 1/3 and 2/3)
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG (9 slides)
`product`: **app_audio** · slide 9 huge magenta script **ЗЕРКАЛО** (RU) / **MIRROR** (EN)

## Source Replication Doctrine

User reference = law. Style lock is the animals collage family (`animals-viktoria-style-lock.png` / `image-851e.png` for palette + collage rhythm only).
**Canon rule for 2026-09-05**: NO host portrait. Face lock is **none**. Zero human portraits across all 9 panels.

Decompose first, then adapt topic objects and animal metaphors.

- **preserve**: dark matte charcoal field `#111111`–`#18181b`, magenta `#ff006e` + white `#ffffff` type mix, torn-paper pills, animals-as-metaphor (cat, dog, owl), seam slice with thin white gutters, 3:4 cells, soft gold `#d4af37` metal foil accents.
- **change**: topic metaphors (mirrors with cold reflections, silent smartphone screens, 4-day silence, life-support metaphors), verbatim copy from `CAROUSEL_SLIDE_COPY.json`, animal assignment per panel, NO human figures.
- **do_not_borrow**: host portrait (NO Victoria, NO Alena), Portuguese text, foreign faces, watermarks, horror elements (skulls/dripping blood), bot-offer, raw URLs.

## Composition Lock

Fixed on all 9 panels:

1. Matte charcoal / obsidian `#111111`–`#18181b` full-bleed per cell with subtle paper/film grain.
2. Heavy white sans headlines (`#ffffff`); vibrant magenta script / torn-tape accents (`#ff006e`).
3. Soft gold (`#d4af37`) foil sparingly as delicate tarot glyphs, constellation lines, or medallion borders.
4. Thin **white** gutters on the master at 1/3 and 2/3. Cells do not bleed type or objects across seams.
5. Safe area ≥10–12% from every cell edge and gutter.
6. Verbatim copy from `CAROUSEL_SLIDE_COPY.json`. No extra labels. No watermarks. No «Сцена» word.
7. **Strictly NO human faces or portraits**. Visual anchor relies on symbolic domain objects (mirrors, silent phones, clocks) and animal metaphors.
8. Animal metaphors: **cat**, **dog**, **owl**. Handled with artistic dignity and emotional weight, never cartoonish or cute pets.
9. Slide 09 CTA is anchored by a huge magenta handwritten trigger word **ЗЕРКАЛО** (RU) / **MIRROR** (EN), accompanied by clean tarot and mirror iconography.

## Philosophy & Vibe

«Зеркальный холод» (The Mirror Test): The chilling silence when you stop reaching out first, and an entire chat dies because only you were breathing life into it.

Atmosphere: contemplative, psychologically mature, sober, empowering. Not horror, not panic, not beige lifestyle fluff.
The room is quiet. The smartphone screen lies dark with zero notifications after 4 days. The cat knows instantly that the energy has shifted. The loyal dog rests by the silent device, waiting. The owl watches with sharp night clarity, decoding the difference between polite replies and genuine pursuit.

Tone: adult, clear-eyed, restorative of self-worth.

## Grid Rules

- One master canvas, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: prompt thin white gutters on the 1/3 and 2/3 lines (horizontal and vertical).
  Code-cut with `scripts/seam_slice_grid.py --split-mode gutter` or canonical slice pipeline.
- If a seam is missing or crooked → rebuild the whole canvas. Never patch one cell.
- Each cell is a self-contained 3:4 Instagram portrait.
- Hook (01) = dramatic scene with silent phone + alert cat + large high-contrast hook typography.
- Internals (02–08) = 50–60% typography balance, animal metaphor integrated at bottom or side, clean spatial separation.
- CTA (09) = **huge magenta script** trigger word + app audio offer + elegant cold mirror / tarot foil motif.
- Static PNG only this run. Slide 01 is static PNG, no video.

## Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#18181b` | full-bleed matte charcoal / obsidian |
| accent | `#ff006e` | script, torn-tape pills, highlight boxes, trigger word |
| type | `#ffffff` | heavy sans headlines + crisp body text |
| surface | `#1a1a1a` | card containers, subtle backing shapes |
| metal | `#d4af37` | soft gold foil, delicate tarot glyphs, constellation dots |

WCAG: High contrast white and vibrant magenta on `#111111` pass AAA for headlines and AA for body.

## Typography & Readability

- Hook must read in **2 seconds** at thumbnail size (~200 px).
- Headline: heavy white sans (`#ffffff`). One clear thought per slide.
- Body: 1–3 short lines. Decoder (05) and checklist (06) use structured stacked lines inside safe areas.
- CTA: **huge** magenta handwritten **ЗЕРКАЛО** (RU) / **MIRROR** (EN) — the most prominent word on slide 09.
- Layering: typography integrates with atmospheric shadows and torn tape, but never crosses a gutter seam.
- Verbatim copy only. Never use the word «Сцена». Write «в моём приложении», never «в нашем приложении».

## Slide Rhythm

```text
01 hook scene     Dark phone, 4 days silence + alert cat (инстинкт чует отчуждение)
02 problem        Silent screen + loyal dog (верность ожиданию у замолчавшего экрана)
03 mistake        Dog head on paws near excuse pills «Вдруг он занят?»
04 mechanism      Cat observing boundary: passenger vs driver of the connection
05 save decoder   Owl night clarity: «Отвечает на вопрос» vs «Сам зовёт на встречу»
06 save checklist Owl diagnostic: 3 признака связи на аппарате ИВЛ
07 save rule      Cat turning away with autonomy: не напоминай тому, кому и так тепло
08 recap          Owl wisdom: взаимность не держится на спасателях
09 CTA            Huge magenta script ЗЕРКАЛО + audio reading in the app
```

Product lock on 09: аудиоразбор **в моём приложении** (Суть – Тень – Вектор) / audio reading in my app (Essence–Shadow–Vector). Not the bot.

## Animal Metaphors (Canon)

1. **Cat** (Slides 01, 04, 07): Metaphor for razor-sharp intuition, detachment, and emotional sovereignty. Senses the cold before logic admits it; refuses to beg for warmth.
2. **Dog** (Slides 02, 03): Metaphor for devoted, faithful waiting by a silent device and the painful trap of generating endless excuses for an unasked question.
3. **Owl** (Slides 05, 06, 08): Metaphor for piercing nocturnal wisdom and objective discernment. Sees straight through comforting illusions to cold, objective facts.

## Do's and Don'ts

**Do**
- Follow visual family `animals_viktoria_collage` with `face_lock: none`.
- Animal metaphors on slides 1–8 (cat, dog, owl).
- Thin white seams at 1/3 and 2/3. Self-contained 3:4 cells.
- Safe area 10–12% from every edge and gutter.
- Verbatim copy from `CAROUSEL_SLIDE_COPY.json`.
- Huge magenta script **ЗЕРКАЛО** / **MIRROR** on slide 9.
- Offer: Direct audio reading in the app («Суть – Тень – Вектор» / «Essence–Shadow–Vector»).

**Don't**
- Generate ANY host portrait, woman face, presenter, selfie, or human figure.
- Reference or use `Виктория.png`, `viktoriaref.png`, `victoria-sheet.png`, `alena*.png`.
- Allow typography or subjects to cross the gutter seams.
- Add white sticker halos or die-cut outlines around animals or objects.
- Add horror elements (skulls, blood, dripping candles, ouija).
- Add Portuguese text, foreign watermarks, or fake logos.
- Offer bot spreads, «3 бесплатных расклада», bot prizes, or raw URLs.
- Write Kie prompt JSON (reserved for `carusel-image-prompter`).
