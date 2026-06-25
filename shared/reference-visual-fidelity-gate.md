# Carusel Reference Visual Fidelity Gate

Адаптация Teya `reference-visual-fidelity-gate.md` для карусели.

## Обязательный артефакт

```text
carusel-memory/design/CAROUSEL_VISUAL_INVENTORY.json
```

## Визуальные зоны (per slide)

- headline zone
- body text zone
- hero object / cutout
- background gradient / texture
- decorative stickers, shapes
- slide number pill
- CTA zone (slide 6)

## Формат zone

```json
{
  "id": "slide-02-hero-object",
  "slide": 2,
  "type": "cutout | illustration | photo | shape | sticker",
  "source_has_image": true,
  "required_for_fidelity": true,
  "implementation": "mcp-image | mcp-remove-bg | css-composite",
  "asset_registry_id": "slide-02-hero-object",
  "status": "ready | blocker"
}
```

## Минимумы

- `minimum_meaningful_image_assets`: ≥ 1 на слайд с value-контентом
- slide 1: hook readable at thumbnail (~200px width preview)
- seamless: ≥ 1 continuity element across seams

## Blocker

Если `CAROUSEL_STYLE_MATCH_SCORECARD.md` < 70 или P0 в inventory → guardian FAIL → regen designer.
