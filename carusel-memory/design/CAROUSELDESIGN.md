---
name: ТАРО СЕЙЧАС — Онлайн-фантом / орбитальный просмотр
pack_id: 2026-08-30-ru-scout
run_id: 2026-08-30-ru-scout
slot: scout-same-day
lang: ru
bilingual_pair: false
product: app_audio
pipeline_gate: required
step: designer
handoff_next: image-prompter
dispatch_id: c99f172aca2f45a7ab3b93c00d178499
dispatched_via: "Task(generalPurpose)"
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
  output: "static_png"
  skip_motion: true
  skip_animate: true
  slice_method: "seam"
colors:
  primary: "#ff006e"
  background: "#111111"
  on-background: "#ffffff"
  accent: "#ff006e"
  surface: "#1a1a1a"
  outline: "#d4af37"
  metal: "soft gold"
typography:
  slide-headline: "heavy sans, white, #ffffff"
  slide-body: "medium sans, white 85–92%"
  slide-cta: "huge thin script / handwritten, magenta #ff006e — ОНЛАЙН"
  slide-number: "small white or gold pill, bottom-right, never on seam"
  slide-script: "thin magenta script for secondary words only"
  slide-pill: "magenta torn-tape / pill blocks for short labels"
grid:
  cols: 3
  rows: 3
  order: "row-major"
  gutters: "thin white seams at 1/3 and 2/3 (horizontal + vertical)"
  gutters_px: 3
  cell_is_self_contained: true
  slice_method: "seam"
  safe_area_pct: 12
  animate_slide: 0
carousel_system:
  carousel_family: "animals_viktoria_collage"
  narrative: "hook-pain-mistake-mechanism-save-save-save-recap-cta"
  product: "app_audio"
  trigger_ru: "ОНЛАЙН"
  face_lock: none
  host_portrait: false
  victoria_slides: []
  slide_roles:
    - hook
    - problem
    - mistake
    - mechanism
    - save_decoder
    - save_checklist
    - save_framework
    - recap
    - cta
identity:
  face_lock: none
  host_portrait: false
  victoria_slides: []
  face_file: none
  rule: "Нет портрета ведущей. Не рисовать Вику. Не класть Виктория.png в генерацию."
  forbidden_on_any_slide:
    - "Виктория.png / viktoriaref.png / victoria-sheet.png / victoria.png"
    - "любое женское лицо / ведущая / presenter / woman"
    - "микрофон у рта"
    - "host portrait / FACE MATCH"
style_lock:
  file: "carusel-memory/references/animals-viktoria-style-lock.png"
  role: "palette + collage rhythm ONLY — never i2i as a face"
  also: "karusel-old/image-851e.png — same role"
animal_map:
  "01": cat
  "02": dog
  "03": dog
  "04": owl
  "05": owl
  "06": cat
  "07": owl
  "08": cat
  "09": none
---

# CAROUSELDESIGN — 2026-08-30-ru-scout · Онлайн-фантом

Только дизайн-контракт. Нет Kie-промпта. Нет пикселей. Нет публикации.

`carousel_family`: **animals_viktoria_collage**  
`face_lock`: **none** · `host_portrait`: **false** · `victoria_slides`: **[]**  
`slice_method`: **seam** (тонкие белые швы на 1/3 и 2/3)  
`generation_mode`: **grid_3x3** · master **3:4 @ 4K** · static PNG  
`product`: **app_audio** · слайд 9 — огромный маджента **ОНЛАЙН** + объект телефона/приложения  
`lang`: **ru only** · handle `@todaytaro_ru`

## Source Replication Doctrine

Референс пользователя = закон. Style lock —
`animals-viktoria-style-lock.png` / `image-851e.png` — **только палитра,
ритм коллажа, типографика**. Это не лицо. Не i2i как портрет.

Сначала decomposition, потом адаптация под тему
«Смотрит сторис сразу — отвечает часами позже».

- **preserve**: угольный фон, микс маджента + белый, рваные плашки,
  животные-метафоры, seam-нарезка, ячейки 3:4, мягкое золото, отсутствие
  портрета ведущей.
- **change**: объекты темы (светящийся экран сторис, «висящий» чат,
  зелёный кружок онлайна, ночные часы), verbatim-копия, карта животных
  cat 1/6/8 · dog 2/3 · owl 4/5/7 · none на 9, CTA-слово **ОНЛАЙН**.
- **do_not_borrow**: португальский текст и чужие лица из style lock,
  Вика / любое женское лицо / микрофон у рта, sticker-halo вокруг
  животных, horror-стол, оффер бота, водяные знаки.

## Composition Lock

На всех 9 панелях зафиксировано:

1. Матовый графит / чёрный `#111111`–`#1a1a1a` full-bleed в каждой ячейке.
2. Тяжёлый белый гротеск для заголовков; маджента-скрипт и torn-tape.
3. Мягкое золото только как фольга (медальон, тонкий блик) — не как заливка.
4. Тонкие **белые** швы на мастере по 1/3 и 2/3. Текст и объекты не
   пересекают швы.
5. Safe area ≥10–12% от края ячейки и шва.
6. Verbatim из `CAROUSEL_SLIDE_COPY.json`. Без лишних лейблов, без
   водяных знаков, без подписи Victoria.
7. **Ни одного человеческого лица.** Ни Вики, ни ведущей, ни женщины,
   ни микрофона у рта. `FACE_CHECK` должен быть ABSENT.
8. Животные = метафоры, не милые питомцы. Минимум 3 слайда (здесь 8 из 9).
9. Слайд 9 = огромный маджента **ОНЛАЙН** + объект телефона / UI приложения.
   Без человека. Без животного.

## Philosophy & Vibe

Темнота комнаты и холодный свет экрана. Он смотрит сторис за две секунды
и оставляет твой диалог висеть с обеда. Это не мистика и не horror.
Это fashion-коллаж про цифровой орбитальный контроль: кот уже чует,
пёс ждёт у экрана, сова называет механизм.

Тон: взрослый, ясный, без виктимности. Контраст структурный
(мгновенный просмотр / часы тишины), не театральный.

Нет ведущей в кадре. Сцену держат объекты и животные.

## Grid Rules

- Один master, **3:4 @ 4K**, **3×3**, row-major:
  `01 02 03 / 04 05 06 / 07 08 09`.
- **Seam slice**: тонкие белые gutters на линиях 1/3 и 2/3.
  Нарезка `scripts/seam_slice_grid.py --split-mode gutter`.
- Кривой холст → пересобрать весь master. Не патчить одну ячейку.
- Каждая ячейка — автономный портрет 3:4. Не 4:5. Не 1:1.
- Hook (01) = крупная сцена + кот + светящийся телефон. Без женщины.
- Internal (02–08) = 50–60% текста, животное снизу или сбоку.
- CTA (09) = **огромный маджента-скрипт ОНЛАЙН** + телефон / app-объект.
- Static PNG. Slide 01 — PNG, не видео.

## Color Guidance

| Role | Hex | Use |
|------|-----|-----|
| background | `#111111`–`#1a1a1a` | full-bleed charcoal |
| accent | `#ff006e` | script, pills, tape, trigger **ОНЛАЙН** |
| type | `#ffffff` | heavy sans headlines + body |
| metal | soft gold `#d4af37` | medallion, light foil |

Нет пастельной радуги. Нет бежевого lifestyle. Нет horror red/black.
WCAG: белый на `#111111` и маджента на `#111111` проходят для large type.

## Typography & Readability

- Хук читается за **2 секунды** на thumbnail (~200 px).
- Headline: тяжёлый белый гротеск. Одна идея на панель.
- Body: 1–3 короткие строки. Decoder (05) и чеклист (06) — стек;
  всё внутри safe area.
- CTA: **огромное** рукописное маджента **ОНЛАЙН** — самое большое
  слово на холсте.
- Тип может быть за и перед объектами, но никогда через gutter.
- Только verbatim. Нет слова «Сцена». Нет водяных знаков.

## Slide Rhythm

```text
01 hook scene     кот + светящийся экран сторис / висящий чат
02 problem        пёс ждёт у телефона, который не для неё
03 mistake        пёс + плашки оправданий («просто занят»)
04 mechanism      сова видит орбитальный поводок за 0 усилий
05 save decoder   сова: иллюзия внимания vs реальность
06 save checklist кот: 3 признака «ты лишь зритель»
07 save framework сова: Суть – Тень – Вектор
08 recap          кот отворачивается от экрана — просмотр ≠ поступок
09 CTA            огромный маджента ОНЛАЙН + телефон / app UI
```

Продукт на 09: аудиоразбор **в моём приложении**. Суть – Тень – Вектор.
Не бот. Не «3 бесплатных расклада». Не сырой URL.

## Animals (this pack)

| Slide | Animal | Metaphor |
|-------|--------|----------|
| 01 | cat | интуиция чует неладное при взгляде на экран |
| 02 | dog | преданность безответному ожиданию у экрана |
| 03 | dog | ловушка надежды и поиска скрытых смыслов |
| 04 | owl | ночная ясность и вскрытие скрытого мотива |
| 05 | owl | трезвое различение фактов и фантазий |
| 06 | cat | чутьё распознает скрытую манипуляцию |
| 07 | owl | мудрость глубокой трансформации |
| 08 | cat | возвращение себе автономии и гордости |
| 09 | — | объект: телефон / UI приложения |

Животные сидят **в сцене**, не как die-cut стикеры с белым ореолом.
Style-lock sticker-halo **не заимствовать**.

## Slide 9 object (no person)

Огромное рукописное **ОНЛАЙН** `#ff006e`. Рядом — тёмный смартфон
с интерфейсом приложения / светящимся экраном. Можно тонкий золотой
медальон ТАРО / СЕЙЧАС, если садится нативно. Нет женщины. Нет ведущей.
Нет микрофона. Нет животного.

## Do's and Don'ts

**Do**

- `face_lock: none`. Сцена + тип + животное / объект.
- Животные-метафоры на слайдах, где их назвал copy.
- Тонкие белые швы. Автономные ячейки. Verbatim-копия.
- Огромный маджента **ОНЛАЙН** на слайде 9 + телефон / app.
- Style lock только как палитра / ритм.

**Don't**

- i2i `Виктория.png` / `viktoriaref.png` / `victoria-sheet.png` /
  `victoria.png` / Alena / style-lock как лицо.
- Любое женское лицо, ведущая, presenter, микрофон у рта.
- Белый ореол / die-cut вокруг животных.
- Horror, черепа, кровь, стекающие свечи, ouija.
- Португальский текст, чужие лица, чужие бренды, подпись Victoria.
- Приз бота, «3 бесплатных расклада», сырые URL, слово «Сцена».
- Триггеры прошлых паков: ШАГ / STEP / ПАУЗА / PAUSE / ТЕПЛО /
  WARMTH / ПРОЧИТАНО / СТАТУС / STATUS / LABELS / СУББОТА / WEEKEND.
- Копировать live СУББОТА / noface-rebuild / EN WEEKEND.
- Писать Kie JSON (это image-prompter) или генерировать пиксели.
