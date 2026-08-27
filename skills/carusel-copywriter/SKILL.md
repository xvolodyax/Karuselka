---
name: carusel-copywriter
description: Копирайт 9 слайдов Instagram-карусели (grid 3×3) + caption.
---

# Carusel Copywriter

**Model:** `gemini-3.7-flash-high`. Caption is THIS step — there is no separate caption worker.
Spawn: `Task(carusel-copywriter)` or cloud `Task(generalPurpose, model=gemini-3.7-flash-high)`.
Stamp `written_by: gemini` on `CAROUSEL_SLIDE_COPY.json`, `CAROUSEL_CAPTION.json`, `CAROUSEL_CAPTION.md`, and the fragment.
Director / Opus / Sonnet / Composer must not write these files. Do not restyle Gemini’s voice.
See `shared/swarm-spawn-contract.md`.

## Вход

- `carusel-memory/00-brief.md`
- `carusel-memory/research/carousel-research-dossier.md`
- `shared/carousel-professional-playbook.md`
- `shared/taro-seichas-canon.md` **обязательно**
- `shared/locale-brand-contract.md`
- `shared/caption-format-contract.md`

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
3. Построй 9-panel **teaching** arc (не vibe-список):
   - 01 hook **SCENE** — первая строка = сцена («Он смотрит сторис. Третью неделю.»), не название механики
   - 02 pain
   - 03 mistake — как клиентка слышит приговор
   - 04 mechanism — чем пауза является
   - 05–07 save — минимум **два** с реальной рамкой / вопросами / «говорит vs слышишь»
   - 08 recap / decision rule
   - 09 CTA — одно слово-триггер, один продукт
4. Каждая value-панель = **одна идея**. Пустой вайб без урока = FAIL.
5. Панели save: чеклист, 3 вопроса, «говорит/слышишь», 3 состояния — не цитаты настроения.
6. CTA = comment trigger (`ПАУЗА` / `PAUSE`) + один продукт (бот **или** приложение). Не мешать. Не «личный аудиоразбор». EN: без Academy.
7. Простой разговорный язык. Не целиться в 13–17. Не пугать одиночеством.

## CAROUSEL_SLIDE_COPY.json — 9 slides

```json
{
  "hook_options": [
    { "framework": "pain", "headline": "...", "why_it_swipes": "..." }
  ],
  "hook_rationale": "...",
  "hook_is_scene": true,
  "visual_family": "animals_viktoria_collage",
  "trigger_word": "ПАУЗА",
  "product": "bot_three_spreads",
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

Следуй `shared/caption-format-contract.md`:

- `full_caption` ≤ 2200 chars
- hashtags ≤ 30
- mentions ≤ 20

## Handoff

```text
=== CARUSEL-COPYWRITER ===
Статус: ✅ OK
Slides: carusel-memory/design/CAROUSEL_SLIDE_COPY.json
Caption chars: N
incident_report: none
```

## Конец задачи

`shared/subagent-end-of-task-contract.md`
