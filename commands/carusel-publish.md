# Carusel — Publish

После `GATE PASS` + FACE_CHECK MATCH vs `viktoriaref.png` и `✅ DESIGN OK`.

**Task**(`carusel-publish`):

```bash
python scripts/composio_instagram_publish.py --pack carusel-memory/packs/YYYY-MM-DD
```

Env: `COMPOSIO_API_KEY`. Alias: `instagram-ru` / `instagram-en`. Не default. Не Telegram.

Нет ключа → SKIP «нет COMPOSIO_API_KEY». Уже live → не перезаливать.
