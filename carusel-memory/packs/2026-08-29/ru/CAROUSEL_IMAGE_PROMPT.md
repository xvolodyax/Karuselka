# CAROUSEL_IMAGE_PROMPT — RU — 2026-08-29

**Kie prompt is short.** Face lock first. Details live in JSON structured fields.

| Field | Value |
|-------|--------|
| pack / run | `2026-08-29` / `2026-08-29-1110` |
| lang | ru |
| generation_mode | `grid_3x3` |
| aspect / res | `3:4` @ `4K` |
| slice_method | `seam` — thin white gutters at 1/3 and 2/3 (Excalibur) |
| slide 01 | **static PNG** — no video, no Grok, no motion |
| face | **only** `carusel-memory/references/Виктория.png` |
| i2i_source | `carusel-memory/references/Виктория.png` |
| input_urls | local path to that file (HTTPS set at slice upload) |
| prompt_char_count | **2029** (≤ 2200) |
| product | `app_audio` — trigger **СТАТУС** |

## Face lock (first lines of `prompt`)

Same woman as `Виктория.png`; same face, one woman.  
Eyes green with a slight hazel-brown tint (зелёные с лёгким карим).  
Warm honey blonde with darker roots, **not platinum**. Soft tender expression.

Never i2i: `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`, `victoria_ref.jpg`, `alena*.png`, `character-sheet-2k`, `animals-viktoria-style-lock.png` as a face.

## Style lock

Family `animals_viktoria_collage`. Dark charcoal `#111111`–`#1a1a1a` + magenta `#ff006e` + white heavy sans. Type in-scene, no sticker halo. Torn magenta tape as graphic only.

## Wardrobe this pack (not the ref)

| Slide | Outfit / pose |
|-------|----------------|
| 01 | graphite silk pajama shirt, open collar, no necklace + black wide-leg trousers; 3/4 seated on rumpled dark bed, look over shoulder |
| 09 | petrol-teal silk blouse, soft high neck + cropped espresso suede jacket open + slim black trousers; standing 3/4, tender-firm |

Do not copy ref white cami + gold pendant. Do not repeat 2026-08-28 burgundy turtleneck / black satin wrap.

## Animals (metaphor)

- 01 cat — чует фальшь  
- 02 dog — ждёт у закрытой двери  
- 04 owl — видит расчёт 100/0  

## Copy

Verbatim from `CAROUSEL_SLIDE_COPY.json`, in quotes. No extra labels. Never write «Сцена».  
Slide 09 CTA: «Напиши СТАТУС» / «Аудиоразбор в моём приложении. Суть – Тень – Вектор.» / «Слово СТАТУС в комментариях» / «Ясность сейчас».

## Grid

One master 3:4 @ 4K. Nine self-contained 3:4 cells, row-major. Thin white gutters exactly at 1/3 and 2/3. Safe margin 10–12% from every cut line and edge.

## Handoff

Machine file: `carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json`  
EN sibling: `carusel-memory/design/en/CAROUSEL_IMAGE_PROMPT.json`  
Next: **slice** (upload face, Kie i2i, seam cut). This step does not call Kie.
