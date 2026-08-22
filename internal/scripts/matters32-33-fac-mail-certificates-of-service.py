#!/usr/bin/env python3
"""Deprecated shim -- use generate-proof-of-service.py / lib/proof_of_service.py."""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).with_name("generate-proof-of-service.py")),
        run_name="__main__",
    )
