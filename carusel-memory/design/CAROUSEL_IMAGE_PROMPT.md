# CAROUSEL IMAGE PROMPT — RU

**Pack ID:** `2026-09-01`  
**Topic:** Вторничное «завтра»: днем «сегодня вечером созвонимся», в 23:41 «сорри, давай завтра»  
**Visual family:** `animals_viktoria_collage`  
**Face lock:** `none` (No host portrait, no Victoria, no presenter face)  
**Slice method:** `seam` (Thin white gutters at 1/3 and 2/3, Excalibur method)  
**Format:** Grid 3×3 (9 equal 3:4 panels), Master 3:4 @ 4K, Static PNG  
**Trigger word:** `ЗАВТРА` (Slide 9 huge magenta script)  
**Product:** `app_audio` (Суть – Тень – Вектор)  
**Input URLs:** `["carusel-memory/references/animals-viktoria-style-lock.png"]` (Palette/rhythm only, not a face)  
**Prompt char count:** 1787 chars (target 1900–2100, max 2200)

---

## Reference Contract & Style Lock

- **Preserve:**
  - Dark matte charcoal `#111111`–`#1a1a1a` full-bleed background
  - Hot magenta `#ff006e` accent + handwritten script + torn-tape pills
  - White `#ffffff` heavy sans typography hierarchy
  - Soft gold foil accents used sparingly and natively
  - 3×3 master grid 3:4 @ 4K with thin white seams at 1/3 and 2/3
  - Animals as emotion metaphors (cat 1/4/7, dog 2/3, owl 6/8)
  - Safe text margin ≥12% from edges and seams
  - No host portrait / no female faces

- **Change:**
  - Midweek tomorrow-loop objects (cooling tea, clock 23:41, dark phone, torn tape)
  - Verbatim Tuesday Russian copy from `CAROUSEL_SLIDE_COPY.json`
  - Huge magenta trigger word `ЗАВТРА` on slide 9

- **Do Not Borrow:**
  - `Виктория.png`, `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`
  - Any recognizable host face or woman portrait
  - Sheet wardrobe (white cami, jeans, ivory blazer)
  - Portuguese collage text and foreign logos
  - Sticker halos / die-cut outlines, horror candle table, bot offer, raw URLs

---

## Active Kie Prompt (RU)

```text
No host portrait. No woman. No Victoria. No presenter face. Без портрета ведущей, без лиц, без Вик. Style lock = palette only (#111111 matte charcoal, white heavy sans, #ff006e hot magenta, soft gold foil), not a face.
Одно статичное PNG 3:4@4K, сетка 3×3. Thin white gutters at 1/3 and 2/3 (Excalibur seam_slice). Текст ≥12% от швов. Animals + objects only. Без видео.

01 cat, cooling tea, phone: "13:20: «вечером созвон». 23:41: «давай завтра».".
02 dog by dark phone: "Ты держишь вечер открытым" / "Отказываешься от планов и ждешь звонка. А около полуночи остаешься с чувством, что тебя снова подвинули.".
03 dog at closed door, pills: "Ошибка — писать: «Конечно, отдыхай»" / "Ты прячешь досаду за понимающей улыбкой, приучая человека к тому, что твое время ничего не стоит.".
04 cat watching clock loop: "Механизм 24-часовой петли" / "Короткое дневное обещание удерживает твою лояльность 12 часов без малейших реальных усилий с его стороны.".
05 screenshot decoder card: "Декодер вечерних переносов" / "• «Без сил, завтра 100%» → Ресурса на близость нет, но важно держать тебя про запас.\n• «Давай на днях» → Снимает с себя вину прямо сейчас.".
06 owl by neon 23:41 clock: "3 маркера хронического переноса" / "1. Сообщение приходит после 23:00.\n2. Нет нового точного времени.\n3. Петля повторяется второй раз за неделю.".
07 cat leaves empty chair: "Твой вечер — не зал ожидания" / "Если созвон отменился в последнюю минуту — вечер не потерян. Он мгновенно возвращается в твое распоряжение.".
08 owl, gold medallion: "Главное правило середины недели" / "Тот, кто действительно хочет контакта, ищет точное время. Тот, кто сомневается, кормит словом «завтра».".
09 huge magenta ЗАВТРА, phone, no people: "Напиши ЗАВТРА" / "Аудиоразбор в приложении. Суть – Тень – Вектор." / "Слово ЗАВТРА в комментариях".
```

---

## Negative Prompt

```text
Виктория.png, viktoriaref.png, victoria-sheet.png, victoria.png, woman, girl, host portrait, female face, presenter, human face, Alena, platinum hair, white cami, jeans, ivory blazer, host wardrobe, horror, skulls, dripping candles, blood, sticker outline, white halo around subjects, cutout border, bot, 3 free spreads, Academy, video, animated
```
