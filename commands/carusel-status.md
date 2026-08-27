# Carusel — статус пайплайна

Покажи ledger, не делая работу субагентов.

```bash
python scripts/pipeline_gate.py --workspace . status
python scripts/pipeline_gate.py --workspace . next
python scripts/pipeline_gate.py --workspace . assert-complete
```

Ответ пользователю: `lang`, handle, таблица 12 шагов, `dispatch_mode` (plugin-agents vs generalPurpose-fallback), какой шаг пропущен, какой Task вызвать дальше.
