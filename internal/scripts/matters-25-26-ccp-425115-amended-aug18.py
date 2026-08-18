#!/usr/bin/env python3
"""Re-execute the Matter 25/26 amended CCP §425.115 notices for August 18, 2026.

Same operative text as the unsigned August 7, 2026 generated originals
($250,000.00; supersedes the August 4, 2026 $25,000.00 notices), dated
August 18, 2026 and signed with the portfolio universal signature.
Does not overwrite the August 7 or August 17 files.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sys

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(SCRIPT_DIR))
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

SOURCE = SCRIPT_DIR / "matters25-26-27-29-ccp-425115-punitive-notices.py"
EXEC_DATE = "August 18, 2026"
KEEP_MATTERS = {25, 26}


def load_generator():
    spec = importlib.util.spec_from_file_location("ccp425115_notices", SOURCE)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load generator: {SOURCE}")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    gen.EXEC_DATE = EXEC_DATE
    gen.SIGNATURE_IMG = SIGNATURE_PATH
    gen.SIG_IMG_W_PX, gen.SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
    return gen


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    gen = load_generator()
    paths = []
    for matter in gen.MATTERS:
        if matter["matter"] not in KEEP_MATTERS:
            continue
        for defendant in matter["defendants"]:
            old = defendant["filename"]
            if "Aug 7 2026" not in old:
                raise SystemExit(f"Unexpected filename (need Aug 7 stem to retag): {old}")
            defendant["filename"] = old.replace("Aug 7 2026", "Aug 18 2026")
            out = Path(gen.build_notice(matter, defendant))
            if not out.is_file() or out.stat().st_size < 10_000:
                raise SystemExit(f"Bad output: {out}")
            paths.append(out)
    print(f"Done — {len(paths)} signed amended notices, execution date {EXEC_DATE}.")
    for p in paths:
        print(f"  {p.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
