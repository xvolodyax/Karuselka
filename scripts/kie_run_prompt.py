#!/usr/bin/env python3
"""Run Kie.ai generation from CAROUSEL_IMAGE_PROMPT.json (delegates to kie_carousel_gen)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CAROUSEL_GEN = SCRIPT_DIR / "kie_carousel_gen.py"


def main() -> int:
    p = argparse.ArgumentParser(description="Generate carousel from CAROUSEL_IMAGE_PROMPT.json")
    p.add_argument("--prompt-json", default="carusel-memory/design/CAROUSEL_IMAGE_PROMPT.json")
    p.add_argument("--workspace", default=".")
    p.add_argument("--slice", action="store_true", help="(legacy) slice is always on for grid_3x3")
    p.add_argument("--no-slice", action="store_true", help="ignored for grid_3x3")
    args = p.parse_args()

    workspace = Path(args.workspace).resolve()
    prompt_path = Path(args.prompt_json)
    if not prompt_path.is_absolute():
        prompt_path = workspace / prompt_path

    cmd = [
        sys.executable,
        str(CAROUSEL_GEN),
        "--workspace",
        str(workspace),
        "--prompt-json",
        str(prompt_path),
    ]
    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
