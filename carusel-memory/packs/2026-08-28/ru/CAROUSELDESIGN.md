---
name: ТАРО СЕЙЧАС — Тепло – холодно / Today Tarot — Hot & Cold
lang: ru
bilingual_pair: true
en_source: carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json
pack_id: 2026-08-28
run_id: 2026-08-28-1110
topic_ru: "Тепло – холодно: почему он то держит за руку, то отдаляется на неделю?"
topic_en: "Hot & Cold: Why he holds your hand all weekend and goes cold on Monday"
product: app_audio
trigger_ru: ТЕПЛО
trigger_en: WARMTH
publish_requested: false
format:
  generation_mode: "grid_3x3"
  slide_count: 9
  grid:
    cols: 3
    rows: 3
    order: "row-major"
  master_aspect: "3:4"
  resolution: "4K"
  panel_aspect: "3:4"
  slice_method: "seam"
colors:
  primary: "#ffffff"
  background: "#111111"
  on-background: "#ffffff"
  accent: "#ff006e"
  surface: "#1a1a1a"
  outline: "#ff006e"
  metal: "#c9a86a"
typography:
  slide-headline: "heavy grotesque sans, #ffffff, dominant"
  slide-body: "medium grotesque sans, #ffffff, 1–2 short lines"
  slide-script: "thin handwritten / italic script, #ff006e"
  slide-cta: "huge magenta script trigger + white body"
  slide-number: "tiny magenta pill, bottom-right, 01–09"
grid:
  cols: 3
  rows: 3
  order: "row-major"
  gutters_px: 3
  gutters: "thin white seams on 1/3 and 2/3"
  cell_is_self_contained: true
  animate_slide: 1
  this_run_slide_01: "static_png"
carousel_system:
  carousel_family: "animals_viktoria_collage"
  narrative: "hook-pain-mistake-mechanism-save-save-save-recap-cta"
  slide_roles:
    - hook
    - pain
    - mistake
    - mechanism
    - save
    - save
    - save
    - recap
    - cta
face_lock: victoria-sheet.png
hair_lock: "warm honey/wheat blonde with darker roots as on victoria-sheet.png"
---

# CAROUSELDESIGN — Тепло / холодно · Hot & Cold

Дизайн-контракт для одной bilingual-пары. RU primary. EN — та же визуальная семья, текст strictly из `carusel-memory/design/en/CAROUSEL_SLIDE_COPY.json`. Пиксели и Kie-промпт **не** входят в этот шаг.

## Source Replication Doctrine

Референс = закон. Style/layout lock: `karusel-old/image-851e.png` / `animals-viktoria-style-lock` (палитра, коллаж, heavy sans + magenta script, животные-метафоры). Face/hair lock: **только** `victoria-sheet.png` (лицо и волосы). Смысловая глубина save-карточек — из `slide-04.png` (говорит / слышишь), не визуал.

Сначала decomposition (`CAROUSEL_SOURCE_DECOMPOSITION.json`), затем адаптация темы «тепло – холодно». Не описывать референс словами «в этом стиле».

**Preserve:** тёмное поле, `#ff006e`, белый гротеск, magenta script, torn-tape pills, Victoria на 1 и 9, ≥3 животных-метафор, 3×3 / 3:4, тонкие белые gutters, safe 10–12%.

**Change:** сюжет (суббота → вторник), одежда и поза Виктории, объекты (телефон, фазы, чек-лист), copy, CTA `ТЕПЛО` / `WARMTH`, продукт `app_audio`.

**Do not borrow:** португальский текст, чужие женские лица, Alena (`victoria.png`), platinum, white cami+jeans с листа, ivory blazer, horror-стол, логотипы чужих брендов, слово «Сцена», бот как приз.

## Composition Lock

- Один master `3:4 @ 4K`, сетка 3×3, row-major `01 02 03 / 04 05 06 / 07 08 09`.
- Каждая ячейка — самостоятельная панель 3:4. Не horizontal strip.
- Тонкие белые gutters на 1/3 и 2/3 (Excalibur). Код режет **по** швам. Zero-gutter / sticker-halo запрещены.
- Safe margin ≥10–12% от всех швов и краёв ячейки. Текст не у нижнего края.
- Victoria in-scene на **01 и 09** (не стикер, не ореол). Лицо+волосы с листа; одежда и поза **новые**.
- Животные: кот (01), пёс (02), сова (04). Метафора, не мем.
- Save 05–07 — рамки / карточки / вопросы (минимум две; в этом run все три).
- Слайд 09 продаёт **аудиоразбор в приложении** (Суть – Тень – Вектор / Essence–Shadow–Vector). Не бот.
- Verbatim copy. Никаких лишних лейблов, водяных знаков, подписи Victoria, слова «Сцена».

## Philosophy & Vibe

Кинематографичный контраст температур: субботнее тепло (золотой rim, близость взгляда) против вторничного холода (ледяное свечение экрана, сухое «занят»). Не пастель, не бежевый lifestyle, не horror. Fashion-collage на антраците. Читательница узнаёт сцену за 2 секунды и свайпает за механизмом, не за вайбом.

## Grid Rules

- `generation_mode: grid_3x3`, `aspect_ratio: 3:4`, `resolution: 4K`.
- Gutters: тонкие белые линии, ~3 px visual, без bleed между ячейками.
- `cell_is_self_contained: true` — ни один headline не пересекает шов.
- Этот run: `slide_01: static_png`, motion/animate skip. Композиция 01 всё равно motion-safe (крупный headline, один герой, один зверь, спокойный центр).
- Нарезка: `seam_slice_grid.py --split-mode gutter`. Кривой шов → пересборка всего холста.

## Color Guidance

| Роль | Hex | Где |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed антрацит |
| type | `#ffffff` | headlines, body |
| accent | `#ff006e` | script, pills, tape, губы, триггер |
| metal | soft gold `#c9a86a` | медальон, hoop, лёгкий foil на 08 |
| cold glow | cool phone light | экран на 01–02, не horror-синий |

Контраст белого на `#111111` ≈ 18:1 (WCAG AAA). Magenta script только на тёмном поле, крупно.

## Typography & Readability

- Headline: heavy sans, белый, 1 строка (или 2 на hook).
- Body: короче, белый, не плотный абзац.
- Script magenta: «Тепло – холодно» / «Hot & Cold» на 01; `ТЕПЛО` / `WARMTH` гигант на 09.
- Pills / torn tape: короткие ярлыки фаз и правил.
- Точный текст в кавычках для prompter. `verbatim, no substitutions, no extra labels`.
- Кириллица читаемая. EN pair — те же зоны, английские строки из locked copy.
- Запрещено: «Сцена», «Slide 1», watermark, подпись Victoria, сырые URL.

## Slide Rhythm

```text
01 hook SCENE   Victoria + кот + сцена суббота/вторник
02 pain         пёс у экрана, поиск ошибки
03 mistake      pills: ловушка «греть сквозняк»
04 mechanism    сова + прерывистое подкрепление
05 save A       рамка: Тепло vs Холод
06 save B       рамка: Говорит / Слышишь / Реальность
07 save C       рамка-чек-лист: 3 правила
08 recap        правило ясности + золотой медальон
09 CTA          Victoria + ТЕПЛО/WARMTH + Суть–Тень–Вектор
```

## Do's and Don'ts

**Do**

- Лицо и волосы только с `victoria-sheet.png`.
- Новая одежда: 01 burgundy turtleneck; 09 black satin wrap. Не cami+jeans, не ivory blazer.
- Honey/wheat + darker roots. Глаза зелёные с hazel.
- ≥3 животных с работой (кот / пёс / сова).
- Две+ save-рамки на 05–07.
- CTA = comment trigger → app audio. RU Суть – Тень – Вектор. EN Essence–Shadow–Vector.
- Thin white gutters. Safe 10–12%.

**Don't**

- Platinum / Alena / `cover-refs/victoria.png` / studio-blazer / doubles.
- Horror, кровь, черепа, свечи, ouija.
- Стикер-ореол, die-cut, zero-gutter.
- Бот, «3 бесплатных расклада», «личный аудиоразбор», Academy (EN), сырые URL.
- Слово «Сцена» на слайдах.
- Пустые vibe-панели без урока.
- Писать `CAROUSEL_IMAGE_PROMPT.json` (зона image-prompter).
- Публиковать.
