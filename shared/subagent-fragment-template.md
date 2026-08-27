# Шаблон fragment субагента Carusel

Каждый субагент пишет в `carusel-memory/fragments/<role>.md` и блок в `.cursor/carusel-handoff.md`.

```text
=== CARUSEL-<ROLE> ===
Статус: ✅ OK | ⚠️ WARN | ❌ BLOCKER | ❌ FAIL
dispatched_via: Task(carusel-<role>) | Task(generalPurpose)
dispatch_id: <from pipeline_gate record-dispatch>
lang: ru|en
skill: skills/carusel-<role>/SKILL.md
Кратко: ...

Артефакты:
- path/to/file

incident_report: none
HANDOFF_NEXT: <next-step-id>
```

Если была проблема — сначала append в `carusel-memory/pipeline-fix-queue.md`, затем:

```text
incident_report: carusel-memory/pipeline-fix-queue.md#INC-YYYYMMDD-HHMM-role-slug
```

## Обязательно в конце задачи

1. Статус и пути артефактов
2. **dispatched_via** + **dispatch_id** (кроме Director intake)
3. **incident_report** (none или ссылка на INC)
4. **HANDOFF_NEXT** — имя следующего шага, не его работа
5. Если BLOCKER — что нужно Директору/пользователю

Без `incident_report` и без `dispatched_via: Task(...)` fragment **невалиден**.  
`pipeline_gate.py verify` не пропустит шаг. Директор не имеет права дописать fragment за субагента.
