#!/usr/bin/env python3
# ==========================================================
# Search the full-text document index built by build-document-index.py.
#
# Usage:
#   python3 internal/scripts/search-documents.py "designated recipient"
#   python3 internal/scripts/search-documents.py "certifying official" --matter 20
#   python3 internal/scripts/search-documents.py "214.14" -i     # case-insensitive
#
# Prints matter number, filename, and a short context snippet around each
# match, so verifying a quote or finding which document mentions a phrase
# is a search instead of manually opening files one at a time.
# ==========================================================
import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
INDEX_PATH = os.path.join(REPO_ROOT, "internal", "docs", "document_index.jsonl")

CONTEXT_CHARS = 80


def main():
    ap = argparse.ArgumentParser(description="Search the portfolio's full-text document index.")
    ap.add_argument("query", help="Text to search for (plain substring, not regex, unless --regex)")
    ap.add_argument("--matter", type=int, default=None, help="Restrict to a single matter number")
    ap.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    ap.add_argument("--regex", action="store_true", help="Treat query as a regular expression")
    ap.add_argument("--max-results", type=int, default=40)
    args = ap.parse_args()

    if not os.path.exists(INDEX_PATH):
        print(f"No index found at {INDEX_PATH}. Run build-document-index.py first.", file=sys.stderr)
        sys.exit(1)

    flags = re.IGNORECASE if args.ignore_case else 0
    pattern = re.compile(args.query if args.regex else re.escape(args.query), flags)

    hits = 0
    with open(INDEX_PATH) as f:
        for line in f:
            entry = json.loads(line)
            if args.matter is not None and entry.get("matter") != args.matter:
                continue
            text = entry.get("text", "")
            for m in pattern.finditer(text):
                if hits >= args.max_results:
                    print(f"\n... stopped at --max-results={args.max_results}, refine your query for more.")
                    return
                start = max(0, m.start() - CONTEXT_CHARS)
                end = min(len(text), m.end() + CONTEXT_CHARS)
                snippet = text[start:end].replace("\n", " ")
                matter_tag = f"Matter {entry['matter']}" if entry.get("matter") is not None else "(unmatched matter)"
                print(f"[{matter_tag}] {entry['filename']}")
                print(f"  ...{snippet}...")
                print(f"  path: {entry['path']}\n")
                hits += 1

    if hits == 0:
        print("No matches.")
    else:
        print(f"{hits} match(es).")


if __name__ == "__main__":
    main()
