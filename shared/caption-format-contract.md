# Carusel — Caption Format Contract (ТАРО СЕЙЧАС)

Канон: `shared/taro-seichas-canon.md`. Locale: `shared/locale-brand-contract.md`.

## Instagram limits

| Параметр | Лимит |
|----------|-------|
| caption | 2200 символов |
| hashtags | 30 |
| @mentions | 20 |

## Обязательные правила

1. **Нет сырых URL.** Они не кликабельны и ломают gate.
2. **Одно слово-триггер** в комментарии. Команда отвечает в Direct.
3. **Один продукт** на карусель: `bot_three_spreads` или `app_audio`. Не мешать.
4. Не писать «личный аудиоразбор».
5. EN: без Academy.
6. Первая строка caption = та же сцена, что на слайде 1.

## Структура

```markdown
## Hook (первая строка)
Сцена. Без хештегов. Без URL.

## Body
2–4 коротких абзаца. Что пауза есть на самом деле + зачем свайпить было.
Эмодзи 0–3.

## CTA
Напиши в комментарии слово {TRIGGER}.
Пришлём в Direct {один продукт}.

## Handle + slogan
@todaytaro_ru / Ясность сейчас
@todaytaro_bot / Clarity now

## Hashtags
5–12, в конце. Без спама.
```

## Выход copywriter

`carusel-memory/design/CAROUSEL_CAPTION.md` + `CAROUSEL_CAPTION.json`:

```json
{
  "hook": "Он смотрит твои истории. Третью неделю. Сообщения нет.",
  "body": "...",
  "cta": "Напиши в комментарии слово ПАУЗА — пришлём в Direct 3 бесплатных расклада в боте.",
  "trigger_word": "ПАУЗА",
  "product": "bot_three_spreads",
  "hashtags": ["#таросейчас"],
  "mentions": ["@todaytaro_ru"],
  "full_caption": "...",
  "char_count": 0,
  "hashtag_count": 0
}
```

`trigger_word` обязателен. `full_caption` не содержит `http`, `instagram.com`, `t.me`.
