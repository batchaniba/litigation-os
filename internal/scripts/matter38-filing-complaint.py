#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility shim — live Matter 38 generator is matter38-edca-complaint.py.

The San Joaquin state-court draft on this path was converted to an E.D. Cal.
Sacramento diversity complaint. Keep the old command working.

    python3 internal/scripts/matter38-filing-complaint.py
    python3 internal/scripts/matter38-filing-complaint.py --dump-md
"""

from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parent / "matter38-edca-complaint.py"),
    run_name="__main__",
)
