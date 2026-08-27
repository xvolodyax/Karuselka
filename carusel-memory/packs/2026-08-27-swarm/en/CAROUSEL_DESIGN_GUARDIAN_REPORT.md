# CAROUSEL_DESIGN_GUARDIAN_REPORT

Verdict: ✅ DESIGN OK
Score: 92/100

role: carusel-design-guardian
lang: en
handle: @todaytaro_bot
pack: 2026-08-27-v2 / Ping vs step
trigger: STEP
product: bot_three_spreads (Telegram bot, not an app)
carousel_family: animals_viktoria_collage
dispatch_id: 924e0d811d0e451fa5d56452acee5702
reviewed: 9 PNG under `carusel-memory/output/slides/` + `carusel-memory/output/video/slide-01.mp4`

## P0 Blockers
(none)

## Warnings
- Slide 09 repeats `Comment STEP below` (magenta pill + body line). Both strings exist in `CAROUSEL_SLIDE_COPY.json` (`cta` + start of `body`); not invented copy, but a zone duplicate.
- Slide 01 neon chat bubble restates `'Hey, you up?'` already in the headline. Scene lock, not a random label.
- MP4 is `816×1104` vs PNG slides `816×1088`. Frame-0 matches the hook (MAE 13.79 / animate 6.35, threshold 35). Upload must normalize file1 to slide size (pitfall 11.2). Do not crop publish PNGs.
- Loop first-vs-last MAE 12.73 (threshold 15 — pass). Text stays locked; glow + cat micro-move only.
- Slide 09 right hand is in a pocket vs blueprint “relaxed at her side”. Same closer wardrobe (leather jacket + charcoal turtleneck). Not a face/outfit fail.

## Canon gate (HARD EXTRA)

| Lock | Result |
|------|--------|
| Victoria on 1 + 9, same face as `victoria-sheet.png` | PASS — oval/heart, high cheekbones; no Alena; no second woman |
| Hair honey/wheat + darker roots; no platinum | PASS on 01 and 09 |
| Eyes green / hazel | PASS |
| Clothes not sheet tank+jeans; not ivory blazer | PASS — 01 burgundy satin + black trousers seated; 09 leather jacket + charcoal turtleneck + dark chocolate trousers standing |
| Animals ≥3 with jobs | PASS — cat 01 (senses the ping), dog 02 (waits at the lit screen), owl 04 (night scan) |
| Hook is a scene | PASS — 24 days silent / 11:42 PM / `Hey, you up?` |
| ≥2 save frameworks | PASS — 05 PING vs STEP table; 06 Texts / You hear / Reality; 07 three questions |
| EN trigger STEP | PASS — huge magenta STEP on 09; comment CTA; no Academy |
| No empty vibe-only slides | PASS — each panel teaches one beat of the arc |

## P0 checklist

| Check | Status | Evidence |
|-------|--------|----------|
| 9 slides, row-major 01–09 | PASS | `slice-manifest.json` 3×3, files slide-01…09 |
| Token drift (colors/fonts) | PASS | charcoal `#111111–#1a1a1a`, white heavy sans, magenta `#ff006e` script/pills, soft gold throughout |
| Slide 1 hook readable <2s | PASS | scene line + clock + quote dominate at thumbnail |
| Slide 9 CTA visible | PASS | STEP + Comment STEP below + 3 free bot spreads |
| Reference preserve/change | PASS | family collage locked; topic objects changed; no Portuguese / Pause / Alena |
| Wrong extra text / random labels | PASS | no watermarks, no Victoria signature, no URLs, no Academy; duplicates noted as warn |
| Vertical bleed orphan text rows 2–3 | PASS | top 40px of 04–09: 0 white pixels; no leftover headline from the row above |
| Mixed aspect/size on 9 PNG | PASS | all `816×1088`, aspect `0.75` (3:4) |
| `grid-gutter-qa-clean.json` status ok | PASS | `status: ok`, `failures: []` |
| Style score ≥ 70 | PASS | designer card 86 (layout); pixel review 92 |
| Kie 400 recovery order | PASS | success stayed `3:4 @ 4K`; `aspect_ratio_fallback: false`; `prompt_compacted: true`; `prompt_char_count: 4179` (≤4500) |
| Canon family + hair lock | PASS | see canon table |
| Hook scene + ≥2 save frameworks | PASS | see canon table |
| No empty vibe-only | PASS | teaching arc 01–09 |

## Professional QA

1. **Reference fidelity:** charcoal field, magenta+white type, torn pills, cutouts, animals-as-metaphor, Victoria 1+9. Changed: ping/step objects and verbatim EN copy.
2. **Thumbnail test:** `Silent for 24 days` + `11:42 PM` + `'Hey, you up?'` reads immediately.
3. **Grid test:** 3×3 row-major; each cell self-contained 3:4.
4. **Typography test:** headlines/bodies match `CAROUSEL_SLIDE_COPY.json`. Latin only. No Russian / Portuguese / Pause / PAUSE / Academy.
5. **Save test:** 05 contrast table, 06 three-layer decode, 07 numbered checklist, 08 recap rule — screenshot-ready.
6. **CTA test:** one action, one trigger **STEP**, product = 3 free spreads in the Telegram bot. Team answers in Direct. No raw URL.
7. **Motion test:** 5.000s loop; text frozen; phone glow + cat blink/ear tick; first/last same scene.
8. **Bleed test:** top-40 inspection of 04–09 — no orphan type. Gold dots / fabric at cut are in-cell, not row-above leftovers.
9. **Video source test:** frame 0 of `slide-01.mp4` is the same hook as `slide-01.png` (MAE 13.79 guardian / 6.35 animate ≤ 35).
10. **No-frame QA:** `carusel-memory/output/debug/grid-gutter-qa-clean.json` `status: ok`. Edge white ratios ≤ 0.0009.
11. **Kie recovery:** compacted prompt used at 4179 chars before any aspect/resolution change; successful run `3:4 @ 4K`.

## Scoring

| Criterion | Score | Notes |
|-----------|------:|-------|
| Hook / thumbnail | 14/15 | Scene lock is strong; extra neon bubble is redundant |
| Family + face + hair | 15/15 | Victoria 1+9, honey/wheat + dark roots, green/hazel, new clothes |
| Grid / seams / gutters | 14/15 | QA clean; MP4 height offset is upload work |
| Copy fidelity + CTA | 13/15 | Verbatim EN; STEP visible; 09 CTA duplicated |
| Save architecture | 15/15 | Three real frameworks + recap rule |
| Motion / source match | 14/15 | MAE pass; loop 12.73 under 15; text stable |
| Token consistency | 7/10 | Palette and type locked; gold 2×3 dots recur |

**Total: 92/100**

90–100 → ✅ DESIGN OK. Publish of pixels is allowed after upload. `brief.publish_requested` is false — this role does not upload or publish.

## Per-slide

| Slide | Role | Readability | Reference fidelity | Notes |
|-------|------|-------------|--------------------|-------|
| 01 | hook SCENE | high | high | Victoria + cat + phone glow; burgundy satin, not sheet cami |
| 02 | pain | high | high | Dog waits at magenta-lit phone — loyalty metaphor |
| 03 | mistake | high | high | Type + leather leash; no extra woman / animal |
| 04 | mechanism | high | high | Owl + gold hook; “This is not a step. It's a ping” |
| 05 | save A | high | high | PING vs STEP contrast table |
| 06 | save B | high | high | Texts / You hear / Reality layers |
| 07 | save C | high | high | 3 questions before send |
| 08 | recap | high | high | Peace rule + optional Today Tarot gold medallion |
| 09 | CTA | high | high | Victoria closer + magenta STEP; bot spreads; no Academy |

## Video

- Path: `carusel-memory/output/video/slide-01.mp4`
- 5.000s, 24 fps, h264 yuv420p, 816×1104
- Frame 0 / mid / last = same night scene, same locked EN type
- Animate log MAE 6.35; this review MAE 13.79 (resize 1104→1088)
- Loop MAE 12.73 — pass
- Speech: none. Instagram: not published.

## Handoff

Next role: **upload** (do not execute here). Normalize MP4 to PNG slide size on file1. Do not publish unless `publish_requested` becomes true.
