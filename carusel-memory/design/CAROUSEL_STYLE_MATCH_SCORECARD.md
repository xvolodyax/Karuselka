# Style match scorecard — 2026-08-30-ru-scout designer contract

`carousel_family`: animals_viktoria_collage  
`face_lock`: none · `host_portrait`: false  
Pass threshold: **70**. This score is **contract completeness**, not pixel fidelity
(pixels are not generated at designer).

| Criterion | Score | Notes |
|-----------|------:|-------|
| Reference decomposition present | 12/12 | preserve / change / do_not_borrow + roles |
| Family from canon | 12/12 | animals_viktoria_collage |
| 9-panel grid blueprint | 12/12 | row-major 3×3, seam gutters |
| No host portrait lock | 12/12 | face_lock none; victoria_slides []; no Виктория.png |
| Animal metaphors ≥3 | 10/10 | 8 of 9 slides — cat 1/6/8, dog 2/3, owl 4/5/7 |
| Palette + type mix | 10/10 | #111111 / #ff006e / #ffffff / gold |
| CTA / product | 8/8 | huge ОНЛАЙН + phone/app, app_audio |
| Thumbnail + save tests | 8/8 | 01 hook scene; 05–07 save |
| Negative constraints | 8/8 | no host, no mic, no halo, no bot, no prior triggers |
| **Total** | **92/100** | **PASS** |

## P0 blockers — none

- [x] reference decomposition
- [x] carousel_family = animals_viktoria_collage
- [x] 9-panel grid blueprint
- [x] preserve / change / do_not_borrow
- [x] prompt_hints for image-prompter (all required keys)
- [x] face_lock none / host_portrait false / victoria_slides []

Pixel score is for design-guardian after slice.
