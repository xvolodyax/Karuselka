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
SEAM_SLICE = SCRIPT_DIR / "seam_slice_grid.py"
REMOVE_GRID_GUTTERS = SCRIPT_DIR / "remove_grid_gutters.py"
CLEAN_SLIDE_EDGES = SCRIPT_DIR / "clean_slide_edges.py"
GRID_GUTTER_QA = SCRIPT_DIR / "grid_gutter_qa.py"

SLIDE_COUNT = 9
GRID_COLS = 3
GRID_ROWS = 3
DEFAULT_ASPECT = "3:4"
# After seam cut, leftover white can sit on cell edges (row-2 bottoms).
# Strip at least that leftover; 10 covers the typical ~9px Kie 4K sliver.
SEAM_EDGE_STRIP_DEFAULT = 10
SEAM_PREFIX = (
    "Canvas 3:4 @ 4K exact 3x3; nine 3:4 panels; thin white gutters; no bleed. "
    "Draw two vertical and two horizontal #ffffff seams at exactly 1/3 and 2/3, "
    "edge to edge, 6–12px, like a window pane. No white border on the outer canvas. "
    "People and animals live inside each night scene."
)


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


def _ensure_seam_language(text: str, slice_method: str) -> str:
    if slice_method != "seam":
        return text
    lowered = text.lower()
    if "thin white gutter" in lowered:
        return text
    return f"{SEAM_PREFIX}\n{text}"


def build_grid_master_prompt(prompt_data: dict[str, Any], workspace: Path) -> str:
    """Full Russian prompt for single grid master."""
    base = (prompt_data.get("prompt") or "").strip()
    slice_method = str(prompt_data.get("slice_method") or "seam")
    negative = (prompt_data.get("negative_prompt") or "").strip()

    def with_negative(text: str) -> str:
        # Kie 4K i2i 422s on ~4900-char prompts. Keep assembled prompt ≤4500.
        if negative and negative not in text and "NEGATIVE:" not in text:
            combined = f"{text}\n\nИзбегать: {negative}"
            if len(combined) <= 4500:
                text = combined
        return _ensure_seam_language(text, slice_method)

    if base and ("3×3" in base or "3x3" in base.lower()):
        return with_negative(base)

    copy_by = slide_copy_map(workspace)
    brief_by = panel_brief_map(prompt_data)
    style = prompt_data.get("style_lock") or {}
    palette = ", ".join(style.get("palette") or [])

    lines = [
        "Одно изображение — превью-сетка Instagram-карусели: ровно 9 равных панелей в сетке 3 колонки x 3 ряда.",
        "Каждая панель — вертикальный формат 3:4 (как отдельный слайд). НЕ горизонтальная полоса. НЕ 2×3.",
        "Весь текст держать внутри safe-area: минимум 10–12% от швов и краёв ячейки.",
        "Canvas exact 3x3; thin white gutters on the 1/3 and 2/3 lines; no bleed. Code cuts on those seams.",
        "People and animals live inside each scene. No outer white frame around the whole canvas.",
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

    if negative:
        lines.extend(["", f"Избегать: {negative}"])

    if base:
        lines.extend(["", "Доп. контекст:", base])

    return with_negative("\n".join(line for line in lines if line))


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


def leftover_gutter_px(width: int, height: int, cols: int = GRID_COLS, rows: int = GRID_ROWS) -> int:
    """Pixels left after integer 3x3 split. Kie 4K 2480x3312 -> width remainder 2."""
    if width <= 0 or height <= 0:
        return 0
    return max(width % cols, height % rows)


def seam_edge_strip_px(
    width: int,
    height: int,
    cols: int = GRID_COLS,
    rows: int = GRID_ROWS,
    default: int = SEAM_EDGE_STRIP_DEFAULT,
) -> int:
    """clean_slide_edges strip: at least leftover gutter, default 10."""
    return max(default, leftover_gutter_px(width, height, cols, rows))


def source_size_from_manifest(manifest: Path) -> tuple[int, int]:
    if not manifest.is_file():
        return (0, 0)
    data = load_json(manifest)
    size = data.get("source_size") or {}
    return (int(size.get("width") or 0), int(size.get("height") or 0))


def run_subprocess_step(name: str, cmd: list[str]) -> int:
    print(f"{name}:", " ".join(cmd))
    return subprocess.run(cmd, check=False).returncode


def run_slide_edge_cleanup(
    slides_dir: Path,
    debug_dir: Path,
    strip: int,
    log: dict[str, Any],
) -> int:
    log["edge_cleanup"]["enabled"] = True
    log["edge_cleanup"]["strip"] = strip
    rc = run_subprocess_step(
        "Slide edge cleanup",
        [
            sys.executable,
            str(CLEAN_SLIDE_EDGES),
            "--slides-dir",
            str(slides_dir.resolve()),
            "--slides",
            "1-9",
            "--strip",
            str(strip),
            "--edges",
            "top,right,bottom,left",
            "--report",
            str((debug_dir / "clean-slide-edges-report.json").resolve()),
        ],
    )
    if rc != 0:
        log["edge_cleanup"]["status"] = "failed"
        log["edge_cleanup"]["exit_code"] = rc
        return rc
    log["edge_cleanup"]["status"] = "ok"
    return 0


def run_gutter_qa(
    master_out: Path,
    slides_dir: Path,
    debug_dir: Path,
    log: dict[str, Any],
    *,
    mode: str = "equal",
) -> int:
    log["gutter_qa"]["enabled"] = True
    log["gutter_qa"]["mode"] = mode
    cmd = [
        sys.executable,
        str(GRID_GUTTER_QA),
        "--master",
        str(master_out.resolve()),
        "--slides-dir",
        str(slides_dir.resolve()),
        "--mode",
        mode,
        "--max-internal-white",
        "0.20",
        "--max-edge-white",
        "0.35",
        "--output",
        str((debug_dir / "grid-gutter-qa-clean.json").resolve()),
    ]
    rc = run_subprocess_step("Gutter QA", cmd)
    if rc != 0:
        log["gutter_qa"]["status"] = "failed"
        log["gutter_qa"]["exit_code"] = rc
        return rc
    log["gutter_qa"]["status"] = "ok"
    return 0


def run_grid_3x3(
    client: KieImageClient,
    prompt_data: dict[str, Any],
    workspace: Path,
    task_log_path: Path | None,
    resolution: str,
    input_urls: list[str],
    callback_url: str | None,
    bleed_crop_top: int = 0,
    gutter_cleanup: bool = True,
    edge_cleanup: bool = True,
    gutter_qa: bool = True,
    slice_method: str | None = None,
) -> int:
    requested_aspect = prompt_data.get("aspect_ratio") or DEFAULT_ASPECT
    aspect_ratio = requested_aspect
    method = (slice_method or prompt_data.get("slice_method") or "seam").strip().lower()
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
    source_clean_out = master_dir / "source-zero-gutter-clean.png"
    master_out = master_dir / "master.png"
    manifest = workspace / "carusel-memory/output/slice-manifest.json"
    debug_dir = workspace / "carusel-memory/output/debug"
    debug_dir.mkdir(parents=True, exist_ok=True)

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
        "source_clean_path": str(source_clean_out.resolve()) if method != "seam" and gutter_cleanup else None,
        "slides_dir": str(slides_dir.resolve()),
        "animate_slide": 1,
        "slice_method": method,
        "slice_status": "pending",
        "gutter_cleanup": {
            "enabled": method != "seam" and gutter_cleanup,
            "method": "near-white pixels on exact cut-lines; no crop, no resize",
            "strip": 5,
            "report": str((debug_dir / "remove-grid-gutters-report.json").resolve()),
        },
        "edge_cleanup": {
            "enabled": edge_cleanup,
            "method": "copy interior pixels over outer edge strips after slice; no crop, no resize",
            "strip": SEAM_EDGE_STRIP_DEFAULT if method == "seam" else 3,
            "report": str((debug_dir / "clean-slide-edges-report.json").resolve()),
        },
        "gutter_qa": {
            "enabled": gutter_qa,
            "report": str((debug_dir / "grid-gutter-qa-clean.json").resolve()),
        },
    }
    write_task_log(task_log_path, log)

    if method == "seam":
        rc = run_subprocess_step(
            "Seam slice (Excalibur white gutters)",
            [
                sys.executable,
                str(SEAM_SLICE),
                "--input",
                str(source_out.resolve()),
                "--output-dir",
                str(slides_dir.resolve()),
                "--cols",
                str(GRID_COLS),
                "--rows",
                str(GRID_ROWS),
                "--split-mode",
                "gutter",
                "--master-out",
                str(master_out.resolve()),
                "--manifest",
                str(manifest.resolve()),
                "--target-width",
                "1080",
                "--target-height",
                "1440",
            ],
        )
        if rc != 0:
            log["slice_status"] = "failed"
            log["slice_exit_code"] = rc
            log["crooked_canvas"] = rc == 2
            write_task_log(task_log_path, log)
            if rc == 2:
                print(
                    "CROOKED CANVAS: white seams missing or offset. Rebuild the whole master.",
                    file=sys.stderr,
                )
            return rc
        log["slice_status"] = "ok"
        src_w, src_h = source_size_from_manifest(manifest)
        leftover = leftover_gutter_px(src_w, src_h)
        strip = seam_edge_strip_px(src_w, src_h)
        log["edge_cleanup"]["leftover_gutter_px"] = leftover
        log["edge_cleanup"]["strip"] = strip
        if edge_cleanup:
            rc = run_slide_edge_cleanup(slides_dir, debug_dir, strip, log)
            if rc != 0:
                log["slice_status"] = "failed"
                write_task_log(task_log_path, log)
                return rc
        else:
            log["edge_cleanup"]["enabled"] = False
        if gutter_qa:
            rc = run_gutter_qa(master_out, slides_dir, debug_dir, log, mode="seam")
            if rc != 0:
                log["slice_status"] = "failed"
                write_task_log(task_log_path, log)
                return rc
        else:
            log["gutter_qa"]["enabled"] = False
        write_task_log(task_log_path, log)
        return 0

    source_for_slice = source_out
    if gutter_cleanup:
        rc = run_subprocess_step(
            "Zero-gutter cleanup",
            [
                sys.executable,
                str(REMOVE_GRID_GUTTERS),
                "--input",
                str(source_out.resolve()),
                "--output",
                str(source_clean_out.resolve()),
                "--cols",
                str(GRID_COLS),
                "--rows",
                str(GRID_ROWS),
                "--strip",
                "5",
                "--white-threshold",
                "235",
                "--scrub-outer-frame",
                "--report",
                str((debug_dir / "remove-grid-gutters-report.json").resolve()),
            ],
        )
        if rc != 0:
            log["slice_status"] = "failed"
            log["gutter_cleanup"]["status"] = "failed"
            log["gutter_cleanup"]["exit_code"] = rc
            write_task_log(task_log_path, log)
            return rc
        log["gutter_cleanup"]["status"] = "ok"
        source_for_slice = source_clean_out

    cmd = [
        sys.executable,
        str(SLICE_GRID),
        "--input",
        str(source_for_slice.resolve()),
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
    rc = run_subprocess_step("Slicing", cmd)
    if rc != 0:
        log["slice_status"] = "failed"
        log["slice_exit_code"] = rc
        write_task_log(task_log_path, log)
        return rc

    if edge_cleanup:
        rc = run_slide_edge_cleanup(slides_dir, debug_dir, 3, log)
        if rc != 0:
            log["slice_status"] = "failed"
            write_task_log(task_log_path, log)
            return rc

    if gutter_qa:
        rc = run_gutter_qa(master_out, slides_dir, debug_dir, log, mode="equal")
        if rc != 0:
            log["slice_status"] = "failed"
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
    p.add_argument(
        "--no-gutter-cleanup",
        action="store_true",
        help="Disable automatic zero-gutter cleanup before slicing",
    )
    p.add_argument(
        "--no-edge-cleanup",
        action="store_true",
        help="Disable automatic 1-3px edge artifact cleanup after slicing",
    )
    p.add_argument(
        "--no-gutter-qa",
        action="store_true",
        help="Disable gutter/frame QA after slicing",
    )
    p.add_argument(
        "--legacy-zero-gutter",
        action="store_true",
        help="Retired path: scrub cut-lines instead of Excalibur seam slice",
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
        if args.legacy_zero_gutter:
            data["slice_method"] = "zero-gutter"
        return run_grid_3x3(
            client, data, workspace, task_log, resolution, input_urls, callback_url,
            bleed_crop_top=max(0, args.bleed_crop_top),
            gutter_cleanup=not args.no_gutter_cleanup,
            edge_cleanup=not args.no_edge_cleanup,
            gutter_qa=not args.no_gutter_qa,
            slice_method=data.get("slice_method") or "seam",
        )

    print(f"ERROR: unsupported generation_mode: {mode}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
