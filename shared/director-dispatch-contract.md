# Director dispatch contract

Director **оркестрирует**. Director **не** пишет research, copy, design, Kie prompt, slice, motion, video, QA, upload, publish, fixic.

Каждый из 12 шагов — отдельный вызов агента или скилла. Тихо сделать шаг в родительском чате = сломанный пайплайн.

## Канон (12 агентов)

```text
director → researcher → copywriter → designer → image-prompter
  → slice → motion-director → animate → design-guardian
  → upload → publish → fixic
```

Машина: `shared/pipeline-steps.json`.  
Проверка: `python scripts/pipeline_gate.py --workspace . status`

## Почему cloud ломал цепочку

Local plugin agents (`Task(carusel-researcher)` и остальные `carusel-*`) регистрируются **только** когда плагин Каруселька загружен в Cursor Desktop / local plugin host.

**Cloud agent физически не видит эти типы.** В cloud Task обычно есть только:

- `generalPurpose`
- `explore`
- `computerUse`
- `videoReview`
- `cursor-guide`
- `best-of-n-runner`

Старый fallback («если нет carusel-* — сделай сам или как-нибудь generalPurpose») был мягким. Директор игнорировал его и писал карусель в одном чате. Поэтому в логах часто были только director / copywriter / publish.

Это не баг роя. Это ограничение среды. Рой из 12 агентов **нельзя выкидывать**.

## Жёсткий обход (обязателен)

Порядок выбора способа вызова:

1. **Desktop plugin:** `Task(<task_name>)` из `pipeline-steps.json` (`carusel-researcher`, …).
2. **Cloud / нет plugin types:** отдельный `Task(generalPurpose)` на **один** шаг. В промпт целиком входят `agents/carusel-*.md` + `skills/carusel-*/SKILL.md` + этот контракт + brief. Промпт печатает `pipeline_gate.py dispatch-prompt`.
3. **Task недоступен вообще:** стоп.

```text
❌ БЛОКЕР: среда не поддерживает subagents.
Нельзя выполнить шаг в родительском чате.
```

Запрещено:

- сделать два шага в одном Task;
- «для скорости» написать dossier / caption / prompt самому;
- пропустить researcher, designer, image-prompter, slice, motion, animate, guardian, upload, fixic;
- считать, что Read skill-файла = вызов субагента.

Read skill в родительском чате **не** засчитывается как шаг.

## Ритуал на каждый worker-шаг

```bash
python scripts/pipeline_gate.py --workspace . next
python scripts/pipeline_gate.py --workspace . record-dispatch --step <id> --via 'Task(carusel-<role>)'
# или на cloud:
python scripts/pipeline_gate.py --workspace . record-dispatch --step <id> --via 'Task(generalPurpose)'
python scripts/pipeline_gate.py --workspace . dispatch-prompt --step <id>
```

1. Скопировать `dispatch_id` и промпт.
2. Вызвать **Task** (plugin type или `generalPurpose`).
3. Дождаться fragment + артефактов.
4. Проверить:

```bash
python scripts/pipeline_gate.py --workspace . verify --step <id>
```

Если `verify` падает — **стоп**. Не чини шаг сам. Повтори Task или верни blocker пользователю.

## Что пишет только Director

- `carusel-memory/00-brief.md` (intake, `lang=ru|en`)
- `carusel-memory/pipeline-ledger.json` (через `pipeline_gate.py`)
- `.cursor/carusel-handoff.md` (сброс + merge статусов)
- `carusel-memory/fragments/director.md`

Director **не** создаёт файлы из `required_artifacts` чужих шагов.

## Ledger

`carusel-memory/pipeline-ledger.json`

Worker-шаг без `dispatched_via` вида `Task(...)` не может стать `ok`.  
`inline`, `parent`, `self`, пустая строка — для worker **запрещены**.

## Publish и Fixic

- `publish` вызывается отдельным Task **только** если в brief `publish_requested: true` и пользователь явно просил live-пост. Иначе `skip --step publish --reason publish-not-requested`.
- `fixic` вызывается отдельным Task если в `pipeline-fix-queue.md` есть `status: open`. Иначе `skip --step fixic --reason no-open-incidents`.
- Пропуск других шагов **нельзя**.
