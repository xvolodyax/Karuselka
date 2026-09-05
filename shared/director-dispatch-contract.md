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
Первое чтение: `shared/director-once.md`. Не перечитывать `scripts/pipeline_gate.py`.
После GATE PASS / READY — EXIT. Max 2 Read gate-файла за run; третий = FAIL. Нет sleep/poll.

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
3. **researcher + copywriter (caption = тот же шаг, правило Владимира 03.09.2026 + 04.09.2026 + token-burn 05.09.2026):** модель **`inherit`** (родитель уже `gemini-3.8-flash` + `reasoning_effort=low`). high только если Владимир явно переопределил. НЕ передавать slug `gemini-3.8-flash` в Task — его нет в worker catalog. Артефакты обязаны нести `written_by: gemini`.
4. **NO DEFAULT FALLBACK ДЛЯ ТЕКСТА (правило 03.09.2026):** Дефолтный агент / director **НИКОГДА** не пишет captions/slides/CTA сам при недоступной Gemini. Никакого fallback на дефолтную модель (Claude, Sonnet, Opus, Composer, GPT) или выполнение директором в родительском чате. При недоступности Gemini — **только FAIL**.
5. **Task недоступен вообще:** `python scripts/pipeline_gate.py --workspace . hole --reason 'Task tool missing'` и выход. Не делать шаг в родительском чате. Не читать гейт/publish-скрипт в цикле. GATE PASS / READY → EXIT.

```text
❌ БЛОКЕР: среда не поддерживает subagents или Gemini недоступна.
Нельзя выполнить шаг в родительском чате. Default fallback запрещён: только FAIL.
```

Запрещено:

- сделать два шага в одном Task;
- «для скорости» написать dossier / caption / prompt самому;
- дефолтному агенту или директору писать captions/slides/CTA при сбое/недоступности Gemini (только FAIL);
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
# researcher / copywriter (только inherit parent Gemini):
python scripts/pipeline_gate.py --workspace . record-dispatch --step copywriter --via 'Task(generalPurpose)' --model inherit
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
