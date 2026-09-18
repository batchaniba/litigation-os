#!/usr/bin/env python3
"""RETIRED — August 26 wet-ink / "house" stamp extractor.

Deleted September 18, 2026. The wet-ink source JPEG and the bbox/painted
house stamps are gone. The live canonical stamp is the photographed loops
mark at brendan-newanforbi-signature.png (rebuild with
process-signature-photo.py).

This script refuses to run so it cannot recreate the house stamp onto the
canonical path.
"""
from __future__ import annotations

import sys


def main() -> None:
    raise SystemExit(
        "extract-signature-scan.py is retired. The August 26 wet-ink / house "
        "signature was deleted. Use process-signature-photo.py to rebuild "
        "the photographed loops mark as the canonical stamp."
    )


if __name__ == "__main__":
    main()
    sys.exit(1)
