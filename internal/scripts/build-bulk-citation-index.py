#!/usr/bin/env python3
"""Build the local SQLite index for the offline citation-existence oracle.

Downloads the CourtListener bulk citations table (public S3, no auth) and
builds a SQLite index on (reporter, volume, page) -> cluster_id.

The DB lives OUTSIDE the repo (default: ~/workspace/legal-research/citation-bulk/).
lookup-citations.py finds it via $CL_BULK_SQLITE or the default path and
probes it as step 0. If the DB is absent, the probe skips gracefully.

Schema of the bulk table: id,volume,reporter,page,type,cluster_id,
date_created,date_modified. Quarterly refresh; this wires the 2026-06-30
snapshot (edit SNAPSHOT + URL for newer quarters).

Usage:
  python3 internal/scripts/build-bulk-citation-index.py            # download + build
  python3 internal/scripts/build-bulk-citation-index.py --skip-download
  python3 internal/scripts/build-bulk-citation-index.py --check-strings
"""

from __future__ import annotations

import argparse
import bz2
import csv
import os
import sqlite3
import sys
import urllib.request
from pathlib import Path

SNAPSHOT = "2026-06-30"
S3_URL = (
    "https://com-courtlistener-storage.s3.amazonaws.com"
    f"/bulk-data/citations-{SNAPSHOT}.csv.bz2"
)
DEFAULT_DIR = Path.home() / "workspace/legal-research/citation-bulk"

# Every reporter string lookup-citations.py maps to (BULK_REPORTER values).
# --check-strings verifies each one occurs at least once in the snapshot.
EXPECTED_REPORTERS = {
    "U.S.", "S. Ct.", "L. Ed. 2d",
    "F.2d", "F.3d", "F.4th", "F. App'x",
    "F. Supp. 2d", "F. Supp. 3d", "F.R.D.", "M.J.",
    "Cal. 2d", "Cal. 3d", "Cal. 4th", "Cal. 5th",
    "Cal. App. 3d", "Cal. App. 4th", "Cal. App. 5th",
}


def download(dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        S3_URL, headers={"User-Agent": "litigation-portfolio-bulk-index/1.0"}
    )
    print(f"downloading {S3_URL}", file=sys.stderr)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    print(f"saved {dest} ({dest.stat().st_size / 1e6:.1f} MB)", file=sys.stderr)


def iter_rows(bz2_path: Path):
    with open(bz2_path, "rb") as fh:
        dec = bz2.BZ2Decompressor()
        buf = ""
        header_done = False
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break  # EOF: trailing partial line handled in buf below
            data = dec.decompress(chunk)
            if not data:
                continue
            buf += data.decode("utf-8", "replace")
            lines = buf.split("\n")
            buf = lines.pop()
            if not header_done:
                header = lines.pop(0)
                assert header.strip() == "id,volume,reporter,page,type,cluster_id,date_created,date_modified", header
                header_done = True
            for line in lines:
                if line.strip():
                    yield next(csv.reader([line]))
        if buf.strip():
            yield next(csv.reader([buf]))


def build(bz2_path: Path, db_path: Path) -> None:
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.execute(
        "CREATE TABLE citations ("
        " reporter TEXT NOT NULL, volume TEXT NOT NULL, page TEXT NOT NULL,"
        " cite_type TEXT, cluster_id INTEGER NOT NULL)"
    )
    batch = []
    n = 0
    for row in iter_rows(bz2_path):
        # id,volume,reporter,page,type,cluster_id,date_created,date_modified
        batch.append((row[2], row[1], row[3], row[4], int(row[5])))
        if len(batch) >= 50000:
            con.executemany("INSERT INTO citations VALUES (?,?,?,?,?)", batch)
            batch = []
            n += 50000
            if n % 1000000 == 0:
                print(f"  {n // 1000000}M rows", file=sys.stderr)
    if batch:
        con.executemany("INSERT INTO citations VALUES (?,?,?,?,?)", batch)
        n += len(batch)
    con.execute("CREATE INDEX idx_triple ON citations (reporter, volume, page)")
    con.execute("CREATE INDEX idx_cluster ON citations (cluster_id)")
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM citations").fetchone()[0]
    con.close()
    print(f"built {db_path}: {total} rows ({n} inserted)", file=sys.stderr)


def check_strings(bz2_path: Path) -> int:
    found: dict[str, int] = {}
    for row in iter_rows(bz2_path):
        rep = row[2]
        if rep in EXPECTED_REPORTERS and rep not in found:
            found[rep] = 1
            if len(found) == len(EXPECTED_REPORTERS):
                break
    missing = EXPECTED_REPORTERS - set(found)
    print(f"verified reporter strings: {len(found)}/{len(EXPECTED_REPORTERS)}")
    if missing:
        print(f"MISSING: {sorted(missing)}")
        return 1
    print("all BULK_REPORTER strings present in snapshot")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=DEFAULT_DIR,
                    help="local dir for the bz2 + sqlite (NOT the repo)")
    ap.add_argument("--skip-download", action="store_true")
    ap.add_argument("--check-strings", action="store_true",
                    help="verify BULK_REPORTER strings occur in the snapshot; no DB build")
    args = ap.parse_args(argv)
    bz2_path = args.dir / f"citations-{SNAPSHOT}.csv.bz2"
    if args.check_strings:
        if not bz2_path.is_file():
            print(f"missing {bz2_path} — download first", file=sys.stderr)
            return 2
        return check_strings(bz2_path)
    if not args.skip_download or not bz2_path.is_file():
        download(bz2_path)
    db_path = Path(os.environ.get("CL_BULK_SQLITE") or (args.dir / "citations.sqlite"))
    build(bz2_path, db_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
