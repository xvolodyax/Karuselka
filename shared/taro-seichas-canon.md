# ТАРО СЕЙЧАС / Today Tarot — always-on carousel canon

Читать **до** research / copy / design / prompt / guardian на каждом daily run (в т.ч. 11:10).
Пустой красивый вайб без урока = FAIL. Семья `animals_viktoria_collage` не опция, а дефолт.

Контракты рядом: `shared/locale-brand-contract.md`, `shared/animals-viktoria-collage.md`,
`shared/caption-format-contract.md`, `shared/cta-app-audio-contract.md`.
Проверка: `python scripts/canon_gate.py --pack <pack>`.

## Почему этот файл существует

27.08.2026 две карусели уже вышли и **остаются live** (не удалять, не править):

| lang | Handle | Post | Hook |
|------|--------|------|------|
| ru | @todaytaro_ru | https://www.instagram.com/p/Dci-EP1ErI-/ | «Пауза или конец?» |
| en | @todaytaro_bot | https://www.instagram.com/p/Dci-ozwAH4l/ | «Pause or over?» |

Владелец: посты пустые / красивые / глупые относительно OLD Karuselka.
Причина (проверено 27.08): в plugin-scaffold не было visual family + meaning lock.
Locale-контракт фиксировал handle и «без URL», но не сцену, не животных, не Викторию,
не framework на save-слайдах. Copywriter skill писал generic vibe-arc.

Этот канон закрывает дрейф. Новая пара по той же теме — pack `2026-08-27-v2`.

## Профили

| | RU | EN |
|---|----|----|
| Бренд | ТАРО СЕЙЧАС | Today Tarot |
| Handle | @todaytaro_ru | @todaytaro_bot |
| Слоган | Ясность сейчас | Clarity now |
| Лицо | нет портрета ведущей | то же: без Вики |
| Academy | можно не трогать | **NO Academy** |

Клиент: женщины 20–50, ~78% отношения. Не целиться в 13–17.
Не хайпить войну/медицину. Не читать мысли. Не пугать одиночеством.

## Visual family (всегда)

`carousel_family`: **`animals_viktoria_collage`**

Полный spec: `shared/animals-viktoria-collage.md`.

Коротко:

- charcoal/black + magenta `#ff006e` + white + soft gold
- Слайды **без портрета ведущей**. Не рисовать Вику. Не класть `Виктория.png` в генерацию.
  GATE **FAIL** если на слайде лицо Вики / любой узнаваемый портрет ведущей.
  Не FACE MATCH «похожа на Виктория.png». Старое «не класть если лицо не совпало» снято:
  лица не должно быть вообще.
- `Виктория.png` остаётся для статей и историй в других репо. В Karuselka карусель её не ставит.
- Других женских лиц нет. Doubles запрещены.
- Животные = метафоры, не мемы: кот = «чуешь», пёс = верность вопросу, сова = ночные мысли.
- Минимум **3** слайда с животным-метафорой.
- 9 слайдов, каждый 3:4, hook читается за 2 секунды.
- Нет horror / крови / черепов / тёмного стола со свечами.
- Нет подписи Victoria на слайдах.
- Лёгкий tarot-декор можно, если не закрывает headline.
- Опционально золотой медальон ТАРО/СЕЙЧАС, если садится нативно.

## Meaning / copy (то, чего не хватило 27.08 live)

9-slide teaching arc:

```text
01 hook SCENE     — первая строка = сцена, не название механики
02 pain           — что болит в этой сцене
03 mistake        — как клиентка слышит приговор вместо процесса
04 mechanism      — чем пауза является на самом деле
05–07 save        — 2–3 слайда с рамкой / вопросами / «говорит vs слышишь»
08 recap / rule   — правило, которое можно сохранить
09 CTA            — одно действие, одно слово-триггер
```

Первая строка — СЦЕНА. Энергия:

> Он смотрит твои истории. Третью неделю. Сообщения нет.

Не: «5 признаков паузы», «Что такое пауза в таро», «Pause vs ending».

Простой разговорный русский / English. Без поэзии, которую надо объяснять.
Глубина как в OLD `slide-04`: «Говорит: … / Слышишь: …» + конструктивный урок.
Не список вайб-слов.

Запреты в тексте:

- «личный аудиоразбор» — только «аудиоразбор»
- продавать бот как приз за комментарий (3 бесплатных расклада / 3 free readings)
- сырые URL в слайдах и caption (только «ссылки в профиле»)
- пугать одиночеством, войной, болезнью
- EN: Academy

## Caption + продукт

Один пост = **`app_audio`** = одно слово-триггер (новое, по теме, своё для RU и EN).
В Direct — аудиоразбор в приложении по этой карусели:
RU **Суть – Тень – Вектор**, EN **Essence–Shadow–Vector**.
Слайд 9 = тот же оффер. Ссылки в профиле. Не бот.

Live-посты 27.08 (Pause + Ping vs Step) уже вышли с ботом — их не переписывать.
Новые карусели: `shared/cta-app-audio-contract.md`.

Не писать сырые `https://`, `instagram.com`, `t.me`. Handle как `@todaytaro_ru`.

## Референсы

В репо: `carusel-memory/references/` (канон-текст + style lock).
`Виктория.png` в этом репо **не** кладётся в Kie. **Не рендерить live 30.08**, чтобы «доказать» lock.

- Style: `animals-viktoria-style-lock.png` — palette / rhythm only, not a face
- `Виктория.png` — не i2i в карусель
- `viktoriaref.png` / `victoria-sheet.png` — **DELETED**. Never restore. Never i2i.
- Alena files (`victoria.png`, `alena.png`, `*_ref.jpg`) — **DELETED**. Never restore. Never i2i.
- `/workspace/karusel-old/cover-old.png` — RETIRED studio-blazer
- `/workspace/karusel-old/image-851e.png` — STYLE LOCK
- `/workspace/karusel-old/slide-04.png` — DEPTH example

Португальский текст и чужие лица из style collage **не заимствовать**.

## Gate (PASS только если все true)

- (a) нет портрета ведущей; `face_lock=none`; лицо Вики на слайде = FAIL
  (live 27–30.08 historical packs не пересобирать)
- (b) ≥3 слайда с животным как метафорой
- (c) ≥2 save-слайда с настоящей рамкой или вопросами
- (d) hook = сцена
- (e) нет platinum; одежда не с листа и не повтор прошлого pack
- (f) нет пустых vibe-only слайдов
- (i) CTA = `app_audio` (аудиоразбор в приложении); бот как приз за комментарий = FAIL

## Пайплайн

Не изобретать новый рой. Цепочка та же:

`director → researcher → copywriter → designer → image-prompter → slice
 → motion-director → animate → design-guardian → upload → publish → fixic`

`Task(carusel-*)` если plugin types есть. Иначе отдельный `Task(generalPurpose)` на шаг
(`shared/director-dispatch-contract.md` + `shared/swarm-spawn-contract.md` +
`scripts/pipeline_gate.py`).

Жёсткое правило Владимира: researcher + copywriter (текст карусели: dossier, 9 слайдов, caption, CTA) — только Gemini. Parent: `gemini-3.8-flash` + `reasoning_effort=high`. Task-воркеры: `model="inherit"`. Slug `gemini-3.8-flash` в Task запрещён (нет в каталоге).
Дефолтный агент / director НИКОГДА не пишет captions/slides/CTA сам при недоступной Gemini. Никакого default fallback (Claude, Sonnet, Opus, Composer, GPT) — только FAIL + HOLE.

Director **не** делает worker-шаг сам. Нет parent remake. Нет proof-pack
rerender live 30.08 СУББОТА / WEEKEND. Новые кадры без Вики = **новый pack / новый пост**.
Холл тексты не пишет.

Publish / Composio / Instagram — только Hall после human review.
`publish_requested: false` по умолчанию.

## Live posts

Не удалять и не редактировать посты 27.08. Новая пара = новый pack / новый пост.
