"""Shared, corrected check helpers for the PDF audit tiers.

Tier 1-3 each carried their own copy of these checks, and three of them were
producing systematic false positives:

* deadlines   the tiers compared PDF dates to `timeline.json` as ISO strings
              while the timeline stores "Jul. 30, 2026", so the "already
              carried" set was always empty and every hearing-adjacent date
              was reported as missing.
* orphans     `.gitkeep` placeholders and nested subfolders were reported as
              unreferenced filings.
* misfiled    documents that are not court filings at all (agency complaints,
              correspondence) were flagged for "carrying another matter's case
              number" merely because they cite the related federal action.
* mislabeled  a substring match meant "Notice of ... Order" was judged against
              the ORDER marker, and multi-document packets were judged against
              every type named in the filename.
* cross_ref   defendant keys collapsed to generic words ("Director",
              "Service", "Federal"), matching almost any filing.

Everything here is pure so the tiers stay thin and the behaviour is testable.
"""
import os
import re
from datetime import date

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

DATE_RX = re.compile(
    r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+"
    r"(\d{1,2}),?\s+(20\d{2})\b",
    re.I,
)
NUMERIC_DATE_RX = re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](20\d{2})\b")

PROCEEDING_RX = re.compile(
    r"(case management conference|status conference|order to show cause|"
    r"settlement conference|trial setting conference|hearing|trial|cmc|osc|"
    r"motion to dismiss|motion to strike|demurrer|motion)\b",
    re.I,
)
SETTING_RX = re.compile(
    r"(?:is|are|has been|have been|was|were)?\s*"
    r"(?:set|scheduled|calendared|continued|reset|noticed)\s*(?:for|to|on|at)?\b|"
    r"\b(?:hearing|trial|cmc|conference)\s*date\s*[:\-]|"
    r"\bdate\s*[:\-]\s*$",
    re.I,
)
FORM_SETTING_RX = re.compile(
    r"\b(?:dept|department|dep't|div|division|courtroom|time)\s*[:.]?\s*\w", re.I
)
STAMP_RX = re.compile(
    r"Case\s+\d:\d{2}-[a-z]{2}-\d{4,}[^\n]*?Page\s+\d+\s+of\s+\d+", re.I
)
UNASSIGNED_CASE_RX = re.compile(r"case\s*(?:no\.?|number)\s*[:.]?\s*(?:_{3,}|\[?to be assigned\]?|n/?a\b)", re.I)
BLANK_FORM_RX = re.compile(r"\bblank\s*(?:form|copy)\b|\bfillable\b|\btemplate\b", re.I)
CASE_NO_RX = re.compile(r"\b(?:\d:\d{2}-[a-z]{2}-\d{4,}|[0-9]{2}[A-Z]{2,}[0-9]{4,}|[A-Z]{2,}-CV-[A-Z]{2}-\d{4}-\d+)\b")

GENERIC_PARTY_WORDS = {
    "state", "california", "county", "city", "officer", "sergeant", "deputy",
    "individual", "capacity", "official", "does", "inc", "llc", "corporation",
    "company", "services", "service", "department", "program", "united",
    "district", "court", "superior", "director", "federal", "inclusive",
    "through", "national", "american", "group", "employment", "highway",
    "patrol", "commander", "captain", "sheriff", "police", "board", "agency",
    "authority", "commission", "office", "bureau", "center", "hope", "unknown",
    "defendants", "defendant", "respondents", "respondent", "entity", "entities",
}

DOC_TYPE_MARKERS = [
    ("amended complaint", r"AMENDED COMPLAINT"),
    ("complaint", r"COMPLAINT|PETITION|CAUSES? OF ACTION"),
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
]
# a label preceded by one of these is describing the *subject* of the document,
# not the document's own type ("Notice of Supplemental Authority - Serrato Order")
SUBJECT_PREFIX_RX = r"(notice of|opposition to|reply|request for|response to|re[:\s]|ereceipt|gmail)"


def parse_month_date(mt):
    return date(int(mt.group(3)), MONTHS[mt.group(1)[:3].lower()], int(mt.group(2)))


# ---------------------------------------------------------------- timeline side
def parse_timeline_date(value):
    """Parse the timeline's own display format as well as ISO."""
    if not isinstance(value, str):
        return None
    v = value.strip()
    iso = re.match(r"(20\d{2})-(\d{2})-(\d{2})", v)
    if iso:
        return date(int(iso.group(1)), int(iso.group(2)), int(iso.group(3)))
    mt = DATE_RX.search(v)
    if not mt:
        return None
    try:
        return parse_month_date(mt)
    except ValueError:
        return None


def timeline_dates_for(timeline, matter):
    """ISO dates the timeline already carries for one matter ('All' counts)."""
    out = set()
    for ev in timeline:
        d = parse_timeline_date(ev.get("date"))
        if not d:
            continue
        refs = ev.get("matters")
        if refs is None:
            refs = ev.get("matter_refs") or []
        if isinstance(refs, (int, str)):
            refs = [refs]
        hit = False
        for r in refs:
            s = str(r)
            if s.strip().lower() == "all":
                hit = True
                break
            if matter in {int(n) for n in re.findall(r"\d+", s)}:
                hit = True
                break
        if hit or matter == ev.get("matter"):
            out.add(d.isoformat())
    return out


# --------------------------------------------------------------------- orphans
def is_auditable_file(path):
    """Only real filings count; skip dotfiles, placeholders and subfolders."""
    base = os.path.basename(path)
    if base.startswith(".") or base.lower() == "readme.md":
        return False
    if BLANK_FORM_RX.search(base):
        return False  # blank court forms are working templates, not record filings
    if os.path.isdir(path):
        return False
    return True


# -------------------------------------------------------------------- misfiled
def substantive_text(text):
    """Text with the repeated ECF page stamps removed.

    A scanned brief often extracts as nothing but its electronic file stamp on
    every page, which looks like readable text but carries no content.
    """
    return STAMP_RX.sub(" ", text or "").strip()


def looks_like_court_filing(text):
    """A misfile claim only makes sense for something filed in a court."""
    if CASE_NO_RX.search(text):
        return True
    return bool(re.search(r"SUPERIOR COURT|DISTRICT COURT|COURT OF APPEAL|CASE NO", text, re.I))


def misfiled_detail(text_squashed, text, own_case, foreign_cases):
    """foreign_cases: {matter: squashed case number}. Returns detail or None."""
    if not own_case or own_case in text_squashed:
        return None
    if not looks_like_court_filing(text):
        return None
    if UNASSIGNED_CASE_RX.search(text):
        return None  # filed before the court assigned this matter its number
    foreign = [f"matter {o:02d} ({raw})" for o, (sq, raw) in foreign_cases.items() if sq in text_squashed]
    if not foreign:
        return None
    return "text carries only another matter's case number: " + "; ".join(foreign)


# ------------------------------------------------------------------ mislabeled
def mislabel_detail(fname, text):
    low = fname.lower()
    # multi-document packets legitimately name several types
    if re.search(r"packet|combined|complete filing|bundle|\(.*,.*\)", low):
        return None
    for label, marker in DOC_TYPE_MARKERS:
        idx = low.find(label)
        if idx < 0:
            continue
        prefix = low[:idx]
        if re.search(SUBJECT_PREFIX_RX, prefix):
            continue  # label describes the attachment/subject, not this document
        if re.search(marker, text, re.I):
            return None  # primary label is supported; stop at the first real one
        return f"filename says '{label}' but the text has no matching marker"
    return None


# ------------------------------------------------------------------- cross_ref
def party_keys(defendants):
    """Distinctive proper-name keys for cross-reference matching."""
    keys = set()
    for chunk in re.split(r";|\band\b|,", defendants or ""):
        words = [
            w for w in re.findall(r"[A-Z][A-Za-z\-']{3,}", chunk)
            if w.lower() not in GENERIC_PARTY_WORDS
        ]
        if words:
            keys.add(max(words, key=len))
    return keys


# -------------------------------------------------------------------- deadlines
def filename_dates(fname):
    out = set()
    for mt in DATE_RX.finditer(fname):
        try:
            out.add(parse_month_date(mt).isoformat())
        except ValueError:
            pass
    for mt in NUMERIC_DATE_RX.finditer(fname):
        try:
            out.add(date(int(mt.group(3)), int(mt.group(1)), int(mt.group(2))).isoformat())
        except ValueError:
            pass
    return out


def deadline_details(text, fname, carried_iso, floor=date(2026, 1, 1)):
    """Dates a filing actually *sets* that the timeline does not carry.

    Requires explicit setting language (or caption/form field layout) near the
    date, so a prose reference to a date or a date echoed from the filename is
    not reported as a missing deadline.
    """
    fdates = filename_dates(fname)
    seen, out = set(), []
    for mt in DATE_RX.finditer(text):
        at = mt.start()
        before = text[max(0, at - 160):at]
        window = text[max(0, at - 160):at + 80]
        procs = [x for x in PROCEEDING_RX.finditer(window)
                 if not re.match(r"trial\s*date\s*[:.]?\s*not\s*set",
                                 window[x.start():x.start() + 30], re.I)]
        if not procs:
            continue
        anchor = at - max(0, at - 160)
        proc = min(procs, key=lambda x: abs(x.start() - anchor))
        try:
            d = parse_month_date(mt)
        except ValueError:
            continue
        iso = d.isoformat()
        if d < floor or iso in carried_iso or iso in fdates:
            continue
        if not (SETTING_RX.search(before) or FORM_SETTING_RX.search(window)):
            continue
        kind = proc.group(1).lower()
        if (iso, kind) in seen:
            continue
        seen.add((iso, kind))
        out.append((iso, kind, f"filing sets a {kind} on {iso} that the timeline does not carry"))
    return out


def unreadable_detail(text, case_no_squashed=""):
    """None when the document has verifiable content, else the reason."""
    text = text or ""
    body = substantive_text(text)
    if len(body) >= 120:
        return None
    if len(text.strip()) - len(body) > 60:
        return ("text extracts as electronic file stamps only; the body is an "
                "image layer that needs OCR before it can be verified")
    if case_no_squashed and case_no_squashed in squash_ref(body) and len(body) >= 60:
        return None  # thin cover page, but its case number is legible
    return "no usable text after extraction and OCR; content cannot be verified"


def squash_ref(value):
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())
