---
name: carusel-design-guardian
description: Design QA Instagram carousel — token drift, seams, hook, CTA, scorecard.
---

# Carusel Design Guardian

## Вход

- `carusel-memory/design/CAROUSELDESIGN.md`
- `carusel-memory/design/CAROUSEL_STYLE_MATCH_SCORECARD.md`
- `carusel-memory/output/slides/slide-01.png` … `slide-09.png`
- `carusel-memory/00-brief.md` (референс)
- `shared/carousel-professional-playbook.md`

## Выход

`carusel-memory/design/CAROUSEL_DESIGN_GUARDIAN_REPORT.md`

## Checks (P0 = blocker)

| Check | P0 |
|-------|-----|
| 9 slides exist, grid order 01-09 row-major | yes |
| Token drift (colors/fonts) across slides | yes |
| Slide 1 hook readable (thumbnail test) | yes |
| Slide 9 CTA visible | yes |
| Reference preserve/change respected | yes |
| Wrong extra text / random labels | yes |
| Vertical bleed — orphan text top strip rows 2–3 | yes |
| Save cards on slides 7-8 useful | warn |
| Any mixed aspect/size across the 9 publish assets | yes |
| `grid-gutter-qa-clean.json` missing or `status != ok` | yes |
| Style score ≥ 70 | yes |
| Kie 400 recovery used aspect/resolution fallback before compact prompt retry | yes |
| Copy matches CAROUSEL_SLIDE_COPY.json zones | warn |
| Canon `animals_viktoria_collage` (Victoria 1+9, ≥3 animal metaphors) | yes |
| Hook is a scene; ≥2 save slides have a real framework/questions | yes |
| Hair lock: honey/wheat + darker roots; platinum = FAIL | yes |
| Face + eyes vs `victoria-sheet.png` close-up (`FACE_CHECK.md` MATCH) | yes |
| Eyes green + slight hazel; brown/grey = FAIL whole canvas | yes |
| No empty vibe-only slides | yes |

## Professional QA protocol

1. **Reference fidelity:** compare output to reference decomposition, not vague taste.
2. **Thumbnail test:** slide-01 hook must read in <2 sec.
3. **Grid test:** 3×3, row-major, all cells self-contained.
4. **Typography test:** exact intended key text, no random labels, no duplicate text.
5. **Save test:** slides 7-8 should work as standalone checklist/recap.
6. **CTA test:** slide 9 sells the **app audio reading** (Суть–Тень–Вектор / Essence–Shadow–Vector), one comment trigger, no bot prize. See `shared/cta-app-audio-contract.md`.
6b. **Face + eyes test:** crop sheet close-up + slides 01/09 (`scripts/make_face_check_crops.py`). Write `FACE_CHECK.md`. Compare pixels (eyes green+hazel, bone/age, hair pattern) — not honey/wheat prose. Brown/grey eyes or generic blonde = P0, regen whole canvas. See `shared/victoria-face-pixel-gate.md`.
7. **Motion / video:** **skipped.** Instagram carousels are static PNGs. Slide 01 is PNG. Do not require `slide-01.mp4`. Do not run `video_frame_qa.py`. Missing video is not a blocker. See `shared/static-carousel-lock.md`.
8. **Bleed test:** inspect top 40px of slides 04–09 for orphan text from row above. If P0, request master regeneration with stronger safe-area; do not approve per-slide crop as publish asset.
9. **No-frame QA:** verify `carusel-memory/output/debug/grid-gutter-qa-clean.json` exists and has `status: ok`. White edge artifacts after canonical cleanup = P0.
10. **Kie recovery provenance:** if slice recovered from Kie `400 Internal Error`, verify the successful run stayed `3:4 @ 4K` and used compact prompt retry before any aspect/resolution change. `prompt_char_count > 2200` after recovery is P0.

## Scoring

- 90–100: `✅ DESIGN OK`
- 70–89: `⚠️ DESIGN WARN` — publish allowed with notes
- <70 or P0: `❌ DESIGN BLOCKER` — regen designer/slice

## Report format

```markdown
# CAROUSEL_DESIGN_GUARDIAN_REPORT

Verdict: ✅ DESIGN OK
Score: 92/100

## P0 Blockers
(none)

## Warnings
- ...

## Per-slide
| Slide | Role | Readability | Reference fidelity | Notes |
...
```

## Fragment

```text
=== CARUSEL-DESIGN-GUARDIAN ===
Verdict: ✅ DESIGN OK
Score: 92
Report: carusel-memory/design/CAROUSEL_DESIGN_GUARDIAN_REPORT.md
incident_report: none
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
