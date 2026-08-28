# Style Match Scorecard — Тепло / холодно

**carousel_family:** `animals_viktoria_collage`  
**pass threshold:** 70  
**score:** **88**

## P0 blockers (must be absent)

| Check | Status |
|-------|--------|
| Reference decomposition exists | PASS — `CAROUSEL_SOURCE_DECOMPOSITION.json` |
| `carousel_family` ∈ registry | PASS — `animals_viktoria_collage` |
| 9-panel grid blueprint | PASS — `CAROUSEL_SLIDE_BLUEPRINTS.json` 01–09 |
| preserve / change / do_not_borrow | PASS — decomposition + `prompt_hints` |

## Scores

| Criterion | Max | Score | Note |
|-----------|-----|-------|------|
| Source decomposition specificity | 20 | 18 | Roles, preserve/change/do_not_borrow, archetype map, thumbnail + save tests |
| Family + palette lock | 15 | 15 | Dark + `#ff006e` + white + gold |
| 9×3:4 grid + Excalibur gutters | 15 | 15 | seam, safe 10–12% |
| Victoria 1+9 + hair lock + new clothes | 15 | 13 | Face/hair locked; outfits specified (burgundy / satin wrap). Pixels not yet proving it |
| ≥3 animal metaphors with jobs | 10 | 10 | cat / dog / owl |
| Save frames 05–07 | 10 | 10 | three framed cards |
| Hook-as-scene, no «Сцена» | 10 | 9 | scene lines locked from Gemini |
| CTA = app_audio not bot | 5 | 5 | Суть–Тень–Вектор / Essence–Shadow–Vector |
| **Total** | **100** | **88** | PASS (≥70) |

## Warnings (not P0)

- Пикселей нет: fidelity лица/волос подтвердит guardian после slice.
- Style plate не идёт в i2i (намеренно).
- Этот run — static PNG на 01; motion-safe композиция сохранена.

## Fail if later

Platinum, Alena, sheet cami+jeans, ivory blazer, <3 animals, no frames on save slides, bot CTA, crooked seams, word «Сцена».
