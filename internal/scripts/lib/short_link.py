"""Short-link taps rewrite to ``/documents/...`` on Vercel.

Do **not** copy a second PDF onto ``main``. Drop the filing in the matter
folder (documents branch), add/update the catalog entry in
``internal/public/short-links.json``, and run::

    npm run sync:short-links

Court-style parentheses never go in a Vercel destination; the sync script
encodes each path segment. The two public-root leftovers (hope-name-stip,
hope-name-motion) are the exception: those packets are not on the documents
branch yet.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def publish_short_link(src: Path | str, slug: str) -> Path:
    """Return the source path. Does not copy onto ``internal/public/{slug}.pdf``."""
    src_path = Path(src)
    if not src_path.is_file():
        raise FileNotFoundError(src_path)
    _ = slug  # catalog slug; Vercel rewrite is generated from short-links.json
    return src_path
