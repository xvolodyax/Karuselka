# CAROUSEL_IMAGE_PROMPT — Тепло – холодно

written_by: carusel-image-prompter
lang: ru
visual_family / carousel_family: `animals_viktoria_collage`
generation_mode: `grid_3x3`
model: `gpt-image-2-image-to-image`
aspect_ratio: `3:4`
resolution: `4K`
face_lock: `victoria-sheet.png`
slice_method: `seam`
prompt_compacted: true
prompt_char_count: 3631
reference_upload_method: `upload_stream`
input_urls[0]: `https://tempfile.redpandaai.co/kieai/378019/carusel-face-lock/victoria-sheet.png`
product: `app_audio`
trigger: ТЕПЛО
this_run_slide_01: static_png

Machine JSON: `carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json`
Copy source: `carusel-memory/design/CAROUSEL_SLIDE_COPY.json` — verbatim only.

## Style lock

Fashion-collage на антраците, не horror и не бежевый lifestyle.

| Role | Hex |
|------|-----|
| background | `#111111`–`#1a1a1a` |
| type | `#ffffff` |
| accent | `#ff006e` |
| metal | `#c9a86a` |

Тяжёлый белый гротеск. Тонкий маджента-скрипт / рваные плашки только для слов из copy. Тип живёт внутри сцены. Safe margin ≥10–12% от всех швов и краёв ячейки. Текст не у нижнего края.

## Reference contract

| File | Role |
|------|------|
| `image-851e.png` / animals_viktoria_collage | style + layout + palette — описаны текстом, не i2i |
| `carusel-memory/references/victoria-sheet.png` | ONLY face + hair lock → `input_urls[0]` |

**Preserve:** тёмный холст, маджента + белый тип, рваные плашки, животные-метафоры, Виктория на 1+9, 3×3 с тонкими белыми gutters.

**Change:** сюжет суббота/вторник, дословный copy, телефон, фазы Тепло/Холод, Говорит/Слышишь, 3 правила, одежда этого пака, CTA ТЕПЛО + аудиоразбор в приложении.

**Do not borrow:** португальский, чужие лица, Alena, platinum, horror-стол, слово «Сцена», бот, 3 бесплатных расклада, URL, подпись Victoria.

Запретные виды (white cami+jeans, ivory blazer, sticker/cutout/halo) — только в `negative_prompt`, не в positive.

## Face + wardrobe (this pack)

Виктория только на слайдах 1 и 9. Та же женщина. Глаза зелёные с лёгким hazel. Тёплый медово-пшеничный блонд, тёмные корни как на `victoria-sheet.png`. Не осветлять.

- **Slide 1 (NEW):** бордовая водолазка, золотые хупы. Сидит 3/4 к светящемуся телефону.
- **Slide 9 (NEW, другая поза):** чёрная атласная запашная блузка, тёмные брюки, стоит hip-lean, телефон как будто пишет комментарий.

Короткая identity-строка в Kie prompt. Без face essay.

## Animals

| Slide | Animal | Job |
|-------|--------|-----|
| 1 | cat | чуешь: резкая смена температуры контакта |
| 2 | dog | верность неотвеченному вопросу у экрана |
| 4 | owl | ночные мысли, ясное видение механизма |

Нет животных на 3, 5–9. Нет Виктории на 2–8.

## Verbatim panel copy

Из `CAROUSEL_SLIDE_COPY.json`. Не подменять.

1. hook — «В субботу он смотрел в глаза» / «и строил планы на осень. Во вторник — сухое «занят» и три дня тишины.» / скрипт «Тепло – холодно»
2. pain — «Ты ищешь, где ошиблась» / «Перечитываешь переписку. Пугает не пауза, а перепад: от полного тепла до ледяной стены.»
3. mistake — «Ловушка — греть сквозняк» / «Думаешь: «он испугался чувств». Начинаешь проявлять заботу в ответ на холод, закрепляя качели.»
4. mechanism — «Прерывистое подкрепление» / «Непредсказуемость держит нервную систему в напряжении. Мозг путает тревогу с сильной любовью.»
5. save A — «Тепло vs Холод: две фазы» / «Тепло: ему нужен твой ресурс и внимание» / «Холод: маячит близость и ответственность»
6. save B — «Говорит vs Слышишь» / «Говорит: «Сейчас завал, не хочу усложнять»» / «Слышишь: «Я должна согреть его и подождать»» / «Реальность: «Беру тепло без обязательств»»
7. save C — «3 правила возвращения опоры» / «1. Суди по средней температуре, не по пикам» / «2. Сделал шаг назад — оставайся на месте» / «3. Не грей человека, выбравшего холод»
8. recap — «Ясность вместо дежурства» / «Отношения строятся на стабильности, а не на качелях. Твой человек не заставит гадать о своих чувствах.» / «Ясность сейчас»
9. cta — «Напиши ТЕПЛО» / «Аудиоразбор в приложении. Суть – Тень – Вектор.» / «Слово ТЕПЛО в комментариях». Крупный маджента-скрипт **ТЕПЛО**. Не бот.

## Grid

Один master, 3:4 @ 4K, `generation_mode: grid_3x3`, `slice_method: seam`. Row-major 01 02 03 / 04 05 06 / 07 08 09. Тонкие белые gutters на 1/3 и 2/3; код режет по швам. Каждая ячейка — самостоятельная панель 3:4. Панель 1 motion-safe (свечение, микрожест кота; тип неподвижен). Этот run: slide-01 = static PNG.

## Negative (Kie)

platinum, Alena, white cami, jeans from sheet, ivory blazer, cutout, die-cut, sticker outline, white halo, слово «Сцена», 3 free readings — полный список в JSON.

## Handoff

Промпт готов. Не генерировать canvas. Не резать. Next: **slice**.
