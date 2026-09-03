---
name: ТАРО СЕЙЧАС / Today Tarot — Midweek Tomorrow Loop
pack_id: 2026-09-01
run_id: 2026-09-01-1110
slot: 11:10 MSK
weekday: Tuesday
lang_pair: ru+en
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: 50dd866559b844039733c2ae39ecf4c2
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
  narrative: "hook-pain-mistake-mechanism-save-save-reframe-rule-cta"
  product: "app_audio"
  trigger_ru: "ЗАВТРА"
  trigger_en: "TOMORROW"
  face_lock: "none"
  host_portrait: false
  victoria_slides: []
  slide_roles:
    - hook
    - problem
    - mistake
    - mechanism
    - save_framework
    - save_checklist
    - reframe
    - rule
    - cta
host_lock:
  face_lock: none
  host_portrait: false
  wardrobe: none
  rule: "No woman. No presenter. No Victoria. No face. No host clothes."
  slides_1_and_9: "scene + type + animal/object ONLY"
objects:
  - phone (dark screen / last-minute text)
  - analog or digital clock showing 23:41
  - cooling tea / leftover evening cup
  - torn magenta tape
  - gold medallion ТАРО / СЕЙЧАС (optional, native, never covering headline)
identity:
  face_file: none
  face_lock: none
  host_portrait: false
  style_lock: "carusel-memory/references/animals-viktoria-style-lock.png"
  style_lock_role: "palette / rhythm ONLY — never a face ref, never i2i as a person"
  forbidden_face_files:
    - "Виктория.png"
    - "viktoriaref.png"
    - "victoria-sheet.png"
    - "victoria.png"
    - "victoria_ref.jpg"
    - "alena*.png"
---

# CAROUSELDESIGN — 2026-09-01 Midweek Tomorrow Loop

Design contract only. No Kie prompt JSON. No pixels. No publish.

`carousel_family`: **animals_viktoria_collage**
`face_lock`: **none** · `host_portrait`: **false**
`slice_method`: **seam** (thin white gutters at 1/3 and 2/3)
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG
`product`: **app_audio** · slide 9 huge magenta **ЗАВТРА** / **TOMORROW**

Copy is locked. Design around verbatim headlines from
`carusel-memory/design/CAROUSEL_SLIDE_COPY.json` (RU) and
`carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json` (EN). Do not rewrite.

## Source Replication Doctrine

User reference = law. Style lock is the animals collage family
(`animals-viktoria-style-lock.png` / `image-851e.png`) for **palette + collage
rhythm only**. It is **never** a face reference. Never i2i it as a person.
Never put `Виктория.png` in generation. Never restore deleted face files.

Decompose first, then adapt topic objects and animal placement to this Tuesday
hook. No host wardrobe. Objects carry the scene.

- **preserve**: dark charcoal field, magenta + white type mix, torn-paper
  pills, animals-as-metaphor, seam slice, 3:4 cells, soft gold metal accents,
  no host portrait, self-contained panels.
- **change**: midweek-tomorrow topic objects (clock 23:41, cooling tea,
  dark phone, torn magenta tape), verbatim Tuesday copy, which animal on
  which slide, huge ЗАВТРА / TOMORROW trigger.
- **do_not_borrow**: Portuguese text, foreign faces, Victoria, Alena,
  platinum hair, white cami + jeans, ivory blazer, horror candle table,
  other brands, host wardrobe, FACE MATCH vs Виктория.png.

## Composition Lock

Fixed on all 9 panels:

1. Matte charcoal / black `#111111`–`#1a1a1a` full-bleed per cell.
2. Heavy white sans headlines; magenta script / torn-tape accents.
3. Soft gold only as foil (medallion, thin highlight) — never as a pastel wash.
4. Thin **white** gutters on the master at 1/3 and 2/3. Cells do not bleed
   type or subjects across seams.
5. Safe area ≥10–12% from every cell edge and gutter.
6. Verbatim copy from locked JSON. No extra labels. No watermarks. No
   Victoria signature.
7. **Zero human faces.** No woman. No presenter. No Victoria. No doubles.
8. Animals are metaphors, not cute pets. This pack: cat 01/04/07, dog 02/03,
   owl 06/08. Slides 05 and 09 are object / type only.
9. Slides 1 and 9 = **scene + type + animal/object ONLY**. No host clothes.

## Philosophy & Vibe

Tuesday night after a daytime promise. 13:20 he said tonight. 23:41 the
tea is cold and the clock is still waiting. Not horror. Not beige lifestyle.
Not a woman explaining the lesson.

The room is dark and lived-in. The phone is the last-minute text. The clock
reads 23:41. The cat already knows the loop. The dog waits. The owl reads
the excuses. No presenter. The objects and the animals hold the feeling.

Tone: adult, clear, midweek. Contrast is structural (daytime hope /
midnight delay), not theatrical.

## Grid Rules

- One master canvas, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: prompt thin white gutters on the 1/3 and 2/3 lines.
  Code-cut with the seam pipeline. Never zero-gutter cells-touching
  (that spawn sticker outlines).
- If a seam is missing or crooked → rebuild the whole canvas. Never patch
  one cell.
- Each cell is a self-contained 3:4 Instagram portrait. Not 4:5. Not 1:1.
- Hook (01) = large scene line + one animal (cat) + cooling tea / clock.
- Internal (02–08) = 50–60% type, smaller animal or object at bottom or side.
- CTA (09) = **huge magenta script** trigger + object (phone / clock). No woman.
- Static PNG only this run. Slide 01 is not video.

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

- Hook must read in **2 seconds** at thumbnail (~200 px):
  `13:20: «вечером созвон». 23:41: «давай завтра».`
- Headline: heavy white sans. One idea per panel. Verbatim. Do not rewrite.
- Body: 1–3 short lines. Decoder (05) and checklist (06) use stacked
  framework lines; keep inside the safe area.
- CTA: **huge** magenta handwritten **ЗАВТРА** (RU) / **TOMORROW** (EN).
  This is the largest word on the canvas.
- Layer type behind and in front of objects/animals, but never across a gutter.
- No «Сцена» / «Scene» label. No extra watermarks. No host signature.

## Slide Rhythm

```text
01 hook scene     cat + cooling tea + clock 23:41 — daytime promise / night delay
02 problem        dog waits at the dark phone
03 mistake        dog at the closed door — «Конечно, отдыхай»
04 mechanism      cat watches the 24-hour clock loop
05 save decoder   type-heavy says→means framework (screenshot card)
06 save checklist owl + 3 markers (screenshot card)
07 reframe        cat leaves the empty chair — evening returns to you
08 rule           owl + gold medallion — invested finds time
09 CTA            huge magenta ЗАВТРА / TOMORROW + phone/clock — no woman
```

Product lock on 09: аудиоразбор **в моём приложении** / audio reading in
the app. Суть – Тень – Вектор / Essence–Shadow–Vector. Not the bot.

## Host Wardrobe — NONE

There is **no host**. Do not invent clothes, hair, or a pose for a woman.
Do not describe a cami, blazer, knit, slip, jeans, or any presenter look.

Allowed objects only: phone, clock 23:41, cooling tea, torn magenta tape,
gold medallion. Animals: cat, dog, owl as named in copy.

## Do's and Don'ts

**Do**

- `face_lock: none`. `host_portrait: false`. Style lock = palette only.
- Animals as emotion on every slide that names an animal in copy (≥3).
- Thin white seams. Self-contained cells. Verbatim copy.
- Huge magenta **ЗАВТРА** / **TOMORROW** on slide 9.
- Slides 05–06 as screenshot-worthy frameworks.
- Objects: phone, 23:41 clock, cooling tea, torn magenta tape, gold medallion.

**Don't**

- Draw Victoria, any woman, any presenter, any recognizable face.
- i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` / `victoria.png` / Alena.
- i2i style-lock as a face. FACE MATCH vs Виктория.png is retired.
- Platinum hair. White cami + jeans. Ivory blazer. Host wardrobe of any kind.
- White halo / die-cut around animals or objects.
- Horror, skulls, blood, dripping candles, ouija, demon faces.
- Portuguese text, foreign faces, other brands, Victoria signature.
- Bot prize, «3 бесплатных расклада», Academy (EN), raw URLs.
- Write Kie prompt JSON (image-prompter) or generate pixels (slice).
