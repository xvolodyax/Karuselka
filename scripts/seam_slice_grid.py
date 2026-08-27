#!/usr/bin/env python3
"""Excalibur-style seamed canvas slice for a 3×3 carousel.

Copied from taro-excalibur `scripts/excalibur_blog_cover_quad_split.py`:
generate ONE canvas with thin white gutters, then cut ON those seams.
Do not treat people/animals as sticker cutouts.

If a gutter is missing or too far from the geometric 1/3–2/3 lines,
exit 2 so the Director rebuilds the whole canvas (never patch one cell).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image

WHITE_THRESHOLD = 235
MIN_GUTTER_RUN = 2
GUTTER_SEARCH_RADIUS = 48
GUTTER_WHITE_FRACTION = 0.85
GUTTER_MAX_CENTER_OFFSET_PX = 36
PANEL_ASPECT = 3 / 4
SPLIT_MODES = ("auto", "mechanical", "gutter")


def _find_gutter_band(white_fracs: list[float], center: int) -> tuple[int, int] | None:
    lo = max(0, center - GUTTER_SEARCH_RADIUS)
    hi = min(len(white_fracs), center + GUTTER_SEARCH_RADIUS)
    best: tuple[int, int] | None = None
    best_score = -1.0
    i = lo
    while i < hi:
        if white_fracs[i] >= GUTTER_WHITE_FRACTION:
            j = i
            while j < hi and white_fracs[j] >= GUTTER_WHITE_FRACTION:
                j += 1
            run_len = j - i
            if run_len >= MIN_GUTTER_RUN:
                mid = (i + j) / 2
                dist = abs(mid - center)
                score = run_len * 10 - dist
                if score > best_score:
                    best = (i, j)
                    best_score = score
            i = j
        else:
            i += 1
    return best


def _line_white_fracs(img: Image.Image, axis: str) -> list[float]:
    width, height = img.size
    px = img.load()
    if axis == "x":
        fracs: list[float] = []
        for x in range(width):
            white = 0
            for y in range(height):
                r, g, b = px[x, y][:3]
                if min(r, g, b) > WHITE_THRESHOLD:
                    white += 1
            fracs.append(white / height)
        return fracs
    fracs = []
    for y in range(height):
        white = 0
        for x in range(width):
            r, g, b = px[x, y][:3]
            if min(r, g, b) > WHITE_THRESHOLD:
                white += 1
        fracs.append(white / width)
    return fracs


def _mechanical_boxes(width: int, height: int, cols: int, rows: int) -> list[tuple[int, int, int, int]]:
    cell_w = width // cols
    cell_h = height // rows
    boxes: list[tuple[int, int, int, int]] = []
    for row in range(rows):
        for col in range(cols):
            boxes.append((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
    return boxes


def _gutter_boxes(
    width: int,
    height: int,
    v_bands: list[tuple[int, int]],
    h_bands: list[tuple[int, int]],
    cols: int,
    rows: int,
) -> list[tuple[int, int, int, int]]:
    xs = [0] + [b[0] for b in v_bands]
    xe = [b[1] for b in v_bands] + [width]
    ys = [0] + [b[0] for b in h_bands]
    ye = [b[1] for b in h_bands] + [height]
    boxes: list[tuple[int, int, int, int]] = []
    for row in range(rows):
        for col in range(cols):
            boxes.append((xs[col], ys[row], xe[col], ye[row]))
    return boxes


def detect_grid_boxes(
    img: Image.Image,
    *,
    cols: int = 3,
    rows: int = 3,
    split_mode: str = "auto",
) -> tuple[list[tuple[int, int, int, int]], dict[str, Any]]:
    mode = (split_mode or "auto").strip().lower()
    if mode not in SPLIT_MODES:
        raise ValueError(f"split_mode must be one of {SPLIT_MODES}")
    width, height = img.size
    mechanical = _mechanical_boxes(width, height, cols, rows)
    meta: dict[str, Any] = {
        "requested_mode": mode,
        "split_mode": "mechanical_center",
        "v_gutters_px": [],
        "h_gutters_px": [],
    }
    if mode == "mechanical":
        return mechanical, meta

    col_white = _line_white_fracs(img, "x")
    row_white = _line_white_fracs(img, "y")
    v_expected = [round(width * i / cols) for i in range(1, cols)]
    h_expected = [round(height * i / rows) for i in range(1, rows)]
    v_bands = [_find_gutter_band(col_white, x) for x in v_expected]
    h_bands = [_find_gutter_band(row_white, y) for y in h_expected]

    if not all(v_bands) or not all(h_bands):
        meta["fallback_reason"] = "gutter_bands_not_found"
        if mode == "gutter":
            raise SystemExit("CROOKED CANVAS: white seams missing at 1/3 or 2/3. Rebuild the whole canvas.")
        return mechanical, meta

    assert all(v_bands) and all(h_bands)
    v_ok = [b for b in v_bands if b]
    h_ok = [b for b in h_bands if b]
    offsets = []
    for band, expected in zip(v_ok, v_expected):
        offsets.append(abs((band[0] + band[1]) / 2 - expected))
    for band, expected in zip(h_ok, h_expected):
        offsets.append(abs((band[0] + band[1]) / 2 - expected))
    max_offset = max(offsets) if offsets else 0
    meta.update(
        {
            "v_gutters_px": [{"start": a, "end": b} for a, b in v_ok],
            "h_gutters_px": [{"start": a, "end": b} for a, b in h_ok],
            "max_center_offset_px": round(max_offset, 2),
        }
    )
    if max_offset > GUTTER_MAX_CENTER_OFFSET_PX:
        meta["fallback_reason"] = "gutter_too_far_from_expected"
        if mode == "gutter":
            raise SystemExit(
                f"CROOKED CANVAS: seam offset {max_offset:.1f}px > {GUTTER_MAX_CENTER_OFFSET_PX}. "
                "Rebuild the whole canvas."
            )
        return mechanical, meta

    boxes = _gutter_boxes(width, height, v_ok, h_ok, cols, rows)
    meta["split_mode"] = "gutter_detect"
    return boxes, meta


def _center_crop_aspect(im: Image.Image, aspect: float) -> Image.Image:
    w, h = im.size
    if w < 8 or h < 8:
        return im
    current = w / h
    if abs(current - aspect) <= 0.01:
        return im
    if current > aspect:
        new_w = int(round(h * aspect))
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(round(w / aspect))
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def slice_seamed(
    input_path: Path,
    output_dir: Path,
    *,
    cols: int = 3,
    rows: int = 3,
    split_mode: str = "gutter",
    master_out: Path | None = None,
    manifest_path: Path | None = None,
    target_size: tuple[int, int] | None = None,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(input_path) as raw:
        img = raw.convert("RGB")
        source_size = img.size
        if master_out:
            master_out.parent.mkdir(parents=True, exist_ok=True)
            img.save(master_out, "PNG", optimize=True)
        boxes, meta = detect_grid_boxes(img, cols=cols, rows=rows, split_mode=split_mode)
        written: list[Path] = []
        crops: list[Image.Image] = []
        for box in boxes:
            crops.append(img.crop(box))

    if target_size is None:
        sample = _center_crop_aspect(crops[0], PANEL_ASPECT)
        target_size = sample.size

    for index, crop in enumerate(crops, start=1):
        panel = _center_crop_aspect(crop, PANEL_ASPECT)
        if panel.size != target_size:
            panel = panel.resize(target_size, Image.Resampling.LANCZOS)
        out = output_dir / f"slide-{index:02d}.png"
        panel.save(out, "PNG", optimize=True)
        written.append(out)
        print(f"slide-{index:02d} {boxes[index - 1]} -> {out} ({panel.size[0]}x{panel.size[1]})")

    if manifest_path:
        manifest = {
            "mode": "seam",
            "source": str(input_path.resolve()),
            "source_size": {"width": source_size[0], "height": source_size[1]},
            "grid": {"cols": cols, "rows": rows, "order": "row-major"},
            "slice_method": "excalibur_white_seams",
            "split_meta": meta,
            "cell_size": {"width": target_size[0], "height": target_size[1]},
            "cell_aspect_ratio": PANEL_ASPECT,
            "slide_count": cols * rows,
            "master_out": str(master_out.resolve()) if master_out else None,
            "files": [str(p.resolve()) for p in written],
        }
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Manifest: {manifest_path}")
        print(json.dumps({"split_meta": meta}, ensure_ascii=False))
    return written


def main() -> int:
    p = argparse.ArgumentParser(description="Slice a seamed 3x3 canvas on white gutters (Excalibur method)")
    p.add_argument("--input", "-i", required=True)
    p.add_argument("--output-dir", "-o", required=True)
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--rows", type=int, default=3)
    p.add_argument("--split-mode", choices=SPLIT_MODES, default="gutter")
    p.add_argument("--master-out", "-m")
    p.add_argument("--manifest")
    args = p.parse_args()
    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"ERROR: not found: {input_path}", file=sys.stderr)
        return 1
    try:
        slice_seamed(
            input_path,
            Path(args.output_dir),
            cols=args.cols,
            rows=args.rows,
            split_mode=args.split_mode,
            master_out=Path(args.master_out) if args.master_out else None,
            manifest_path=Path(args.manifest) if args.manifest else None,
        )
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
