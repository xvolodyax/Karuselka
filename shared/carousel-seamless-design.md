# Carusel — Seamless Instagram Carousel Design (LEGACY)

> Deprecated for default Carusel runs. Current production format is
> `shared/carousel-grid-design.md`: one Kie master, grid 3×3, 9 panels.
> Use this file only if the user explicitly asks for legacy horizontal seamless panorama.

Правила бесшовной карусели из 6 слайдов для Instagram Feed.

## Размеры

| Элемент | Размер |
|---------|--------|
| Один слайд | **1080 × 1350 px** (4:5) |
| Master canvas | **6480 × 1350 px** (6 × 1080) |
| Safe margin | **64 px** от краёв и от линий нарезки |
| Формат экспорта | PNG, sRGB |

## Линии нарезки (X)

Нарезать master по вертикали на:

```text
x = 0, 1080, 2160, 3240, 4320, 5400, 6480
```

Слайды: `slide-01.png` … `slide-06.png` (слева направо).

## Seamless continuity

Элементы, которые **должны** пересекать границы слайдов:

- горизонтальный градиент фона
- крупный объект (телефон, персонаж, продукт)
- вертикальная линия-якорь
- фоновая текстура
- крупный заголовок, раскрываемый при свайпе (осторожно: не резать буквы на seam)

**Запрещено** на линии нарезки (±64 px):

- лица людей
- ключевые слова заголовка
- логотип целиком
- CTA-кнопка

## Нарратив 6 слайдов

| Slide | Роль | Задача |
|-------|------|--------|
| 1 | Hook | Остановить скролл, интрига, крупный заголовок |
| 2–5 | Value | Один тезис на слайд, плотная польза |
| 6 | CTA | Подписка, ссылка, DM, «сохрани» |

## Визуальные якоря серии

На всех 6 слайдах фиксировать:

- палитру (1 primary + 1–2 accent)
- шрифтовую пару (кириллица: см. aura-cyrillic-google-fonts)
- стиль нумерации (pill 1/6 … 6/6)
- grain/текстуру (если в референсе)
- направление света

## Референс → репликация

1. Разобрать референс по слайдам → `CAROUSEL_SOURCE_DECOMPOSITION.json`.
2. Выбрать `carousel_family` из registry.
3. Зафиксировать series lock в `CAROUSEL_SERIES_CONCEPT.json`.
4. Собрать master 6480×1350 (генерация wide API или композит).
5. Нарезать `scripts/slice_carousel.py`.
6. Проверить seams в guardian (visual diff на границах).

## Phase 2: wide image API

Когда пользователь даст API wide-генерации:

- промпт собирается: `global_prompt_prefix` + `topic_scene` + `global_prompt_suffix`
- целевой размер: 6480×1350 или API-native с последующим resize
- после генерации — тот же slicer

## Phase 3: video на slide 1

- `output/video/slide-01.mp4` заменяет `slide-01.png` в `file1` при publish
- slides 2–6 остаются PNG
- первый файл задаёт aspect ratio всей карусели в Instagram
