#!/usr/bin/env python3
"""Video frame QA — compare MP4 frames to source PNG (MAE).

Used by grok_video_gen.py post-animate and design-guardian runbook.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore[misc, assignment]


def _require_pillow() -> None:
    if Image is None:
        raise RuntimeError("Pillow required. pip install Pillow")


def extract_frame(video_path: Path, frame_index: int = 0, out_png: Path | None = None) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found — required for video frame QA")

    if out_png is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.close()
        out_png = Path(tmp.name)
    else:
        out_png.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"select=eq(n\\,{frame_index})",
        "-vframes",
        "1",
        str(out_png),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_png


def compute_mae(png_a: Path, png_b: Path) -> float:
    """Mean absolute error between two RGB images (0-255 scale). Resizes B to A size."""
    _require_pillow()
    with Image.open(png_a) as raw_a, Image.open(png_b) as raw_b:
        a = raw_a.convert("RGB")
        b = raw_b.convert("RGB")
        if a.size != b.size:
            b = b.resize(a.size, Image.Resampling.LANCZOS)
        pa = list(a.getdata())
        pb = list(b.getdata())
        if len(pa) != len(pb):
            raise ValueError(f"Pixel count mismatch after resize: {a.size} vs {b.size}")
        total = sum(abs(x - y) for (r, g, b_), (x, y, z) in zip(pa, pb) for x, y, z in ((r, g, b_),))
        return total / (len(pa) * 3)


def compare_video_to_png(
    video_path: Path,
    png_path: Path,
    *,
    frame_index: int = 0,
    mae_threshold: float = 35.0,
) -> dict[str, float | bool | str]:
    """Extract frame from video, compare to PNG. Returns QA dict."""
    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")
    if not png_path.exists():
        raise FileNotFoundError(f"PNG not found: {png_path}")

    frame_png = extract_frame(video_path, frame_index)
    try:
        mae = compute_mae(png_path, frame_png)
    finally:
        if str(frame_png).startswith(tempfile.gettempdir()):
            frame_png.unlink(missing_ok=True)

    return {
        "frame_index": frame_index,
        "mae": round(mae, 2),
        "threshold": mae_threshold,
        "pass": mae <= mae_threshold,
        "video": str(video_path.resolve()),
        "png": str(png_path.resolve()),
    }


def compare_loop_seam(
    video_path: Path,
    *,
    mae_threshold: float = 15.0,
) -> dict[str, float | bool]:
    """Compare first and last frame MAE for loop continuity."""
    first = extract_frame(video_path, 0)
    last = extract_frame(video_path, -1)  # ffmpeg select last is tricky; use duration probe
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        last_path = Path(tmp.name)
    try:
        cmd = [
            ffmpeg,
            "-y",
            "-sseof",
            "-0.04",
            "-i",
            str(video_path),
            "-vframes",
            "1",
            str(last_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        mae = compute_mae(first, last_path)
    finally:
        first.unlink(missing_ok=True)
        last_path.unlink(missing_ok=True)

    return {"loop_mae": round(mae, 2), "threshold": mae_threshold, "pass": mae <= mae_threshold}


def main() -> int:
    import argparse
    import json

    p = argparse.ArgumentParser(description="Compare video frame to source PNG (MAE)")
    p.add_argument("--video", required=True)
    p.add_argument("--png", required=True)
    p.add_argument("--frame", type=int, default=0)
    p.add_argument("--mae-threshold", type=float, default=35.0)
    p.add_argument("--loop-check", action="store_true")
    args = p.parse_args()

    try:
        result = compare_video_to_png(
            Path(args.video),
            Path(args.png),
            frame_index=args.frame,
            mae_threshold=args.mae_threshold,
        )
        if args.loop_check:
            result["loop"] = compare_loop_seam(Path(args.video))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        ok = bool(result["pass"]) and (not args.loop_check or bool(result["loop"]["pass"]))
        return 0 if ok else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
