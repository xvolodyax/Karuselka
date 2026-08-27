# Carusel — Caption Format Contract (ТАРО СЕЙЧАС)

Канон: `shared/taro-seichas-canon.md`. Locale: `shared/locale-brand-contract.md`.

## Instagram limits

| Параметр | Лимит |
|----------|-------|
| caption | 2200 символов |
| hashtags | 30 |
| @mentions | 20 |

## Обязательные правила

1. **Нет сырых URL.** Напиши «ссылки в профиле» / «links are in the profile».
2. **Одно слово-триггер** в комментарии — новое каждый день, своё для RU и EN, по теме.
3. **Продукт всегда `app_audio`.** В Direct — аудиоразбор / audio reading **в приложении**
   (RU: Суть – Тень – Вектор; EN: Essence–Shadow–Vector).
4. **Запрещено** продавать бот как приз за комментарий
   (`три бесплатных расклада` / `3 free readings` / `3 free spreads`).
5. Не писать «личный аудиоразбор» — только «аудиоразбор».
6. EN: без Academy.
7. Первая строка caption = та же сцена, что на слайде 1.
8. Слайд 9 = тот же оффер. Контракт: `shared/cta-app-audio-contract.md`.

## Структура

```markdown
## Hook (первая строка)
Сцена. Без хештегов. Без URL.

## Body
2–4 коротких абзаца. Что пауза есть на самом деле + зачем свайпить было.
Эмодзи 0–3.

## CTA
Напиши в комментарии слово {TRIGGER}.
В Direct пришлём аудиоразбор в приложении: Суть – Тень – Вектор.
Ссылки в профиле.

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
  "cta": "Напиши в комментарии слово ПАУЗА. В Direct пришлём аудиоразбор в приложении: Суть – Тень – Вектор. Ссылки в профиле.",
  "trigger_word": "ПАУЗА",
  "product": "app_audio",
  "hashtags": ["#таросейчас"],
  "mentions": ["@todaytaro_ru"],
  "full_caption": "...",
  "char_count": 0,
  "hashtag_count": 0
}
```

`trigger_word` обязателен. `full_caption` не содержит `http`, `instagram.com`, `t.me`.
