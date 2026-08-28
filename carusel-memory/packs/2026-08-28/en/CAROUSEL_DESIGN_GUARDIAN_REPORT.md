# CAROUSEL_DESIGN_GUARDIAN_REPORT

Verdict: ❌ DESIGN BLOCKER
Score: 64/100

lang: ru (standard output/slides) + en pair
handle: @todaytaro_ru / @todaytaro_bot
family: animals_viktoria_collage
pack: 2026-08-28 — Тепло / холодно · Hot & Cold
role: carusel-design-guardian
dispatched_via: Task(generalPurpose)
dispatch_id: abf6786e81164aa38cddd62620c10be6
product: app_audio
trigger_ru: ТЕПЛО
trigger_en: WARMTH
this_run: STATIC (slide-01.mp4 = 1s ffmpeg still stub, not Grok)

Просмотрены 9 RU PNG (`output/slides` = `packs/2026-08-28/ru/slides`) и 9 EN PNG (`packs/2026-08-28/en/slides`). Канон-смысл и CTA держатся. **Publish blocked:** `grid-gutter-qa-clean.json` status=`fail` и видимая белая полоса на низу RU 04–06.

## P0 Blockers

1. **`grid-gutter-qa-clean.json` status != ok** (skill P0). Файл создан скриптом, не выдуман.
   - Path: `carusel-memory/output/debug/grid-gutter-qa-clean.json`
   - RU failures:
     - `master dimensions are not divisible by 3x3: {width: 2, height: 0}`
     - `internal cut line v1 has white_ratio=0.8897`
     - `internal cut line v2 has white_ratio=0.8468`
     - `slide-04.png bottom edge has white_ratio=0.9984`
     - `slide-05.png bottom edge has white_ratio=0.9976`
     - `slide-06.png bottom edge has white_ratio=0.9986`
   - EN (`packs/2026-08-28/en/grid-gutter-qa-clean.json`) also `fail`: remainder width=2 + master internal v1/v2/h1/h2 white. EN **slide edges** pass (no 9px white bar).

2. **White edge artifacts on RU publish slides 04–06.** Pixel rows 1431–1439 (~9 px) are solid white (`white_ratio` 0.99–1.0). Visible leftover horizontal gutter after seam cut. Slice left `gutter_cleanup.enabled=false` and `edge_cleanup.enabled=false`. White frames after the expected cleanup path = P0.

### Exact fixes for Director / slice (do not guardian-patch; do not per-slide crop)

1. Re-dispatch **slice** on the existing RU master. Do not approve cropped cells as publish assets.
2. Enable canonical cleanup, then re-QA:
   ```bash
   python3 scripts/remove_grid_gutters.py \
     --input carusel-memory/packs/2026-08-28/ru/master.png \
     --output carusel-memory/packs/2026-08-28/ru/master.png
   python3 scripts/seam_slice_grid.py --split-mode gutter \
     --input carusel-memory/packs/2026-08-28/ru/master.png \
     --outdir carusel-memory/packs/2026-08-28/ru/slides
   python3 scripts/clean_slide_edges.py \
     --slides-dir carusel-memory/packs/2026-08-28/ru/slides
   python3 scripts/grid_gutter_qa.py \
     --master carusel-memory/packs/2026-08-28/ru/master.png \
     --slides-dir carusel-memory/output/slides \
     --output carusel-memory/output/debug/grid-gutter-qa-clean.json
   ```
   Copy cleaned RU slides to `carusel-memory/output/slides/` (standard path is RU).
3. Target: `status: ok`. RU 04/05/06 bottom white bar gone. Internal v1/v2 white on the **cleaned** master ≤ 0.45.
4. Remainder `{width: 2}` on 2480×3312 is a known 3×3 4K seam remainder. After white edges are gone it is WARN, not P0. Do not invent a fake `ok`.
5. If cleanup cannot remove the 9px bar without eating content: **regenerate the RU master** (same 3:4 @ 4K, compact prompt already 3631) and re-cut. Whole canvas, not one cell.
6. EN: run the same cleanup on `packs/2026-08-28/en/master.png` so EN QA can reach `ok`. EN publish slides already have dark edges; do not rebuild EN unless cleanup fails.
7. Re-dispatch **design-guardian** only after both QA JSONs are `status: ok`.

## Warnings

- RU 03 copy drift: last phrase rendered `закреплля качели` (double л) vs verbatim `закрепляя качели`.
- RU 01 extra graphics (thermometer, snowflake) — not extra text; hook still reads.
- RU 01 last pixel row is white (1 px). After cleanup, confirm it is gone.
- EN 07 row 0 is ~98% white (1 px hairline). 8px-strip average 0.124 < 0.60 so QA did not flag the slide; still clean it.
- RU 06 top row 0 white_ratio=0.4556 (1 px). No orphan **text** bleed on 04–09.
- Copy paraphrase (warn): RU/EN 05–07 use locked frameworks; some body lines shortened vs JSON.
- Style scorecard was pre-pixel 88. Pixel review holds family; gutter fail is separate.

## Canon gate

`python3 scripts/canon_gate.py --pack carusel-memory/packs/2026-08-28` → **PASS** (text/pack lock). Wrote `packs/2026-08-28/GATE.md`. Pixel gutter P0 is **this** report, not GATE.md.

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
Alena / `cover-refs/victoria.png` = нет.
Других женских лиц нет.

## P0 checklist

| Check | P0 | Status |
|-------|----|--------|
| 9 slides, row-major 01–09 | yes | PASS — 9+9 PNG, манифест 3×3 |
| Token drift colors/fonts | yes | PASS — уголь + #ff006e + белый гротеск + золото |
| Slide 1 hook thumbnail <2s | yes | PASS — сцена суббота/вторник |
| Slide 9 CTA visible | yes | PASS — ТЕПЛО / WARMTH + app audio |
| Reference preserve/change | yes | PASS — family lock; тема тепло/холод |
| Wrong extra text / random labels | yes | WARN — icons on 01; no Portuguese / URL / Victoria signature |
| Vertical bleed orphan text rows 2–3 | yes | PASS — no orphan text; white **frame** is the P0 above |
| Save cards 7–8 useful | warn | PASS — 07 чек-лист; 08 правило |
| Mixed aspect/size 9 PNG | yes | PASS — all 1080×1440, 0.75 = 3:4 (RU and EN) |
| `grid-gutter-qa-clean.json` missing / != ok | yes | **P0 FAIL** — status=`fail`; RU 04–06 white bottoms |
| Style score ≥ 70 | yes | PASS — scorecard 88; pixel family ~86 before gutter |
| Kie 400: compact before aspect/res change | yes | PASS — RU 3631 / EN 3843 ≤ 4500; 3:4 @ 4K; `aspect_ratio_fallback: false` |
| Copy vs CAROUSEL_SLIDE_COPY.json | warn | WARN — RU 03 typo; minor paraphrase |
| Canon Victoria 1+9, ≥3 animals | yes | PASS |
| Hook = scene; ≥2 save frameworks | yes | PASS |
| Hair honey/wheat + darker roots; no platinum | yes | PASS |
| No empty vibe-only | yes | PASS |

## Professional QA

1. **Reference fidelity:** charcoal field, magenta+white type, torn pills, animals-as-metaphor, Victoria 1+9. Preserve держит. Change: суббота/вторник, фазы, говорит/слышишь, 3 правила, CTA ТЕПЛО/WARMTH.
2. **Thumbnail:** RU/EN hook читается сразу. Не mechanic title.
3. **Grid:** row-major 01 02 03 / 04 05 06 / 07 08 09. Ячейки самодостаточные.
4. **Typography:** кириллица/латиница верные. Нет Portuguese, нет URL, нет подписи Victoria, нет «Сцена», нет Academy (EN).
5. **Save:** 05–07 карточки; 08 правило.
6. **CTA:** одно действие. RU **ТЕПЛО** + «Аудиоразбор в приложении. Суть – Тень – Вектор.» EN **WARMTH** + «Audio reading in the app. Essence–Shadow–Vector.» Captions match. Не бот, не 3 расклада.
7. **Motion:** N/A this run. `slide-01.mp4` = 1.000s ffmpeg still, 1080×1440 h264. Not Grok. Do not P0 the stub. Motion/video tests = **PASS (N/A)**.
8. **Bleed:** top 40px of 04–09 inspected. No orphan text from the row above. White **bottom** bar on RU 04–06 is the P0 (not text bleed).
9. **Video source:** skipped / N/A. Stub matches PNG geometry 1080×1440. Do not use stub as Instagram file1.
10. **No-frame QA:** file exists. **status=fail**. White edge artifacts are real.
11. **Kie recovery:** successful run stayed `3:4 @ 4K`. Compact prompt. Aspect/resolution not changed.

```text
python3 scripts/grid_gutter_qa.py \
  --master carusel-memory/packs/2026-08-28/ru/master.png \
  --slides-dir carusel-memory/output/slides \
  --output carusel-memory/output/debug/grid-gutter-qa-clean.json
→ status=fail (remainder + v1/v2 white + RU 04/05/06 bottoms)

python3 scripts/canon_gate.py --pack carusel-memory/packs/2026-08-28
→ PASS (GATE.md)

video_frame_qa / loop: N/A (static stub) → PASS
```

## Scoring

| Criterion | Score | Notes |
|-----------|------:|-------|
| Hook scene + thumbnail | 15/15 | Суббота / вторник читается |
| Canon family + Victoria 1+9 | 14/15 | Face/hair lock; new clothes |
| Animals ≥3 with jobs | 15/15 | кот / пёс / сова |
| Save frameworks | 14/15 | три рамки + recap |
| Typography / copy fidelity | 12/15 | RU 03 typo |
| Grid / gutters / size | 0/15 | P0 white bars + QA fail |
| Motion / video source | 10/10 | static stub N/A pass |
| **Total** | **64/100** | P0 → DESIGN BLOCKER |

Deductions: gutter QA fail + RU 04–06 white bar −15 (grid column zeroed); RU 03 typo −3; minor extra icons −2. Content-only would have been ~86. Cannot rubber-stamp.

## Per-slide — RU (output/slides)

| Slide | Role | Readability | Reference fidelity | Notes |
|-------|------|-------------|--------------------|-------|
| 01 | hook SCENE | high | high | Victoria + кот + телефон. Хук читается. Не cami+jeans. |
| 02 | pain | high | high | Пёс у светящегося экрана. |
| 03 | mistake | high | high | «Ловушка — греть сквозняк». Typo закреплля. |
| 04 | mechanism | high | high | Сова. **P0 white bottom bar ~9px.** |
| 05 | save phases | high | high | Тепло vs Холод. **P0 white bottom bar.** |
| 06 | says/hears | high | high | Говорит / Слышишь / Реальность. **P0 white bottom bar.** |
| 07 | checklist | high | high | 3 правила. Save card. |
| 08 | recap | high | high | Правило + медальон ТАРО СЕЙЧАС. |
| 09 | CTA | high | high | Та же Victoria, satin wrap. Скрипт ТЕПЛО. App audio. |

## Per-slide — EN (packs/2026-08-28/en/slides)

| Slide | Role | Readability | Reference fidelity | Notes |
|-------|------|-------------|--------------------|-------|
| 01 | hook SCENE | high | high | Victoria + cat + Hot & Cold script. |
| 02 | pain | high | high | Dog at glowing phone. |
| 03 | mistake | high | high | Trap of warming his draft. |
| 04 | mechanism | high | high | Owl + intermittent reinforcement. Edges clean. |
| 05 | save phases | high | high | Warm vs Cold. Edges clean. |
| 06 | says/hears | high | high | Says / You hear / Reality. |
| 07 | checklist | high | high | 3 rules. 1px white hairline on row 0. |
| 08 | recap | high | high | Clarity over constant waiting + Today Tarot. |
| 09 | CTA | high | high | Same Victoria. WARMTH + Essence–Shadow–Vector. |

## Caption / product (locale)

- RU trigger: **ТЕПЛО**. EN trigger: **WARMTH**. Different words, topic-tied.
- Product: `app_audio`. Direct = аудиоразбор / audio reading in the app.
- RU: Суть – Тень – Вектор. EN: Essence–Shadow–Vector.
- `@todaytaro_bot` = EN Instagram handle, not the prize.
- No raw URLs. Links in profile / ссылки в шапке.
- No Academy on EN. No «личный аудиоразбор». No 3 free bot spreads.

## Handoff

Director: re-slice RU (cleanup + re-QA). Do not upload. Do not publish.
`publish_requested: false`.

HANDOFF_NEXT: upload (blocked until this report is DESIGN OK)
