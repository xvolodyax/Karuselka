---
name: carusel-design-guardian
description: Design QA Instagram carousel — token drift, seams, hook, CTA, scorecard.
---

# Carusel Design Guardian

## Вызов

Только отдельный Task. Director не пишет QA-отчёт сам.  
Проверь 9 слайдов 3×3, slide-01 MP4 если есть, `lang`/handle, отсутствие сырых URL.  
Fragment: `dispatched_via`, `dispatch_id`, `HANDOFF_NEXT: upload`.

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

## Professional QA protocol

1. **Reference fidelity:** compare output to reference decomposition, not vague taste.
2. **Thumbnail test:** slide-01 hook must read in <2 sec.
3. **Grid test:** 3×3, row-major, all cells self-contained.
4. **Typography test:** exact intended key text, no random labels, no duplicate text.
5. **Save test:** slides 7-8 should work as standalone checklist/recap.
6. **CTA test:** slide 9 has one clear action.
7. **Motion test:** if video exists, text remains stable and loop has no hard cut.
8. **Bleed test:** inspect top 40px of slides 04–09 for orphan text from row above. If P0, request master regeneration with stronger safe-area; do not approve per-slide crop as publish asset.
9. **Video source test:** frame 0 of `slide-01.mp4` must match `slide-01.png` (MAE ≤35):
10. **No-frame QA:** verify `carusel-memory/output/debug/grid-gutter-qa-clean.json` exists and has `status: ok`. White edge artifacts after canonical cleanup = P0.
11. **Kie recovery provenance:** if slice recovered from Kie `400 Internal Error`, verify the successful run stayed `3:4 @ 4K` and used compact prompt retry before any aspect/resolution change. `prompt_char_count > 4500` after recovery is P0.

```bash
python scripts/video_frame_qa.py \
  --video carusel-memory/output/video/slide-01.mp4 \
  --png carusel-memory/output/slides/slide-01.png \
  --loop-check
```

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
dispatched_via: Task(carusel-design-guardian) | Task(generalPurpose)
dispatch_id: <from pipeline_gate>
Score: 92
Report: carusel-memory/design/CAROUSEL_DESIGN_GUARDIAN_REPORT.md
incident_report: none
HANDOFF_NEXT: upload
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
