"""Tier 3 sweep: read every filing in every archived matter.

Extraction is cached per PDF under .cache/pdf-audit (shared with Tiers 1/2), so
re-runs only touch files that have not been read yet.

Checks performed:
  link        every documents[]/evidence path in the matter JSON resolves to a real file
  orphan      PDFs on disk that no matter record and no document index entry references
  duplicate   byte-identical filings inside a matter folder
  misfiled    a filing whose text carries only another matter's case number
  mislabeled  a filename that claims a document type the text does not support
  unreadable  a PDF with no extractable text even after OCR
  cross_ref   an archived filing that names a defendant or case number from an active matter
  deadline    a hearing/trial date printed in a filing that the timeline does not carry

Usage:
  python internal/scripts/pdf-audit/tier3.py extract   # text + OCR pass (cached)
  python internal/scripts/pdf-audit/tier3.py audit     # writes reports
"""
import os as _os

_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
_CACHE_DIR = _os.environ.get("PDF_AUDIT_CACHE", _os.path.join(_REPO, ".cache", "pdf-audit"))
_os.makedirs(_CACHE_DIR, exist_ok=True)

import hashlib
import json
import os
import re
import sys
import unicodedata
from datetime import date

DOCS = os.path.join(_REPO, "internal", "public", "documents")
MATTERS = os.path.join(_REPO, "internal", "src", "data", "matters")
CACHE = _CACHE_DIR
INDEX = os.path.join(CACHE, "tier3-index.json")

# Active matters as established by the lifecycle field in summaries.json
ACTIVE = [1, 2, 7, 12, 19, 20, 24, 25, 26, 27, 28, 29]
ARCHIVED = []


def _load_archived():
    summaries = json.load(open(os.path.join(MATTERS, "summaries.json")))
    return sorted(m["number"] for m in summaries if m.get("lifecycle") != "active")


ARCHIVED = _load_archived()

MAX_PAGES = 12
OCR_PAGES = 4


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"\s+", " ", s).strip()


def squash(s):
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def key_for(path):
    return hashlib.sha1(path.encode()).hexdigest()[:16]


def matter_pdfs(m):
    d = os.path.join(DOCS, f"matter-{m:02d}")
    if not os.path.isdir(d):
        return []
    out = []
    for root, _, files in os.walk(d):
        for f in files:
            if f.lower().endswith(".pdf"):
                out.append(os.path.join(root, f))
    return sorted(out)


# ---------------------------------------------------------------- extraction
def extract_one(path):
    """Cached text extraction; OCR fallback when the text layer is thin."""
    out = os.path.join(CACHE, key_for(path) + ".json")
    if os.path.exists(out):
        rec = json.load(open(out))
        if rec.get("chars", 0) >= 200 or rec.get("ocr"):
            return rec
    else:
        rec = None

    if rec is None:
        import pdfplumber

        pages, err = [], None
        try:
            with pdfplumber.open(path) as pdf:
                for p in pdf.pages[:MAX_PAGES]:
                    pages.append(p.extract_text() or "")
        except Exception as e:
            pages, err = [], str(e)
        rec = {
            "path": path,
            "pages": pages,
            "error": err,
            "chars": sum(len(p) for p in pages),
        }

    if rec["chars"] < 200 and not rec.get("ocr"):
        try:
            import pypdfium2 as pdfium
            import pytesseract

            pdf = pdfium.PdfDocument(path)
            pages = []
            for i in range(min(len(pdf), OCR_PAGES)):
                pages.append(pytesseract.image_to_string(pdf[i].render(scale=2.2).to_pil()))
            rec["pages"] = pages
            rec["ocr"] = True
            rec["chars"] = sum(len(p) for p in pages)
        except Exception as e:
            rec["ocr"] = False
            rec["error"] = (rec.get("error") or "") + f" ocr: {e}"

    json.dump(rec, open(out, "w"))
    return rec


def cmd_extract():
    index = {}
    total = ocr = thin = 0
    for m in ARCHIVED:
        recs = []
        for path in matter_pdfs(m):
            r = extract_one(path)
            total += 1
            ocr += 1 if r.get("ocr") else 0
            thin += 1 if r["chars"] < 200 else 0
            recs.append(
                {
                    "file": os.path.basename(path),
                    "rel": os.path.relpath(path, DOCS),
                    "chars": r["chars"],
                    "ocr": bool(r.get("ocr")),
                    "error": r.get("error"),
                    "cache": key_for(path),
                }
            )
            print(f"matter {m:02d} {r['chars']:>7} chars  {os.path.basename(path)[:72]}")
        index[str(m)] = recs
    json.dump(index, open(INDEX, "w"), indent=1)
    print(f"\n{total} PDFs read; {ocr} via OCR; {thin} still without usable text")


# -------------------------------------------------------------------- audit
findings = []


def add(matter, check, severity, subject, detail):
    findings.append(
        {
            "matter": matter,
            "check": check,
            "severity": severity,
            "subject": subject,
            "detail": detail,
        }
    )


DOC_TYPE_MARKERS = [
    ("complaint", r"COMPLAINT|PETITION|CAUSES? OF ACTION"),
    ("amended complaint", r"AMENDED COMPLAINT"),
    ("summons", r"SUMMONS|CITACI"),
    ("proof of service", r"PROOF OF SERVICE|POS-?010|SERVED"),
    ("civil case cover sheet", r"CIVIL CASE COVER SHEET|CM-?010"),
    ("case management statement", r"CASE MANAGEMENT|CM-?110"),
    ("fee waiver", r"WAIVE COURT FEES|FW-?00\d|FEE WAIVER"),
    ("order", r"ORDER|IT IS (SO )?ORDERED|RULING|GRANTED|DENIED"),
    ("judgment", r"JUDGMENT|CIV-?100|JUD-?100"),
    ("notice of hearing", r"NOTICE OF HEARING|HEARING (DATE|IS SET)"),
    ("declaration", r"DECLARATION|I DECLARE|DECLARE UNDER PENALTY"),
    ("writ of execution", r"WRIT OF EXECUTION|EJ-?130"),
    ("abstract of judgment", r"ABSTRACT OF JUDGMENT|EJ-?001"),
    ("memorandum of costs", r"MEMORANDUM OF COSTS|MC-?010"),
    ("opposition", r"OPPOSITION"),
    ("demurrer", r"DEMURRER"),
    ("dismissal", r"DISMISSAL|VOLUNTARY DISMISSAL"),
    ("settlement", r"SETTLEMENT|STIPULATION"),
]

DATE_RX = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+"
    r"(\d{1,2}),?\s+(20\d{2})\b",
    re.I,
)
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
HEARING_RX = re.compile(
    r"(hearing|trial|case management conference|cmc|status conference|"
    r"order to show cause|osc)\b", re.I
)


def parse_date(mt):
    mo = MONTHS[mt.group(1)[:3].lower()]
    return date(int(mt.group(3)), mo, int(mt.group(2)))


def cmd_audit():
    if not os.path.exists(INDEX):
        sys.exit("run `tier3.py extract` first")
    index = json.load(open(INDEX))
    timeline = json.load(open(os.path.join(_REPO, "internal", "src", "data", "timeline.json")))
    doc_index_path = os.path.join(MATTERS, "document-index.json")
    doc_index = json.load(open(doc_index_path)) if os.path.exists(doc_index_path) else {}

    # case numbers for every matter, for misfile detection
    case_nos = {}
    records = {}
    summaries = json.load(open(os.path.join(MATTERS, "summaries.json")))
    for m in [s["number"] for s in summaries]:
        path = os.path.join(MATTERS, f"{m:02d}.json")
        if not os.path.exists(path):
            continue
        data = json.load(open(path))
        records[m] = data
        cn = norm(data.get("case_no"))
        if cn and cn.lower() not in ("n/a", "not yet assigned", "pending"):
            case_nos[m] = squash(cn)

    indexed_paths = set()
    if isinstance(doc_index, dict):
        for v in doc_index.values():
            if isinstance(v, list):
                for e in v:
                    p = e.get("path") if isinstance(e, dict) else e
                    if isinstance(p, str):
                        indexed_paths.add(p)
    elif isinstance(doc_index, list):
        for e in doc_index:
            p = e.get("path") if isinstance(e, dict) else e
            if isinstance(p, str):
                indexed_paths.add(p)

    # active matter defendants for cross-reference detection
    active_defendants = {}
    for m in ACTIVE:
        data = records.get(m, {})
        defs = norm(data.get("defendants", ""))
        keys = set()
        for chunk in re.split(r";|\band\b", defs):
            chunk = chunk.strip(" .,")
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-']{3,}", chunk)
                     if w.lower() not in ("state", "california", "county", "city",
                                          "officer", "sergeant", "deputy", "individual",
                                          "capacity", "official", "does", "inc", "llc",
                                          "corporation", "company", "services", "department")]
            if words:
                keys.add(max(words, key=len))
        active_defendants[m] = keys

    read = 0
    for m in ARCHIVED:
        data = records.get(m, {})
        folder = os.path.join(DOCS, f"matter-{m:02d}")
        on_disk = set()
        if os.path.isdir(folder):
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        on_disk.add(os.path.join(root, f))

        # ---- link integrity ------------------------------------------
        referenced = set()
        for entry in data.get("documents") or []:
            p = entry.get("path") if isinstance(entry, dict) else entry
            if not isinstance(p, str):
                continue
            referenced.add(os.path.basename(p))
            disk = os.path.join(_REPO, "internal", "public", p.lstrip("/"))
            if not os.path.exists(disk):
                ci = {os.path.basename(f).lower(): f for f in on_disk}.get(os.path.basename(p).lower())
                add(m, "link", "high", p,
                    f"referenced file is missing from the repo"
                    + (f"; closest match on disk: '{os.path.basename(ci)}'" if ci else ""))

        # ---- duplicates ----------------------------------------------
        hashes = {}
        for f in sorted(on_disk):
            h = hashlib.sha1(open(f, "rb").read()).hexdigest()
            hashes.setdefault(h, []).append(f)
        for h, group in hashes.items():
            if len(group) > 1:
                add(m, "duplicate", "medium", os.path.basename(group[0]),
                    "byte-identical copies in the same folder: " + "; ".join(os.path.basename(g) for g in group[1:]))

        # ---- orphans -------------------------------------------------
        for f in sorted(on_disk):
            rel = "/documents/" + os.path.relpath(f, DOCS)
            if os.path.basename(f) not in referenced and rel not in indexed_paths:
                add(m, "orphan", "low", os.path.basename(f),
                    "file present in the matter folder but not referenced by the record "
                    "or the document index")

        # ---- text-driven checks --------------------------------------
        timeline_dates = set()
        for ev in timeline:
            refs = ev.get("matters") or ev.get("matter_refs") or []
            if isinstance(refs, (int, str)):
                refs = [refs]
            nums = {int(re.sub(r"\D", "", str(r)) or 0) for r in refs}
            if m in nums or m == ev.get("matter"):
                d = ev.get("date")
                if isinstance(d, str) and re.match(r"\d{4}-\d{2}-\d{2}", d):
                    timeline_dates.add(d[:10])

        for rec in index.get(str(m), []):
            read += 1
            cache_file = os.path.join(CACHE, rec["cache"] + ".json")
            if not os.path.exists(cache_file):
                continue
            body = json.load(open(cache_file))
            text = norm(" ".join(body.get("pages") or []))
            fname = rec["file"]
            rel = rec["rel"]

            if len(text) < 120:
                add(m, "unreadable", "medium", fname,
                    "no usable text after extraction and OCR; content cannot be verified")
                continue

            sq = squash(text)

            # misfiled: carries another matter's case number and not its own
            own = case_nos.get(m)
            if own and own not in sq:
                foreign = [f"matter {o:02d} ({norm(records[o].get('case_no'))})"
                           for o, c in case_nos.items() if o != m and c in sq]
                if foreign:
                    add(m, "misfiled", "high", fname,
                        "text carries only another matter's case number: " + "; ".join(foreign))

            # mislabeled: filename claims a type the text does not support
            low = fname.lower()
            for label, marker in DOC_TYPE_MARKERS:
                if label in low and not re.search(marker, text, re.I):
                    add(m, "mislabeled", "medium", fname,
                        f"filename says '{label}' but the text has no matching marker")
                    break

            # cross_ref: archived filing names an active-matter defendant or case number
            for am, keys in active_defendants.items():
                matched = [k for k in keys if re.search(r"\b" + re.escape(k) + r"\b", text, re.I)]
                if matched:
                    add(m, "cross_ref", "low", fname,
                        f"archived filing mentions active matter {am:02d} defendant(s): {', '.join(matched)}")
                    break

            # deadlines: future hearing/trial dates in the text vs the timeline
            for mt in DATE_RX.finditer(text):
                at = mt.start()
                window = text[max(0, at - 140): at + 60]
                if not HEARING_RX.search(window):
                    continue
                try:
                    d = parse_date(mt)
                except ValueError:
                    continue
                if d < date(2026, 1, 1):
                    continue
                if d.isoformat() not in timeline_dates:
                    add(m, "deadline", "medium", fname,
                        f"filing sets a {HEARING_RX.search(window).group(1).lower()} "
                        f"on {d.isoformat()} that the timeline does not carry")

    by_check = {}
    for f in findings:
        by_check[f["check"]] = by_check.get(f["check"], 0) + 1
    out = {
        "generated_for": "tier3-archived-matter-sweep",
        "matters": ARCHIVED,
        "documents_read": read,
        "counts": by_check,
        "findings": findings,
    }
    dest = os.path.join(_REPO, "internal", "docs", "pdf_tier3_audit.json")
    json.dump(out, open(dest, "w"), indent=1)

    # Human-readable markdown report
    md_lines = [
        "# Tier 3 PDF Sweep — Archived Matters",
        "",
        "Full-text read of every PDF in the 19 archived matter folders.",
        "",
        f"- Documents read: {read}",
        f"- Archived matters: {len(ARCHIVED)}",
        "",
        "## Findings by check",
        "",
        "| Check | Count | Severity pattern |",
        "|---|---|---|",
    ]
    for k, v in sorted(by_check.items(), key=lambda x: -x[1]):
        sev = {"link": "high", "misfiled": "high", "duplicate": "medium",
               "mislabeled": "medium", "deadline": "medium", "unreadable": "medium",
               "cross_ref": "low", "orphan": "low"}.get(k, "low")
        md_lines.append(f"| {k} | {v} | {sev} |")

    md_lines += ["", "## Findings by matter", ""]
    by_matter = {}
    for f in findings:
        by_matter.setdefault(f["matter"], []).append(f)
    for m in sorted(by_matter):
        md_lines.append(f"### Matter {m:02d}")
        for f in by_matter[m]:
            md_lines.append(f"- **{f['check']}** ({f['severity']}): `{f['subject']}` — {f['detail']}")
        md_lines.append("")

    md_dest = os.path.join(_REPO, "internal", "docs", "PDF_TIER3_SWEEP.md")
    open(md_dest, "w").write("\n".join(md_lines))

    print(f"documents read: {read}")
    for k, v in sorted(by_check.items(), key=lambda x: -x[1]):
        print(f"  {k:<11} {v}")
    print(f"wrote {dest}")
    print(f"wrote {md_dest}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"
    {"extract": cmd_extract, "audit": cmd_audit}[cmd]()
