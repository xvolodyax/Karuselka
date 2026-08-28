#!/usr/bin/env python3
"""Retired. Do not crop a 12-up sheet.

Identity lock is carusel-memory/references/viktoriaref.png only.
"""

from __future__ import annotations

import sys


def crop_front_closeup(*_args, **_kwargs):
    raise SystemExit(
        "STOP: do not crop victoria-sheet.png. "
        "i2i ONLY carusel-memory/references/viktoriaref.png"
    )


def crop_tight(*_args, **_kwargs):
    return crop_front_closeup(*_args, **_kwargs)


def main() -> int:
    print(
        "STOP: crop_victoria_sheet_tight is retired. "
        "Use carusel-memory/references/viktoriaref.png as the only i2i face.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
