---
name: ТАРО СЕЙЧАС / Today Tarot — Monday Office Mode
pack_id: 2026-08-31
run_id: 2026-08-31-1110
slot: 11:10 MSK
lang_pair: ru+en
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: 622094fec396441ebc89b1d8dd5f100e
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
  narrative: "hook-pain-mistake-mechanism-save-save-save-recap-cta"
  product: "app_audio"
  trigger_ru: "ПОНЕДЕЛЬНИК"
  trigger_en: "MONDAY"
  face_lock: "none"
  host_portrait: false
  victoria_slides: []
  slide_roles:
    - hook
    - pain
    - mistake
    - mechanism
    - save_decoder
    - save_diagnostic
    - save_shift
    - recap
    - cta
wardrobe_lock:
  carousel_date: "2026-08-31"
  rule: "N/A — no host, no wardrobe, no presenter clothes"
  slide_1: "none — animals + objects + type only"
  slide_9: "none — huge magenta trigger + object only"
  do_not_repeat:
    - "any woman / Victoria / presenter look"
    - "30.08 rumpled oatmeal weekend knit + sofa"
    - "30.08 midnight-blue slip + charcoal cardigan"
    - "sheet white cami + jeans + hand-on-chin"
    - "29.08 graphite pajama"
    - "29.08 petrol-teal + espresso jacket"
identity:
  face_lock: "none"
  host_portrait: false
  face_file: "none"
  do_not_i2i:
    - "Виктория.png"
    - "viktoriaref.png"
    - "victoria-sheet.png"
    - "victoria.png"
    - "victoria_ref.jpg"
    - "alena*.png"
    - "animals-viktoria-style-lock.png as a face"
---

# CAROUSELDESIGN — 2026-08-31 Monday Office Mode

Design contract only. No Kie prompt JSON. No pixels. No publish.

`carousel_family`: **animals_viktoria_collage**
`face_lock`: **none** · `host_portrait`: **false**
`slice_method`: **seam** (Excalibur thin white gutters at 1/3 and 2/3)
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG
`product`: **app_audio** · slide 9 huge magenta **ПОНЕДЕЛЬНИК** / **MONDAY**

Layout reference = yesterday’s **no-face** pack
(`carusel-memory/packs/2026-08-30-ru-noface/`) — **layout only, not copy**.
Style lock `animals-viktoria-style-lock.png` = palette / collage rhythm only.
Never i2i `Виктория.png`. Never draw a woman.

## Source Replication Doctrine

User reference = law. Decompose first, then swap topic objects.

- **preserve**: dark charcoal field, magenta + white type mix, torn-paper
  pills, animals-as-metaphor, **no host portrait**, seam slice, 3:4 cells,
  soft gold metal accents, 50–60% type on internal panels.
- **change**: Monday office-mode objects, verbatim Gemini copy, animal
  assignment cat 01 / dog 02 / owl 05, trigger **ПОНЕДЕЛЬНИК** / **MONDAY**.
- **do_not_borrow**: Victoria / any woman / presenter, weekend sofa-vacuum
  hero (sofa + face-down Friday phone as the Sunday motif), Portuguese
  text, foreign faces, horror table, bot-offer, prior triggers, watermarks.

## Composition Lock

Fixed on all 9 panels:

1. Matte charcoal / black `#111111`–`#1a1a1a` full-bleed per cell.
2. Heavy white sans headlines; magenta script / torn-tape accents.
3. Soft gold only as foil (medallion, buttons, thin highlight).
4. Thin **white** gutters on the master at 1/3 and 2/3. No type or subject
   bleed across seams.
5. Safe area ≥10–12% from every cell edge and gutter.
6. Verbatim copy from `CAROUSEL_SLIDE_COPY.json` (RU) / `design/en/` (EN).
   No extra labels. No watermarks. No Victoria signature. No word «Сцена».
7. **Zero human faces.** No woman. No presenter. No Victoria.
8. Animals are metaphors, not cute pets. Minimum 3 slides: **cat 01,
   dog 02, owl 05**. Other panels = Monday objects + type.
9. Hook and CTA = scene + type + animal / object. Not a woman.

## Philosophy & Vibe

Monday 09:11 after Sunday 2 AM voice notes. The waveform still glows.
The clock says office. The meeting pills are already on the table.
Not horror. Not beige lifestyle. Not yesterday’s empty Saturday sofa.

Tone: adult, tender, clear. Contrast is structural (night closeness /
morning corporate mute), not theatrical. The cat hears the silence.
The dog waits at a closed door. The owl reads the excuses.

## Grid Rules

- One master canvas, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: prompt thin white gutters on the 1/3 and 2/3 lines
  (Excalibur). Code-cut with `scripts/seam_slice_grid.py --split-mode gutter`.
- If a seam is missing or crooked → rebuild the whole canvas. Never patch
  one cell.
- Each cell is a self-contained 3:4 Instagram portrait. Not 4:5. Not 1:1.
- Hook (01) = large scene line + cat + voice-note waveform + 09:11 clock.
- Internal (02–08) = 50–60% type, smaller animal or object at bottom/side.
- CTA (09) = **huge magenta script** trigger + one office object. No person.
- Static PNG only. Slide 01 is not video.

## Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed charcoal |
| accent | `#ff006e` | script, pills, tape, waveform glow, trigger word |
| type | `#ffffff` | heavy sans headlines + body |
| metal | soft gold `#d4af37` | medallion, buttons, light foil |

No pastel rainbow. No beige lifestyle wash. No horror red/black candle table.
WCAG: white on `#111111` and magenta on `#111111` both pass for large type.

## Typography & Readability

- Hook must read in **2 seconds** at thumbnail (~200 px).
- Headline: heavy white sans. One idea per panel. **Verbatim. Do not rewrite.**
- Body: 1–3 short lines. Decoder (05) and checklist (06–07) may stack;
  keep inside the safe area.
- CTA: **huge** magenta handwritten **ПОНЕДЕЛЬНИК** (RU) / **MONDAY** (EN).
  Largest word on the canvas.
- Layer type behind and in front of subjects, but never across a gutter.
- No «Сцена» label. No extra watermarks.

## Slide Rhythm

```text
01 hook scene     cat + voice-note waveform + 09:11 clock
02 pain           dog waits at a closed door / muted phone
03 mistake        phone on mute + pause/waiting pills
04 mechanism      laptop/calendar «совещание» + toggle
05 save decoder   owl: says vs means
06 save diagnostic 3 meeting-pill checks
07 save shift     office coffee — reclaim your Monday
08 recap          gold medallion / calendar rule
09 CTA            huge magenta ПОНЕДЕЛЬНИК / MONDAY + object
```

Product lock on 09: аудиоразбор **в приложении** / audio reading in the app.
Суть – Тень – Вектор / Essence–Shadow–Vector. Not the bot.

## Monday objects (NEW — not weekend sofa vacuum)

| Slide | Object | Job |
|-------|--------|-----|
| 01 | Voice-note waveform + 09:11 clock / watch | night leftover vs morning office |
| 02 | Muted phone at a closed door | loyal waiting |
| 03 | Phone on mute + torn-tape pills | freeze / check-online trap |
| 04 | Laptop + calendar leaf «совещание» | emotional toggle into task mode |
| 05 | Owl + decoder stack | night clarity |
| 06 | Three meeting pills 1–2–3 | diagnostic markers |
| 07 | Office takeaway coffee (lipstick mark OK) | reclaim the day |
| 08 | Soft gold ТАРО СЕЙЧАС medallion or Mon 31 leaf | adult-contact rule |
| 09 | Coffee / muted phone / small app object | CTA companion, not a person |

Do **not** reuse yesterday’s sofa + face-down Friday-18:00 phone as the
hero motif. New wardrobe is **N/A** (no host).

## Do's and Don'ts

**Do**

- Animals as emotion on slides that name them in copy (cat / dog / owl).
- Thin white seams. Self-contained cells. Verbatim Gemini headlines.
- Huge magenta **ПОНЕДЕЛЬНИК** / **MONDAY** on slide 9.
- Style lock as palette only. First prompt line: no host, no woman.

**Don't**

- i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` /
  `victoria.png` / Alena / style-lock as a face.
- Draw any woman, presenter, or recognizable host.
- Copy 30.08 sofa-vacuum hero or СУББОТА / WEEKEND.
- White halo / die-cut around animals.
- Horror, skulls, blood, dripping candles, ouija, demon faces.
- Portuguese text, foreign faces, other brands, Victoria signature.
- Bot prize, «3 бесплатных расклада», Academy (EN), raw URLs.
- Write Kie prompt JSON (image-prompter) or generate pixels (slice).
