---
name: ТАРО СЕЙЧАС / Today Tarot — Midnight Window
pack_id: 2026-09-03
run_id: 2026-09-03-1110
slot: 11:10 MSK
lang_pair: ru+en
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: 005c5291288c443dab2a36d37c4e81fa
dispatched_via: Task(generalPurpose)
pixels: forbidden_this_step
kie_prompt: forbidden_this_step
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
  slide_01: "static_png"
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
  slide-script: "thin magenta script for secondary words and the trigger"
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
  trigger_ru: "ПОЛНОЧЬ"
  trigger_en: "MIDNIGHT"
  face_lock: "none"
  victoria_slides: []
  host_portrait: false
  slide_roles:
    - hook
    - problem
    - mistake
    - mechanism
    - save_decoder
    - save_checklist
    - save_questions
    - recap
    - cta
subjects:
  rule: "scene + type + animal/object. No woman. No host. No wardrobe lock."
  hook: "owl on night watch + phone at 00:47 + night lamp + voice-note waveform"
  cta: "owl + huge magenta trigger + phone/app object"
  animals_min: 3
  animals_this_pack: "owl 01/04/08/09 · dog 02/03/07 · cat 05/06"
identity:
  face_lock: "none"
  host_portrait: false
  face_file: none
  forbidden_face_files:
    - "Виктория.png"
    - "viktoriaref.png"
    - "victoria-sheet.png"
    - "victoria.png"
    - "victoria_ref.jpg"
    - "alena*.png"
    - "character-sheet-2k"
style_reference:
  file: "carusel-memory/references/animals-viktoria-style-lock.png"
  role: "palette / rhythm only — NEVER i2i as a face"
---

# CAROUSELDESIGN — 2026-09-03 Midnight Window

Design contract only. No Kie prompt JSON. No pixels. No publish.

`carousel_family`: **animals_viktoria_collage**
`slice_method`: **seam** (thin white gutters at 1/3 and 2/3)
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG
`product`: **app_audio** · slide 9 huge magenta **ПОЛНОЧЬ** / **MIDNIGHT**
`face_lock`: **none** · `victoria_slides`: **[]**

## Source Replication Doctrine

User reference = law. Style lock is the animals-Victoria collage family
(`animals-viktoria-style-lock.png` / `image-851e.png` for palette + collage
rhythm only). **Never i2i the style lock as a face.** Never restore deleted
face files. Never draw a host.

Decompose first, then adapt **this** topic's objects and animals.

- **preserve**: dark charcoal field, magenta + white type mix, torn-paper
  pills, animals-as-metaphor, seam slice, 3:4 cells, soft gold metal
  accents, no host portrait, high contrast.
- **change**: midnight-window topic objects, verbatim copy, which animal on
  which slide, hook/CTA as scene + type + animal/object (not a woman).
- **do_not_borrow**: Portuguese text, foreign faces, other brands, horror
  table, `Виктория.png`, host portrait, weekend-suitcase objects as the
  main story, bot-offer, watermarks, Victoria signature.

## Composition Lock

Fixed on all 9 panels:

1. Matte charcoal / black `#111111`–`#1a1a1a` full-bleed per cell.
2. Heavy white sans headlines; thin magenta script / torn-tape accents.
3. Soft gold only as foil (medallion, buttons, thin highlight) — never as
   a pastel wash.
4. Thin **white** gutters on the master at 1/3 and 2/3. Cells do not bleed
   type or subjects across seams.
5. Safe area ≥10–12% from every cell edge and gutter.
6. Verbatim copy from `CAROUSEL_SLIDE_COPY.json` (RU) / `design/en/` (EN).
   No extra labels. No watermarks. No Victoria signature.
7. **No host. No women's faces. No doubles.** FACE_CHECK must be ABSENT.
8. Animals are metaphors, not cute pets. Minimum 3 slides (this pack uses
   owl / dog / cat on all 9).
9. Hook (01) and CTA (09) = scene + type + animal / object. **Not a woman.**

## Philosophy & Vibe

A lived-in night that does not travel into the day. At 00:47 the phone is
warm: a voice note, a lamp, an owl on watch. At 14:20 the same chat is
empty — grey ticks, no blue. Not horror. Not beige lifestyle. Not a
weekend suitcase. Not a candle altar.

The room is dark and ordinary. The owl sees the night window. The dog
stays loyal to hours that do not answer. The cat catches the swap between
the line and the fact.

Tone: adult, calm, exact. Contrast is structural (night density / daylight
absence), not theatrical.

## Grid Rules

- One master canvas, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: prompt thin white gutters on the 1/3 and 2/3 lines.
  Code-cut later. If a seam is missing or crooked → rebuild the whole
  canvas. Never patch one cell.
- Each cell is a self-contained 3:4 Instagram portrait. Not 4:5. Not 1:1.
- Hook (01) = large scene line + owl + phone / lamp. No host.
- Internal (02–08) = 50–60% type, smaller animal at bottom or side.
- CTA (09) = **huge magenta script** trigger + owl / object. No host.
- Static PNG only this run. Slide 01 is PNG, not video.

## Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed charcoal |
| accent | `#ff006e` | script, pills, tape, trigger word |
| type | `#ffffff` | heavy sans headlines + body |
| metal | soft gold `#d4af37` | medallion, buttons, light foil |

No pastel rainbow. No beige lifestyle wash. No horror red/black candle table.
WCAG: white on `#111111` and magenta on `#111111` both pass for large type.

## Typography & Readability

- Hook must read in **2 seconds** at thumbnail (~200 px).
- Headline: heavy white sans. One idea per panel.
- Secondary / trigger: thin magenta script. Slide 9 **ПОЛНОЧЬ** / **MIDNIGHT**
  is the largest word on the canvas.
- Body: 1–3 short lines. Decoder (05), checklist (06), questions (07) may
  use stacked lines; keep inside the safe area.
- Layer type behind and in front of animals / objects, but never across a gutter.
- Verbatim copy only. No «Сцена» label. No extra watermarks.

## Slide Rhythm

```text
01 hook scene     owl + phone 00:47 + lamp + waveform
02 problem        dog waits at a dark daytime screen
03 mistake        dog shifts sleep under 01:12
04 mechanism      owl looks through a night window, not an altar
05 save decoder   cat: Говорит / Слышишь / Есть
06 save checklist cat: 3 daylight checks
07 save questions dog stands up from the midnight watch
08 recap          owl closes the night shift with one rule
09 CTA            owl + huge magenta ПОЛНОЧЬ / MIDNIGHT
```

Product lock on 09: аудиоразбор **в моём приложении** / audio reading in
the app. Суть – Тень – Вектор / Essence–Shadow–Vector. Not the bot.

## Topic objects (THIS pack — 03.09)

New objects. Do not reuse 30.08 weekend-suitcase as the main story.

- Phone screen at **00:47**
- Voice-note **waveform**
- Warm **night lamp**
- **Missing blue ticks** / grey ticks at 14:20
- **Empty daytime chat**
- Clock / time **01:12** on the mistake slide (optional, inside the cell)
- Night window as a **window**, not an altar

Not the main story: Friday 18:00 / Monday «Как ты?», Saturday calendar,
weekend suitcase, cold weekend coffee, last-seen-yesterday weekend chat.

## Do's and Don'ts

**Do**

- `face_lock: none`. No host. No women's faces. No doubles.
- Animals as emotion on every slide that names an animal in copy.
- Thin white seams. Self-contained cells. Verbatim copy.
- Huge magenta **ПОЛНОЧЬ** / **MIDNIGHT** on slide 9.
- Hook + CTA = scene + type + animal / object.

**Don't**

- Draw Vika. i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png`
  / `victoria.png` / Alena / style-lock as a face.
- FACE MATCH «похожа на Виктория.png».
- Weekend-suitcase objects as the main story (СУББОТА / WEEKEND pack).
- Horror, skulls, blood, dripping candles, ouija, demon faces.
- Portuguese text, foreign faces, other brands, Victoria signature.
- Bot prize, «3 бесплатных расклада», Academy (EN), raw URLs.
- Write Kie prompt JSON (image-prompter) or generate pixels (slice).
