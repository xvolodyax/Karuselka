#!/usr/bin/env python3
"""Generate carousel image via Kie.ai gpt-image-2-image-to-image (no MCP).

Flow:
  1. createTask → taskId
  2. poll recordInfo until success
  3. download result URL → local file
  4. optional: fit to 6480x1350 + slice into 6 slides
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from kie_client import KieImageClient
from kie_common import find_env_file

SCRIPT_DIR = Path(__file__).resolve().parent
SLICE_SCRIPT = SCRIPT_DIR / "slice_carousel.py"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Kie.ai image generation for Carusel")
    p.add_argument("--prompt", "-p", required=True, help="Generation prompt")
    p.add_argument(
        "--input-url",
        action="append",
        dest="input_urls",
        default=[],
        help="Reference image URL (repeatable). Required for image-to-image style.",
    )
    p.add_argument(
        "--aspect-ratio",
        default="3:1",
        help="Wide ratio for carousel master (default 3:1, then resized to 6480x1350)",
    )
    p.add_argument("--resolution", default="2K", choices=["1K", "2K", "4K"])
    p.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output path for downloaded source image (e.g. carusel-memory/output/master/source.png)",
    )
    p.add_argument(
        "--workspace",
        default=".",
        help="Workspace root (for slice paths)",
    )
    p.add_argument("--slice", action="store_true", help="After download, slice to 6 slides")
    p.add_argument("--master-out", help="Normalized master 6480x1350 path")
    p.add_argument("--slides-dir", help="Slides output directory")
    p.add_argument("--manifest", help="Slice manifest JSON path")
    p.add_argument("--fit", choices=("cover", "contain"), default="cover")
    p.add_argument("--api-key", help="Override KIE_API_KEY from .env")
    p.add_argument("--task-log", help="JSON log with taskId and result URLs")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    env_file = find_env_file()
    if env_file:
        print(f"Env: {env_file}")
    else:
        print("WARN: .env not found - set KIE_API_KEY or use --api-key", file=sys.stderr)

    client = KieImageClient(api_key=args.api_key)
    print(f"Creating task (model=gpt-image-2-image-to-image, resolution={args.resolution})...")
    task_id = client.create_task(
        prompt=args.prompt,
        input_urls=args.input_urls or None,
        aspect_ratio=args.aspect_ratio,
        resolution=args.resolution,
    )
    print(f"taskId: {task_id}")

    data = client.wait_for_task(task_id)
    urls = client.extract_result_urls(data)
    if not urls:
        print("ERROR: No resultUrls in task result", file=sys.stderr)
        return 1

    output = Path(args.output)
    client.download(urls[0], output)
    print(f"Downloaded: {output} ({output.stat().st_size} bytes)")
    print(f"Result URL: {urls[0]}")

    if args.task_log:
        log_path = Path(args.task_log)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            json.dumps(
                {
                    "taskId": task_id,
                    "resultUrls": urls,
                    "local_path": str(output.resolve()),
                    "prompt": args.prompt,
                    "aspect_ratio": args.aspect_ratio,
                    "resolution": args.resolution,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        print(f"Task log: {log_path}")

    if args.slice:
        workspace = Path(args.workspace).resolve()
        master_out = Path(args.master_out or workspace / "carusel-memory/output/master/master.png")
        slides_dir = Path(args.slides_dir or workspace / "carusel-memory/output/slides")
        manifest = Path(args.manifest or workspace / "carusel-memory/output/slice-manifest.json")

        cmd = [
            sys.executable,
            str(SLICE_SCRIPT),
            "--input",
            str(output.resolve()),
            "--master-out",
            str(master_out),
            "--output-dir",
            str(slides_dir),
            "--manifest",
            str(manifest),
            "--fit",
            args.fit,
        ]
        print("Slicing:", " ".join(cmd))
        result = subprocess.run(cmd, check=False)
        return result.returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
