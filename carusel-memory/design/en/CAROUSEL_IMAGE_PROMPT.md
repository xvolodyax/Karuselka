# CAROUSEL IMAGE PROMPT — EN

**Pack ID:** `2026-09-01`  
**Topic:** The Midweek "Tomorrow" Loop  
**Visual family:** `animals_viktoria_collage`  
**Face lock:** `none` (No host portrait, no Victoria, no presenter face)  
**Slice method:** `seam` (Thin white gutters at 1/3 and 2/3, Excalibur method)  
**Format:** Grid 3×3 (9 equal 3:4 panels), Master 3:4 @ 4K, Static PNG  
**Trigger word:** `TOMORROW` (Slide 9 huge magenta script)  
**Product:** `app_audio` (Essence–Shadow–Vector)  
**Input URLs:** `["carusel-memory/references/animals-viktoria-style-lock.png"]` (Palette/rhythm only, not a face)  
**Prompt char count:** 1827 chars (target 1900–2100, max 2200)

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
  - Midweek tomorrow-loop objects (cooling tea, clock 11:41 PM, dark phone, torn tape)
  - Verbatim Tuesday English copy from `CAROUSEL_SLIDE_COPY.json`
  - Huge magenta trigger word `TOMORROW` on slide 9

- **Do Not Borrow:**
  - `Виктория.png`, `viktoriaref.png`, `victoria-sheet.png`, `victoria.png`
  - Any recognizable host face or woman portrait
  - Sheet wardrobe (white cami, jeans, ivory blazer)
  - Portuguese collage text and foreign logos
  - Sticker halos / die-cut outlines, horror candle table, bot offer, Academy, raw URLs

---

## Active Kie Prompt (EN)

```text
No host portrait. No woman. No Victoria. No presenter face. Без портрета ведущей, без лиц, без Вик. Style lock = palette only (#111111 matte charcoal, white heavy sans, #ff006e hot magenta, soft gold foil), not a face.
Одно статичное PNG 3:4@4K, сетка 3×3. Thin white gutters at 1/3 and 2/3 (Excalibur seam_slice). Текст ≥12% от швов. Animals + objects only. Без видео.

01 cat, cooling tea, phone: "1:20 PM: \"Call tonight\". 11:41 PM: \"Tomorrow\".".
02 dog by dark phone: "You keep your evening open" / "You turn down plans and wait for the call. Near midnight, you're left feeling pushed aside once again.".
03 dog at closed door, pills: "Mistake: \"No worries, get some rest\"" / "You hide your frustration behind understanding, teaching him that your time has zero value.".
04 cat watching clock loop: "The 24-Hour Postponement Loop" / "A tiny daytime promise buys 12 hours of your patience and loyalty with zero effort on his part.".
05 screenshot decoder card: "Late-Night Reschedule Decoder" / "• \"Drained today, tomorrow 100%\" → No capacity for depth, but wants to keep you on reserve.\n• \"Let's talk soon\" → Easing his immediate guilt.".
06 owl by neon 11:41 PM clock: "3 Signs of Chronic Delay" / "1. The message arrives past 11 PM.\n2. No specific replacement time is set.\n3. The loop repeats for the second time this week.".
07 cat leaves empty chair: "Your schedule is not a waiting room" / "When a call drops at the last minute, your evening isn't lost. It belongs right back to you.".
08 owl, gold medallion: "The Golden Midweek Rule" / "A man who wants connection makes specific time. A man who doubts feeds you with \"tomorrow\".".
09 huge magenta TOMORROW, phone, no people: "Comment TOMORROW" / "Audio reading in the app. Essence–Shadow–Vector." / "Write TOMORROW in the comments".
```

---

## Negative Prompt

```text
Виктория.png, viktoriaref.png, victoria-sheet.png, victoria.png, woman, girl, host portrait, female face, presenter, human face, Alena, platinum hair, white cami, jeans, ivory blazer, host wardrobe, horror, skulls, dripping candles, blood, sticker outline, white halo around subjects, cutout border, bot, 3 free spreads, Academy, video, animated
```
