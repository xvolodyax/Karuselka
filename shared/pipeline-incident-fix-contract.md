# Carusel — incident memory и Fixic loop

Контракт: субагенты фиксируют проблемы → **carusel-fixic** чинит пайплайн в коде.

## Canonical files

| File | Purpose |
|------|---------|
| `carusel-memory/pipeline-fix-queue.md` | durable incident memory (workspace) |
| `carusel-memory/fragments/*.md` | runtime handoff per agent |
| `.cursor/carusel-handoff.md` | Director exchange |
| `shared/pipeline-incident-fix-contract.md` | этот контракт |
| `shared/agent-pipeline-pitfalls.md` | устойчивые уроки (читать до run) |
| `agents/carusel-fixic.md` | Fixic agent |
| `skills/carusel-fixic/SKILL.md` | runbook Fixic |

Runtime artifacts (`output/slides/`, publish logs) — **не** место для durable fixes.

## Когда писать incident

Каждый субагент **append** в `pipeline-fix-queue.md`, если было:

- blocker, timeout, 401/402 API, schema mismatch;
- retry, workaround, fallback не из документации;
- артефакт переписан из-за неясного контракта;
- устаревший skill/script заставил лишние шаги;
- validation fail + fix «из головы»;
- пользователь поправил то, что контракт не покрывал.

**Не писать** если всё прошло штатно без corrective action.

## Формат incident

```markdown
## INC-YYYYMMDD-HHMM-<role>-<slug>
status: open
run_date: YYYY-MM-DD
role: carusel-<role>
topic: <из 00-brief> | n/a
severity: low | medium | high | blocker
category: prompt | script | docs | env | api | handoff | kie | instagram | qa | other

### What went wrong
- ...

### How the agent recovered this run
- ...

### Durable fix needed before next run
- ...

### Suggested files to inspect/change
- `path/to/file`

### Secrets
- none recorded

### Fixic resolution
- pending
```

**Запрещено** в incident: токены, пароли, приватные URL с секретами.

## Конец каждой задачи субагента

В fragment **обязательно**:

```text
incident_report: none
```

или:

```text
incident_report: carusel-memory/pipeline-fix-queue.md#INC-YYYYMMDD-HHMM-role-slug
```

Шаблон fragment: `shared/subagent-fragment-template.md`

## Director

После `carusel-publish` (успех) **или** терминального blocker:

1. Прочитать `carusel-memory/pipeline-fix-queue.md`
2. Если есть `status: open` за текущий run → **Task(`carusel-fixic`)**
3. Не начинать новую карусель с open blocker-incidents без явного OK пользователя

## Fixic

- Читает open incidents
- Правит **durable**: `skills/`, `agents/`, `shared/`, `scripts/`
- Прогоняет минимальные checks (`py_compile`, JSON parse)
- Помечает incident `fixed` или `needs-human`
- Дополняет `shared/agent-pipeline-pitfalls.md` если урок общий

Fixic **не** публикует в Instagram и **не** генерирует карусель.
