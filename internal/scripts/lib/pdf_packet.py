"""Concatenate existing PDFs. Matter scripts import these instead of a local loop.

``assemble(paths, out)`` writes a new file. ``append_pdf`` / ``append_page``
mutate a caller-owned ``PdfWriter`` when the packet is built piece by piece
(single pages pulled from a multi-page summons, annotated inserts, etc.).
"""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def page_count(path: Path | str) -> int:
    return len(PdfReader(str(path)).pages)


def append_pdf(writer: PdfWriter, path: Path | str) -> int:
    """Append every page of ``path``. Returns the number of pages added."""
    reader = PdfReader(str(path))
    for page in reader.pages:
        writer.add_page(page)
    return len(reader.pages)


def append_page(writer: PdfWriter, path: Path | str, index: int) -> None:
    """Append one page (0-based) from ``path``."""
    writer.add_page(PdfReader(str(path)).pages[index])


def assemble(paths: list[Path | str], out: Path | str) -> int:
    """Write ``paths`` in order to ``out``. Returns total page count."""
    writer = PdfWriter()
    total = 0
    for path in paths:
        total += append_pdf(writer, path)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as fh:
        writer.write(fh)
    return total
