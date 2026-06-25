#!/usr/bin/env python3
"""Carousel Kie generation modes.

Default: grid_3x3: one 3:4 @ 4K master -> slice 3x3 -> 9 slides.
3:4 is intentional because Kie 4K may not support 4:5.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from kie_client import KieImageClient
from kie_common import find_env_file

SCRIPT_DIR = Path(__file__).resolve().parent
SLICE_GRID = SCRIPT_DIR / "slice_grid.py"

SLIDE_COUNT = 9
GRID_COLS = 3
GRID_ROWS = 3
DEFAULT_ASPECT = "3:4"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slide_copy_map(workspace: Path) -> dict[int, dict[str, Any]]:
    copy_path = workspace / "carusel-memory/design/CAROUSEL_SLIDE_COPY.json"
    if not copy_path.exists():
        return {}
    data = load_json(copy_path)
    return {int(s["index"]): s for s in (data.get("slides") or []) if "index" in s}


def panel_brief_map(prompt_data: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(b["slide"]): b for b in (prompt_data.get("panel_visual_brief") or []) if "slide" in b}


def build_grid_master_prompt(prompt_data: dict[str, Any], workspace: Path) -> str:
    """Full Russian prompt for single grid master."""
    base = (prompt_data.get("prompt") or "").strip()
    if base and "3×3" in base or "3x3" in base.lower():
        return base

    copy_by = slide_copy_map(workspace)
    brief_by = panel_brief_map(prompt_data)
    style = prompt_data.get("style_lock") or {}
    palette = ", ".join(style.get("palette") or [])

    lines = [
        "Одно изображение — превью-сетка Instagram-карусели: ровно 9 равных панелей в сетке 3 колонки x 3 ряда.",
        "Каждая панель — вертикальный формат 3:4 (как отдельный слайд). НЕ горизонтальная полоса. НЕ 2×3.",
        "Весь текст держать внутри safe-area: минимум 10–12% от линий сетки и краёв ячейки.",
        "Между панелями тонкие визуальные границы или единый стиль бренда; каждая ячейка — самостоятельная композиция.",
        f"Палитра: {palette}." if palette else "",
        "",
        "Порядок панелей (слева направо, сверху вниз):",
    ]

    for i in range(1, SLIDE_COUNT + 1):
        copy = copy_by.get(i, {})
        brief = brief_by.get(i, {})
        headline = (copy.get("headline") or "").strip()
        body = (copy.get("body") or "").strip()
        visual = (brief.get("visual_only") or "").strip()
        role = brief.get("role") or copy.get("role") or "value"
        lines.append(
            f"Панель {i} ({role}): «{headline}». {body} Визуал: {visual}".strip()
        )

    negative = (prompt_data.get("negative_prompt") or "").strip()
    if negative:
        lines.extend(["", f"Избегать: {negative}"])

    if base:
        lines.extend(["", "Доп. контекст:", base])

    return "\n".join(line for line in lines if line)


def adapt_prompt_for_aspect(prompt: str, aspect_ratio: str) -> str:
    if aspect_ratio == DEFAULT_ASPECT:
        return (
            prompt.replace("4:5", "3:4")
            .replace("1632×2048", "1536×2048")
            .replace("1632x2048", "1536x2048")
            .replace("1080×1350", "3:4")
            .replace("1080x1350", "3:4")
            .replace("2K", "4K")
        )
    return prompt


def write_task_log(path: Path | None, data: dict[str, Any]) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Task log: {path}")


def run_grid_3x3(
    client: KieImageClient,
    prompt_data: dict[str, Any],
    workspace: Path,
    task_log_path: Path | None,
    resolution: str,
    input_urls: list[str],
    callback_url: str | None,
    bleed_crop_top: int = 0,
) -> int:
    requested_aspect = prompt_data.get("aspect_ratio") or DEFAULT_ASPECT
    aspect_ratio = requested_aspect
    prompt = adapt_prompt_for_aspect(build_grid_master_prompt(prompt_data, workspace), aspect_ratio)
    if aspect_ratio != DEFAULT_ASPECT:
        print(
            f"WARN: grid_3x3 default is aspect_ratio {DEFAULT_ASPECT} @ 4K, got {aspect_ratio}",
            file=sys.stderr,
        )

    master_dir = workspace / "carusel-memory/output/master"
    slides_dir = workspace / "carusel-memory/output/slides"
    master_dir.mkdir(parents=True, exist_ok=True)
    slides_dir.mkdir(parents=True, exist_ok=True)

    source_out = master_dir / "source.png"
    master_out = master_dir / "master.png"
    manifest = workspace / "carusel-memory/output/slice-manifest.json"

    print(f"=== grid_3x3: one Kie task aspect={aspect_ratio} resolution={resolution} ===")
    print(f"Prompt length: {len(prompt)} chars")

    task_id = client.create_task(
        prompt=prompt,
        input_urls=input_urls or None,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        callback_url=callback_url,
    )
    print(f"taskId: {task_id}")

    data = client.wait_for_task(task_id)
    urls = client.extract_result_urls(data)
    if not urls:
        print("ERROR: no resultUrls", file=sys.stderr)
        return 1

    client.download(urls[0], source_out)
    print(f"Downloaded: {source_out} ({source_out.stat().st_size} bytes)")

    log = {
        "generation_mode": "grid_3x3",
        "taskId": task_id,
        "resultUrls": urls,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "aspect_ratio_requested": requested_aspect,
        "aspect_ratio_fallback": False,
        "aspect_ratio_fallback_reason": None,
        "resolution": resolution,
        "grid": {"cols": GRID_COLS, "rows": GRID_ROWS},
        "slide_count": SLIDE_COUNT,
        "source_path": str(source_out.resolve()),
        "slides_dir": str(slides_dir.resolve()),
        "animate_slide": 1,
        "slice_status": "pending",
    }
    write_task_log(task_log_path, log)

    cmd = [
        sys.executable,
        str(SLICE_GRID),
        "--input",
        str(source_out.resolve()),
        "--output-dir",
        str(slides_dir.resolve()),
        "--cols",
        str(GRID_COLS),
        "--rows",
        str(GRID_ROWS),
        "--master-out",
        str(master_out.resolve()),
        "--manifest",
        str(manifest.resolve()),
    ]
    if bleed_crop_top > 0:
        cmd.extend(["--bleed-crop-top", str(bleed_crop_top)])
    print("Slicing:", " ".join(cmd))
    rc = subprocess.run(cmd, check=False).returncode
    if rc != 0:
        log["slice_status"] = "failed"
        log["slice_exit_code"] = rc
        write_task_log(task_log_path, log)
        return rc

    log["slice_status"] = "ok"
    write_task_log(task_log_path, log)

    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Carusel Kie generation from CAROUSEL_IMAGE_PROMPT.json")
    p.add_argument("--workspace", default=".")
    p.add_argument("--prompt-json", default="carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json")
    p.add_argument("--api-key", default=None)
    p.add_argument(
        "--bleed-crop-top",
        type=int,
        default=0,
        help="Crop N px from top of rows 2+ during slice (0=off)",
    )
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    prompt_path = Path(args.prompt_json)
    if not prompt_path.is_absolute():
        prompt_path = workspace / prompt_path
    if not prompt_path.exists():
        print(f"ERROR: {prompt_path} not found", file=sys.stderr)
        return 1

    env_file = find_env_file()
    if env_file:
        print(f"Env: {env_file}")

    data = load_json(prompt_path)
    mode = data.get("generation_mode") or "grid_3x3"
    resolution = data.get("resolution") or "4K"
    input_urls = list(data.get("input_urls") or [])
    callback_url = os.getenv("KIE_CALLBACK_URL") or data.get("callback_url")

    client = KieImageClient(api_key=args.api_key)
    task_log = workspace / "carusel-memory/output/kie-task-log.json"

    if mode == "grid_3x3":
        return run_grid_3x3(
            client, data, workspace, task_log, resolution, input_urls, callback_url,
            bleed_crop_top=max(0, args.bleed_crop_top),
        )

    print(f"ERROR: unsupported generation_mode: {mode}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
