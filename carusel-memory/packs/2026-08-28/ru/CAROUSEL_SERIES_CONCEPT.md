# Series Concept — Тепло – холодно / Hot & Cold

**carousel_family:** `animals_viktoria_collage`  
**pack:** 2026-08-28 · run `2026-08-28-1110`  
**lang:** ru primary + EN pair (одна визуальная семья)  
**product:** `app_audio` (не публиковать)  
**триггеры:** `ТЕПЛО` / `WARMTH`

Машинный lock: `CAROUSEL_SERIES_CONCEPT.json` (включая полный `prompt_hints`).

## Что фиксирует серия

| Слой | Lock |
|------|------|
| Семья | `animals_viktoria_collage` ∈ registry |
| Сетка | 3×3, 9 панелей, каждая 3:4, master 3:4 @ 4K |
| Швы | тонкие белые gutters, Excalibur `seam` |
| Палитра | `#111111`–`#1a1a1a` + `#ff006e` + `#ffffff` + soft gold |
| Лицо | Victoria, только `victoria-sheet.png` (лицо + волосы) |
| Волосы | тёплый honey/wheat + тёмные корни. Platinum = P0 |
| Одежда | новая: 01 burgundy turtleneck; 09 black satin wrap. Не cami+jeans, не ivory blazer |
| Животные | кот 01, пёс 02, сова 04 (≥3, с работой) |
| Save | рамки на 05, 06, 07 |
| CTA | comment trigger → аудиоразбор в приложении: Суть – Тень – Вектор / Essence–Shadow–Vector |
| Copy | verbatim Gemini; RU `CAROUSEL_SLIDE_COPY.json`; EN `design/en/CAROUSEL_SLIDE_COPY.json` |

## Двуязычность

Один дизайн, два текстовых слоя. EN не меняет композицию, животных, одежду, палитру. Меняются только quoted strings.

Этот run: `slide_01 = static_png`. Motion/animate skip. Композиция 01 всё равно motion-safe.

## Что не пишет этот шаг

- `CAROUSEL_IMAGE_PROMPT.json` — `carusel-image-prompter`
- пиксели / Kie — `carusel-slice`
- публикация — запрещена (`publish_requested: false`)
