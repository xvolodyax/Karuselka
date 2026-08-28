## INC-20260828-0948-slice-seam-edge-bar
status: fixed
run_date: 2026-08-28
role: carusel-slice
topic: Тепло – холодно / Hot & Cold
severity: medium
category: qa
fixed_at: 2026-08-28
fix_summary:
- Seam path no longer turns `edge_cleanup` off after `seam_slice_grid.py`.
- `kie_carousel_gen.py` runs `clean_slide_edges.py` with strip ≥ leftover gutter (default 10).
- `grid_gutter_qa.py --mode seam`: 2480×3312 remainder width=2 is WARN; internals checked on a cropped+scrubbed copy.

### What went wrong
- First seam slice left `edge_cleanup` off. RU slides 04–06 kept a ~9px solid white bottom bar (rows 1431–1439). Guardian P0.
- `grid-gutter-qa-clean.json` also failed on seam master internal v1/v2 white (expected gutters) and Kie 4K remainder `{width: 2}` (2480 % 3).

### How the agent recovered this run
- Re-cut existing RU/EN `source.png` with `seam_slice_grid.py --split-mode gutter` (no cell crop, no Kie regen).
- `clean_slide_edges.py --strip 10` on all 9 slides; same 1080×1440.
- `remove_grid_gutters.py` used only on a **copy** of master for QA (not the slice input).
- Cropped 1px left + 1px right on the cleaned QA master (2478×3312) so remainder is 0. Slides unchanged.
- Both QA JSONs `status: ok`.

### Durable fix needed before next run
- After seam slice, `kie_carousel_gen.py` should run `clean_slide_edges.py` (strip ≥ leftover gutter, default 10).
- `grid_gutter_qa.py` in seam mode should treat 4K 2480×3312 remainder width=2 as WARN, or auto-use a scrubbed master.

### Suggested files to inspect/change
- `scripts/kie_carousel_gen.py`
- `scripts/grid_gutter_qa.py`
- `scripts/clean_slide_edges.py`

### Secrets
- none recorded

### Fixic resolution
- Implemented in `cursor/seam-edge-bar-4bf4`. Next seam run ships edge-cleaned 1080×1440 slides.
