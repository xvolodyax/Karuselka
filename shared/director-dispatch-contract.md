# Director dispatch contract

Director **оркестрирует**. Director **не** пишет research, copy, design, Kie prompt, slice, motion, video, QA, upload, publish, fixic.

Каждый из 12 шагов — отдельный вызов агента или скилла. Тихо сделать шаг в родительском чате = сломанный пайплайн.

## Канон (12 агентов)

```text
director → researcher → copywriter → designer → image-prompter
  → slice → [skip motion-director] → [skip animate] → design-guardian
  → upload → publish → fixic

Instagram carousels are static PNGs. Slide 01 is PNG. See `shared/static-carousel-lock.md`.
```

Машина: `shared/pipeline-steps.json` + `shared/swarm-spawn-contract.md`.  
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
2. **Cloud / нет plugin types:** отдельный `Task(generalPurpose)` на **один** шаг. В промпт целиком входят `agents/carusel-*.md` + `skills/carusel-*/SKILL.md` + этот контракт + `shared/swarm-spawn-contract.md` + brief. Промпт печатает `pipeline_gate.py dispatch-prompt`.
3. **researcher + copywriter (caption = тот же шаг):** модель **`gemini-3.7-flash-high`**. Не inherit модели Director. Артефакты обязаны нести `written_by: gemini`.
4. **Task недоступен вообще:** стоп. Не делать шаг в родительском чате. Не писать «я теперь копирайтер».

```text
❌ БЛОКЕР: среда не поддерживает subagents.
Нельзя выполнить шаг в родительском чате.
```

Запрещено:

- сделать два шага в одном Task;
- «для скорости» написать dossier / caption / prompt самому;
- пропустить researcher, designer, image-prompter, slice, guardian, upload, fixic;
- запускать motion/animate/Grok video без явной просьбы Hall;
- считать, что Read skill-файла = вызов субагента.

Read skill в родительском чате **не** засчитывается как шаг.

## Ритуал на каждый worker-шаг

```bash
python scripts/pipeline_gate.py --workspace . next
python scripts/pipeline_gate.py --workspace . record-dispatch --step <id> --via 'Task(carusel-<role>)'
# или на cloud:
python scripts/pipeline_gate.py --workspace . record-dispatch --step <id> --via 'Task(generalPurpose)'
# researcher / copywriter:
python scripts/pipeline_gate.py --workspace . record-dispatch --step copywriter --via 'Task(generalPurpose)' --model gemini-3.7-flash-high
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

- `publish` вызывается отдельным Task **только** если в brief `publish_requested: true` и пользователь явно просил live-пост. Иначе `skip --step publish --reason publish-not-requested`. По умолчанию publish **не** запускать.
- `fixic` вызывается отдельным Task если в `pipeline-fix-queue.md` есть `status: open`. Иначе `skip --step fixic --reason no-open-incidents`.
- Пропуск других шагов **нельзя**.
- Не рендерить proof-pack / 18 слайдов, чтобы «доказать» face-lock. Канон = текст в `shared/taro-seichas-canon.md`.

Сухой прогон без PNG:

```bash
python scripts/pipeline_gate.py --workspace /tmp/carusel-dry-run dry-run --lang ru
```
