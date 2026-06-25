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
  "input_urls": ["https://HTTPS_REFERENCE"],
  "aspect_ratio": "3:4",
  "resolution": "4K",
  "grid": { "cols": 3, "rows": 3, "order": "row-major" },
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

Контракт: `shared/carousel-grid-design.md`

## Правила промпта (русский)

1. **Одно** изображение — **9 панелей** в сетке **3×3**, каждая **3:4**. НЕ horizontal strip. НЕ 2×3 если brief требует 3×3.
2. **Стиль = референс** (UNILIBRE-style grid или brief).
3. Панель 1 — **motion-friendly** (оживляется Grok).
4. Каждый текст, который должен быть на изображении, брать из `CAROUSEL_SLIDE_COPY.json` и писать в кавычках.
5. Обязательно добавить: `verbatim text, no substitutions, no extra labels, no duplicate text`.
6. Промпт должен явно разделять **preserve / change / do_not_borrow**.
7. Не генерировать generic prompt. Если в `prompt` нет 9 панелей 01-09 — fragment `❌ BLOCKER`.
8. **Compact Kie prompt:** активное поле `prompt` держать ≤4500 символов (target 2800–4200). Детальные данные хранить в `style_lock`, `reference_contract`, `typography_rules`, `panel_visual_brief`, а не раздувать `prompt`.
9. Если Kie i2i возвращает повторный `400 Internal Error` на 3:4 @ 4K при валидном reference URL — сначала сделать compact prompt retry, не менять aspect/resolution без явного разрешения.

## Сборка промпта (шаблон)

```
[STYLE LOCK from reference]
One Instagram carousel master image, grid 3×3, exactly 9 equal cells,
each cell is a standalone vertical panel, brand-consistent but NOT a horizontal seamless strip,
[style: carousel_family], palette [colors], [typography], [lighting direction].

[REFERENCE CONTRACT]
Reference role: style + layout reference.
Preserve: [palette], [grid], [typography hierarchy], [spacing], [panel archetypes].
Change: [topic], [objects], [copy], [CTA], [domain metaphors].
Do not borrow: [original logos], [people], [mascot], [brand name], [accidental text].

[PANEL FLOW — row-major 1..9]
Panel 1 (hook, motion-safe): exact headline "..."; visual zones ...
Panel 2-8 (value/save): exact headline "..."; short body "..."; visual zones ...
Panel 9 (cta): exact headline "..."; exact CTA "..."; visual zones ...

[TYPOGRAPHY]
Verbatim text only; no substitutions; no extra labels; no duplicate text.
Headline dominant, body smaller, pills tiny but legible. High contrast.

[GRID RULES]
Master aspect ratio 3:4, resolution 4K. 3 columns × 3 rows; zero visible gutters;
each resulting cell is a standalone 3:4 vertical panel. Cells touch edge-to-edge:
no white dividers, no borders, no whitespace, no outer frame. Use invisible cut
lines at 1/3 and 2/3 only; full-bleed background reaches every cell edge.
Objects and key text stay inside each cell; no 2×3 grid; no 6-panel horizontal
strip; consistent style across all 9 panels.
**Safe margin:** all headline/body/pills must stay **≥10–12% away from every
imaginary cut line and cell edge**. Do not place text near the bottom edge.

[NEGATIVE]
wrong number of panels, horizontal strip, 2x3 grid, visible gutters, white borders, outer frame, watermark, blurry, inconsistent styles.

[TOPIC]
Adapt scene for: {topic from brief}
```

## Compact prompt contract

- `prompt` — только активная инструкция для Kie: стиль, reference contract, grid, 9 коротких panel lines, typography, negative.
- Подробный разбор референса, decomposition, rationale, длинные списки объектов и альтернативы — в структурные поля JSON и `CAROUSEL_IMAGE_PROMPT.md`.
- Перед handoff записать `prompt_compacted: true|false`, `prompt_char_count`, `prompt_compacted_reason` если был retry после Kie 400.
- `prompt_char_count > 4500` для активного Kie `prompt` = `❌ BLOCKER`, пока не compacted.

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
