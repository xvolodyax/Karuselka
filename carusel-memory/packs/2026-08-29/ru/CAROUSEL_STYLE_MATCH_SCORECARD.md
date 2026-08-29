# Style Match Scorecard — 2026-08-29 labels/status

**Family:** `animals_viktoria_collage`  
**Score:** 88 / 100  
**Pass threshold:** 70  
**Verdict:** PASS (design contract). Pixels not generated in this step.

## P0 blockers

| Check | Status |
|-------|--------|
| Reference decomposition present | PASS — `CAROUSEL_SOURCE_DECOMPOSITION.json` + `CAROUSEL_SOURCE_ANALYSIS.md` |
| `carousel_family` is `animals_viktoria_collage` | PASS — brand canon (not AURA registry slug; gate requires this family) |
| 9-panel grid blueprint | PASS — `CAROUSEL_SLIDE_BLUEPRINTS.json` 01–09 |
| preserve / change / do_not_borrow | PASS — in concept JSON + prompt_hints |
| Face lock `viktoriaref.png` | PASS |
| `slice_method: seam` | PASS |
| Static PNG / no video | PASS |
| Verbatim copy, no «Сцена» | PASS |
| Animals ≥3 as metaphor | PASS — cat 01, dog 02, owl 04 |
| New wardrobe vs ref and vs 2026-08-28 | PASS |

## Breakdown

| Axis | Score | Note |
|------|------:|------|
| Palette lock | 10 | charcoal + #ff006e + white + soft gold |
| Type hierarchy | 9 | heavy sans / magenta script / no extra pills with invented words |
| Grid + seam | 10 | 3×3, 3:4, thin white gutters |
| Face / hair / eyes | 10 | viktoriaref only; honey + darker roots; green+hazel |
| In-scene vs sticker | 9 | explicit change away from style-lock die-cut |
| Animal jobs | 9 | three assigned jobs from locked copy |
| Hook thumbnail | 9 | lived first line + Victoria + cat |
| Save architecture | 9 | 05–08 screenshotable |
| Wardrobe novelty | 8 | pajama shirt / petrol blouse — distinct from cami and burgundy |
| Copy fidelity | 10 | JSON verbatim, dual locale |

**Total: 88**

## Warnings (not P0)

- Style-lock still shows sticker borders; prompter must keep negative on halo.
- Slide 05 JSON has both `lines` and a slightly different `body` — blueprints prefer headline + lines on image.
- Magenta script is large-only (contrast).

## Not scored here

Pixel fidelity, Cyrillic spelling on canvas, seam geometry — after slice / guardian.
