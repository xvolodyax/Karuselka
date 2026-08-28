# CAROUSEL_IMAGE_PROMPT — Hot & Cold

written_by: carusel-image-prompter
lang: en
visual_family / carousel_family: `animals_viktoria_collage`
generation_mode: `grid_3x3`
model: `gpt-image-2-image-to-image`
aspect_ratio: `3:4`
resolution: `4K`
face_lock: `victoria-sheet.png`
slice_method: `seam`
prompt_compacted: true
prompt_char_count: 3843
reference_upload_method: `upload_stream`
input_urls[0]: `https://tempfile.redpandaai.co/kieai/378019/carusel-face-lock/victoria-sheet.png`
product: `app_audio`
trigger: WARMTH
handle: @todaytaro_bot
this_run_slide_01: static_png
no_academy: true

Machine JSON: `carusel-memory/design/en/CAROUSEL_IMAGE_PROMPT.json`
Copy source: `carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json` — verbatim only.

Kie/Grok instructions stay in Russian. Quoted on-image text is English.

## Style lock

Fashion-collage on charcoal. Not horror. Not beige lifestyle.

| Role | Hex |
|------|-----|
| background | `#111111`–`#1a1a1a` |
| type | `#ffffff` |
| accent | `#ff006e` |
| metal | `#c9a86a` |

Heavy white grotesque. Thin magenta script / torn-tape pills only for words already in copy. Subjects live inside each scene. Safe margin ≥10–12% from every seam and cell edge. No type on the bottom strip.

## Reference contract

| File | Role |
|------|------|
| `image-851e.png` / animals_viktoria_collage | style + layout + palette — described in text, not i2i |
| `carusel-memory/references/victoria-sheet.png` | ONLY face + hair lock → `input_urls[0]` |

**Preserve:** dark field, magenta + white type, torn-paper pills, animals-as-metaphor, Victoria on 1+9, 3×3 with thin white gutters.

**Change:** Saturday/Tuesday topic, verbatim EN copy, phone, Warm/Cold phases, Says/You Hear, 3 rules, this-pack clothes, CTA WARMTH + audio reading in the app.

**Do not borrow:** Portuguese, foreign faces, Alena, platinum, horror table, the word Scene, bot, 3 free readings, Academy, URLs, Victoria signature.

Banned looks (white cami+jeans, ivory blazer, sticker/cutout/halo) live in `negative_prompt` only.

## Face + wardrobe (this pack)

Victoria only on slides 1 and 9. Same woman. Green eyes with a hint of hazel. Warm honey/wheat blonde with darker roots as on `victoria-sheet.png`. Never lighten.

- **Slide 1 (NEW):** burgundy turtleneck, gold hoops. Seated 3/4 toward a glowing phone.
- **Slide 9 (NEW, different pose):** black satin wrap blouse, dark trousers, standing hip-lean, phone as if typing a comment.

Short identity line in the Kie prompt. No face essay.

## Animals

| Slide | Animal | Job |
|-------|--------|-----|
| 1 | cat | you sense the sudden temperature drop |
| 2 | dog | loyalty to the unanswered question by the screen |
| 4 | owl | night thoughts seeing the hidden loop |

No animals on 3, 5–9. No Victoria on 2–8.

## Verbatim panel copy

From `design/en/CAROUSEL_SLIDE_COPY.json`. Do not substitute.

1. hook — "On Saturday he looked into your eyes" / "and talked about trips together. By Tuesday — a dry \"busy\" and 3 days of cold silence." / script "Hot & Cold"
2. pain — "Searching for what you did wrong" / "You scroll through messages. The silence hurts, but the brutal temperature drop hurts worse."
3. mistake — "The trap of warming his draft" / "You think: \"he's scared of his feelings.\" You respond to distance with double the warmth, fueling the cycle."
4. mechanism — "Intermittent reinforcement" / "Unpredictability spikes your nervous system. Your brain confuses chronic anxiety with genuine passion."
5. save A — "Warm vs Cold: two phases" / "Warm: craving your energy, validation, and attention" / "Cold: retreating the moment consistency is required"
6. save B — "Says vs You Hear" / "Says: \"Work is crazy, don't want complications\"" / "You hear: \"I need to be patient and warm him up\"" / "Reality: \"I want intimacy without accountability\""
7. save C — "3 rules of self-grounding" / "1. Measure the baseline, not weekend peaks" / "2. When he steps back, stay where you are" / "3. Never warm up someone choosing the cold"
8. recap — "Clarity over constant waiting" / "Real connection brings stability, not an emotional roller coaster. The right person never leaves you guessing." / "Clarity now"
9. cta — "Comment WARMTH" / "Audio reading in the app. Essence–Shadow–Vector." / "Write WARMTH in the comments". Huge magenta script **WARMTH**. Not a bot. No Academy.

## Grid

One master, 3:4 @ 4K, `generation_mode: grid_3x3`, `slice_method: seam`. Row-major 01 02 03 / 04 05 06 / 07 08 09. Thin white gutters at 1/3 and 2/3; code cuts on those seams. Each cell is a standalone 3:4 panel. Panel 1 is motion-safe. This run: slide-01 = static PNG.

## Negative (Kie)

platinum, Alena, white cami, jeans from sheet, ivory blazer, cutout, die-cut, sticker outline, white halo, Scene, 3 free readings, Academy, Cyrillic on panels — full list in JSON.

## Handoff

Prompt ready. Do not generate the canvas. Do not slice. Next: **slice**.
