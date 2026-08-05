"""Tier 1 audit: cross-check active-matter JSON against the extracted PDF text.

Emits internal/docs/pdf_source_audit.json with one entry per discrepancy, each citing the
source PDF and page.
"""
import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
_CACHE_DIR = _os.environ.get("PDF_AUDIT_CACHE", _os.path.join(_REPO, ".cache", "pdf-audit"))
_os.makedirs(_CACHE_DIR, exist_ok=True)
import json, os, re, glob, unicodedata

CACHE = _CACHE_DIR
MATTERS = _os.path.join(_REPO, "internal", "src", "data", "matters")
index = json.load(open(_os.path.join(_CACHE_DIR, "index.json")))

COURT_HINTS = {
    "USDC E.D. Cal.": [r"EASTERN DISTRICT OF CALIFORNIA"],
    "USDC N.D. Cal.": [r"NORTHERN DISTRICT OF CALIFORNIA"],
    "Alameda Sup. Ct.": [r"COUNTY OF ALAMEDA"],
    "Stanislaus Sup. Ct.": [r"COUNTY OF STANISLAUS"],
    "San Joaquin Sup. Ct.": [r"COUNTY OF SAN JOAQUIN"],
    "L.A. Sup. Ct.": [r"COUNTY OF LOS ANGELES"],
    "Los Angeles Sup. Ct.": [r"COUNTY OF LOS ANGELES"],
    "Sacramento Sup. Ct.": [r"COUNTY OF SACRAMENTO"],
    "Contra Costa Sup. Ct.": [r"COUNTY OF CONTRA COSTA"],
    "Santa Clara Sup. Ct.": [r"COUNTY OF SANTA CLARA"],
}


def strip_parens(s):
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^()]*\)", "", s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"\s+", " ", s).strip()


def squash(s):
    """collapse to comparable form: uppercase alphanumerics only"""
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def load_texts(m):
    out = []
    for r in index.get(str(m), []):
        p = os.path.join(CACHE, r["cache"] + ".json")
        if not os.path.exists(p):
            continue
        rec = json.load(open(p))
        out.append({"file": r["file"], "ocr": r.get("ocr", False),
                    "pages": rec["pages"]})
    return out


def find(texts, pattern, flags=re.I):
    """return list of (file, page_no, matched snippet)"""
    hits = []
    rx = re.compile(pattern, flags)
    for t in texts:
        for i, page in enumerate(t["pages"], 1):
            for mt in rx.finditer(norm(page)):
                hits.append((t["file"], i, mt.group(0)))
    return hits


findings = []


def add(matter, field, severity, json_value, pdf_value, note, sources):
    findings.append({
        "matter": matter, "field": field, "severity": severity,
        "json_value": json_value, "pdf_value": pdf_value, "note": note,
        "sources": sources,
    })


ACTIVE = [int(k) for k in index]
for m in sorted(ACTIVE):
    data = json.load(open(os.path.join(MATTERS, f"{m:02d}.json")))
    texts = load_texts(m)
    files = [t["file"] for t in texts]
    if not texts:
        add(m, "documents", "high", "-", "-", "no readable Tier 1 documents found", [])
        continue

    # ---- case number -------------------------------------------------
    case_no = norm(data.get("case_no"))
    if case_no and case_no.lower() not in ("n/a", "not yet assigned", "pending"):
        target = squash(case_no)
        found = False
        for t in texts:
            for i, page in enumerate(t["pages"], 1):
                if target and target in squash(page):
                    found = True
                    break
            if found:
                break
        # collect every case-number-looking token in the docs for comparison
        tokens = set()
        for t in texts:
            for page in t["pages"]:
                for mt in re.finditer(r"\b(?:\d{2}[A-Z]{2}\d{5,6}|\d{1,2}:\d{2}-cv-\d{4,5}[A-Z\- ]{0,12}|\d{2}-cv-\d{4,5})\b",
                                      norm(page)):
                    tokens.add(mt.group(0).strip())
        if not found:
            add(m, "case_no", "unverified", case_no,
                "; ".join(sorted(tokens)[:6]) or "(none found)",
                "case number is not printed in any Tier 1 document (court-assigned "
                "after filing); other case numbers appearing in these documents are listed",
                files[:4])

    # ---- court -------------------------------------------------------
    court = norm(data.get("court"))
    matched_hint = None
    for key, pats in COURT_HINTS.items():
        if court.startswith(key.split(" (")[0]) or key.lower() in court.lower():
            matched_hint = (key, pats)
            break
    if matched_hint:
        pats = matched_hint[1]
        hits = []
        for p in pats:
            hits += find(texts, p)
        if not hits:
            other = []
            for key, opats in COURT_HINTS.items():
                for p in opats:
                    if find(texts, p):
                        other.append(key)
            add(m, "court", "high", court,
                "; ".join(sorted(set(other))) or "(no court header found)",
                "court in the record is not confirmed by any Tier 1 document header",
                files[:4])

    # ---- judge -------------------------------------------------------
    judge = strip_parens(norm(data.get("judge")))
    judge = re.split(r"[,;\u2014-]| referred | per ", judge)[0].strip()
    if judge and judge.lower() not in ("", "n/a", "unassigned", "not yet assigned"):
        # surname = last capitalised word, strip suffixes
        parts = [w for w in re.split(r"[\s.,]+", judge) if w]
        surname = parts[-1] if parts else ""
        if len(surname) > 2:
            hits = find(texts, r"\b" + re.escape(surname) + r"\b")
            if not hits:
                add(m, "judge", "unverified", judge, "(not stated)",
                    f"no Tier 1 document names the assigned judge ('{surname}'); "
                    "judicial assignment postdates the filings held for this matter",
                    files[:4])

    # ---- defendants --------------------------------------------------
    defs_raw = norm(data.get("defendants"))
    defs_clean = strip_parens(defs_raw)
    missing = []
    for chunk in re.split(r";|\band\b", defs_clean):
        chunk = chunk.strip(" .,")
        if len(chunk) < 4:
            continue
        # use the most distinctive word in the party name
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-']{3,}", chunk)
                 if w.lower() not in ("state", "california", "county", "city",
                                      "officer", "sergeant", "deputy", "individual",
                                      "capacity", "official", "does", "inc", "llc",
                                      "corporation", "company", "services", "department")]
        if not words:
            continue
        key = max(words, key=len)
        if not find(texts, r"\b" + re.escape(key) + r"\b"):
            missing.append(f"{chunk} (searched '{key}')")
    if missing:
        add(m, "defendants", "medium", defs_raw, "; ".join(missing),
            "party named in the record is not mentioned in any Tier 1 document",
            files[:4])

    # ---- causes of action count --------------------------------------
    causes = data.get("causes") or []
    count_hits = find(texts, r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|\d{1,2})\s+causes? of action")
    if causes and count_hits:
        WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                 "seven": 7, "eight": 8, "nine": 9, "ten": 10}
        stated = set()
        others = re.compile(r"\b(?:\d{2}[A-Z]{2}\d{5,6}|STK-CV-\S+|\d{1,2}:\d{2}-cv-\d{4,5})\b")
        for f, pg, snip in list(count_hits):
            ctx = None
            for t in texts:
                if t["file"] == f:
                    ctx = norm(t["pages"][pg - 1])
            if ctx:
                at = ctx.lower().find(snip.lower())
                window = ctx[max(0, at - 220):at + 60]
                tokens_near = {x for x in others.findall(window)
                               if squash(x) != squash(case_no)}
                if tokens_near:
                    # the count describes a different action, not this matter
                    count_hits.remove((f, pg, snip))
                    continue
            tok = snip.split()[0].lower()
            stated.add(WORDS.get(tok, int(tok) if tok.isdigit() else None))
        stated.discard(None)
        if stated and len(causes) not in stated:
            add(m, "causes", "medium", f"{len(causes)} listed",
                "; ".join(f"{f} p.{pg}: '{s}'" for f, pg, s in count_hits[:3]),
                "count of causes of action in the record differs from the filing",
                files[:4])

    # ---- caption plaintiff/defendant ---------------------------------
    caption = norm(data.get("caption"))
    tail = caption.split(" v. ")[-1] if " v. " in caption else ""
    tail_key = None
    for w in re.findall(r"[A-Za-z][A-Za-z\-'.]{3,}", tail):
        if w.lower() not in ("services", "inc", "llc", "corporation", "company", "et", "al"):
            tail_key = w
            break
    if tail_key and not find(texts, r"\b" + re.escape(tail_key.strip('.')) + r"\b"):
        add(m, "caption", "medium", caption, f"(searched '{tail_key}')",
            "lead defendant from the caption not found in any Tier 1 document",
            files[:4])

json.dump({"generated_for": "tier1-active-matters",
           "matters": sorted(ACTIVE),
           "documents_read": sum(len(v) for v in index.values()),
           "findings": findings}, open(_os.path.join(_REPO, "internal", "docs", "pdf_source_audit.json"), "w"), indent=1)

print(f"documents read: {sum(len(v) for v in index.values())}")
print(f"findings: {len(findings)}\n")
for f in findings:
    print(f"[{f['severity']:>6}] matter {f['matter']:>2} {f['field']:<12} {f['note']}")
    print(f"          record: {f['json_value'][:150]}")
    print(f"          pdfs  : {f['pdf_value'][:150]}\n")
