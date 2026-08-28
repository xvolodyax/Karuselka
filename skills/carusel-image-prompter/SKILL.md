---
name: carusel-image-prompter
description: Сборка русского промпта для Kie.ai — один master 3:4 @ 4K с сеткой 3×3 (9 панелей).
---

# Carusel Image Prompter

## Роль

**Единственный агент**, который пишет **финальный промпт** для **одного** изображения Kie: master **3:4 @ 4K** с **9 панелями** (сетка 3×3).

Не генерирует картинку. Не режет слайды. Не пишет caption для Instagram.

## Вход

- `carusel-memory/00-brief.md` — тема, референс, бренд
- `carusel-memory/research/carousel-research-dossier.md`
- `carusel-memory/design/CAROUSEL_SLIDE_COPY.json` — смысл **9** слайдов
- `carusel-memory/design/CAROUSELDESIGN.md`
- `carusel-memory/design/CAROUSEL_SERIES_CONCEPT.json`
- `carusel-memory/design/CAROUSEL_SOURCE_DECOMPOSITION.json`
- `carusel-memory/design/CAROUSEL_SLIDE_BLUEPRINTS.json`
- `shared/carousel-professional-playbook.md`

## Выход (обязательно)

```text
carusel-memory/design/CAROUSEL_IMAGE_PROMPT.md   # human: логика, style lock
carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json  # machine: для kie_run_prompt.py
```

Fragment: `carusel-memory/fragments/image-prompter.md`

## CAROUSEL_IMAGE_PROMPT.json — схема

```json
{
  "version": "2",
  "generation_mode": "grid_3x3",
  "model": "gpt-image-2-image-to-image",
  "prompt": "Одно изображение: 9 равных панелей 3×3, каждая 3:4, стиль как референс...",
  "negative_prompt": "...",
  "input_urls": [
    "https://HTTPS_VICTORIA_SHEET_CLOSEUP"
  ],
  "slice_method": "seam",
  "face_lock": "victoria-sheet.png",
  "aspect_ratio": "3:4",
  "resolution": "4K",
  "grid": { "cols": 3, "rows": 3, "order": "row-major", "gutters": "thin_white_seams" },
  "animate_slide": 1,
  "reference_contract": {
    "reference_role": "style + layout reference",
    "preserve": ["..."],
    "change": ["..."],
    "do_not_borrow": ["..."]
  },
  "style_lock": { ... },
  "prompt_compaction": {
    "active_prompt_max_chars": 4500,
    "details_in_structured_fields": true
  },
  "typography_rules": {
    "exact_text": true,
    "no_extra_text": true,
    "hierarchy": "headline > short body > pill"
  },
  "panel_visual_brief": [
    { "slide": 1, "role": "hook", "visual_only": "..." },
    ...
    { "slide": 9, "role": "cta", "visual_only": "..." }
  ]
}
```

Контракт: `shared/carousel-grid-design.md`, `shared/carousel-seam-slice-contract.md`, `shared/victoria-identity-lock.md`.

## Правила промпта (русский)

1. **Одно** изображение — **9 панелей** в сетке **3×3**, каждая **3:4**. НЕ horizontal strip. НЕ 2×3 если brief требует 3×3.
2. **Стиль = референс** (UNILIBRE-style grid или brief).
3. Панель 1 — статичный PNG, как остальные. Не помечать slide-01 как motion-safe video.
4. Каждый текст, который должен быть на изображении, брать из `CAROUSEL_SLIDE_COPY.json` и писать в кавычках.
5. Обязательно добавить: `verbatim text, no substitutions, no extra labels, no duplicate text`.
6. Промпт должен явно разделять **preserve / change / do_not_borrow**.
7. Не генерировать generic prompt. Если в `prompt` нет 9 панелей 01-09 — fragment `❌ BLOCKER`.
8. **SHORT Kie prompt:** активное поле `prompt` ≤2200 символов (target 900–1800). **Face lock first.** Длинный MUST/collage/type/wardrobe essay (3000+) морит лицо. Детали — в `style_lock`, `reference_contract`, `panel_visual_brief`.
9. **Один i2i файл:** обрезать крупный фронтальный портрет слева с `victoria-sheet.png` (`scripts/crop_victoria_sheet_tight.py`). Залить **только этот кроп** как `file_name=victoria-sheet.png`. Не слать всю 12-up сетку. Не слать `animals-viktoria-style-lock.png`.
10. Если Kie i2i возвращает повторный `400 Internal Error` на 3:4 @ 4K при валидном reference URL — сначала сделать compact prompt retry, не менять aspect/resolution без явного разрешения.

## Сборка промпта (шаблон)

```
[FACE FIRST]
Same woman as the attached sheet: green eyes with a slight hazel/light-brown mix,
warm honey-wheat blonde with darker roots. Not Alena. Not platinum.

[GRID + STYLE — one short block]
One Instagram carousel master, 3:4 @ 4K, exact 3×3, thin white gutters at 1/3
and 2/3 (Excalibur seam cut). Charcoal #111–#1a, white type, magenta #ff006e,
gold #c9a86a. Fashion collage. Victoria on 1 and 9 only. New clothes, not
sheet tank+jeans. Safe margin ≥10–12% from seams.

[PANEL FLOW — row-major 1..9, short]
Panel 1: new wardrobe + pose; exact headline "..."; exact body "..."
...
Panel 9: different new wardrobe; exact CTA from copy (app audio, not bot).

[TYPOGRAPHY]
Verbatim text only; no extra labels; no sticker/cutout/halo in the positive.
```

## Compact prompt contract

- `prompt` — короткая активная инструкция: **лицо первым**, сетка, 9 коротких panel lines с verbatim copy.
- Подробный разбор референса, decomposition, rationale — в структурные поля JSON и `CAROUSEL_IMAGE_PROMPT.md`.
- Перед handoff записать `prompt_compacted: true|false`, `prompt_char_count`.
- `prompt_char_count > 2200` для активного Kie `prompt` = `❌ BLOCKER`. 3631-char collage novel = FAIL.

## Разделение с designer

| carusel-designer | carusel-image-prompter |
|------------------|------------------------|
| CAROUSELDESIGN, decomposition, blueprints | **Финальный русский prompt** для Kie |
| Визуальный контракт | `CAROUSEL_IMAGE_PROMPT.json` |
| Style scorecard | `panel_visual_brief` per slide |

## Handoff block

```text
=== CARUSEL-IMAGE-PROMPTER ===
Статус: ✅ OK | ❌ BLOCKER
Prompt: carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json
aspect_ratio: 3:4 | resolution: 4K
input_urls: 1 URL | BLOCKER: need HTTPS reference
incident_report: none
```

## Blocker

Если brief даёт локальный референс:

1. Сначала пробуй `KieFileUploadClient.upload_stream()`.
2. Если stream upload даёт multipart/boundary ошибку — используй `upload_base64()` для файла ≤10MB.
3. Запиши метод в `reference_upload_method`.

Если HTTPS URL всё равно нет — `❌ BLOCKER` в fragment + incident в `pipeline-fix-queue.md`.

## Конец задачи

`shared/subagent-end-of-task-contract.md`
