# Carusel — статус пайплайна

Покажи ledger, не делая работу субагентов.

```bash
python scripts/pipeline_gate.py --workspace . status
python scripts/pipeline_gate.py --workspace . next
python scripts/pipeline_gate.py --workspace . assert-complete
```

Сухой прогон (11 worker records, без PNG, publish skip):

```bash
python scripts/pipeline_gate.py --workspace /tmp/carusel-dry-run dry-run --lang ru
```

Ответ пользователю: `lang`, handle, таблица 12 шагов, `dispatch_mode` (plugin-agents vs generalPurpose-fallback), `required_model` для researcher/copywriter (`gemini-3.7-flash-high`), какой шаг пропущен, какой Task вызвать дальше. Publish по умолчанию не запускать.
