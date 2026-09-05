# Style match scorecard — 2026-09-05 designer contract

`carousel_family`: **animals_viktoria_collage**
`face_lock`: **none** (NO host portrait, NO Victoria face on any slide)
Pass threshold: **70**. This score evaluates **contract completeness**, not pixel fidelity
(pixels are not generated at the designer step).

| Criterion | Score | Notes |
|-----------|------:|-------|
| Reference decomposition present | 12/12 | preserve / change / do_not_borrow + roles clearly mapped |
| Family from canon | 12/12 | `animals_viktoria_collage` strictly adhered to |
| 9-panel grid blueprint | 12/12 | row-major 3×3, 3:4 @ 4K, seam gutters at 1/3 and 2/3 |
| Face lock rule compliance | 10/10 | face_lock: none, 0 human faces, NO Victoria, NO presenter |
| Animal metaphors ≥3 | 10/10 | cat, dog, owl across slides 01–08 |
| Palette + type mix | 10/10 | #111111 / #ff006e / #ffffff / soft gold #d4af37 |
| CTA / product | 8/8 | huge magenta script ЗЕРКАЛО / MIRROR, app_audio (Суть – Тень – Вектор) |
| Thumbnail + save tests | 8/8 | 01 hook reads in <2s; 05–08 provide diagnostic bookmark value |
| Negative constraints | 8/8 | no human faces, no halo, no horror, no bot offer, no raw URLs |
| **Total** | **90/100** | **PASS** |

## P0 blockers — none

- [x] reference decomposition complete
- [x] carousel_family = animals_viktoria_collage
- [x] 9-panel grid blueprint complete
- [x] preserve / change / do_not_borrow complete
- [x] prompt_hints for image-prompter complete
- [x] face_lock: none strictly implemented (NO host portrait, NO Victoria face)
- [x] product: app_audio locked
