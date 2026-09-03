# CAROUSEL_DESIGN_GUARDIAN_REPORT

Verdict: ✅ DESIGN OK
Score: 93/100

Pack: `2026-09-02` — план-фантом / floating week-plan (среда, дня нет)
Langs: RU + EN (18 PNG, seam 3×3, static PNG only, no mp4)
Face lock: `none` — no host portrait. FACE_CHECK verdict ABSENT. Not FACE MATCH vs Виктория.png.
Product: `app_audio` — ПЛАН / SLOT → аудиоразбор in the APP (Суть – Тень – Вектор / Essence–Shadow–Vector)
Slice: Excalibur white gutters; RU taskId `9b7bcafcfb787eefb0ee21409777ea3d`; EN `0f45adfb5c9cb231b023d43d4fab17b1`
Motion: N/A — `skip_motion` / `skip_animate` / static-png-only. Missing `slide-01.mp4` is not a blocker.

RU score: **92/100**
EN score: **93/100**
Combined: **93/100**

## P0 Blockers
(none)

## Gate checklist (a–j)

| # | Check | RU | EN |
|---|-------|----|----|
| (a) | no host portrait; face_lock=none; no i2i Виктория.png | PASS ABSENT | PASS ABSENT |
| (b) | ≥3 animal-metaphor slides | PASS (8/9: cat/dog/owl) | PASS (8/9: cat/dog/owl) |
| (c) | ≥2 save/framework slides | PASS (05 decoder, 06 checklist, 07 rule) | PASS (05 decoder, 06 checklist, 07 rule) |
| (d) | Hook is a scene | PASS («На этой неделе увидимся») | PASS (Monday: "this week". Wednesday. No day.) |
| (e) | No platinum | PASS | PASS |
| (f) | No vibe-only empty slides | PASS | PASS |
| (g) | New objects (calendar-without-a-day / chips / reservation card — not 23:41 clock) | PASS | PASS |
| (h) | Seam 9+9 PNG, no mixed size, no mp4 required | PASS 9×1080×1440 | PASS 9×1080×1440 |
| (i) | CTA app_audio: ПЛАН / SLOT → аудиоразбор in the APP | PASS | PASS |
| (j) | FACE_CHECK verdict ABSENT | PASS | PASS |

## Warnings
- RU 01 canvas compresses locked hook to «НА ЭТОЙ НЕДЕЛЕ увидимся» — «Среда. Дня нет.» is not on the PNG (caption still carries the full scene). Still a scene hook, readable <2s. Not P0.
- Slide 9 on-canvas omits «Слово ПЛАН в комментариях» / «Write SLOT in the comments» as a separate line; headline Напиши ПЛАН / Comment SLOT is the action. Captions carry the comment instruction.
- Extra object labels: RU 04/09 gold «БРОНЬ»; EN 04/09 «RESERVATION / THIS WEEK TBD». Thematic, not random slogans.
- Kie renders headlines in heavy all-caps; meaning matches locked copy.
- EN 03 is dog + type (closed planner object not hero). Copy still readable.

## Professional QA

| Test | Result |
|------|--------|
| 9 slides exist, grid 01–09 row-major | PASS both langs |
| Token drift colors/fonts | PASS (#111 dark, #fff heavy sans, #ff006e script, soft gold) |
| Slide 1 hook thumbnail <2s | PASS both (RU scene line; EN Monday→Wednesday→No day) |
| Slide 9 CTA visible | PASS: ПЛАН / SLOT + app audio |
| Reference preserve/change | PASS: animals_viktoria_collage, no host, new midweek objects |
| Wrong extra text | WARN only (БРОНЬ / RESERVATION TBD on cards) |
| Vertical bleed top 40px slides 04–09 | PASS — mean RGB 5–12, white_ratio 0.0, no orphan type |
| Save cards 05–07 useful | PASS decoder / 1-2-3 / midweek close rule |
| Mixed aspect/size | PASS all 1080×1440 PNG (output = RU pack hashes) |
| `grid-gutter-qa-clean.json` status ok | PASS (output + ru/en pack debug; failures []) |
| Style score ≥ 70 | PASS designer contract 90; pixel 93 |
| Copy zones | WARN RU 01 missing «Среда. Дня нет.» on canvas; slide 9 comment-line in caption |
| Kie 400 recovery | PASS EN attempt 1 was 400 then whole-master regen; kept run 3:4 @ 4K, `aspect_ratio_fallback: false`, prompt 2186 ≤ 4500 |
| Motion / video | N/A — static-png-only; no mp4 required |
| Host portrait / Vika | PASS ABSENT on all 18 PNGs |

## FACE_CHECK (pixel)

verdict: ABSENT
rule: no host portrait / без лица Вики / без портрета ведущей
compared: none — do not FACE MATCH Виктория.png

Every RU and EN slide is animals + objects + type. No woman. No presenter. No Vika. Crops vs `Виктория.png` were not taken (rule is absence, not likeness).

## CTA test

RU 09: «НАПИШИ ПЛАН» + «Аудиоразбор в моём приложении. Суть – Тень – Вектор.» — not bot, not «три бесплатных расклада».
EN 09: «COMMENT SLOT» + «Audio reading in my app. Essence–Shadow–Vector.» — not bot, not 3 free readings.
Captions: comment trigger ПЛАН / SLOT → Direct аудиоразбор / audio reading in the app; Суть – Тень – Вектор / Essence–Shadow–Vector; links in profile; no raw URLs; no Academy; `product: app_audio`.

## Gutter QA

| File | status |
|------|--------|
| `carusel-memory/output/debug/grid-gutter-qa-clean.json` | **ok** |
| `carusel-memory/packs/2026-09-02/ru/debug/grid-gutter-qa-clean.json` | **ok** |
| `carusel-memory/packs/2026-09-02/en/debug/grid-gutter-qa-clean.json` | **ok** |

All publish slides 1080×1440; edge white_ratio 0.0; failures []. Seam remainder-width WARN is expected; internal scrubbed lines under threshold.

## Per-slide

### RU (`output/slides/` = `packs/2026-09-02/ru/slides/`)

| Slide | Role | Readability | Reference fidelity | Notes |
|------:|------|-------------|--------------------|-------|
| 01 | hook | high | med-high | Scene: НА ЭТОЙ НЕДЕЛЕ + magenta «увидимся». Cat + blank calendar + phone. «Среда. Дня нет.» off canvas. No woman. |
| 02 | problem | high | high | Dog + empty gold chips. Четверг и пятница уже заморожены. |
| 03 | mistake | high | high | Dog + closed planner. Ошибка — ждать «напишет в последний миг». |
| 04 | mechanism | high | high | Cat + БРОНЬ card. «На неделе» — бронь без обязательств. |
| 05 | save_decoder | high | high | Owl + Говорит / слышишь / реально. |
| 06 | save_checklist | high | high | Owl + 3 признака настоящего приглашения. |
| 07 | save_rule | high | high | Cat + X calendar. Нет дня к вечеру — неделя закрыта. |
| 08 | recap | high | high | Owl. Бронирует время, не занимает тревогу. |
| 09 | cta | high | high | Objects only. НАПИШИ ПЛАН + app audio Суть – Тень – Вектор. No person. |

### EN (`packs/2026-09-02/en/slides/`)

| Slide | Role | Readability | Reference fidelity | Notes |
|------:|------|-------------|--------------------|-------|
| 01 | hook | high | high | Full scene: Monday: "this week". Wednesday. No day. Cat + calendar + phone. No woman. |
| 02 | problem | high | high | Dog + gold tokens. Thursday and Friday nights are frozen. |
| 03 | mistake | high | high | Dog + type. The mistake: waiting for a last-minute ping. |
| 04 | mechanism | high | high | Cat + RESERVATION TBD card. "This week" books you with zero cost. |
| 05 | save_decoder | high | high | Owl + What he says vs what it means. |
| 06 | save_checklist | high | high | Owl + 3 signs of a real invitation. |
| 07 | save_rule | high | high | Cat. No day by evening — week is yours. |
| 08 | recap | high | high | Owl. He books your time, not your anxiety. |
| 09 | cta | high | high | Objects only. COMMENT SLOT + Audio reading in my app. Essence–Shadow–Vector. No person. |

## Score

| Criterion | Pts |
|-----------|----:|
| Grid 9+9 seam PNG, one size | 12 |
| Face ABSENT (no host / no Vika) | 12 |
| Hook scene + CTA app_audio | 12 |
| Animal metaphors ≥3 | 10 |
| Save frameworks ≥2 | 10 |
| New objects (not yesterday 23:41) | 10 |
| Palette / type tokens | 10 |
| Bleed / gutter QA ok | 9 |
| Copy fidelity (RU 01 midweek line off canvas; extra card labels) | 8 |
| **Total** | **93** |

✅ DESIGN OK — publish allowed after FACE GATE + CANON GATE. Guardian does not publish.
