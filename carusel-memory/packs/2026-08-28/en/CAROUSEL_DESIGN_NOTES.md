# Design notes — EN pair (Hot & Cold)

Same visual family as RU. Do not restyle.

- **carousel_family:** `animals_viktoria_collage`
- **Copy source:** `carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json` (verbatim)
- **Trigger:** `WARMTH`
- **Product:** `app_audio` — Essence–Shadow–Vector (not the bot, no Academy)
- **Handle:** `@todaytaro_bot` (account name, not the prize)
- **Slogan:** Clarity now

Layouts, clothes, animals, gutters, palette, Victoria face/hair lock are identical to RU:

| Slide | EN headline (locked) | Visual |
|-------|----------------------|--------|
| 01 | On Saturday he looked into your eyes | Victoria + cat + script «Hot & Cold» |
| 02 | Searching for what you did wrong | Dog by the glowing screen |
| 03 | The trap of warming his draft | Magenta tape, no animal |
| 04 | Intermittent reinforcement | Owl |
| 05 | Warm vs Cold: two phases | Framed two-column card |
| 06 | Says vs You Hear | Framed depth card |
| 07 | 3 rules of self-grounding | Framed checklist |
| 08 | Clarity over constant waiting | Large type + optional metal mark |
| 09 | Comment WARMTH | Victoria + huge WARMTH + Essence–Shadow–Vector pills |

Blueprints: `carusel-memory/design/CAROUSEL_SLIDE_BLUEPRINTS.json` → `copy_en` on each slide.  
Prompt hints: `CAROUSEL_SERIES_CONCEPT.json` → `prompt_hints.per_panel_scene_hints[].en`.

No word «Scene» on slides. No `CAROUSEL_IMAGE_PROMPT.json` in the designer step.
