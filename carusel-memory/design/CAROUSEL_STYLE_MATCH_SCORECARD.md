# Style match scorecard — 2026-09-02 designer contract

`carousel_family`: animals_viktoria_collage
Pass threshold: **70**. This score is **contract completeness**, not pixel fidelity
(pixels are not generated at designer).

| Criterion | Score | Notes |
|-----------|------:|-------|
| Reference decomposition present | 12/12 | preserve / change / do_not_borrow + roles |
| Family from canon | 12/12 | animals_viktoria_collage |
| 9-panel grid blueprint | 12/12 | row-major 3×3, seam gutters |
| Face lock none + no host | 10/10 | face_lock none; victoria_slides []; no woman |
| Animal metaphors ≥3 | 10/10 | 8 of 9 slides (cat/dog/owl as locked copy) |
| Palette + type mix | 10/10 | #111111–#1a1a1a / #ff006e / #ffffff / gold |
| CTA / product | 8/8 | huge thin magenta ПЛАН / SLOT, app_audio |
| Thumbnail + save tests | 8/8 | 01 hook; 05–07 save |
| Negative constraints | 8/8 | no host, no 23:41 hero, no halo, no bot |
| **Total** | **90/100** | **PASS** |

## P0 blockers — none

- [x] reference decomposition
- [x] carousel_family = animals_viktoria_collage
- [x] 9-panel grid blueprint
- [x] preserve / change / do_not_borrow (top-level + prompt_hints)
- [x] prompt_hints for image-prompter (all required keys + 9 panel hints)

Pixel score is for design-guardian after slice.
