#!/usr/bin/env python3
"""Run Grok video from CAROUSEL_VIDEO_PROMPT.json."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
GROK_GEN = SCRIPT_DIR / "grok_video_gen.py"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--prompt-json",
        default="carusel-memory/design/CAROUSEL_VIDEO_PROMPT.json",
    )
    p.add_argument("--workspace", default=".")
    p.add_argument("--image-url", help="Override HTTPS URL for slide-01")
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    cmd = [
        sys.executable,
        str(GROK_GEN),
        "--workspace",
        str(workspace),
        "--prompt-json",
        args.prompt_json,
    ]
    if args.image_url:
        cmd.extend(["--image-url", args.image_url])

    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
