"""Copy a generated filing to ``internal/public/{slug}.pdf`` for the short tap URL.

The slug, long download filename, and Vercel Content-Disposition header live
in ``internal/public/short-links.json``. After adding an entry, run::

    node internal/scripts/sync-short-links.mjs

Never put the court-style filename in a Vercel redirect destination.
"""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def publish_short_link(src: Path | str, slug: str) -> Path:
    """Copy ``src`` to ``internal/public/{slug}.pdf``. Returns the dest path."""
    dest = REPO_ROOT / "internal/public" / f"{slug}.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return dest
