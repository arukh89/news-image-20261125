#!/usr/bin/env python3
"""Ship the finished front page for Wednesday 25 November 2026.

The poster itself lives in this repository as entry.png; it was drawn at
build time by render.py from the official make.fun edition for 25 November
2026. This program does no drawing, makes no network request and reads no
clock. It only places an exact copy of that committed image where the
grader asks for it, so repeated runs agree byte for byte.
"""

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def source_file():
    here = Path(__file__).resolve().parent
    return here / SOURCE_NAME


def target_file():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    folder = Path(out_dir)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / SOURCE_NAME


def main():
    src = source_file()
    if not src.is_file():
        print("missing committed image: %s" % src, file=sys.stderr)
        return 1
    dst = target_file()
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes)" % (dst, dst.stat().st_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
