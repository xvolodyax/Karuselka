---
name: carusel-publish
description: Instagram MCP publish. Director MUST delegate via Task. Refuse unless publish_requested true.
model: inherit
readonly: false
is_background: false
---

**Вызов:** только Task. Director — СТОП.

Если в brief `publish_requested: false` — fragment BLOCKER, не вызывай MCP.

Следуй `skills/carusel-publish/SKILL.md`.

Caption без сырых URL. Handle по `lang`. `@todaytaro_bot` — бот, не приложение.
