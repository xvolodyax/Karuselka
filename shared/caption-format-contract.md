# Carusel — Caption Format Contract

> **Статус:** placeholder — пользователь пришлёт финальный формат подписи.

## Instagram limits (MCP)

| Параметр | Лимит |
|----------|-------|
| caption | 2200 символов |
| hashtags | 30 |
| @mentions | 20 |

## Текущий draft-формат (до спецификации пользователя)

```markdown
## CAROUSEL_CAPTION.md structure

### Hook (первая строка)
- 1 предложение, интрига, без хештегов

### Body
- 2–4 коротких абзаца
- эмодзи умеренно (0–3)

### CTA
- одно действие: подписка / сохрани / ссылка в bio

### Hashtags
- блок в конце, 5–15 релевантных
- mix: broad + niche

### Mentions
- @аккаунты по необходимости
```

## Выход copywriter

`carusel-memory/design/CAROUSEL_CAPTION.md` + `CAROUSEL_CAPTION.json`:

```json
{
  "hook": "...",
  "body": "...",
  "cta": "...",
  "hashtags": ["#..."],
  "mentions": ["@..."],
  "full_caption": "...",
  "char_count": 0,
  "hashtag_count": 0
}
```

## Phase 2 — пользовательский формат

Когда пользователь пришлёт шаблон:

1. Обновить этот файл.
2. Обновить `skills/carusel-copywriter/SKILL.md`.
3. Не менять MCP publish — только `caption` string.
