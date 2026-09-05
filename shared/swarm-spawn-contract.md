# Swarm spawn contract

Director **только оркестрирует**. Каждый worker — отдельный **Task**.
Тихо сделать шаг в родительском чате = сломанный пайплайн.

Машина: `shared/pipeline-steps.json` + `python scripts/pipeline_gate.py`.
Не изобретать 13-го агента.

## Почему пустые красивые посты

Гипотеза (подтверждена): Director пропустил researcher+copywriter и прыгнул к vibe-пикселям.
PR #2/#3 зафиксировали только pipeline, не pack. Live 27.08 = empty pretty.
Цепочка должна быть **11 worker records**, не один агент «я теперь копирайтер».

## 12 шагов (11 worker records)

```text
director (parent intake)
  → researcher          Task + Gemini     written_by: gemini
  → copywriter          Task + Gemini     slides AND caption; written_by: gemini
  → designer            Task              layout/style only
  → image-prompter      Task              prompts from locked copy; no face ref
  → slice               Task          HANDOFF_NEXT=design-guardian
  → motion-director     SKIP at init  static-png-only (do not dispatch)
  → animate             SKIP at init  static-png-only (do not dispatch)
  → design-guardian     Task
  → upload              Task
  → publish             SKIP unless brief.publish_requested true
  → fixic               SKIP unless open incidents
```

Cloud не видит `Task(carusel-*)`. Sanctioned spawn:

`Task(generalPurpose)` **на один шаг**, промпт из `pipeline_gate.py dispatch-prompt`.

Desktop plugin: `Task(carusel-<role>)`. Один Task = один шаг. `inline`/`parent`/`self` = FAIL.

Publish по умолчанию `skip: publish-not-requested`. Не Instagram / Composio / Make.

## Весь человеческий текст = Gemini (Правило Владимира 03.09.2026 + fix 04.09.2026)

Vladimir: «весь текст пишет gemini».
Researcher и copywriter — **только Gemini**. Parent уже `gemini-3.8-flash` + `reasoning_effort=high`.
В каталоге Task **нет** slug `gemini-3.8-flash`. Текстовые воркеры спавнятся с `model="inherit"`.

| Артефакт | Кто пишет | Stamp |
|----------|-----------|--------|
| research dossier | researcher | `written_by: gemini` |
| 9 slides | copywriter | `written_by: gemini` |
| caption | copywriter (тот же шаг) | `written_by: gemini` |
| image prompts | image-prompter | своя модель |

Spawn: `model="inherit"`. НЕ передавать slug `gemini-3.8-flash` в Task.

### НЕТ ДЕФОЛТНОГО FALLBACK (NO DEFAULT FALLBACK)
Дефолтный агент / director **НИКОГДА** не пишет captions/slides/CTA сам при недоступной Gemini.
Никакого fallback на дефолтную модель (Claude, Sonnet, Opus, Composer, GPT) или исполнение в родительском чате.
Если inherit не даёт Gemini в runtime — **только FAIL + HOLE**. Не читать гейт/publish-скрипт в цикле.
Gate **отклоняет** copy/caption/brief без `written_by: gemini` (opus/sonnet/composer = FAIL).
Не переписывать голос Gemini.

## Host portrait (не открывать заново)

Нет лица Вики. Не класть `Виктория.png` в генерацию. Не FACE MATCH.
Alena / `viktoriaref.png` / `victoria-sheet.png` deleted. Live 30.08 не пересобирать.

## Dry-run (без пикселей)

```bash
python scripts/pipeline_gate.py --workspace /tmp/carusel-dry-run dry-run --lang ru --force
```
