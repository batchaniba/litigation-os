#!/usr/bin/env python3
"""Publish the Matter 19 habeas immediate-discharge petition as a short-link packet.

The complete packet is the April 3, 2026 Petition for Writ of Habeas Corpus
(caption: IMMEDIATE DISCHARGE FROM PAROLE REQUESTED) with Exhibits A–F
already bound — 67 pages, Santa Clara C2604791. This script does not rewrite
that filed pleading. It copies the existing PDF to the phone-tappable slug
and to /opt/cursor/artifacts.

    python3 internal/scripts/matter19-habeas-discharge-packet.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from short_link import publish_short_link  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
PETITION = (
    ROOT
    / "internal/public/documents/matter-19"
    / "Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf"
)
SHORT_LINK_SLUG = "habeas-discharge"
ARTIFACTS_DIR = Path("/opt/cursor/artifacts")
ARTIFACT_PDF = ARTIFACTS_DIR / (
    "Habeas Immediate Discharge Requested Packet "
    "(Santa Clara C2604791 filed Apr 3 2026).pdf"
)


def main() -> None:
    if not PETITION.is_file() or PETITION.stat().st_size < 1000:
        raise SystemExit(f"Missing petition: {PETITION}")
    short = publish_short_link(PETITION, SHORT_LINK_SLUG)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PETITION, ARTIFACT_PDF)
    print(f"source:     {PETITION}")
    print(f"short link: /{SHORT_LINK_SLUG}  ({short.stat().st_size} bytes)")
    print(f"artifact:   {ARTIFACT_PDF}")


if __name__ == "__main__":
    main()
