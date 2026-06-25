# Шаблон fragment субагента Carusel

Каждый субагент пишет в `carusel-memory/fragments/<role>.md` и блок в `.cursor/carusel-handoff.md`.

```text
=== CARUSEL-<ROLE> ===
Статус: ✅ OK | ⚠️ WARN | ❌ BLOCKER | ❌ FAIL
Кратко: ...

Артефакты:
- path/to/file

incident_report: none
```

Если была проблема — сначала append в `carusel-memory/pipeline-fix-queue.md`, затем:

```text
incident_report: carusel-memory/pipeline-fix-queue.md#INC-YYYYMMDD-HHMM-role-slug
```

## Обязательно в конце задачи

1. Статус и пути артефактов
2. **incident_report** (none или ссылка на INC)
3. Если BLOCKER — что нужно Директору/пользователю

Без `incident_report` строки fragment **невалиден**.
