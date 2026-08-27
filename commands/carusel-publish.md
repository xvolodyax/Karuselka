# Carusel — Publish

Только после `✅ DESIGN OK` от **отдельного** Task `carusel-design-guardian` и `verify --step design-guardian`.

Не публикуй из чата Директора. Не публикуй без явного «опубликуй» / `publish_requested: true`.

```bash
python scripts/pipeline_gate.py --workspace . record-dispatch --step upload --via 'Task(carusel-upload)'
# Task upload …
python scripts/pipeline_gate.py --workspace . verify --step upload

python scripts/pipeline_gate.py --workspace . record-dispatch --step publish --via 'Task(carusel-publish)'
# Task publish …
python scripts/pipeline_gate.py --workspace . verify --step publish
```

Cloud: тот же ритуал с `Task(generalPurpose)` и `dispatch-prompt`.

`publish-urls.json`: `file1` video + `file2`…`file9` images, caption из `CAROUSEL_CAPTION.json`.  
Caption без сырых URL. Handle: `@todaytaro_ru` или `@todaytaro_bot` по `lang`.

MCP: `user-instagram carusel` / `t4528_carrusel_instagram`
