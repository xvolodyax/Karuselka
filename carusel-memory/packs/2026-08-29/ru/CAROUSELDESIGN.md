---
name: Labels Status — animals_viktoria_collage
pack_id: "2026-08-29"
run_id: "2026-08-29-1110"
lang: ru
en_pair: true
topic: "Зачем вешать ярлыки: почему он ведёт себя как твой мужчина, но боится статуса?"
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
colors:
  primary: "#ffffff"
  background: "#111111"
  background_alt: "#1a1a1a"
  on-background: "#ffffff"
  accent: "#ff006e"
  surface: "#1a1a1a"
  outline: "#ff006e"
  metal: "#c9a227"
typography:
  slide-headline:
    family: "heavy condensed sans"
    color: "#ffffff"
    role: "primary keywords, hook, numbers"
  slide-body:
    family: "medium sans"
    color: "#ffffff"
    role: "one short supporting line"
  slide-script:
    family: "thin handwritten script"
    color: "#ff006e"
    role: "secondary word from locked copy only"
  slide-cta:
    family: "huge magenta script + heavy white sans"
    color: "#ff006e"
    role: "trigger СТАТУС / LABELS"
  slide-number:
    enabled: false
    note: "no extra labels; no Сцена; no slide-index pills"
grid:
  cols: 3
  rows: 3
  order: "row-major"
  gutters: "thin white seams at 1/3 and 2/3 (Excalibur / seam)"
  gutters_px: 8
  cell_is_self_contained: true
  animate_slide: false
  slide_01: "static_png"
carousel_system:
  carousel_family: "animals_viktoria_collage"
  face_lock: "viktoriaref.png"
  face_lock_path: "carusel-memory/references/viktoriaref.png"
  slice_method: "seam"
  static_png_only: true
  narrative: "hook-value-cta"
  trigger_word_ru: "СТАТУС"
  trigger_word_en: "LABELS"
  product: "app_audio"
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
wardrobe:
  slide_01: "graphite silk pajama shirt, open collar, no necklace, high-waist black wide-leg trousers"
  slide_09: "petrol-teal silk blouse with soft high neck, cropped espresso suede jacket open, slim black trousers"
  forbidden:
    - "white cami + gold pendant from viktoriaref.png"
    - "burgundy turtleneck (pack 2026-08-28 slide 01)"
    - "black satin wrap (pack 2026-08-28 slide 09)"
identity:
  eyes: "green with slight hazel"
  hair: "warm honey blonde + darker roots, not platinum"
  victoria_slides: [1, 9]
  in_scene: true
  sticker_halo: false
---

# Source Replication Doctrine

Референс семьи — `animals-viktoria-style-lock.png` / `image-851e.png`: **style + layout + palette**. Не лицо. Не i2i как face.

Face lock — **только** `carusel-memory/references/viktoriaref.png`. Одна женщина. Фронтальное фото для идентификации. `виктория.png` — Алёна. Никогда i2i `виктория.png`, `victoria-sheet.png`, `victoria.png`, `victoria_ref.jpg`, `alena*.png`, `character-sheet-2k`.

Сначала decomposition, потом адаптация под тему ярлыков / статуса. Не «в этом стиле». Копируем систему: тёмное поле, маджента + белый тип, рваные плашки, животные-как-метафора, Виктория на 1 и 9, seam-нарезка. Меняем тему, копирайт, объекты, гардероб, позу.

# Composition Lock

- Master: одно полотно **3:4 @ 4K**, сетка **3×3**, row-major `01 02 03 / 04 05 06 / 07 08 09`.
- `slice_method: seam` — тонкие белые швы на 1/3 и 2/3 (Excalibur). Не zero-gutter. Не sticker-halo вокруг людей и животных.
- Каждая ячейка self-contained, 3:4. Текст и лица **≥10–12%** от внешних краёв и от швов.
- Виктория **в сцене** на 01 и 09. Без вырезки, без белого ореола, без дублей.
- Животные на **≥3** слайдах как метафора: 01 кот, 02 пёс, 04 сова.
- Статические PNG. Slide 01 — PNG. Нет video / Grok / motion.
- Verbatim copy из `CAROUSEL_SLIDE_COPY.json` (RU) и `design/en/CAROUSEL_SLIDE_COPY.json` (EN). Без лишних подписей. Слово «Сцена» не писать нигде на слайдах.

# Philosophy & Vibe

Ночная близость против утреннего уклонения. Не horror-свечи, не бежевый lifestyle, не пастель. Fashion-collage на антраците: тяжёлый белый гротеск режет хук за 2 секунды, маджентовый скрипт шепчет вторичное слово из лоченного копирайта. Животное делает работу — чует, ждёт, видит расчёт. Виктория не наклейка и не студийный блейзер: она в комнате этой истории, в новой одежде.

# Grid Rules

- 3 колонки × 3 ряда. Чтение слева направо, сверху вниз.
- Тонкие белые gutters ровно на линиях 1/3 и 2/3. Кривой шов = пересборка всего canvas.
- Фон ячейки full-bleed до шва. Объекты не пересекают шов.
- Safe margin 10–12% внутри каждой панели.
- Не 2×3, не horizontal strip, не 4:5, не 1:1.

# Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed charcoal |
| type | `#ffffff` | heavy sans headlines + body |
| accent | `#ff006e` | script, torn-tape, trigger |
| metal | soft gold `#c9a227` | optional ТАРО / СЕЙЧАС medallion on 08 |

Белый на `#111111` — AAA. Маджента — только крупный скрипт или белый текст на маджентовой плашке. Мелкий magenta body запрещён.

# Typography & Readability

- Headline: тяжёлый белый sans, хук читается на thumbnail.
- Body: 1 короткая белая строка под заголовком.
- Script: тонкий handwritten magenta — только слова из JSON (`script`, trigger, slogan).
- Torn-tape pills: графика без новых слов, либо точная цитата из locked copy.
- Нет watermark, нет подписи Victoria, нет «Сцена», нет RESET / SPA MINDSET и прочих лейблов референса.
- EN canvas: те же зоны, verbatim EN copy. Trigger `LABELS`. Slogan `Clarity now`.

# Slide Rhythm

```text
01 hook lived-situation   Victoria + cat
02 pain                   dog at the closed door
03 mistake                type + torn magenta tape
04 mechanism              owl + 100/0
05 save A                 Отношения vs Серая зона
06 save B                 Говорит vs Слышишь vs Реальность
07 save C                 3 теста
08 rule                   Определённость — это база
09 CTA                    Victoria + СТАТУС
```

# Wardrobe this pack

Новый гардероб. Не копировать референс и не повторять вчера.

- **01:** графитовая шёлковая пижамная рубашка, ворот открыт на две пуговицы, без подвески; чёрные wide-leg брюки. Поза 3/4 сидя на краю смятой тёмной постели, взгляд через плечо.
- **09:** петрольно-бирюзовая шёлковая блуза с мягкой высокой горловиной (не водолазка, не wrap); укороченный жакет из эспрессо-замши нараспашку; узкие чёрные брюки. Поза стоя, вес на бедре, взгляд в камеру мягкий и твёрдый.

Запрещено: white cami + gold pendant; burgundy turtleneck; black satin wrap; ivory studio-blazer; platinum hair.

# Do's and Don'ts

**Do**

- Face lock `viktoriaref.png` as first and only i2i input.
- Eyes green + slight hazel. Hair warm honey + darker roots.
- Animals as metaphor, in-scene, no die-cut halo.
- Seam gutters. Static PNG. Verbatim copy.
- New clothes and pose vs ref and vs 2026-08-28.

**Don't**

- i2i Alena / `виктория.png` / sheet files / style-lock as a face.
- Sticker white halo. Zero-gutter «cells touch».
- Extra labels, Portuguese text, foreign faces, horror table.
- Video on slide 01. Raw URLs. Bot spreads. Word «Сцена».
- Write `CAROUSEL_IMAGE_PROMPT.json` in this step.
