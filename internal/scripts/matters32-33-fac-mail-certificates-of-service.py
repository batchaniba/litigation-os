#!/usr/bin/env python3
"""Deprecated shim - FAC mail proofs of service now use the E.D. Cal.-style
N.D. Cal. form generator.

Run:  python3 internal/scripts/ndcal-proof-of-service.py
"""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("ndcal-proof-of-service.py")), run_name="__main__")
