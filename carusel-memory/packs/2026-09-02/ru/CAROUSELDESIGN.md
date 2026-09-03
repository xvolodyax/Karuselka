---
name: ТАРО СЕЙЧАС / Today Tarot — Floating Week-Plan
pack_id: 2026-09-02
run_id: 2026-09-02-1110
slot: 11:10 MSK
weekday: Wednesday
lang_pair: ru+en
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: d28a556162be41d4a9185ea2303887d2
dispatched_via: Task(generalPurpose)
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
  slide-cta: "huge thin script / handwritten, magenta #ff006e — ПЛАН / SLOT"
  slide-number: "optional small white or gold pill, bottom-right, never on seam; no extra words"
  slide-script: "thin magenta script for secondary word only (ПЛАН / SLOT on slide 9)"
  slide-pill: "magenta torn-tape / pill blocks — quote locked copy fragments only, no new slogans"
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
  trigger_ru: "ПЛАН"
  trigger_en: "SLOT"
  face_lock: "none"
  host_portrait: false
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
object_wardrobe:
  carousel_date: "2026-09-02"
  rule: "new objects this pack; never reuse yesterday 23:41 clock-as-hero"
  pack_objects:
    - calendar-without-a-day
    - empty weekday chips
    - floating reservation card
    - coffee cup
    - phone face-down
    - magenta tape
  forbidden_hero:
    - "Tuesday 23:41 clock as hero"
    - "tomorrow-loop phone-clock"
identity:
  face_lock: none
  host_portrait: false
  victoria: false
  women: false
  presenter: false
  style_lock: "carusel-memory/references/animals-viktoria-style-lock.png — PALETTE/RHYTHM ONLY, never a face ref"
  forbidden_face_files:
    - "Виктория.png"
    - "viktoriaref.png"
    - "victoria-sheet.png"
    - "victoria.png"
    - "victoria_ref.jpg"
    - "alena*.png"
---

# CAROUSELDESIGN — 2026-09-02 Floating Week-Plan

Design contract only. No Kie prompt JSON. No pixels. No publish.

`carousel_family`: **animals_viktoria_collage**
`face_lock`: **none** · `host_portrait`: **false** · `victoria_slides`: **[]**
`slice_method`: **seam** (Excalibur thin white gutters at 1/3 and 2/3)
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG
`product`: **app_audio** · slide 9 huge thin magenta script **ПЛАН** / **SLOT**

Copy is **LOCKED**. Headlines and bodies are verbatim from
`CAROUSEL_SLIDE_COPY.json` (RU) and `design/en/CAROUSEL_SLIDE_COPY.json` (EN).
Do not rewrite copy. Do not add labels. Do not sign Victoria.

## Source Replication Doctrine

User reference = law. Style lock
(`animals-viktoria-style-lock.png` / `image-851e.png`) is **palette + collage
rhythm only**. Never i2i it as a face. Never restore deleted face files.
Never draw a woman.

Decompose first, then swap topic objects and animal seats. Do not remake
Tuesday’s 24-hour tomorrow-loop (clock 23:41 as hero).

- **preserve**: dark charcoal field, magenta + white type mix, torn-paper
  pills, animals-as-metaphor, seam slice, no host portrait, 3:4 cells,
  soft gold metal accents.
- **change**: midweek floating-plan objects (calendar-without-a-day, empty
  weekday chips, floating reservation card, coffee cup, phone face-down,
  magenta tape), exact locked copy, which animal sits on which slide.
- **do_not_borrow**: Portuguese text, foreign faces, other brands, horror
  table, Victoria / Alena / any woman, yesterday’s 23:41 clock-as-hero,
  sheet clothes, platinum hair, sticker die-cut halo, bot-offer,
  watermarks, Victoria signature.

## Composition Lock

Fixed on all 9 panels:

1. Matte charcoal / black `#111111`–`#1a1a1a` full-bleed per cell.
2. Heavy white sans headlines; thin magenta script only for the secondary
   word **ПЛАН** / **SLOT** on slide 9.
3. Soft gold only as foil (medallion, thin highlight) — never a pastel wash.
4. Thin **white** gutters on the master at 1/3 and 2/3. Cells do not bleed
   type or animals across seams.
5. Safe area ≥10–12% from every cell edge and gutter.
6. Verbatim copy. No extra slogans. No «Сцена». No watermarks. No signature.
7. **No host. No woman. No presenter. No faces.** `victoria: false` on every slide.
8. Animals are metaphors, not cute pets. This pack: cat 01/04/07, dog 02/03,
   owl 05/06/08, none on 09 (8 of 9 — above the ≥3 minimum).
9. Animals sit **in-scene** on the charcoal field. No white die-cut / sticker
   halo (style-lock cutouts are rhythm only — do not copy the outline).

## Philosophy & Vibe

Wednesday evening. Monday he said «на этой неделе увидимся». The week is
past the equator. The calendar slot is held open for a date that was never
written. Not a 24-hour «давай завтра». Not a day-name clone of «СРЕДА».

The room is dark and still. A calendar with no day. Hollow weekday chips.
A reservation card that floats because it has nothing to pin to. Coffee
going cold. A phone face-down — not a clock shouting 23:41.

The cat already senses the promise dissolving. The dog stays loyal to a
door that never opened. The owl reads the words against the meaning.

Tone: adult, clear, midweek. Contrast is structural (promise without a
weekday), not theatrical. Not horror. Not beige lifestyle.

## Grid Rules

- One master canvas, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: prompt thin white gutters on the 1/3 and 2/3 lines.
  Code-cut with `scripts/seam_slice_grid.py --split-mode gutter`.
- If a seam is missing or crooked → rebuild the whole canvas. Never patch
  one cell.
- Each cell is a self-contained 3:4 Instagram portrait. Not 4:5. Not 1:1.
- Hook (01) = large scene line + one animal (cat) + calendar-without-a-day.
  Readable in **2 seconds** at thumbnail. No host.
- Internal (02–08) = 50–60% type, smaller animal at bottom or side.
- CTA (09) = huge thin magenta script trigger + objects (coffee, phone
  face-down, tape, reservation card). No host. No animal required.
- Static PNG only. Slide 01 is not video.

## Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed charcoal |
| accent | `#ff006e` | script, pills, tape, trigger word |
| type | `#ffffff` | heavy sans headlines + body |
| metal | soft gold `#d4af37` | medallion, light foil |

No pastel rainbow. No beige lifestyle wash. No horror red/black candle table.
WCAG: white on `#111111` and magenta on `#111111` both pass for large type.

## Typography & Readability

- Hook must read in **2 seconds** at thumbnail (~200 px).
- Headline: heavy white sans. One idea per panel. Verbatim.
- Body: 1–3 short lines. Decoder (05) and checklist (06) may stack lines
  inside the safe area.
- CTA: **huge thin magenta handwritten** **ПЛАН** (RU) / **SLOT** (EN).
  Largest word on the canvas. «Напиши» / «Comment» stays heavy white sans.
- Layer type behind and in front of subjects, but never across a gutter.
- Torn-tape pills may echo a locked fragment («на неделе» / «this week»).
  No new brand labels. No Victoria signature.

## Slide Rhythm

```text
01 hook scene     cat + calendar-without-a-day
02 problem        dog + empty weekday chips (Thu/Fri frozen)
03 mistake        dog waits at a closed calendar door
04 mechanism      cat + floating reservation card (hold, no day)
05 save decoder   owl: говорит / слышишь / реально
06 save checklist owl: 3 признака настоящего приглашения
07 save rule      cat closes the week (нет дня к вечеру)
08 recap          owl: бронирует время, не занимает тревогу
09 CTA            objects + huge magenta ПЛАН / SLOT — no host
```

Product lock on 09: аудиоразбор **в моём приложении** / audio reading in
my app. Суть – Тень – Вектор / Essence–Shadow–Vector. Not the bot.
Links in the profile. No raw URLs.

## Object Wardrobe (02.09) — NEW

Do not reuse Tuesday’s tomorrow-loop hero (clock 23:41, «вечером → завтра»).

| Slide | Hero object | Animal |
|-------|-------------|--------|
| 01 | calendar-without-a-day (ghost week, no circled weekday) + magenta tape | cat |
| 02 | empty weekday chips (hollow evening slots, no extra slogans) | dog |
| 03 | closed / unopened planner door + empty chips | dog |
| 04 | floating reservation card hovering over a dateless calendar | cat |
| 05 | decoder stack; small ghost calendar as support | owl |
| 06 | 1–3 checklist; filled slot vs empty chip contrast | owl |
| 07 | week-closed calendar; reservation card turned away | cat |
| 08 | booked slot vs question-mark hold | owl |
| 09 | coffee cup + phone face-down + magenta tape + reservation card | none |

Phone face-down is a still object, not a lit lock-screen clock. Optional light
tarot card if it does not cover a headline. Optional gold medallion if native.

## Do's and Don'ts

**Do**

- `face_lock: none`. Scene + type + animal / object. Never a woman.
- Animals as emotion on every slide that names an animal in copy.
- Thin white seams. Self-contained cells. Verbatim copy.
- Huge thin magenta **ПЛАН** / **SLOT** on slide 9.
- New midweek objects listed above.

**Don't**

- Draw Victoria, Alena, any woman, any presenter, any face.
- i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` /
  `victoria.png` / style-lock as a face.
- Platinum hair, sheet clothes, white cami, jeans, hand-on-chin.
- Clock 23:41 as hero. Tomorrow-loop props as the cover.
- White halo / die-cut / «вырезка» around animals.
- Horror, skulls, blood, dripping candles, ouija, demon faces.
- Portuguese text, foreign faces, other brands, Victoria signature.
- Bot prize, «3 бесплатных расклада», Academy (EN), raw URLs.
- Word «Сцена» / «Scene» as a label.
- Video / motion / Grok this run.
- Write Kie prompt JSON (image-prompter) or generate pixels (slice).
