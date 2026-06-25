---
name: carusel-fixic
description: Fixic — после run читает incidents, правит пайплайн Carusel (skills, scripts, pitfalls).
---

# Carusel Fixic

## Когда запускаться

После успешного `carusel-publish` **или** терминального blocker, если в  
`{workspace}/carusel-memory/pipeline-fix-queue.md` есть `status: open`.

Fixic **не** в production-path карусели — только post-run улучшение.

## Вход

- `carusel-memory/pipeline-fix-queue.md`
- `shared/pipeline-incident-fix-contract.md`
- `shared/agent-pipeline-pitfalls.md`
- Пути из `Suggested files to inspect/change` в каждом INC
- git status / diff (если доступен)

Workspace: `{PROJECT_ROOT}` = `Carusel/` на машине пользователя.

## Алгоритм

1. Прочитать весь `pipeline-fix-queue.md`.
2. Выбрать open-инциденты **текущего run** (по `run_date` или последние без `fixed`).
3. Сгруппировать по root cause.
4. Для каждого INC определить тип fix:
   - prompt / agent contract → `agents/`, `skills/`
   - script / validator → `scripts/`
   - docs → `shared/`
   - env → `.env.example`, contract (не писать секреты)
5. Внести **минимальный** durable diff в plugin `carusel/`.
6. Если урок общий — добавить пункт в `shared/agent-pipeline-pitfalls.md`.
7. Проверки:
   - `python -m py_compile` на изменённых `.py`
   - JSON parse на изменённых `.json` skills templates
8. Обновить каждый INC:

```markdown
status: fixed
fixed_at: YYYY-MM-DD
fix_summary:
- ...
files_changed:
- `...`
checks_run:
- ...
```

Или `status: needs-human` с `needed_decision_or_secret`.

## Что править

| Можно | Нельзя |
|-------|--------|
| `skills/`, `agents/`, `shared/`, `scripts/` | `carusel-memory/output/*` как fix |
| `agent-pipeline-pitfalls.md` | secrets в memory |
| `.env.example` | пользовательский `.env` |

## Выход

Fragment: `carusel-memory/fragments/fixic.md`

```text
=== CARUSEL-FIXIC ===
Статус: fixed | needs-human | no-open-incidents
incidents_handled:
- INC-...
files_changed:
- ...
checks:
- ...
incident_report: none
```

## Запреты

- Не закрывать INC без реального fix или `needs-human`
- Не публиковать в Instagram
- Не перегенерировать карусель ради проверки
- Не дублировать секреты в queue/pitfalls
