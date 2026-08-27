# Swarm spawn contract

Director **только оркестрирует**. Каждый worker — отдельный **Task**.
Тихо сделать шаг в родительском чате = сломанный пайплайн.

Машина: `shared/pipeline-steps.json` + `python scripts/pipeline_gate.py`.

## 12 шагов (11 worker records)

```text
director (parent intake)
  → researcher          Task + Gemini
  → copywriter          Task + Gemini  (slides AND caption — same step)
  → designer            Task
  → image-prompter      Task
  → slice               Task
  → motion-director     Task
  → animate             Task
  → design-guardian     Task
  → upload              Task
  → publish             SKIP unless brief.publish_requested true
  → fixic               SKIP unless open incidents
```

Это **11 worker records**. Publish по умолчанию `skip: publish-not-requested`.
Не публиковать в Instagram / Composio / Make из Director.

## Модель

| Step | Model |
|------|--------|
| researcher | **`gemini-3.7-flash-high`** |
| copywriter (включая caption) | **`gemini-3.7-flash-high`** |
| все остальные workers | inherit / plugin default |

Cloud: `Task(generalPurpose)` **на один шаг**, `model` как в таблице.
Desktop plugin: `Task(carusel-researcher)` / `Task(carusel-copywriter)` с тем же `model`.

`pipeline_gate.py record-dispatch` сам ставит Gemini на researcher/copywriter.
Другая модель на этих шагах = FAIL.

## Запреты

- два шага в одном Task
- Director пишет dossier / caption / design / Kie prompt / PNG
- proof-pack / 18-slide rerender «чтобы проверить канон»
- считать Read skill = вызов субагента
- Instagram, пока `publish_requested: false`

## Dry-run (без пикселей)

```bash
python scripts/pipeline_gate.py --workspace /tmp/carusel-dry-run dry-run --lang ru
```

Пишет 11 worker records. **Не** создаёт PNG/MP4. **Не** вызывает Kie/Grok/Instagram.
Verify в режиме `dry-run` не требует бинарных картинок/видео.
