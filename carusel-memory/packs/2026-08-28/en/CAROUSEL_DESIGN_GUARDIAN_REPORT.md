# CAROUSEL_DESIGN_GUARDIAN_REPORT

Verdict: ✅ DESIGN OK
Score: 93/100

lang: ru (standard output/slides) + en pair (same report)
handle: @todaytaro_ru / @todaytaro_bot
family: animals_viktoria_collage
pack: 2026-08-28 — Тепло / холодно · Hot & Cold
role: carusel-design-guardian
dispatched_via: Task(generalPurpose)
dispatch_id: b4a17d3a3e1e48bfa1686cfa2deec807
product: app_audio
trigger_ru: ТЕПЛО
trigger_en: WARMTH
this_run: STATIC PNG ONLY. Slide 01 is PNG. Do not require slide-01.mp4. video_frame_qa not run. Missing video is not a blocker.

Просмотрены 9 RU PNG (`output/slides` = pack ru, md5 match) и 9 EN PNG.
Лицо: независимый pixel read кропов `packs/2026-08-28/face-check/` + 2× eye-band + HSV сэмпл радужки vs `victoria-sheet-front.png`.
`grid_gutter_qa.py --mode seam` перезапущен на текущих master. RU / EN / output/debug все `status: ok`, `failures: []`.

## P0 Blockers
(none)

## Warnings
- RU 02 и EN 03: чайная свеча / candle still-life. Не horror-стол и не dripping candles; не P0.
- RU 08 / EN 08: золотой медальон ТАРО СЕЙЧАС / Today Tarot не обязателен и почти не читается — recap держится на правиле.
- Style scorecard до пикселей 88; pixel family держится.
- Kie 4K remainder width=2 — WARN в seam mode (ожидаемо).

## Canon gate

`python3 scripts/canon_gate.py --pack carusel-memory/packs/2026-08-28` → **PASS**.
`python3 scripts/face_gate.py --pack carusel-memory/packs/2026-08-28` → **PASS**.

| Check | Result |
|-------|--------|
| (a) Victoria = `victoria-sheet.png`, не Alena, не studio-blazer | PASS — 1 и 9 одно лицо; honey/wheat + darker roots; не platinum |
| (b) ≥3 слайда с животным-метафорой | PASS — кот 01, пёс 02, сова 04 (RU + EN) |
| (c) ≥2 save с рамкой/вопросами | PASS — 05 фазы, 06 говорит/слышит, 07 3 правила |
| (d) hook = сцена | PASS — суббота глаза / вторник «занят» |
| (e) нет platinum; одежда не с листа | PASS — 01 burgundy turtleneck; 09 black satin wrap |
| (f) нет пустых vibe-only | PASS |
| (i) CTA = `app_audio` | PASS — ТЕПЛО / WARMTH; Суть–Тень–Вектор / Essence–Shadow–Vector; не бот |

Hair lock: тёплый медово-пшеничный блонд, корни темнее. Platinum = нет.
Sheet tank+jeans = нет.
Alena = нет. Других женских лиц нет.

## Face + eyes (pixel, this dispatch)

Crops re-made: `python3 scripts/make_face_check_crops.py --pack carusel-memory/packs/2026-08-28`.
Read: `sheet-front.png`, `ru-slide-01-face.png`, `ru-slide-09-face.png`, `en-slide-01-face.png`, `en-slide-09-face.png`, plus tight eye zooms.

Sheet close-up irises (the lock the canon names green + slight hazel): sampled hue ~22–24°, RGB ~ (145,100,75).
RU/EN 01 and 09 irises sit in the same hue family (~21–26°). Night key on 09 is warmer than the studio sheet; that is lighting, not a grey or stranger-brown eye.
Bone / age / hair pattern match the sheet woman. Not a generic older blonde. Not Alena.

`FACE_CHECK.md` verdict: **MATCH**.

## P0 checklist

| Check | P0 | Status |
|-------|----|--------|
| 9 slides, row-major 01–09 | yes | PASS — 9+9 PNG, манифест 3×3 |
| Token drift colors/fonts | yes | PASS — уголь + #ff006e + белый тип + золото |
| Slide 1 hook thumbnail <2s | yes | PASS — сцена суббота/вторник |
| Slide 9 CTA visible | yes | PASS — ТЕПЛО / WARMTH + app audio |
| Reference preserve/change | yes | PASS — family lock; тема тепло/холод |
| Wrong extra text / random labels | yes | PASS — нет Portuguese / URL / Victoria signature / «Сцена» |
| Vertical bleed orphan text rows 2–3 | yes | PASS — top 40px 04–09 white=0 / bright=0 |
| Save cards 7–8 useful | warn | PASS — 07 чек-лист; 08 правило |
| Mixed aspect/size 9 PNG | yes | PASS — all 1080×1440, 0.75 = 3:4 (RU and EN) |
| `grid-gutter-qa-clean.json` missing / != ok | yes | PASS — RU + EN + output/debug all `status: ok` |
| Style score ≥ 70 | yes | PASS — scorecard 88; pixel ~90 |
| Kie 400: compact before aspect/res change | yes | PASS — RU 1842 / EN 2008 ≤ 2200; 3:4 @ 4K; `aspect_ratio_fallback: false`. RU retry was Kie 500 same payload, not 400. |
| Copy vs CAROUSEL_SLIDE_COPY.json | warn | PASS — RU 03 now `закрепляя качели` (prior typo closed). Tight crop RU 09 = «Аудиоразбор» |
| Canon Victoria 1+9, ≥3 animals | yes | PASS |
| Hook = scene; ≥2 save frameworks | yes | PASS |
| Hair honey/wheat + darker roots; no platinum | yes | PASS |
| Face + eyes vs sheet close-up MATCH | yes | PASS |
| Eyes green + slight hazel; brown/grey = FAIL | yes | PASS |
| No empty vibe-only | yes | PASS |

## Professional QA

1. **Reference fidelity:** charcoal field, magenta+white type, gold frames, animals-as-metaphor, Victoria 1+9.
2. **Thumbnail:** RU/EN hook читается сразу. Не mechanic title.
3. **Grid:** row-major 01 02 03 / 04 05 06 / 07 08 09. Ячейки самодостаточные.
4. **Typography:** кириллица/латиница верные. Нет Portuguese, URL, подписи Victoria, «Сцена», Academy (EN).
5. **Save:** 05–07 framed cards; 08 rule.
6. **CTA:** RU **ТЕПЛО** + «Аудиоразбор в приложении. Суть – Тень – Вектор.» EN **WARMTH** + «Audio reading in the app. Essence–Shadow–Vector.» Captions match. Не 3 free bot readings / не три бесплатных расклада.
6b. **Face + eyes:** MATCH vs victoria-sheet close-up. See FACE_CHECK.md.
7. **Motion / video:** skipped (`static-png-only`). Slide 01 is PNG. `video_frame_qa.py` not run. Missing mp4 is not a blocker.
8. **Bleed:** top 40px of 04–09 — no orphan text. Bottom leftover bar — gone (white=0).
9. **No-frame QA:** re-ran `grid_gutter_qa.py --mode seam`. All three JSON `status: ok`, `failures: []`.
10. **Kie recovery:** stayed `3:4 @ 4K`. Compact prompt (1842 / 2008). No aspect/resolution fallback.

```text
python3 scripts/make_face_check_crops.py --pack carusel-memory/packs/2026-08-28
python3 scripts/grid_gutter_qa.py --master …/ru/master.png --slides-dir …/ru/slides --mode seam
python3 scripts/grid_gutter_qa.py --master …/en/master.png --slides-dir …/en/slides --mode seam
python3 scripts/face_gate.py --pack carusel-memory/packs/2026-08-28
python3 scripts/canon_gate.py --pack carusel-memory/packs/2026-08-28
```

## Scoring

| Criterion | Score | Notes |
|-----------|------:|-------|
| Hook scene + thumbnail | 15/15 | Суббота / вторник читается |
| Canon family + Victoria 1+9 + eyes | 15/15 | Pixel MATCH vs sheet close-up |
| Animals ≥3 with jobs | 15/15 | кот / пёс / сова |
| Save frameworks | 14/15 | три рамки + recap |
| Typography / copy fidelity | 13/15 | candles on 02/03; 08 without medallion |
| Grid / gutters / size | 15/15 | QA ok; no bleed; 1080×1440 |
| Motion / video | 6/10 | N/A static-png-only (not a P0; scored as skipped) |
| **Total** | **93/100** | 90–100 = DESIGN OK |

## Per-slide — RU (output/slides = pack ru)

| Slide | Role | Readability | Reference fidelity | Notes |
|-------|------|-------------|--------------------|-------|
| 01 | hook SCENE | high | high | Victoria + кот + телефон. Хук читается. Не cami+jeans. Eyes MATCH. |
| 02 | pain | high | high | Пёс у светящегося экрана. Чайная свеча — warn. |
| 03 | mistake | high | high | «Ловушка — греть сквозняк». Verbatim `закрепляя качели`. |
| 04 | mechanism | high | high | Сова. Края чистые. |
| 05 | save phases | high | high | Тепло vs Холод. Framed. |
| 06 | says/hears | high | high | Говорит / Слышишь / Реальность. Framed. |
| 07 | checklist | high | high | 3 правила. Save card. |
| 08 | recap | high | high | Правило ясности. |
| 09 | CTA | high | high | Та же Victoria, satin wrap. Скрипт ТЕПЛО. App audio. Eyes MATCH. |

## Per-slide — EN (packs/2026-08-28/en/slides)

| Slide | Role | Readability | Reference fidelity | Notes |
|-------|------|-------------|--------------------|-------|
| 01 | hook SCENE | high | high | Victoria + cat + Hot & Cold script. Eyes MATCH. |
| 02 | pain | high | high | Dog at glowing screen. |
| 03 | mistake | high | high | Trap of warming his draft. Candle still-life. |
| 04 | mechanism | high | high | Owl + intermittent reinforcement. |
| 05 | save phases | high | high | Warm vs Cold. Framed. |
| 06 | says/hears | high | high | Says / You hear / Reality. |
| 07 | checklist | high | high | 3 rules. |
| 08 | recap | high | high | Clarity over constant waiting. |
| 09 | CTA | high | high | Same Victoria. WARMTH + Essence–Shadow–Vector. Eyes MATCH. |

## Caption / product (locale)

- RU trigger: **ТЕПЛО**. EN trigger: **WARMTH**.
- Product: `app_audio`. Direct = аудиоразбор / audio reading in the app.
- RU: Суть – Тень – Вектор. EN: Essence–Shadow–Vector.
- `@todaytaro_bot` = EN handle, not the prize.
- No raw URLs. No Academy. No 3 free bot spreads.

## Handoff

Upload may proceed (URLs only). `publish_requested: false`. Do not publish. Do not merge.

HANDOFF_NEXT: upload
