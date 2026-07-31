#!/usr/bin/env python3
# ==========================================================
# Builds a full-text search index across every PDF/DOCX in
# internal/public/documents/, so cross-document verification (does this
# quote actually appear in the Petition, which exhibit number is this)
# is a search instead of a "which of 475 files do I need to open" hunt.
#
# Output: internal/docs/document_index.jsonl -- one JSON object per line
# (matter, label-less filename, relative path, page/paragraph count,
# extracted text), so it's both machine-parseable and directly greppable:
#
#   grep -i "designated recipient" internal/docs/document_index.jsonl
#
# For a nicer CLI with matter/path/snippet output, use
# internal/scripts/search-documents.py instead of raw grep.
#
# Usage: python3 internal/scripts/build-document-index.py
# ==========================================================
import json
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DOCS_ROOT = os.path.join(REPO_ROOT, "internal", "public", "documents")
OUT_PATH = os.path.join(REPO_ROOT, "internal", "docs", "document_index.jsonl")

try:
    import fitz  # PyMuPDF
except ImportError:
    os.system(f"{sys.executable} -m pip install -q pymupdf")
    import fitz

try:
    import docx
except ImportError:
    os.system(f"{sys.executable} -m pip install -q python-docx")
    import docx


def matter_for(rel_path):
    parts = rel_path.split(os.sep)
    if parts and parts[0].startswith("matter-"):
        try:
            return int(parts[0].replace("matter-", ""))
        except ValueError:
            return None
    return None


def extract_pdf(full_path):
    doc = fitz.open(full_path)
    text = "\n".join(page.get_text() for page in doc)
    pages = len(doc)
    doc.close()
    return text, pages


def extract_docx(full_path):
    d = docx.Document(full_path)
    text = "\n".join(p.text for p in d.paragraphs)
    return text, None


def main():
    start = time.time()
    entries = []
    errors = []
    skipped = 0

    for root, _dirs, files in os.walk(DOCS_ROOT):
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in (".pdf", ".docx"):
                continue
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, DOCS_ROOT)
            try:
                if ext == ".pdf":
                    text, pages = extract_pdf(full_path)
                else:
                    text, pages = extract_docx(full_path)
            except Exception as e:  # noqa: BLE001 -- best-effort across ~475 heterogeneous files
                errors.append(f"{rel_path}: {e}")
                skipped += 1
                continue

            text = text.strip()
            entries.append({
                "matter": matter_for(rel_path),
                "path": f"/documents/{rel_path}",
                "filename": fname,
                "pages": pages,
                "chars": len(text),
                "text": text,
            })

    entries.sort(key=lambda e: (e["matter"] if e["matter"] is not None else 9999, e["path"]))

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    elapsed = time.time() - start
    total_chars = sum(e["chars"] for e in entries)
    empty = sum(1 for e in entries if e["chars"] == 0)

    print(f"Indexed {len(entries)} documents ({total_chars:,} chars total) in {elapsed:.1f}s")
    print(f"  {empty} document(s) yielded no extractable text (likely scanned images, no OCR run)")
    print(f"  {skipped} document(s) failed to extract and were skipped")
    if errors:
        print("\nErrors:")
        for e in errors[:20]:
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
