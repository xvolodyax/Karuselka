# CAROUSEL_IMAGE_PROMPT — Ping vs step

written_by: carusel-image-prompter  
lang: en  
handle: @todaytaro_bot  
visual_family / carousel_family: `animals_viktoria_collage`  
generation_mode: `grid_3x3`  
model: `gpt-image-2-image-to-image`  
aspect_ratio: `3:4`  
resolution: `4K`  
face_lock: `victoria-sheet.png`  
prompt_compacted: true  
prompt_char_count: 4179  
Kie: not run (slice next)

Machine JSON: `carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json`  
Copy source: `carusel-memory/design/CAROUSEL_SLIDE_COPY.json` — verbatim English only. No invented slogans.  
Visual twin: `/tmp/carusel-run-ru/carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json` (wardrobe, animals, grid, family). Kie instructions are Russian; quoted panel text is English.

## Style lock

Night-fashion collage, not occult horror and not beige lifestyle.

| Role | Hex |
|------|-----|
| background | `#111111`–`#1a1a1a` |
| type | `#ffffff` |
| accent | `#ff006e` |
| metal | `#c4a35a` |

Heavy white grotesque headlines. Thin magenta script / torn-tape pills only for words already in the slide copy. Type layers behind and in front of cutouts. Safe margin ≥10–12% from every imaginary 1/3 and 2/3 cut and from every cell edge.

## Reference contract

| File | Role |
|------|------|
| `carusel-memory/references/animals-viktoria-style-lock.png` | style + layout + palette |
| `carusel-memory/references/victoria-sheet.png` | ONLY face + hair lock |
| box: `/workspace/cover-refs/victoria-sheet.png` | same face lock on box |

**Preserve:** charcoal field, magenta + white type, cutouts, pills, animals-as-metaphor, Victoria on 1+9, 3×3 zero-gutter grid.

**Change:** topic objects and exact English copy (night ping at 11:42 PM, leash/hook, PING vs STEP table, three-layer decode, three-question checklist), this-pack wardrobe, animal seats cat/dog/owl.

**Do not borrow:** Portuguese, foreign faces, Alena, ivory-blazer studio, sheet outfit/pose, platinum hair, horror table, slogans not in the copy JSON, raw URLs, Academy, Russian headlines.

## Face + wardrobe (this pack — same as RU)

Victoria **only** on slides 1 and 9. Same woman. Eyes green with a slight hazel mix. Warm honey / wheat blonde with darker roots as on the sheet. Never lighten.

- **Slide 1 (NEW):** deep burgundy satin blouse, open collar, black high-waist trousers. Seated on a dark bed edge, 3/4, looking down at a phone in her left hand. Screen glow. Hair loose over one shoulder.
- **Slide 9 (NEW, different pose):** black leather jacket over a fitted charcoal turtleneck, dark chocolate wide-leg trousers. Standing 3/4, chin slightly lifted, looking at camera, right hand relaxed at her side.

Banned looks live in `negative_prompt` only (platinum, Alena, white cami, jeans from sheet, ivory blazer, other women's faces). Do not name those looks in the positive Kie prompt.

## Animals

| Slide | Animal | Job |
|-------|--------|-----|
| 1 | cat | stares at the notification — you sense it |
| 2 | dog | sits by the glowing screen — loyalty to the unanswered question |
| 4 | owl | night watch — cold scan / night thoughts |

No animals on 3, 5–9. No Victoria on 2–8. Empty pretty pets without a job = FAIL.

## Verbatim panel copy

Quoted from `CAROUSEL_SLIDE_COPY.json`. Do not substitute.

1. hook — «Silent for 24 days. At 11:42 PM: 'Hey, you up?'» / «The exact night you finally stopped checking his page.»
2. problem — «Your heart races like a month ago» / «Another sleepless night sending screenshots: 'Does he miss me? Did he finally realize?'»
3. mistake — «The trap: mistaking impulse for love» / «Looking for signs of destiny where someone is simply testing the length of their leash.»
4. mechanism — «This is not a step. It's a ping» / «Zero effort. He sensed losing control and tossed a hook: 'Are you still waiting?'»
5. save A — «Ping vs Real Step: The difference» / «PING: Midnight texts, story views, zero actions.» / «STEP: Daytime call, specific time and place to meet.»
6. save B — «What he texts vs what you hear» / «Texts: 'Thinking of us.'» / «You hear: 'He wants me back.'» / «Reality: 'I need free validation tonight.'»
7. save C — «3 questions before you hit send» / «1. Is there concrete action?» / «2. Has his behavior actually changed?» / «3. Ready for another 3 weeks of silence?»
8. recap — «The rule that protects your peace» / «Whoever wants to be near takes a step. Whoever is bored sends a ping. Never settle for an availability check.»
9. cta — «What is truly behind his text?» / «Comment STEP below» / «Comment STEP below. We'll DM you 3 free spreads in our bot to reveal his true motives.» Huge magenta script **STEP**.

Product is 3 free spreads in the Telegram bot. Trigger is **STEP**. Team answers in Direct. No raw URLs. No Academy.

## Grid

Master one image, 3:4 @ 4K, `generation_mode: grid_3x3`. Row-major 01 02 03 / 04 05 06 / 07 08 09. Zero visible gutters. Each cell is a standalone 3:4 panel. Slide 1 is motion-friendly (phone glow, cat micro-move; type stays still).

## Negative (Kie)

platinum, Alena, white cami, jeans from sheet, ivory blazer, other women's faces, Portuguese, horror — plus strip/gutter/watermark extras in JSON.

## Handoff

Prompt ready. Do **not** invent copy. Next: **slice** (Kie i2i + 3×3 cut). Image-prompter does not generate pixels.
