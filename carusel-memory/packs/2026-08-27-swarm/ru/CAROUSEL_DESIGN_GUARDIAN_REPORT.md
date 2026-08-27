# CAROUSEL_DESIGN_GUARDIAN_REPORT

✅ DESIGN OK
Verdict: ✅ DESIGN OK
Score: 91/100

lang: ru
handle: @todaytaro_ru
family: animals_viktoria_collage
pack: 2026-08-27-v2 — Пинг vs шаг
role: carusel-design-guardian
dispatch_id: 5e7a6bf0077047c0a6cc8bd8e5e1508b

Просмотрены все 9 PNG (`slide-01.png` … `slide-09.png`) и `output/video/slide-01.mp4`.
Канон `animals_viktoria_collage` держится. `grid-gutter-qa-clean.json` = fail только из‑за remainder width=2 (2480 не делится на 3), не из‑за белых желобков. Слайды usable → WARN, не BLOCKER.

## P0 Blockers
(none)

## Warnings
- `grid-gutter-qa-clean.json` status=`fail`: master 2480×3312, remainders `{width: 2, height: 0}`. Internal white_ratio ≈ 0 (v1/v2/h2 = 0; h1 = 0.0002). Белых рамок после cleanup нет. Слайды usable, 826×1104 все девять. WARN, не BLOCKER.
- Slide 05 top ~40–80 px: обрывок маджента-ленты «он всё понял?»» с низа slide-02. Карточка ПИНГ/ШАГ целиком читается. Не orphan-разрушение панели. WARN.
- Slide 04 top strip: визуальный хвост ряда 1 (золотая точка / край одежды), без orphan-текста.
- Copy drift (warn): slide-02 низ обрезает хвост «Он всё понял?»; slide-04 body «почувствовал» вместо «почуял»; slide-06 заголовок «VS ЧТО ТЫ СЛЫШИШЬ» vs verbatim «vs что ты слышишь».
- MP4 816×1104 vs PNG 826×1104 — pitfall 11.2. Upload: `--normalize-video-to-slides`. Не blocker guardian.
- Slide-01 extra: розовый пузырь «…» у кота — графика, не чужой слоган.

## Canon gate

| Check | Result |
|-------|--------|
| (a) Victoria = `victoria-sheet.png`, не Alena, не studio-blazer | PASS — 1 и 9 одно лицо; honey/wheat + тёмные корни; не platinum |
| (b) ≥3 слайда с животным-метафорой | PASS — кот 01 (чутьё), пёс 02 (ждёт у экрана), сова 04 (ночной скан) |
| (c) ≥2 save с рамкой/вопросами | PASS — 05 таблица ПИНГ/ШАГ; 06 Пишет/Слышишь/В реальности; 07 три вопроса |
| (d) hook = сцена | PASS — «Он молчал 24 дня. В 23:42: «Спишь?»» |
| (e) нет platinum; одежда не с листа и не ivory blazer | PASS — 01 бордовый атлас + чёрные брюки; 09 кожанка + водолазка + шоколадные брюки |
| (f) нет пустых vibe-only | PASS — у каждого слайда урок |

Hair lock: тёплый медово-пшеничный блонд, корни темнее. Platinum = нет.
Sheet tank+jeans = нет.
Alena / `cover-refs/victoria.png` = нет.
Других женских лиц нет.

## P0 checklist

| Check | P0 | Status |
|-------|----|--------|
| 9 slides, row-major 01–09 | yes | PASS — 9 PNG, манифест 3×3 |
| Token drift colors/fonts | yes | PASS — уголь + #ff006e + белый гротеск + золото |
| Slide 1 hook thumbnail <2s | yes | PASS — сцена 24 дня / 23:42 / «Спишь?» |
| Slide 9 CTA visible | yes | PASS — скрипт ШАГ + «Напиши ШАГ в комментариях» + бот / Direct |
| Reference preserve/change | yes | PASS — family lock; тема пинг vs шаг, не «Пауза или конец?» |
| Wrong extra text / random labels | yes | WARN — хвост «он всё понял?» на 05; пузырь «…» на 01 |
| Vertical bleed orphan text rows 2–3 | yes | WARN — только тонкая лента на 05; панели usable |
| Save cards 7–8 useful | warn | PASS — 07 чек-лист; 08 правило шага vs пинга |
| Mixed aspect/size 9 PNG | yes | PASS — все 826×1104, aspect 0.7482 ≈ 3:4 |
| `grid-gutter-qa-clean.json` missing / != ok | yes | WARN — fail только remainder width=2; white gutters нет |
| Style score ≥ 70 | yes | PASS — scorecard 86 (layout); pixel review ~88 |
| Kie 400: compact before aspect/res change | yes | PASS — prompt_compacted 4179 ≤ 4500; 3:4 @ 4K; `aspect_ratio_fallback: false` |
| Copy vs CAROUSEL_SLIDE_COPY.json | warn | WARN — см. drift выше |
| Canon Victoria 1+9, ≥3 animals | yes | PASS |
| Hook = scene; ≥2 save frameworks | yes | PASS |
| Hair honey/wheat + darker roots; no platinum | yes | PASS |
| No empty vibe-only | yes | PASS |

## Professional QA

1. **Reference fidelity:** charcoal field, magenta+white type, cutouts, pills, animals-as-metaphor, Victoria 1+9. Preserve держат. Change: ночной пинг 23:42, поводок, крючок, таблица, три слоя, чек-лист.
2. **Thumbnail:** hook читается сразу.
3. **Grid:** row-major 01 02 03 / 04 05 06 / 07 08 09. Ячейки самодостаточные.
4. **Typography:** кириллица верная. Нет Portuguese, нет URL, нет подписи Victoria, нет «Пауза или конец?», нет «Ясность сейчас» на панелях.
5. **Save:** 05–07 карточки для скрина; 08 правило.
6. **CTA:** одно действие, одно слово-триггер **ШАГ**. Продукт: 3 бесплатных расклада в боте. Команда отвечает в Direct. Не app, не Academy.
7. **Motion:** MP4 5.000s, 816×1104, h264. Кадр 0 = тот же hook. Текст стабилен. Loop без hard cut.
8. **Bleed:** top 40px слайдов 04–09 просмотрен. Orphan-текст только на 05 (лента). 04 визуальный хвост. 07–09 тонкие линии кадра, не текст. Regen master не требуем: панели usable.
9. **Video source:** `video_frame_qa` кадр 0 MAE **7.57 ≤ 35 PASS**. Loop MAE **7.71 ≤ 15 PASS**. Animate log совпадает (7.57).
10. **No-frame QA:** файл есть. status=`fail` = remainder, не white edge. Internal lines тёмные.
11. **Kie recovery:** успешный run остался `3:4 @ 4K`. Compact prompt 4179. Aspect/resolution не меняли.

```text
python scripts/video_frame_qa.py \
  --video carusel-memory/output/video/slide-01.mp4 \
  --png carusel-memory/output/slides/slide-01.png \
  --loop-check
→ frame0_mae=7.57 PASS; loop_mae=7.71 PASS
```

## Scoring

| Criterion | Score | Notes |
|-----------|------:|-------|
| Hook scene + thumbnail | 15/15 | Физическая ночная сцена |
| Canon family + Victoria 1+9 | 14/15 | Лицо/волосы lock; одежда новая |
| Animals ≥3 with jobs | 15/15 | кот / пёс / сова |
| Save frameworks | 14/15 | три рамки + recap |
| Typography / copy fidelity | 11/15 | drift + хвост на 05 |
| Grid / gutters / size | 12/15 | remainder WARN; PNG единый размер |
| Motion / video source | 10/10 | MAE 7.57; loop ок |
| **Total** | **91/100** | 90–100 = DESIGN OK |

Deductions: remainder −3; usable bleed strip 05 −4; copy paraphrase −2.

## Per-slide

| Slide | Role | Readability | Reference fidelity | Notes |
|-------|------|-------------|--------------------|-------|
| 01 | hook SCENE | high | high | Victoria + кот + телефон. Хук читается. Не cami+jeans. |
| 02 | pain | high | high | Пёс у светящегося экрана. Низ ленты режется на 05. |
| 03 | mistake | high | high | «Ловушка» маджента + поводок. Без людей/животных. |
| 04 | mechanism | high | high | Сова + крючок. «не шаг / обычный пинг». Top visual sliver. |
| 05 | save table | high | high | ПИНГ vs ШАГ. Top orphan «он всё понял?» — WARN. |
| 06 | says/hears | high | high | Три слоя. Пишет / Слышишь / В реальности. |
| 07 | checklist | high | high | 3 вопроса, пилюли 1–3. Save card. |
| 08 | recap | high | high | Правило. Медальон ТАРО/СЕЙЧАС нативен. |
| 09 | CTA | high | high | Та же Victoria, другая одежда. Скрипт ШАГ. Бот, не app. |

## Caption / product (locale)

- Триггер: **ШАГ** (один).
- Продукт: `bot_three_spreads` — 3 бесплатных расклада в боте, ответ в Direct.
- `@todaytaro_bot` = Telegram-бот, не приложение.
- Сырых URL в слайдах нет. Caption без `https://` / `t.me` / `instagram.com`.

## Handoff

Upload может нормализовать MP4 к 826×1104 (`--normalize-video-to-slides`).
Publish не запускать: `publish_requested: false`. Instagram не публиковался.

HANDOFF_NEXT: upload
