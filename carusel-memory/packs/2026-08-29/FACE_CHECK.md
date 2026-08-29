# FACE_CHECK — 2026-08-29 Labels / Статус

compared: carusel-memory/references/viktoriaref.png
forbidden: Alena / cover-refs/victoria.png / виктория.png / victoria-sheet.png — not used
crops: packs/2026-08-29/face-check/
guardian_dispatch: e90ee380f44f4278bc22cd351911b54e
crops_rerun: python3 scripts/make_face_check_crops.py --pack carusel-memory/packs/2026-08-29

verdict: MATCH

Pixel compare this dispatch (not hair-prose, not a prior FACE_CHECK stamp).
Looked at viktoriaref.png + ru/en slide-01/09 face crops with Read, plus iris-box samples
(RGB/HSV) on the actual PNGs.

## Lock (viktoriaref.png)

Bone / age: oval-to-heart, high cheekbones, defined jaw, slightly pointed chin, ~late-20s/early-30s.
Eyes on lock: green with a slight hazel / light-brown tint around the pupil (зелёные с лёгким карим).
Iris sample this run: mean RGB ~ (62,38,20) / (74,48,30), hue ~24.8–25.0°, sat ~61–69%, G>B.
That is the official lock color — not grey, not a different dark-brown stranger.
Hair on lock: warm honey / wheat blonde, darker medium-brown roots, off-center part.
Lips: dusty rose. Warm complexion. Not the white-cami identity as wardrobe (clothes must change).

brown/grey = FAIL — not the viktoriaref.png lock. Not observed as a different eye on these slides.

## Pixel compare (01 / 09 vs viktoriaref.png)

### RU slide-01
- eyes: green + slight hazel (over-shoulder night key; iris still the lock mix, not grey)
- iris sample hue ~23.8° — same family as viktoriaref.png
- bone / age: same oval, high cheekbones, same jaw; same young-adult age as lock
- hair: warm honey blonde, darker roots, not platinum
- clothes: graphite silk pajama (new pack wardrobe, not sheet white cami + jeans)
- not Alena

### RU slide-09
- eyes: green with slight hazel / light-brown mix, looking at camera
- iris sample hue ~22.4–22.9°, G>B; night key pushes the same iris toward amber, not grey
- bone / age: same woman as 01 and viktoriaref.png
- hair: same warm blonde + darker roots pattern
- clothes: petrol-teal blouse + espresso suede jacket
- not Alena

### EN slide-01
- eyes: green with slight hazel (night lamp; lids shadow iris but green+hazel, not grey)
- iris sample hue ~19.0–23.2° — same family as viktoriaref.png (G>B, sat ~38–53%)
- bone / age: same cheek / jaw / chin as lock
- hair: warm blonde, darker roots, not platinum
- clothes: graphite silk pajama
- not Alena

### EN slide-09
- eyes: green with slight hazel / light-brown mix (outer ring + warmer center — Excalibur)
- iris sample hue ~21.9–22.5°, same mix as viktoriaref.png, not grey
- bone / age: same woman as EN 01 and lock
- hair: warm honey blonde + darker roots, not platinum
- clothes: petrol blouse + espresso jacket
- not Alena

brown/grey = FAIL — not observed on these four crops as a different eye from viktoriaref.png.
Platinum / generic older blonde / Alena = FAIL — not observed.

i2i this pack: carusel-memory/references/viktoriaref.png uploaded as viktoriaref.png.
Not виктория.png. Not victoria-sheet. Not animals-viktoria-style-lock.png.
