#!/usr/bin/env python3
"""Verify Carusel Instagram MCP connection and document results."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    workspace = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
    slides_dir = workspace / "carusel-memory" / "output" / "slides"
    report_path = workspace / "carusel-memory" / "output" / "mcp-connection-report.md"

    slides = [slides_dir / f"slide-{i:02d}.png" for i in range(1, 7)]
    missing = [str(p) for p in slides if not p.exists()]

    mcp_tool_schema = {
        "server": "user-instagram carusel",
        "toolName": "t4528_carrusel_instagram",
        "arguments": {
            "file1": str(slides[0].resolve()) if slides[0].exists() else "",
            "file2": str(slides[1].resolve()) if slides[1].exists() else "",
            "File3": str(slides[2].resolve()) if slides[2].exists() else "",
            "file4": str(slides[3].resolve()) if slides[3].exists() else "",
            "file5": str(slides[4].resolve()) if slides[4].exists() else "",
            "file6": str(slides[5].resolve()) if slides[5].exists() else "",
            "caption": "[TEST] Carusel MCP connection check — safe to delete",
        },
        "notes": [
            "Slide 3 parameter MUST be File3 (capital F)",
            "caption max 2200 chars, 30 hashtags, 20 mentions",
        ],
    }

    payload_path = workspace / "carusel-memory" / "output" / "mcp-test-payload.json"
    payload_path.write_text(json.dumps(mcp_tool_schema, indent=2, ensure_ascii=False), encoding="utf-8")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    status = "READY" if not missing else "BLOCKED_MISSING_SLIDES"

    report = f"""# MCP Connection Report

Generated: {now}

## Server

- **server:** `user-instagram carusel`
- **tool:** `t4528_carrusel_instagram`

## Slide files

| Slide | Param | Path | Exists |
|-------|-------|------|--------|
| 1 | file1 | `{slides[0]}` | {slides[0].exists()} |
| 2 | file2 | `{slides[1]}` | {slides[1].exists()} |
| 3 | **File3** | `{slides[2]}` | {slides[2].exists()} |
| 4 | file4 | `{slides[3]}` | {slides[3].exists()} |
| 5 | file5 | `{slides[4]}` | {slides[4].exists()} |
| 6 | file6 | `{slides[5]}` | {slides[5].exists()} |

## Status

**{status}**

"""
    if missing:
        report += f"\nMissing slides: {', '.join(missing)}\n"
    else:
        report += """
## Next step (agent)

Call MCP via CallMcpTool with payload in `mcp-test-payload.json`.

After call, append MCP response to `publish-log.md`.
"""

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"Payload: {payload_path}")
    print(f"Report: {report_path}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
