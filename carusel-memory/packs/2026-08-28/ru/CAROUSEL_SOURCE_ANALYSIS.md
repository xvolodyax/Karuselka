# Source Analysis — animals_viktoria_collage × Тепло / холодно

Разбор как арт-директор. Референс = закон. Тема адаптируется после decomposition.

## 1. Роли референсов

| Файл | Роль | Что брать | Что не брать |
|------|------|-----------|--------------|
| `image-851e.png` | style + layout + mood | антрацит, `#ff006e`, коллаж, sans+script, животные | PT текст, чужие лица, логотипы плиты |
| `victoria-sheet.png` | face + hair only | овал лица, honey/wheat + darker roots, green-hazel | одежда (white cami+jeans), поза листа |
| `slide-04.png` | content inspiration | глубина «говорит / слышишь / урок» | визуальная семья, старый headline |
| `victoria.png` | FORBIDDEN | — | Alena |
| `cover-old.png` | RETIRED | — | ivory blazer cutout |

Style lock описывается текстом. Не класть `image-851e` в `input_urls`: плита — стикер-коллаж, модель скопирует ореолы. Единственный i2i вход — `victoria-sheet.png`.

## 2. Что сохраняем (preserve)

Тёмное поле, magenta heat, белый гротеск, тонкий script, torn-tape pills, Victoria на hook+CTA, животное как эмоция слайда, 3×3 с белыми швами, безопасные 10–12%, высокий контраст для thumbnail.

## 3. Что меняем (change)

Сюжет суббота→вторник. Locked copy RU/EN. Новая одежда/поза Виктории. Объекты: телефон, фазы, матрица восприятия, чек-лист. Триггер `ТЕПЛО`/`WARMTH`. Продукт — три pill-а приложения, не UI бота.

## 4. Что нельзя брать (do_not_borrow)

Чужие лица, Alena, platinum, cami+jeans с листа, ivory blazer, португальский, horror-стол, слово «Сцена», бот-приз, Academy, URL, watermark, подпись Victoria, die-cut halo.

## 5. Карта архетипов 01–09

См. `CAROUSEL_SOURCE_DECOMPOSITION.json` → `panel_archetype_map`. Кратко: 01/09 герой; 02/04 тип+животное; 03 pills; 05–07 рамки; 08 recap+медальон.

## 6. Thumbnail test (slide 01)

За 2 секунды: лицо Victoria + кот + белая сцена про субботний взгляд + magenta «Тепло – холодно» + холод экрана. Не название механики.

## 7. Save test

05 (две фазы), 06 (говорит/слышишь/реальность), 07 (3 правила) — карточки с рамкой. Их будут скриншотить.

## 8. Риски для prompter

- Кириллица в мелких pills → держать коротко, verbatim в кавычках.
- Hair drift в platinum → явный hair lock + negative.
- Животные как наклейки → прописать job в сцене.
- Швы: thin white gutters; не zero-gutter.
