# Carusel — Caption Format Contract

> Locale: `shared/locale-brand-contract.md`. `lang=ru|en` обязателен.

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
- одно действие
- RU: «ссылка в шапке» / сохрани / подпишись
- EN: «link in bio» / save / follow
- **без сырых URL** (`https://`, `t.me/`, `instagram.com/`)

### Hashtags
- блок в конце, 5–15 релевантных
- mix: broad + niche

### Mentions
- `lang=ru` → `@todaytaro_ru`
- `lang=en` → `@todaytaro_bot` (Telegram **bot**, не app)
```

## Выход copywriter

`carusel-memory/design/CAROUSEL_CAPTION.md` + `CAROUSEL_CAPTION.json`:

```json
{
  "lang": "ru",
  "hook": "...",
  "body": "...",
  "cta": "ссылка в шапке",
  "hashtags": ["#..."],
  "mentions": ["@todaytaro_ru"],
  "full_caption": "...",
  "char_count": 0,
  "hashtag_count": 0
}
```

`pipeline_gate.py verify --step copywriter` падает, если в caption есть сырой URL или нет handle для `lang`.

## Phase 2 — пользовательский формат

Когда пользователь пришлёт шаблон:

1. Обновить этот файл.
2. Обновить `skills/carusel-copywriter/SKILL.md`.
3. Не менять MCP publish — только `caption` string.
