"""Tier 1 extraction: pull text from the record-setting PDFs of each active matter.

Caches per-PDF text under .cache/pdf-audit so re-runs are cheap.
"""
import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
_CACHE_DIR = _os.environ.get("PDF_AUDIT_CACHE", _os.path.join(_REPO, ".cache", "pdf-audit"))
_os.makedirs(_CACHE_DIR, exist_ok=True)
import json, os, re, sys, hashlib
import pdfplumber

DOCS = _os.path.join(_REPO, "internal", "public", "documents")
CACHE = _CACHE_DIR
ACTIVE = [1, 2, 7, 12, 19, 20, 24, 25, 26, 27, 28, 29]
MAX_PAGES = 8
PER_MATTER = 8

# filename keywords that mark a record-setting document, highest signal first
KEY_PATTERNS = [
    (100, r"\bcomplaint\b"),
    (98, r"\bpetition\b"),
    (95, r"findings|f&r|\bf-?r\b"),
    (92, r"\border\b|\bruling\b|tentative"),
    (88, r"objections?"),
    (85, r"scheduling|case assignment|notice of hearing"),
    (82, r"demurrer|motion to dismiss"),
    (78, r"opposition"),
    (70, r"case management statement|cm-?110"),
    (65, r"judgment"),
    (60, r"summons"),
]
SKIP = re.compile(r"blank form|blank-template|receipt|ereceipt|postage|fee waiver|"
                  r"change of address|wage reference|dfpi|transcript|dashcam|"
                  r"e-?filing|proof of service|pos010|garnishee|abstract of judgment|"
                  r"writ of execution|memorandum of costs|claim of exemption", re.I)


def score(name):
    low = name.lower()
    if SKIP.search(low):
        return -1
    best = 0
    for weight, pat in KEY_PATTERNS:
        if re.search(pat, low):
            best = max(best, weight)
    # prefer filed/court-stamped copies and later-dated versions
    if re.search(r"filed|stamped|electronically", low):
        best += 4
    if re.search(r"draft|proposed|pre-?drafted|pending", low):
        best -= 12
    return best


def select(matter):
    d = os.path.join(DOCS, f"matter-{matter:02d}")
    if not os.path.isdir(d):
        return []
    cands = [f for f in os.listdir(d) if f.lower().endswith(".pdf")]
    scored = sorted(((score(f), f) for f in cands), key=lambda x: (-x[0], x[1]))
    return [os.path.join(d, f) for s, f in scored if s > 0][:PER_MATTER]


def extract(path):
    key = hashlib.sha1(path.encode()).hexdigest()[:16]
    out = os.path.join(CACHE, key + ".json")
    if os.path.exists(out):
        return json.load(open(out))
    pages = []
    try:
        with pdfplumber.open(path) as pdf:
            for p in pdf.pages[:MAX_PAGES]:
                pages.append(p.extract_text() or "")
    except Exception as e:  # corrupt / image-only container
        pages = []
        err = str(e)
    else:
        err = None
    rec = {"path": path, "pages": pages, "error": err,
           "chars": sum(len(p) for p in pages)}
    os.makedirs(CACHE, exist_ok=True)
    json.dump(rec, open(out, "w"))
    return rec


def main():
    os.makedirs(CACHE, exist_ok=True)
    index = {}
    for m in ACTIVE:
        files = select(m)
        recs = []
        for f in files:
            r = extract(f)
            recs.append({"file": os.path.basename(f), "chars": r["chars"],
                         "error": r["error"], "cache": hashlib.sha1(f.encode()).hexdigest()[:16]})
            print(f"matter {m:02d}  {r['chars']:>6} chars  {os.path.basename(f)[:70]}")
        index[str(m)] = recs
    json.dump(index, open(_os.path.join(_CACHE_DIR, "index.json"), "w"), indent=1)
    scanned = sum(len(v) for v in index.values())
    empty = sum(1 for v in index.values() for r in v if r["chars"] < 200)
    print(f"\n{scanned} PDFs extracted; {empty} with little/no text layer (OCR candidates)")


if __name__ == "__main__":
    main()
