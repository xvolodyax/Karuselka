# Carusel brief — ТАРО СЕЙЧАС / Today Tarot — PENDING new-day

lang: ru
topic: ТАРО СЕЙЧАС
handle: @todaytaro_ru
publish_requested: false
visual_family: animals_viktoria_collage
face_lock: none
slice_method: seam
cta_style: comment_trigger
trigger_word: PENDING
trigger_word_en: PENDING
product: app_audio
cta_offer: comment trigger → Direct audio reading in the APP (Суть – Тень – Вектор / Essence–Shadow–Vector)
bot_vs_app: sell the APP audio reading, not 3 free bot spreads
slides: 9
grid: 3x3
slide_01: static_png
skip_motion: true
skip_animate: true
skip_glavred: true
skip_publish: true
bilingual_pair: true
en_handle: @todaytaro_bot
en_brand: Today Tarot
slot: 11:10 MSK
date: PENDING
pack_id: PENDING
**run_id:** PENDING

## Canon (next swarm)

- Parent: `gemini-3.8-flash` + `reasoning_effort=high`
- Text Task workers: `model="inherit"` only. No slug `gemini-3.8-flash`. No Claude/GPT/Composer fallback. No Gemini → FAIL + HOLE
- No host portrait (без лица Вики). FACE_CHECK ABSENT
- 9+9 static PNG. Slide-01 is PNG
- CTA = app audio, not bot
- Director reads `shared/director-once.md` once, then CLI + Task. Do not loop-read gate/publish scripts
- Archive Instagram permalinks (including 30.08 `DcqJGCblQqv` / `DcqJS--m0op`) are FORBIDDEN as today's report

## Intake

- audience: женщины 20–50, отношения (~78%). Не целиться в 13–17. Не пугать одиночеством.
- goal: лиды в приложение через comment trigger → Direct аудиоразбор (Суть – Тень – Вектор / Essence–Shadow–Vector)
- reference_carousel: family `animals_viktoria_collage`; live packs 27.08–30.08 are FORBIDDEN repeats
- slide_copy_notes: auto — Gemini (inherit) пишет 9 RU + 9 EN + две подписи. Director не пишет слайды.
- cta_target: header_link — «ссылки в шапке профиля» / «links in the profile». No raw URLs.
- brand: ТАРО СЕЙЧАС / Today Tarot. Dark + magenta. No host portrait.
- caption_preferences: Gemini writes RU caption AND EN caption in the same copywriter step. Product `app_audio`.

## One swarm, one chain (this run)

researcher (Gemini via inherit) → copywriter (9 RU + RU caption AND 9 EN + EN caption, via inherit) → designer → image-prompter → slice (Kie pixels) → skip motion → skip animate → design-guardian + FACE_CHECK ABSENT → upload → publish only if Hall set publish_requested true

SKIP this run: motion-director, animate/Grok video, Glavred, Telegram.

Hall does not write, draw, review slides, or publish. Start with:

```bash
python scripts/pipeline_gate.py --workspace . new-day --date YYYY-MM-DD --lang ru
```

## Topic lock (Gemini researcher locks the exact hook)

Researcher MUST pick a NEW relationship-pain topic. Code word must be new. RU ≠ EN.

FORBIDDEN repeats:
- «Пауза или конец» / Pause or over
- «Пинг или шаг» / Ping vs step
- «Тепло – холодно» / Hot & Cold (2026-08-28)
- «Зачем вешать ярлыки» / Why Put Labels On It (2026-08-29)
- «Он пропадает на выходных» / weekend vacuum (2026-08-30 СУББОТА / WEEKEND)
- triggers ШАГ / STEP / ПАУЗА / PAUSE / ТЕПЛО / WARMTH / ПРОЧИТАНО / СТАТУС / STATUS / LABELS / СУББОТА / WEEKEND

Never use the word «Сцена» on slides or in caption.
Write «в моём приложении», never «в нашем приложении».

## CTA (hard gate)

Last slide + caption sell the IN-APP audio reading on THIS carousel topic.
- RU: «Суть – Тень – Вектор»
- EN: Essence–Shadow–Vector
Do NOT sell 3 free bot spreads. Do NOT sell the bot.
No raw URLs — only «ссылки в шапке профиля» / «links in the profile».

## Face + cut

- No host portrait on any slide (face_lock: none)
- NEVER i2i `Виктория.png`, `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`, `victoria_ref.jpg`, `alena*.png`
- Seam slice: Excalibur white gutters at 1/3 and 2/3
- On CROOKED CANVAS: regen whole master, never patch one cell

## Publish

Default: `publish_requested: false`. Hall must flip it to true for a live day.
After GATE PASS + FACE_CHECK ABSENT: Composio aliases `instagram-ru` / `instagram-en`.
403 / no tool_execution → FAIL + HOLE. Do not copy archive URLs.
GATE FAIL (bot-offer, host face, video, duplicate code word, missing 9+9): stop, do not publish.
