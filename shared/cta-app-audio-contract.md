# CTA canon — APP audio reading (not the bot)

Locked 27.08.2026. Director / Gemini / copywriter **cannot** sell 3 free bot
spreads as the Instagram comment prize.

Host portrait is **none**. Excalibur seam slice and this CTA stay unchanged.
Already-live 27.08 Ping vs Step / Pause posts stay. Do not restyle them.

## Offer (every new carousel)

1. Ask the reader to write a **code word** in the comments.
   - RU and EN each have their **own** trigger, **new each day**, tied to the topic.
2. Promise that in **Direct** they get an **audio reading**
   (`аудиоразбор` / `audio reading`) **in the APP** that helps with **this**
   carousel topic:
   - RU: **Суть – Тень – Вектор**
   - EN: **Essence – Shadow – Vector**
3. We sell the **app audio reading**. Not 3 free bot spreads.
4. Captions: **no raw URLs**. Say links are in the profile / ссылка в шапке.
5. Slide 9 hook must match this offer.

`product` in copy + caption + PACK.json = **`app_audio`**.

Do not write «личный аудиоразбор». Write «аудиоразбор» / «audio reading».
EN: no Academy.

`@todaytaro_bot` is the EN Instagram handle name. It is **not** the comment prize.
The prize is the audio reading in the app.

## Templates (tiny examples — swap the trigger + topic)

Copywriter fills `{TRIGGER}` from today’s topic. Do not reuse yesterday’s word.

**RU caption CTA**

```text
Напиши в комментариях слово {TRIGGER}.
В Direct пришлём аудиоразбор в приложении по этой теме: Суть – Тень – Вектор.
Ссылки в профиле.
```

**EN caption CTA**

```text
Comment the word {TRIGGER} below.
We'll DM an audio reading in the app for this topic: Essence–Shadow–Vector.
Links are in the profile.
```

**RU slide 9**

```text
headline: Напиши {TRIGGER}
body: Аудиоразбор в приложении. Суть – Тень – Вектор.
cta: Слово {TRIGGER} в комментариях
```

**EN slide 9**

```text
headline: Comment {TRIGGER}
body: Audio reading in the app. Essence–Shadow–Vector.
cta: Write {TRIGGER} in the comments
```

## Gate

`scripts/canon_gate.py` and `scripts/pipeline_gate.py verify --step copywriter`
FAIL if caption or slides sell the bot (`3 free readings` / `три бесплатных расклада`)
as the comment prize, or if `product` is not `app_audio`.

Live packs `2026-08-27-swarm` and `2026-08-27-v2` are legacy (already shipped).
New packs cannot opt out.

## Skills

- `skills/carusel-copywriter/SKILL.md`
- `skills/carusel-researcher/SKILL.md`
- `skills/carusel-design-guardian/SKILL.md`
- `skills/director-carusel/SKILL.md`
