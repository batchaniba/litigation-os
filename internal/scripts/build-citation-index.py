#!/usr/bin/env python3
# ==========================================================
# Catalog every legal citation in the document corpus, with page-level
# provenance.
#
# The point is verifiability. internal/docs/citation_audit.json (July 12, 2026)
# hand-checked 147 citations across 24 matters and found two that appear to be
# fabricated outright -- so the failure mode is real and already in the record.
# That audit sampled motion practice and cited documents by filename only. This
# is the mechanical counterpart: every citation in every extractable PDF, keyed
# to the exact page it sits on, so a drafted cite can be traced back to a source
# page instead of trusted.
#
# Outputs, written together so their figures cannot drift apart:
#   internal/docs/citation_index.json
#     citations[]  -- one entry per distinct normalized citation, with every
#                     occurrence (matter, document, page, surrounding context)
#     documents[]  -- per-document extraction status, including which PDFs have
#                     no text layer and therefore need OCR before they can be
#                     trusted as "no citations found"
#   internal/docs/CITATION_INDEX.md
#     the findings report -- corpus counts, per-matter coverage, the unverified
#     and uncorroborated queue, and where the known-bad citations still sit
#
# Usage:
#   python3 internal/scripts/build-citation-index.py
#   python3 internal/scripts/build-citation-index.py --check   # exit 1 on drift
# ==========================================================
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF required: python3 -m pip install pymupdf")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DOCS_ROOT = os.path.join(REPO_ROOT, "internal", "public", "documents")
OUT_PATH = os.path.join(REPO_ROOT, "internal", "docs", "citation_index.json")
REPORT_PATH = os.path.join(REPO_ROOT, "internal", "docs", "CITATION_INDEX.md")
AUDIT_PATH = os.path.join(REPO_ROOT, "internal", "docs", "citation_audit.json")
SUMMARIES_PATH = os.path.join(REPO_ROOT, "internal", "src", "data", "matters", "summaries.json")

CONTEXT_CHARS = 160

# ---------------------------------------------------------------- patterns
#
# Ordered most-specific first; a span already claimed by an earlier pattern is
# not re-matched, so "42 U.S.C. § 1983" is a statute rather than three numbers.

# Periods are optional throughout: the corpus contains "381 US 479" alongside
# "442 U.S. 200", and missing the bare form is not a silent gap -- it lets the
# authority pairer below run past the real reporter and attach the *next*
# case's numbers to this case's name.
REPORTERS = [
    r"U\.?\s?S\.?",
    r"S\.?\s?Ct\.?",
    r"L\.?\s?Ed\.?(?:\s?2d)?",
    r"F\.?\s?(?:2d|3d|4th)",
    r"F\.?\s?Supp\.?(?:\s?2d|\s?3d)?",
    r"F\.?\s?App'?x",
    r"F\.?R\.?D\.?",
    r"Cal\.?\s?(?:2d|3d|4th|5th)",
    r"Cal\.?\s?App\.?\s?(?:2d|3d|4th|5th)?",
    r"Cal\.?\s?Rptr\.?(?:\s?2d|\s?3d)?",
    r"P\.?\s?(?:2d|3d)",
    r"Cal\.?\s?App\.?\s?Supp\.?",
    # Military Justice -- the QI research cites United States v. Jessie,
    # 79 M.J. 437 (C.A.A.F. 2020), which went uncaptured until this was added.
    r"M\.?\s?J\.?",
]
REPORTER_ALT = "|".join(REPORTERS)

# Westlaw-only cites (2014 WL 2807986) name unpublished decisions, which are the
# hardest for a reader to check and therefore the likeliest place for a bad cite
# to sit unnoticed. Reporter-shaped patterns miss them entirely -- the volume is
# a year and the "page" is a docket-style number.
WESTLAW_CITE = re.compile(r"\b(?:19|20)\d{2}\s+WL\s+\d{4,}")

PATTERNS = [
    # 42 U.S.C. § 1983 / 28 U.S.C. §§ 2201-2202
    ("statute_federal",
     r"\b\d{1,2}\s+U\.?\s?S\.?\s?C\.?\s*§{1,2}\s*\d+[A-Za-z0-9()\-–.]*"),
    # 8 C.F.R. § 214.14(a)(14)(ii)
    ("regulation_federal",
     r"\b\d{1,2}\s+C\.?\s?F\.?\s?R\.?\s*§{1,2}\s*[\d.]+[A-Za-z0-9()\-–.]*"),
    # 15 CCR § 3574(f)(1) / 15 Cal. Code Regs. § 3574
    ("regulation_state",
     r"\b\d{1,2}\s+(?:C\.?\s?C\.?\s?R\.?|Cal\.\s?Code\s?Regs\.?)[^§\n]{0,24}§{1,2}\s*[\d.]+[A-Za-z0-9()\-–.]*"),
    # Reporter citation: 540 F.3d 1082 / 66 Cal.App.5th 200 / 442 U.S. 200
    ("case_reporter",
     rf"\b\d{{1,4}}\s+(?:{REPORTER_ALT})\s+\d{{1,4}}"),
    # California code sections, incl. the CCP/PC/Gov abbreviations in use here
    ("statute_state",
     r"\b(?:Penal|Civil|Government|Vehicle|Evidence|Labor|Welfare\s+(?:and|&)\s+Institutions|"
     r"Health\s+(?:and|&)\s+Safety|Business\s+(?:and|&)\s+Professions|Code\s+of\s+Civil\s+Procedure|"
     r"Civ\.\s?Proc\.|C\.C\.P\.|CCP|Pen\.|Civ\.|Gov(?:'t|t)?\.|Veh\.|Evid\.|Lab\.|W(?:elf)?\.?\s?&\s?I\.?)"
     r"[^§\n]{0,20}(?:Code)?[^§\n]{0,12}§{1,2}\s*[\d.]+[A-Za-z0-9()\-–.]*"),
    # Bare "§ 1983" style back-references, only when clearly a section cite
    ("section_shorthand",
     r"§{1,2}\s*\d[\d.]*[A-Za-z0-9()\-–.]*"),
    # FRCP 12(a)(1)(A) / Fed. R. Civ. P. 26(f) / Rule 12(b)(6)
    ("rule_federal",
     r"\b(?:F\.?R\.?C\.?P\.?|Fed\.?\s?R\.?\s?Civ\.?\s?P\.?|Fed\.?\s?R\.?\s?Evid\.?|"
     r"Federal\s+Rules?\s+of\s+Civil\s+Procedure)[^\n]{0,6}\s*\d+[A-Za-z0-9()\-–.]*"),
    ("rule_local",
     r"\b(?:Civil\s+L\.?R\.?|ADR\s+L\.?R\.?|Local\s+Rule|L\.?R\.?)\s*[\d]+[\-–.\d]*[A-Za-z0-9()]*"),
    ("rule_state",
     r"\b(?:California\s+Rules?\s+of\s+Court|Cal\.?\s?Rules?\s+of\s+Court|CRC)[^\n]{0,10}"
     r"\s*(?:rule\s*)?[\d.]+[A-Za-z0-9()\-–.]*"),
    ("case_westlaw", WESTLAW_CITE.pattern),
    ("constitutional",
     r"\b(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Fourteenth)\s+Amendment"),
]
COMPILED = [(kind, re.compile(rx, re.IGNORECASE if kind.startswith("rule") else 0))
            for kind, rx in PATTERNS]

# Case name: "Shanks v. Dressel", "In re Gadlin", "Alliance for X v. Macomber".
# Deliberately conservative -- capitalized runs only, bounded length, so ordinary
# prose containing " v. " does not produce noise. A party may carry a
# comma-separated suffix ("Lerma, Jr. v. Amazon"); without that the match would
# otherwise start mid-name at "Jr." and lose the party it belongs to.
_SUFFIX = r"(?:Jr|Sr|II|III|IV|Inc|LLC|L\.L\.C|Corp|Co|Ltd|N\.A|P\.C|LLP)\.?"
_WORD = r"[A-Z][A-Za-z'’.\-]*"
_PARTY = (
    rf"{_WORD}(?:\s+(?:of|for|the|and|&|de|del|los|en)\s+)?"
    rf"(?:\s*{_WORD}){{0,5}}"
    rf"(?:,\s*{_SUFFIX})?"
)
CASE_NAME = re.compile(
    rf"\b(?:In\s+re\s+{_WORD}(?:\s+{_WORD}){{0,4}}"
    rf"|{_PARTY}\s+v\.?\s+{_PARTY})"
)

# A match that opens with one of these lost its real first party to a line break
# or a preceding comma; recording it would create a phantom case name.
LEADING_JUNK = re.compile(rf"^(?:{_SUFFIX})\b", re.IGNORECASE)

# Party names that are the litigant's own dockets, not cited authority.
OWN_CAPTION = re.compile(
    r"\b(?:Newanforbi|Nforbi|Ngwa)\b", re.IGNORECASE
)


MATTERS_DIR = os.path.join(REPO_ROOT, "internal", "src", "data", "matters")


def load_document_owners():
    """Map document path -> set of matter numbers that cite it.

    The folder a PDF sits in is not reliably its matter. Matters 32 and 33 are
    document-home entries holding the docket PDFs of Matters 1, 2, 7, 20 and 24
    under from-NN/ subfolders, so folder-derived attribution reports zero
    citations for five active matters and piles their authorities onto 32/33.
    The matter JSON documents[] arrays are the actual ownership record.
    """
    owners = defaultdict(set)
    for fname in sorted(os.listdir(MATTERS_DIR)):
        if not re.fullmatch(r"\d+\.json", fname):
            continue
        with open(os.path.join(MATTERS_DIR, fname)) as f:
            data = json.load(f)
        number = data.get("number")
        for ref in data.get("documents") or []:
            path = ref.get("path")
            if path:
                owners[path].add(number)
    return owners


DOC_OWNERS = load_document_owners()


def folder_matter(rel_path):
    head = rel_path.split(os.sep)[0]
    if head.startswith("matter-"):
        try:
            return int(head.replace("matter-", ""))
        except ValueError:
            return None
    return None


def matters_for(rel_path):
    """Every matter this document belongs to, cross-references included."""
    found = set(DOC_OWNERS.get(f"/documents/{rel_path}", ()))
    folder = folder_matter(rel_path)
    if folder is not None:
        found.add(folder)
    return sorted(found)


def matter_for(rel_path):
    """Primary matter -- the citing matter where one exists, else the folder."""
    owned = sorted(DOC_OWNERS.get(f"/documents/{rel_path}", ()))
    if owned:
        return owned[0]
    return folder_matter(rel_path)


# Document role drives how much a citation in it is worth scrutinising: an
# authority quoted in a court's own order is already vetted, one asserted in
# Plaintiff's brief is not.
ROLE_RULES = [
    # Discovery first: responses are dense with boilerplate objection citations
    # (privacy, relevance) that would otherwise swamp the filing counts.
    ("discovery", r"frogs|srogs|\brfp\b|rfa\b|disc0|interrogator|request for production|"
                  r"requests? for admission|discovery response|resp plntf"),
    ("court_order", r"\border\b|\bruling\b|tentative|findings|f&r|judgment|opinion|"
                    r"decision|screening"),
    ("opposing_filing", r"demurrer|motion to dismiss|opposition by|reply iso demurrer|"
                        r"\banswer\b|notice of joinder|mpa iso"),
    ("plaintiff_filing", r"complaint|petition|opposition|reply|brief|objections?|memorandum|"
                         r"points and authorities|motion|notice of supplemental|rjn|"
                         r"request for judicial notice|declaration"),
    ("service_admin", r"summons|proof of service|pos-?010|usm-?285|ser-?001|civil cover|"
                      r"case cover|fee waiver|fw-00|change of address|receipt|ereceipt|"
                      r"postage|notice of case assignment|cm-0|civ-1"),
]

# "Notice and Request for Ruling" is Plaintiff asking for one, not a court
# issuing one -- without this guard the packet is scored as authority.
NOT_A_COURT_ORDER = re.compile(
    r"request for (?:a )?(?:ruling|order)|notice and request|"
    r"motion for (?:an? )?(?:order|ruling)|proposed order", re.IGNORECASE
)


def role_for(rel_path):
    low = rel_path.lower()
    for role, rx in ROLE_RULES:
        if re.search(rx, low):
            if role == "court_order" and NOT_A_COURT_ORDER.search(low):
                continue
            return role
    return "other"


# California code names appear in at least four abbreviations each across the
# corpus; without folding them, the same section lands under several keys and
# the occurrence counts lie.
# Boundary is "end of the code name", i.e. whatever precedes the section symbol
# -- not \b, which fails after the optional trailing period in "Civ. Proc.".
_END = r"(?=[\s,§]|$)"
CODE_ALIASES = [
    (rf"^(?:Code\s+of\s+Civil\s+Procedure|Code\s+Civ\.?\s?Proc\.?|Civ\.?\s?Proc\.?|C\.?C\.?P\.?){_END}",
     "Code of Civil Procedure"),
    (rf"^(?:Penal\s+Code|Pen\.?\s?Code|Pen\.){_END}", "Penal Code"),
    (rf"^(?:Civil\s+Code|Civ\.?\s?Code){_END}", "Civil Code"),
    (rf"^(?:Government\s+Code|Gov'?t?\.?\s?Code|Gov\.){_END}", "Government Code"),
    (rf"^(?:Vehicle\s+Code|Veh\.?\s?Code|Veh\.){_END}", "Vehicle Code"),
    (rf"^(?:Evidence\s+Code|Evid\.?\s?Code|Evid\.){_END}", "Evidence Code"),
    (rf"^(?:Labor\s+Code|Lab\.?\s?Code|Lab\.){_END}", "Labor Code"),
    (rf"^(?:Welfare\s+(?:and|&)\s+Institutions\s+Code|W(?:elf)?\.?\s?&\s?I\.?){_END}",
     "Welfare and Institutions Code"),
    (rf"^(?:Health\s+(?:and|&)\s+Safety\s+Code){_END}", "Health and Safety Code"),
    (rf"^(?:Business\s+(?:and|&)\s+Professions\s+Code){_END}", "Business and Professions Code"),
]


# Federal compilations appear with and without interior periods; fold them so
# "8 CFR § 214.14" and "8 C.F.R. § 214.14" count as one authority.
FEDERAL_ABBREV = [
    (r"\bU\.?\s?S\.?\s?C\.?", "U.S.C."),
    (r"\bC\.?\s?F\.?\s?R\.?", "C.F.R."),
    (r"\bC\.?\s?C\.?\s?R\.?", "C.C.R."),
]


def _tidy_prefix(s):
    """Spacing fixes that are safe on the code/reporter name, but not on a
    section number -- '214.14' must not become '214. 14'."""
    # "U. S. C." -> "U.S.C."
    s = re.sub(r"\b([A-Z])\.\s+(?=[A-Z]\.)", r"\1.", s)
    # "Evid.408" -> "Evid. 408"; the lookbehind requires a letter before the
    # dot, so a decimal inside a section number is left alone.
    s = re.sub(r"(?<=[A-Za-z])\.(?=\d)", ". ", s)
    # "CCP§" handled by the caller; this catches "Rule12" style run-ons.
    s = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def normalize(kind, raw):
    """Collapse spacing/punctuation variants so '42 U.S.C. §1983',
    '42 U. S. C. § 1983' and '42 U.S.C. § 1983.)' land on the same key."""
    s = re.sub(r"\s+", " ", raw.replace("\xa0", " ")).strip()
    s = s.replace("§§", "§")

    # Drop trailing sentence punctuation and any close-paren the citation does
    # not open itself -- "§ 214.14(a)(12).)" is a cite inside a parenthetical.
    while s and s[-1] in ".,;:)":
        if s[-1] == ")" and s.count("(") >= s.count(")"):
            break
        s = s[:-1]

    if "§" in s:
        prefix, _, section = s.partition("§")
        # Strip a trailing comma only -- a trailing period belongs to the
        # abbreviation ("42 U.S.C." must not become "42 U.S.C").
        prefix = _tidy_prefix(prefix.rstrip().rstrip(","))
        if kind in ("statute_federal", "regulation_federal", "regulation_state"):
            for rx, canonical in FEDERAL_ABBREV:
                if re.search(rx, prefix):
                    prefix = re.sub(rx, canonical, prefix, count=1)
                    break
        if kind == "statute_state":
            for rx, canonical in CODE_ALIASES:
                if re.match(rx, prefix, re.IGNORECASE):
                    prefix = re.sub(rx, canonical, prefix, count=1, flags=re.IGNORECASE)
                    break
        # Section numbers keep their internal punctuation verbatim.
        section = re.sub(r"\s+", "", section)
        s = f"{prefix} § {section}".strip()
    else:
        s = _tidy_prefix(s)

    if kind == "constitutional":
        s = s.title()
    return s


def extract_pages(path):
    """Return list of page texts; empty list if the file cannot be opened."""
    try:
        doc = fitz.open(path)
    except Exception:
        return None
    try:
        return [page.get_text() for page in doc]
    finally:
        doc.close()


# A full authority is "Name, <reporter cite> (year)" or the California form
# "Name (year) <reporter cite>". Cataloguing the name and the reporter numbers
# as separate rows makes the index useless for drafting -- you cannot check
# "424 U.S. 319" without knowing it is meant to be Mathews v. Eldridge.
REPORTER_RX = re.compile(
    rf"\b\d{{1,4}}\s+(?:{REPORTER_ALT})\s+\d{{1,4}}|{WESTLAW_CITE.pattern}")
YEAR_RX = re.compile(r"\((?:19|20)\d{2}\)")
PAIR_WINDOW = 140


def pair_authority(text, name_match):
    """Given a case-name match, return (reporter, year, end) by looking just past
    it -- and just before it, for the California '(year) cite' style.

    Refuses to pair across an intervening case name. Without that guard, a cite
    string whose own reporter failed to match ("381 US 479" when the pattern
    demanded periods) silently adopts the *next* case's numbers, which is how
    "Griswold v. Connecticut, 20 Cal.3d 844" -- Britt's reporter -- gets
    manufactured. A citation index that invents citations is worse than none.
    """
    tail = text[name_match.end(): name_match.end() + PAIR_WINDOW]
    rep = REPORTER_RX.search(tail)
    if not rep:
        return None, None, None
    nxt = CASE_NAME.search(tail)
    if nxt and nxt.start() < rep.start():
        return None, None, None
    # Year may sit before the reporter (Cal. style) or after it (federal style).
    year = None
    lead = tail[: rep.start()]
    ym = YEAR_RX.search(lead) or YEAR_RX.search(tail[rep.end(): rep.end() + 24])
    if ym:
        year = ym.group(0).strip("()")
    reporter = re.sub(r"\s+", " ", rep.group(0)).strip()
    return reporter, year, rep.end()


def scan_page(text):
    """Yield (kind, raw, start, end), skipping spans already claimed."""
    claimed = []

    def overlaps(a, b):
        return any(not (b <= s or a >= e) for s, e in claimed)

    for kind, rx in COMPILED:
        for m in rx.finditer(text):
            if overlaps(m.start(), m.end()):
                continue
            claimed.append((m.start(), m.end()))
            yield kind, m.group(0), m.start(), m.end()

    for m in CASE_NAME.finditer(text):
        raw = m.group(0)
        if OWN_CAPTION.search(raw) or LEADING_JUNK.match(raw):
            continue
        if overlaps(m.start(), m.end()):
            continue
        reporter, year, _end = pair_authority(text, m)
        if reporter:
            # Emit the joined authority; the bare reporter numbers were already
            # claimed by case_reporter above, which is fine -- this row is the
            # one a drafter actually cites.
            full = f"{normalize('case_name', raw)}, {reporter}"
            if year:
                full += f" ({year})"
            yield "authority", full, m.start(), m.end()
        yield "case_name", raw, m.start(), m.end()


def _slug(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def build_report(out):
    """Render CITATION_INDEX.md from the same data that produced the JSON.

    Generated here rather than by a side script so the prose figures cannot
    drift from the index they describe -- --check covers both files.
    """
    with open(AUDIT_PATH) as f:
        audit = json.load(f)
    with open(SUMMARIES_PATH) as f:
        summaries = json.load(f)

    caption = {m["number"]: m["caption"] for m in summaries}
    active = sorted(m["number"] for m in summaries
                    if m.get("lifecycle") in ("active", "pre_filing"))
    audit_blob = _slug(json.dumps(audit["citations"]))

    cites = out["citations"]
    auth = [c for c in cites if c["kind"] == "authority"]
    unverified = [a for a in auth if _slug(a["citation"].split(",")[0]) not in audit_blob]
    risky = sorted(
        [a for a in unverified
         if "plaintiff_filing" in {o["role"] for o in a["occurrences"]}
         and not ({o["role"] for o in a["occurrences"]} & {"court_order", "opposing_filing"})],
        key=lambda c: -c["occurrenceCount"])

    by_matter = defaultdict(set)
    for c in cites:
        for m in c["matters"]:
            by_matter[m].add(c["citation"])
    gaps = [d for d in out["documents"]
            if d["status"] != "ok" and set(d["matters"]) & set(active)]

    c = out["corpus"]
    kinds = Counter(x["kind"] for x in cites)
    L = []
    w = L.append
    w("# Citation Index\n")
    w("Mechanical catalog of every legal citation in the document corpus, keyed to the page")
    w("it appears on. Generated by `internal/scripts/build-citation-index.py`; machine-readable")
    w("output in `internal/docs/citation_index.json`. Both files are written together, so the")
    w("figures below always describe the committed index.\n")
    w("Companion to `CITATION_AUDIT.md` (July 12, 2026), which hand-verified 147 citations")
    w("across 24 matters and found two that appear fabricated. That audit sampled motion")
    w("practice and identified documents by filename. This one is exhaustive and records page")
    w("numbers, so a citation in a draft can be traced to a source page rather than trusted.\n")
    w("## Corpus\n")
    w("| | |\n|---|---|")
    w(f"| PDFs scanned | {c['documents']} |")
    w(f"| Pages | {c['pages']:,} |")
    w(f"| Readable | {c['readable']} |")
    w(f"| **No text layer (not searched)** | **{c['noTextLayer']}** |")
    w(f"| Unreadable | {c['unreadable']} |")
    w(f"| Distinct citations | {len(cites):,} |")
    w(f"| Total occurrences | {sum(x['occurrenceCount'] for x in cites):,} |\n")
    w("A PDF with no text layer yields no citations. That is **not** the same as containing")
    w("none — those documents are unsearched until OCR'd.\n")
    w("## What was catalogued\n")
    w("| Kind | Distinct |\n|---|---|")
    for k, n in kinds.most_common():
        w(f"| `{k}` | {n} |")
    w("\n`authority` rows join a case name to its reporter cite and year — the form a drafter")
    w("writes. `case_name` and `case_reporter` are the unjoined fragments, kept because many")
    w("citations appear in only one form.\n")
    w("## Coverage by active matter\n")
    w("Attribution follows each matter's `documents[]` cross-references, not the folder a PDF")
    w("sits in — Matters 32 and 33 are document homes holding other matters' dockets, and")
    w("folder-derived attribution reported zero for Matters 1, 2, 7 and 20.\n")
    w("| Matter | Caption | Distinct citations |\n|---|---|---|")
    for m in active:
        w(f"| {m} | {caption.get(m, '')[:44]} | {len(by_matter.get(m, ()))} |")
    w("\n## Highest-exposure citations\n")
    w(f"{len(unverified)} of {len(auth)} paired authorities do not appear in the July audit. Of those,")
    w(f"**{len(risky)} are asserted only in Plaintiff's own filings**, with no court order or")
    w("opposing brief in the corpus citing them back. Unverified *and* uncorroborated is where a")
    w("fabricated or miscited authority survives undetected — the queue worth working first.\n")
    w("| Uses | Authority | Matters |\n|---|---|---|")
    for a in risky[:40]:
        w(f"| {a['occurrenceCount']} | {a['citation'][:70]} | {', '.join(map(str, a['matters']))} |")
    w(f"\n_{len(risky)} total; full list in the JSON._\n")
    w("## Known-bad citations from the July audit — current locations\n")
    for label, pat in [("In re Leman — *likely fabricated*", r"\bLeman\b"),
                       ("Friends of the Trinity River — *likely fabricated*", r"Trinity River"),
                       ("ACSOL v. Macomber — *wrong court in M9/M19*", r"Alliance for Constitutional")]:
        w(f"**{label}**\n")
        locs = sorted({(o["document"], o["page"], o["role"])
                       for x in cites if re.search(pat, x["citation"], re.I)
                       for o in x["occurrences"]})
        for doc, page, role in locs[:12]:
            w(f"- `{doc}` p.{page} — {role}")
        if len(locs) > 12:
            w(f"- …and {len(locs) - 12} more")
        w("")
    w("## Catalog gaps — unsearchable documents in active matters\n")
    w(f"{len(gaps)} documents in active matters have no text layer. Until OCR'd, the index cannot")
    w("speak to what they cite. Court orders are the ones that matter.\n")
    w("| Matter | Role | Pages | Document |\n|---|---|---|---|")
    for d in sorted(gaps, key=lambda x: (x["role"] != "court_order", x["matter"] or 0))[:24]:
        w(f"| {d['matter']} | {d['role']} | {d['pages']} | {d['path'].split('/')[-1][:56]} |")
    w(f"\n_{len(gaps)} total._\n")
    w("## Regenerating\n```\npython3 -m pip install pymupdf")
    w("python3 internal/scripts/build-citation-index.py")
    w("python3 internal/scripts/build-citation-index.py --check\n```\n")
    w("## Known limitations\n")
    w("- Reporter series is occasionally dropped where source spacing is unusual (`47 Cal App 214`")
    w("  for `47 Cal.App.4th 214`) — numbers right, series not.")
    w("- Pairing refuses to join a case name to a reporter across an intervening case name, so an")
    w("  unparseable reporter leaves the authority unpaired rather than joined to the next case's")
    w("  numbers. An index that invents citations would be worse than none.")
    w("- Nothing here verifies a citation exists or says what it is claimed to say. This locates")
    w("  and counts; verification remains the audit's job.")
    return "\n".join(L) + "\n"


def main():
    check_only = "--check" in sys.argv
    start = time.time()

    citations = defaultdict(lambda: {"kind": None, "occurrences": []})
    documents = []

    for root, _dirs, files in os.walk(DOCS_ROOT):
        for fname in sorted(files):
            if not fname.lower().endswith(".pdf"):
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, DOCS_ROOT)
            pages = extract_pages(full)
            if pages is None:
                documents.append({"path": f"/documents/{rel}", "matter": matter_for(rel),
                                  "matters": matters_for(rel),
                                  "role": role_for(rel), "pages": 0, "chars": 0,
                                  "status": "unreadable", "citations": 0})
                continue

            chars = sum(len(p) for p in pages)
            found = 0
            for pageno, text in enumerate(pages, start=1):
                if not text.strip():
                    continue
                for kind, raw, s, e in scan_page(text):
                    key = normalize(kind, raw)
                    if len(key) < 3:
                        continue
                    entry = citations[key]
                    entry["kind"] = entry["kind"] or kind
                    ctx = re.sub(r"\s+", " ",
                                 text[max(0, s - CONTEXT_CHARS): e + CONTEXT_CHARS]).strip()
                    entry["occurrences"].append({
                        "matter": matter_for(rel),
                        "matters": matters_for(rel),
                        "document": f"/documents/{rel}",
                        "role": role_for(rel),
                        "page": pageno,
                        "raw": raw.strip(),
                        "context": ctx,
                    })
                    found += 1

            documents.append({
                "path": f"/documents/{rel}",
                "matter": matter_for(rel),
                "matters": matters_for(rel),
                "role": role_for(rel),
                "pages": len(pages),
                "chars": chars,
                # "no text layer" is the load-bearing distinction: a scanned PDF
                # yielding zero citations means "not searched", not "none cited".
                "status": "ok" if chars > 50 else "no_text_layer",
                "citations": found,
            })

    out = {
        "generatedBy": "internal/scripts/build-citation-index.py",
        "corpus": {
            "documents": len(documents),
            "readable": sum(1 for d in documents if d["status"] == "ok"),
            "noTextLayer": sum(1 for d in documents if d["status"] == "no_text_layer"),
            "unreadable": sum(1 for d in documents if d["status"] == "unreadable"),
            "pages": sum(d["pages"] for d in documents),
        },
        "citations": sorted(
            ({"citation": k, "kind": v["kind"],
              "occurrenceCount": len(v["occurrences"]),
              "matters": sorted({m for o in v["occurrences"] for m in o["matters"]}),
              "occurrences": v["occurrences"]}
             for k, v in citations.items()),
            key=lambda c: (-c["occurrenceCount"], c["citation"]),
        ),
        "documents": sorted(documents, key=lambda d: (d["matter"] or 9999, d["path"])),
    }

    payload = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    report = build_report(out)

    if check_only:
        stale = [name for name, path, want in
                 (("citation_index.json", OUT_PATH, payload),
                  ("CITATION_INDEX.md", REPORT_PATH, report))
                 if (open(path).read() if os.path.exists(path) else "") != want]
        if stale:
            print(f"{', '.join(stale)} out of date. Run: "
                  "python3 internal/scripts/build-citation-index.py")
            return 1
        print(f"OK — citation index current ({len(out['citations'])} distinct citations).")
        return 0

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        f.write(payload)
    with open(REPORT_PATH, "w") as f:
        f.write(report)

    c = out["corpus"]
    print(f"Scanned {c['documents']} PDFs ({c['pages']:,} pages) in {time.time() - start:.1f}s")
    print(f"  {c['readable']} readable, {c['noTextLayer']} with no text layer, "
          f"{c['unreadable']} unreadable")
    print(f"Found {len(out['citations']):,} distinct citations "
          f"({sum(x['occurrenceCount'] for x in out['citations']):,} occurrences)")
    print(f"\nWrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
