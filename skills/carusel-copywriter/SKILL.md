---
name: carusel-copywriter
description: Копирайт 9 слайдов Instagram-карусели (grid 3×3) + caption.
---

# Carusel Copywriter

## Вызов

Только отдельный Task. Director не пишет слайды сам.  
`lang=ru|en`. Handle: `@todaytaro_ru` / `@todaytaro_bot`.  
`@todaytaro_bot` — Telegram bot, не приложение.  
Без сырых URL. CTA: «ссылка в шапке» / «link in bio».  
9 слайдов, grid 3×3. Fragment: `dispatched_via`, `dispatch_id`, `HANDOFF_NEXT: designer`.

Читай `shared/locale-brand-contract.md`.

## Вход

- `carusel-memory/00-brief.md`
- `carusel-memory/research/carousel-research-dossier.md`
- `shared/carousel-professional-playbook.md`

## Выход

- `carusel-memory/design/CAROUSEL_SLIDE_COPY.json`
- `carusel-memory/design/CAROUSEL_CAPTION.md`
- `carusel-memory/design/CAROUSEL_CAPTION.json`

Fragment: `carusel-memory/fragments/copywriter.md`

## Лимиты (панель 3:4, grid preview)

| Zone | Slides | Max chars headline |
|------|--------|-------------------|
| hook | 1 | 50 |
| value | 2–8 | 45 |
| cta | 9 | 40 + 30 sub |

## Professional copy process

1. Напиши **5 вариантов hook** до выбора финального:
   - pain
   - contrarian
   - mistake
   - mechanism
   - specific result / number
2. Выбери один hook и объясни в JSON `hook_rationale`: почему он создаёт information gap.
3. Построй 9-panel arc:
   - 01 hook
   - 02 problem
   - 03 hidden cost / mistake
   - 04 mechanism
   - 05 proof / number
   - 06 flow / steps
   - 07 save checklist
   - 08 recap / decision rule
   - 09 CTA
4. Каждая value-панель = **одна идея**.
5. Панели 7-8 должны быть save-worthy: чеклист, decision tree, короткий framework.
6. CTA на slide 9 = один action: сохранить / подписаться / отправить команде. Не просить 5 действий сразу.

## CAROUSEL_SLIDE_COPY.json — 9 slides

```json
{
  "hook_options": [
    { "framework": "pain", "headline": "...", "why_it_swipes": "..." }
  ],
  "hook_rationale": "...",
  "slide_count": 9,
  "grid": { "cols": 3, "rows": 3 },
  "slides": [
    { "index": 1, "role": "hook", "headline": "...", "body": "", "notes": "animate; readable under 2 sec" },
    { "index": 2, "role": "problem", "headline": "...", "body": "...", "notes": "" },
    ...
    { "index": 9, "role": "cta", "headline": "...", "body": "...", "cta": "..." }
  ],
  "save_value": ["slide-07 checklist", "slide-08 recap"]
}
```

## Caption

Следуй `shared/caption-format-contract.md` и `shared/locale-brand-contract.md`:

- `full_caption` ≤ 2200 chars
- hashtags ≤ 30
- mentions ≤ 20, обязательно `@todaytaro_ru` или `@todaytaro_bot` по `lang`
- никаких `https://`, `t.me/`, `instagram.com/` в caption и на слайдах
- EN: пиши bot / Telegram bot, не app

## Handoff

```text
=== CARUSEL-COPYWRITER ===
Статус: ✅ OK
dispatched_via: Task(carusel-copywriter) | Task(generalPurpose)
dispatch_id: <from pipeline_gate>
lang: ru|en
handle: @todaytaro_ru | @todaytaro_bot
Slides: carusel-memory/design/CAROUSEL_SLIDE_COPY.json
Caption chars: N
incident_report: none
HANDOFF_NEXT: designer
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
