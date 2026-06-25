# Конец задачи — все субагенты Carusel

**Обязательно** перед завершением любого шага пайплайна.

## 1. Прочитать pitfalls

`shared/agent-pipeline-pitfalls.md` — не повторять известные ошибки.

## 2. Incident memory

Контракт: `shared/pipeline-incident-fix-contract.md`

Если в задаче был blocker, retry, workaround, несоответствие skill/API — **append** в:

`{workspace}/carusel-memory/pipeline-fix-queue.md`

Формат INC: см. контракт. **Без секретов.**

## 3. Fragment

Путь: `carusel-memory/fragments/<role>.md` + блок в `.cursor/carusel-handoff.md`

Шаблон: `shared/subagent-fragment-template.md`

**Обязательная строка:**

```text
incident_report: none
```

или:

```text
incident_report: carusel-memory/pipeline-fix-queue.md#INC-YYYYMMDD-HHMM-<role>-<slug>
```

Fragment **без** `incident_report` — невалиден; Директор не переходит к следующему шагу.

## 4. Fixic (не твоя роль)

После всего run Директор вызывает `carusel-fixic`, если есть open incidents. Субагент Fixic не запускает.
