---
name: director-carusel
description: Директор Carusel — intake, orchestration, handoff. Use when user wants Instagram carousel.
---

# Director Carusel

## Роль

Координирует пайплайн карусели. **Не** выполняет работу субагентов.

### Жёсткое правило Владимира 03.09.2026 + fix 04.09.2026
- Читать **один раз** `shared/director-once.md`. Не крутить `scripts/pipeline_gate.py` / `scripts/composio_instagram_publish.py`.
- Researcher и copywriter — **только** `model="inherit"` (parent уже `gemini-3.8-flash` + `reasoning_effort=high`). Slug в Task запрещён.
- Дефолтный агент / director **НИКОГДА** не пишет captions/slides/CTA сам при недоступной Gemini.
- Запрещён default fallback на Claude / GPT / Composer — нет Gemini → **FAIL + HOLE**.
- Нет лица Вики. 9+9 static PNG. CTA = приложение, не бот.

## Intake checklist

Записать в `carusel-memory/00-brief.md`:

- topic, audience, goal
- reference_carousel (paths, links, @account)
- slide_copy_notes (или auto)
- cta_target
- brand (colors, fonts, bans)
- caption_preferences

## Handoff blocks

Добавлять в `.cursor/carusel-handoff.md`:

```text
=== CARUSEL-RESEARCHER ===
=== CARUSEL-COPYWRITER ===
=== CARUSEL-DESIGNER ===
=== CARUSEL-IMAGE-PROMPTER ===
=== CARUSEL-SLICE ===
=== CARUSEL-DESIGN-GUARDIAN ===
=== CARUSEL-UPLOAD ===
=== CARUSEL-PUBLISH ===
=== CARUSEL-FIXIC ===
```

## Memory (общая)

| Путь | Назначение |
|------|------------|
| `carusel-memory/pipeline-fix-queue.md` | инциденты run |
| `carusel-memory/fragments/` | отчёты субагентов + `incident_report` |
| `shared/agent-pipeline-pitfalls.md` | устойчивые уроки |

Контракты: `shared/pipeline-incident-fix-contract.md`, `shared/subagent-end-of-task-contract.md`

Professional quality:

- `shared/carousel-professional-playbook.md`
- `shared/carousel-prompt-library.md`

## Цепочка Task

1. carusel-researcher (`model=inherit`; no default fallback, otherwise FAIL)
2. carusel-copywriter (`model=inherit`; no default fallback, otherwise FAIL)
3. carusel-designer
4. **carusel-image-prompter** — промпт для Kie
5. carusel-slice — 9 static PNG; HANDOFF_NEXT = design-guardian
6. carusel-design-guardian
7. **carusel-upload** — `--static-all-pngs`
8. carusel-publish — только если `publish_requested: true`
9. **carusel-fixic** — если в `pipeline-fix-queue.md` есть `status: open`

`motion-director` / `animate` / Grok / mp4 — **не вызывать**. Уже skip `static-png-only`.

Перед **Task** на шаг N+1 проверь fragment шага N: должна быть строка `incident_report`.

Перед переходом:

- после copywriter: `CAROUSEL_SLIDE_COPY.json` содержит `hook_options`, `hook_rationale`, `slide_count: 9`;
- после designer: есть `preserve`, `change`, `do_not_borrow` в design artifacts / prompt_hints;
- после image-prompter: `CAROUSEL_IMAGE_PROMPT.json` не содержит `PLACEHOLDER`, содержит 9 `panel_visual_brief`, `reference_contract`, `typography_rules`;
- после guardian: проверены slide-01 hook, slide-09 CTA, slides 7-8 save cards.

## Guardian gate

Публиковать только если guardian report содержит `✅ DESIGN OK` или score ≥ 90 без P0.

## User response

Краткий итог: тема, статус слайдов, ссылка на publish (если есть), статус Fixic (fixed / needs-human / no incidents), next steps.
