#!/usr/bin/env python3
"""Multi-source citation existence lookup (offline bulk oracle + CourtListener + CAP).

Probe order:
  0. cl_bulk_offline — CourtListener bulk citations table (local SQLite,
     exact (volume, reporter, page) triple). Existence only; cannot
     fuzzy-match, so it cannot launder a fabricated cite. A miss is not
     NOT_FOUND (quarterly snapshot) — it falls through to live probes.
  1. CourtListener Citation Lookup (POST /api/rest/v4/citation-lookup/) when
     COURTLISTENER_TOKEN is set — the pin API (200 / 404 / 400 / 300)
  2. CourtListener REST search API (unauthenticated /api/rest/v4/search/) as corroboration
  3. Caselaw Access Project bulk metadata at static.case.law (CasesMetadata.json)
  4. (opt-in --probe-extra) govinfo.gov search API (USCOURTS collection; POST +
     name-match) and cdn.ca9.uscourts.gov (9th Circuit PDFs; opinions then
     memoranda). Evidence only — does not vote in consensus. Unbound U.S.
     Reports slips (*Horn*) are supremecourt.gov, not USCOURTS.

Also records reachability for Justia and Google Scholar (usually blocked).

Consensus vocabulary: FOUND / NOT_FOUND / UNRESOLVED / PARTIAL /
CAPTION_MISMATCH / BLOCKED / UNKNOWN. NOT_FOUND requires every applicable
live pin source to have run and missed (incl. an explicit citation-lookup 404);
anything less is UNRESOLVED. A skipped bulk DB never blocks a citation-lookup
404. Name-only search hits (no reporter/WL pin behind them) cap at PARTIAL.

Pin confidence is separate from existence: only CAP reporter HTML
page-label anchors or an official preliminary-print/bound PDF confirm a
reporter pin (PRIMARY). Pins confirmed through CourtListener plain_text,
govinfo/ca9/courts.ca.gov slip PDFs, or unbound U.S. cites are SECONDARY
by construction.

This does NOT mark portfolio statuses by itself — it produces evidence for
manual / round-overlay confirmation. Characterization still needs opinion text.

Usage:
  python3 internal/scripts/lookup-citations.py
  python3 internal/scripts/lookup-citations.py --cite "521 U.S. 399"
  python3 internal/scripts/lookup-citations.py --batch controls
  python3 internal/scripts/lookup-citations.py --batch high-risk
  python3 internal/scripts/lookup-citations.py --matter 28
  python3 internal/scripts/lookup-citations.py --cites-file /tmp/cites.json
  python3 internal/scripts/lookup-citations.py --cite "765 F.3d 999" --probe-extra
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_PATH = DOCS / "citation_lookup_multisource.json"

UA = "litigation-portfolio-citation-verify/1.0 (+local; research)"
CL_SEARCH = "https://www.courtlistener.com/api/rest/v4/search/"
CL_CITATION_LOOKUP = "https://www.courtlistener.com/api/rest/v4/citation-lookup/"
CAP_STATIC = "https://static.case.law"
CL_TOKEN_ENV = "COURTLISTENER_TOKEN"
CL_TOKEN_ENV_ALT = "COURTLISTENER_API_TOKEN"

_citation_lookup_disabled = False
_citation_lookup_last_call = 0.0

# reporter slug on static.case.law → regex capturing (volume, page)
REPORTER_MAP = [
    (r"(\d+)\s+U\.?\s*S\.?\s+(\d+)", "us", "U.S."),
    (r"(\d+)\s+F\.\s*R\.\s*D\.\s+(\d+)", "frd", "F.R.D."),
    (r"(\d+)\s+F\.\s*2d\s+(\d+)", "f2d", "F.2d"),
    (r"(\d+)\s+F\.\s*3d\s+(\d+)", "f3d", "F.3d"),
    (r"(\d+)\s+F\.\s*4th\s+(\d+)", "f4th", "F.4th"),
    (r"(\d+)\s+F\.\s*App'?x\s+(\d+)", "f-appx", "F. App'x"),
    (r"(\d+)\s+F\.\s*Supp\.\s*2d\s+(\d+)", "f-supp-2d", "F. Supp. 2d"),
    (r"(\d+)\s+F\.\s*Supp\.\s*3d\s+(\d+)", "f-supp-3d", "F. Supp. 3d"),
    (r"(\d+)\s+M\.?\s*J\.?\s+(\d+)", "mj", "M.J."),
    (r"(\d+)\s+Cal\.\s*App\.\s*5th\s+(\d+)", "cal-app-5th", "Cal. App. 5th"),
    (r"(\d+)\s+Cal\.\s*App\.\s*4th\s+(\d+)", "cal-app-4th", "Cal. App. 4th"),
    (r"(\d+)\s+Cal\.\s*App\.\s*3d\s+(\d+)", "cal-app-3d", "Cal. App. 3d"),
    (r"(\d+)\s+Cal\.\s*5th\s+(\d+)", "cal-5th", "Cal. 5th"),
    (r"(\d+)\s+Cal\.\s*4th\s+(\d+)", "cal-4th", "Cal. 4th"),
    (r"(\d+)\s+Cal\.\s*3d\s+(\d+)", "cal-3d", "Cal. 3d"),
    (r"(\d+)\s+Cal\.\s*2d\s+(\d+)", "cal-2d", "Cal. 2d"),
    (r"(\d+)\s+S\.\s*Ct\.\s+(\d+)", "s-ct", "S. Ct."),
    (r"(\d+)\s+L\.\s*Ed\.\s*2d\s+(\d+)", "l-ed-2d", "L. Ed. 2d"),
]

WL_RE = re.compile(r"(?:WL|Westlaw)\s*(\d{7,})", re.I)
NAME_RE = re.compile(
    r"^(?:See\s+)?(.+?),\s+\d+\s+(?:U\.S\.|F\.|Cal\.)",
    re.I,
)

# Offline existence oracle: CourtListener bulk citations table (public S3).
# Build once with: python3 internal/scripts/build-bulk-citation-index.py
# DB lives outside the repo. A miss is not NOT_FOUND (quarterly cutoff).
BULK_SNAPSHOT = "2026-06-30"
BULK_S3_URL = (
    "https://com-courtlistener-storage.s3.amazonaws.com"
    f"/bulk-data/citations-{BULK_SNAPSHOT}.csv.bz2"
)
BULK_SQLITE_ENV = "CL_BULK_SQLITE"
BULK_SQLITE_DEFAULT = str(
    Path.home() / "workspace/legal-research/citation-bulk/citations.sqlite"
)
BULK_REPORTER = {
    "U.S.": "U.S.",
    "S. Ct.": "S. Ct.",
    "L. Ed. 2d": "L. Ed. 2d",
    "F.2d": "F.2d",
    "F.3d": "F.3d",
    "F.4th": "F.4th",
    "F. App'x": "F. App'x",
    "F. Supp. 2d": "F. Supp. 2d",
    "F. Supp. 3d": "F. Supp. 3d",
    "F.R.D.": "F.R.D.",
    "M.J.": "M.J.",
    "Cal. 2d": "Cal. 2d",
    "Cal. 3d": "Cal. 3d",
    "Cal. 4th": "Cal. 4th",
    "Cal. 5th": "Cal. 5th",
    "Cal. App. 3d": "Cal. App. 3d",
    "Cal. App. 4th": "Cal. App. 4th",
    "Cal. App. 5th": "Cal. App. 5th",
}

_bulk_db_ok: bool | None = None


@dataclass
class SourceHit:
    source: str
    found: bool
    url: str = ""
    case_name: str = ""
    citations: list[str] = field(default_factory=list)
    notes: str = ""
    http_status: int | None = None
    # True when the hit came from a caption/name search with no reporter- or
    # WL-pin match behind it. Name-only hits can never produce FOUND alone:
    # they cap at PARTIAL (the fuzzy path that launders fabricated captions).
    name_only: bool = False


@dataclass
class LookupResult:
    query: str
    case_name_guess: str
    reporter_pin: str | None
    wl_pin: str | None
    sources: list[SourceHit] = field(default_factory=list)
    consensus: str = "UNKNOWN"  # FOUND / NOT_FOUND / UNRESOLVED / PARTIAL / CAPTION_MISMATCH / BLOCKED / UNKNOWN
    matched_name: str = ""
    matched_citations: list[str] = field(default_factory=list)


_cap_cache: dict[str, list[dict]] = {}


def http_get(url: str, accept: str = "application/json", timeout: int = 45, retries: int = 3):
    last = (-1, "error", b"")
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": UA, "Accept": accept},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            last = (e.code, str(e.reason), body)
            if e.code in (429, 502, 503, 504) and attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            return last
        except Exception as e:
            last = (-1, type(e).__name__, str(e).encode())
            if attempt + 1 < retries:
                time.sleep(0.75 * (attempt + 1))
                continue
            return last
    return last


def http_post_form(
    url: str,
    fields: dict[str, str],
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 45,
    retries: int = 3,
):
    last = (-1, "error", b"")
    body_bytes = urllib.parse.urlencode(fields).encode()
    for attempt in range(retries):
        req_headers = {
            "User-Agent": UA,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        if headers:
            req_headers.update(headers)
        req = urllib.request.Request(url, data=body_bytes, headers=req_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            last = (e.code, str(e.reason), body)
            if e.code in (429, 502, 503, 504) and attempt + 1 < retries:
                wait = 2.0 * (attempt + 1)
                if e.code == 429:
                    wait = 65.0
                time.sleep(wait)
                continue
            return last
        except Exception as e:
            last = (-1, type(e).__name__, str(e).encode())
            if attempt + 1 < retries:
                time.sleep(0.75 * (attempt + 1))
                continue
            return last
    return last


def http_post_json(
    url: str,
    payload: dict,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 45,
    retries: int = 3,
):
    last = (-1, "error", b"")
    body_bytes = json.dumps(payload).encode()
    for attempt in range(retries):
        req_headers = {
            "User-Agent": UA,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if headers:
            req_headers.update(headers)
        req = urllib.request.Request(url, data=body_bytes, headers=req_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read()
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            last = (e.code, str(e.reason), body)
            if e.code in (429, 502, 503, 504) and attempt + 1 < retries:
                wait = 2.0 * (attempt + 1)
                if e.code == 429:
                    wait = 65.0
                time.sleep(wait)
                continue
            return last
        except Exception as e:
            last = (-1, type(e).__name__, str(e).encode())
            if attempt + 1 < retries:
                time.sleep(0.75 * (attempt + 1))
                continue
            return last
    return last


def _dotenv_value(*keys: str) -> str | None:
    wanted = {k.strip() for k in keys}
    for path in (ROOT.parent / ".env", ROOT / ".env"):
        if not path.is_file():
            continue
        try:
            lines = path.read_text().splitlines()
        except OSError:
            continue
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            key, sep, val = line.partition("=")
            if not sep:
                continue
            if key.strip() not in wanted:
                continue
            val = val.strip().strip("'").strip('"')
            if val:
                return val
    return None


def _dotenv_token() -> str | None:
    return _dotenv_value(CL_TOKEN_ENV, CL_TOKEN_ENV_ALT)


def courtlistener_token() -> str | None:
    if _citation_lookup_disabled:
        return None
    tok = (os.environ.get(CL_TOKEN_ENV) or os.environ.get(CL_TOKEN_ENV_ALT) or "").strip()
    if tok:
        return tok
    return _dotenv_token()


def reporter_pin_key(citation: str) -> str | None:
    rep = parse_reporter(citation)
    if not rep:
        return None
    slug = re.sub(r"[^a-z0-9]+", "", str(rep["label"]).lower())
    return f"{rep['volume']} {slug} {rep['page']}"


def parse_reporter(citation: str):
    c = citation.replace("Cal.App.", "Cal. App.").replace("Cal.App ", "Cal. App. ")
    c = re.sub(r"\s+", " ", c)
    for pat, slug, label in REPORTER_MAP:
        m = re.search(pat, c, re.I)
        if m:
            vol, page = m.group(1), m.group(2)
            return {
                "volume": vol,
                "page": page,
                "slug": slug,
                "label": label,
                "pin": f"{vol} {label} {page}",
            }
    return None


def bulk_db_path() -> Path | None:
    """SQLite index path, or None when it has not been built."""
    global _bulk_db_ok
    if _bulk_db_ok is False:
        return None
    p = Path(os.environ.get(BULK_SQLITE_ENV) or BULK_SQLITE_DEFAULT)
    if p.is_file():
        _bulk_db_ok = True
        return p
    _bulk_db_ok = False
    return None


def probe_bulk_offline(citation: str) -> SourceHit:
    """Step 0: exact (volume, reporter, page) existence check, offline."""
    rep = parse_reporter(citation)
    db = bulk_db_path()
    if not rep:
        return SourceHit(
            source="cl_bulk_offline",
            found=False,
            notes="skipped: no reporter pin to form a (volume, reporter, page) triple",
        )
    if db is None:
        return SourceHit(
            source="cl_bulk_offline",
            found=False,
            notes=(
                "skipped: bulk SQLite index not built "
                "(run internal/scripts/build-bulk-citation-index.py)"
            ),
        )
    reporter = BULK_REPORTER.get(rep["label"])
    if not reporter:
        return SourceHit(
            source="cl_bulk_offline",
            found=False,
            notes=f"skipped: reporter {rep['label']!r} has no bulk-table string mapping",
        )
    import sqlite3

    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        rows = con.execute(
            "SELECT cluster_id, cite_type FROM citations "
            "WHERE reporter = ? AND volume = ? AND page = ?",
            (reporter, str(rep["volume"]), str(rep["page"])),
        ).fetchall()
        con.close()
    except Exception as e:
        return SourceHit(
            source="cl_bulk_offline",
            found=False,
            notes=f"bulk index read error: {type(e).__name__}",
        )
    if not rows:
        return SourceHit(
            source="cl_bulk_offline",
            found=False,
            notes=(
                f"triple ({rep['volume']}, {reporter}, {rep['page']}) absent from "
                f"{BULK_SNAPSHOT} snapshot — not NOT_FOUND (quarterly cutoff); "
                "falls through to live probes"
            ),
        )
    cluster_ids = sorted({r[0] for r in rows})
    first = cluster_ids[0]
    notes = (
        f"exact triple hit in {BULK_SNAPSHOT} snapshot: "
        f"{len(rows)} row(s), {len(cluster_ids)} cluster(s); "
        "existence only — caption/pin/holdings unverified"
    )
    if len(cluster_ids) > 1:
        notes += "; multiple clusters share this page (table-page collision — disambiguate by caption)"
    return SourceHit(
        source="cl_bulk_offline",
        found=True,
        url=f"https://www.courtlistener.com/api/rest/v4/clusters/{first}/",
        citations=[rep["pin"]],
        notes=notes,
    )


def guess_name(citation: str) -> str:
    c = citation.strip()
    c = re.sub(
        r"^(?:See|Under|In|Holding\s+Key\s+Fact)\s+",
        "",
        c,
        flags=re.I,
    )
    m = NAME_RE.search(c)
    if m:
        return m.group(1).strip()
    # fallback: text before first digit run
    m2 = re.match(r"^([^0-9]+)", c)
    return (m2.group(1).strip(" ,") if m2 else citation)[:80]


def normalize_name(s: str) -> str:
    s = s.lower()
    s = s.replace("’", "'").replace("‘", "'")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _party_tokens(name: str) -> tuple[set[str], set[str]]:
    """Split a caption into plaintiff/defendant token sets when 'v' is present."""
    noise = {
        "v",
        "vs",
        "inc",
        "llc",
        "ltd",
        "co",
        "corp",
        "the",
        "of",
        "and",
        "see",
        "re",
        "in",
    }
    n = normalize_name(name)
    parts = n.split(" v ")
    if len(parts) == 1:
        toks = set(n.split()) - noise
        return toks, set()
    left = set(parts[0].split()) - noise
    right = set(parts[1].split()) - noise
    return left, right


def names_compatible(a: str, b: str) -> bool:
    na, nb = normalize_name(a), normalize_name(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    la, ra = _party_tokens(a)
    lb, rb = _party_tokens(b)
    # Both sides of "v." present: require left overlap and a tight right match.
    if ra and rb:
        # Leading plaintiff token must agree (blocks Home ⊂ "... at Home").
        def lead(name: str) -> str | None:
            n = normalize_name(name).split(" v ")[0]
            noise2 = {"v", "vs", "inc", "llc", "ltd", "co", "corp", "the", "of", "and", "see", "re", "in"}
            toks = [t for t in n.split() if t not in noise2]
            return toks[0] if toks else None

        def ordered_left(name: str) -> list[str]:
            n = normalize_name(name).split(" v ")[0]
            noise2 = {
                "v",
                "vs",
                "inc",
                "llc",
                "ltd",
                "co",
                "corp",
                "the",
                "of",
                "and",
                "see",
                "re",
                "in",
                "department",
                "dept",
            }
            return [t for t in n.split() if t not in noise2]

        oa_l, ob_l = ordered_left(a), ordered_left(b)
        lead_a, lead_b = (oa_l[0] if oa_l else None), (ob_l[0] if ob_l else None)
        left_seq_ok = False
        if oa_l and ob_l:
            if oa_l == ob_l:
                left_seq_ok = True
            elif len(oa_l) >= 2 and oa_l == ob_l[: len(oa_l)]:
                left_seq_ok = True
            elif len(ob_l) >= 2 and ob_l == oa_l[: len(ob_l)]:
                left_seq_ok = True
            elif len(oa_l) >= 2 and any(
                oa_l == ob_l[i : i + len(oa_l)] for i in range(len(ob_l) - len(oa_l) + 1)
            ):
                # "California Highway Patrol" inside "Department of California Highway Patrol"
                left_seq_ok = True
            elif len(ob_l) >= 2 and any(
                ob_l == oa_l[i : i + len(ob_l)] for i in range(len(oa_l) - len(ob_l) + 1)
            ):
                left_seq_ok = True
        if lead_a and lead_b and lead_a != lead_b and not left_seq_ok:
            return False
        left_ok = left_seq_ok or bool(la & lb) or not la or not lb
        if not left_ok:
            return False
        # Ordered prefix: "Dry Creek" ≈ "Dry Creek Joint Elementary School District",
        # but a 1-token right side ("Morgan") must not absorb a longer different entity
        # ("Morgan Hill Unified").
        def ordered(name: str, side: str) -> list[str]:
            n = normalize_name(name)
            parts = n.split(" v ")
            chunk = parts[0] if side == "left" else (parts[1] if len(parts) > 1 else n)
            noise2 = {"v", "vs", "inc", "llc", "ltd", "co", "corp", "the", "of", "and", "see", "re", "in"}
            return [t for t in chunk.split() if t not in noise2]

        oa, ob = ordered(a, "right"), ordered(b, "right")
        if oa and ob:
            if oa == ob:
                return True
            if len(oa) >= 2 and len(oa) <= len(ob) and oa == ob[: len(oa)]:
                return True
            if len(ob) >= 2 and len(ob) <= len(oa) and ob == oa[: len(ob)]:
                return True
            return bool(ra & rb) and len(ra & rb) >= 2
        return bool(ra & rb)

    # One-sided / In re captions
    if na in nb or nb in na:
        return True
    ta, tb = la | ra, lb | rb
    if not ta or not tb:
        return False
    overlap = ta & tb
    return len(overlap) >= min(2, len(ta), len(tb))


def load_cap_volume(slug: str, volume: str) -> list[dict] | None:
    key = f"{slug}/{volume}"
    if key in _cap_cache:
        return _cap_cache[key]
    url = f"{CAP_STATIC}/{slug}/{volume}/CasesMetadata.json"
    status, ctype, body = http_get(url)
    if status != 200 or b"[" not in body[:20]:
        _cap_cache[key] = None  # type: ignore
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        _cap_cache[key] = None  # type: ignore
        return None
    _cap_cache[key] = data
    return data


def lookup_cap(citation: str, name_guess: str) -> SourceHit:
    rep = parse_reporter(citation)
    if not rep:
        return SourceHit(
            source="case.law_static",
            found=False,
            notes="No supported reporter pin to resolve on static.case.law",
        )
    meta = load_cap_volume(rep["slug"], rep["volume"])
    if meta is None:
        # volume missing — for negative controls this is informative
        url = f"{CAP_STATIC}/{rep['slug']}/{rep['volume']}/CasesMetadata.json"
        status, _, _ = http_get(url)
        return SourceHit(
            source="case.law_static",
            found=False,
            url=url,
            http_status=status,
            notes=f"Volume metadata unavailable for {rep['slug']}/{rep['volume']}",
        )
    page = str(rep["page"])
    # Prefer exact first_page match (table pages may host multiple dispositions).
    exact = [c for c in meta if str(c.get("first_page")) == page]
    chosen = None
    if exact:
        # if multiple, prefer name match
        for c in exact:
            if names_compatible(name_guess, c.get("name_abbreviation") or c.get("name") or ""):
                chosen = c
                break
        chosen = chosen or exact[0]
    if not chosen:
        return SourceHit(
            source="case.law_static",
            found=False,
            url=f"{CAP_STATIC}/{rep['slug']}/{rep['volume']}/CasesMetadata.json",
            notes=f"No case with first_page={page} in CAP volume {rep['slug']}/{rep['volume']}",
        )
    cites = [x.get("cite", "") for x in (chosen.get("citations") or []) if x.get("cite")]
    fname = chosen.get("file_name") or ""
    case_url = (
        f"{CAP_STATIC}/{rep['slug']}/{rep['volume']}/html/{fname}.html"
        if fname
        else f"{CAP_STATIC}/{rep['slug']}/{rep['volume']}/CasesMetadata.json"
    )
    name = chosen.get("name_abbreviation") or chosen.get("name") or ""
    name_ok = names_compatible(name_guess, name)
    notes = "Exact first_page match in CAP CasesMetadata.json"
    if not name_ok:
        notes += f"; caption mismatch vs query name ({name_guess!r} vs {name!r})"
    return SourceHit(
        source="case.law_static",
        found=True,
        url=case_url,
        case_name=name,
        citations=cites,
        notes=notes,
        http_status=200,
    )


def _cluster_name(cluster: dict) -> str:
    return (
        cluster.get("case_name")
        or cluster.get("caseName")
        or cluster.get("case_name_full")
        or ""
    )


def _cluster_url(cluster: dict) -> str:
    path = cluster.get("absolute_url") or cluster.get("frontend_url") or ""
    if path.startswith("/"):
        return "https://www.courtlistener.com" + path
    return path


def _cluster_cites(cluster: dict) -> list[str]:
    out = []
    for item in cluster.get("citations") or []:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
        elif isinstance(item, dict):
            vol, reporter, page = item.get("volume"), item.get("reporter"), item.get("page")
            if vol and reporter and page:
                out.append(f"{vol} {reporter} {page}")
    return out


def _citation_lookup_row(rows: list[dict], citation: str) -> dict | None:
    if not rows:
        return None
    pin = reporter_pin_key(citation)
    if not pin:
        return rows[0]
    for row in rows:
        candidates = [row.get("citation") or ""] + list(row.get("normalized_citations") or [])
        if any(reporter_pin_key(str(c) or "") == pin for c in candidates if c):
            return row
    return rows[0]


def citation_lookup_hit(
    rows: list[dict],
    citation: str,
    name_guess: str,
    *,
    http_status: int | None,
    url: str,
) -> SourceHit:
    """Map a citation-lookup JSON array to a SourceHit. No network."""
    row = _citation_lookup_row(rows, citation)
    if not row:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=url,
            http_status=http_status,
            notes="Eyecite parsed no case citation (Westlaw-only pins often miss)",
        )
    status = row.get("status")
    clusters = [c for c in (row.get("clusters") or []) if isinstance(c, dict)]
    error = row.get("error_message") or ""
    cites = list(row.get("normalized_citations") or [])
    if row.get("citation"):
        cites = [row["citation"]] + [c for c in cites if c != row["citation"]]

    if status == 404:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=url,
            citations=cites,
            http_status=http_status,
            notes=error or f"Citation-lookup 404 for {row.get('citation') or citation}",
        )
    if status == 400:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=url,
            citations=cites,
            http_status=http_status,
            notes=error or "Citation-lookup 400: reporter not in Eyecite",
        )
    if status == 429:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=url,
            citations=cites,
            http_status=http_status,
            notes=error or "Citation-lookup 429: too many citations in this request",
        )
    if status not in {200, 300} or not clusters:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=url,
            citations=cites,
            http_status=http_status,
            notes=error or f"Citation-lookup status={status} with no clusters",
        )

    compatible = [c for c in clusters if names_compatible(name_guess, _cluster_name(c))]
    chosen = compatible[0] if compatible else clusters[0]
    name = _cluster_name(chosen)
    cluster_url = _cluster_url(chosen) or url
    cluster_cites = _cluster_cites(chosen) or cites
    notes = f"Citation-lookup status={status}; clusters={len(clusters)}"
    if status == 300:
        notes += "; ambiguous reporter/pin — picked by party-name overlap" if compatible else (
            "; ambiguous reporter/pin — no party-name overlap"
        )
    elif not compatible and name:
        notes += f"; caption mismatch vs query name ({name_guess!r} vs {name!r})"
    return SourceHit(
        source="courtlistener_citation",
        found=True,
        url=cluster_url,
        case_name=name,
        citations=cluster_cites,
        notes=notes,
        http_status=http_status,
    )


def lookup_courtlistener_citation(citation: str, name_guess: str) -> SourceHit:
    """Pin API. Requires COURTLISTENER_TOKEN. 60 valid citations/minute."""
    global _citation_lookup_disabled, _citation_lookup_last_call
    token = courtlistener_token()
    if not token:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=CL_CITATION_LOOKUP,
            notes="skipped (no COURTLISTENER_TOKEN)",
        )
    elapsed = time.monotonic() - _citation_lookup_last_call
    if _citation_lookup_last_call and elapsed < 1.05:
        time.sleep(1.05 - elapsed)

    rep = parse_reporter(citation)
    fields = {"text": citation}
    if rep:
        fields = {
            "volume": str(rep["volume"]),
            "reporter": str(rep["label"]),
            "page": str(rep["page"]),
        }
    headers = {"Authorization": f"Token {token}"}
    status, _ctype, body = http_post_form(CL_CITATION_LOOKUP, fields, headers=headers)
    _citation_lookup_last_call = time.monotonic()
    if status == 401:
        _citation_lookup_disabled = True
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=CL_CITATION_LOOKUP,
            http_status=401,
            notes="401 — COURTLISTENER_TOKEN rejected; citation-lookup disabled this run",
        )
    if status != 200 or not body:
        if rep and fields.get("volume"):
            status, _ctype, body = http_post_form(
                CL_CITATION_LOOKUP, {"text": citation}, headers=headers
            )
            _citation_lookup_last_call = time.monotonic()
        if status == 401:
            _citation_lookup_disabled = True
            return SourceHit(
                source="courtlistener_citation",
                found=False,
                url=CL_CITATION_LOOKUP,
                http_status=401,
                notes="401 — COURTLISTENER_TOKEN rejected; citation-lookup disabled this run",
            )
        if status != 200 or not body:
            return SourceHit(
                source="courtlistener_citation",
                found=False,
                url=CL_CITATION_LOOKUP,
                http_status=status if isinstance(status, int) else None,
                notes=f"citation-lookup HTTP {status}",
            )
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return SourceHit(
            source="courtlistener_citation",
            found=False,
            url=CL_CITATION_LOOKUP,
            http_status=status if isinstance(status, int) else None,
            notes="citation-lookup returned non-JSON",
        )
    rows = payload if isinstance(payload, list) else payload.get("results") or []
    return citation_lookup_hit(
        [r for r in rows if isinstance(r, dict)],
        citation,
        name_guess,
        http_status=status if isinstance(status, int) else None,
        url=CL_CITATION_LOOKUP,
    )


def lookup_courtlistener(citation: str, name_guess: str) -> SourceHit:
    rep = parse_reporter(citation)
    wl = WL_RE.search(citation)
    queries = []
    if rep:
        queries.append(f'"{rep["pin"]}"')
        # CL often stores "Cal. App. 4th" with spaces; also try compact form
        compact = rep["pin"].replace("Cal. App.", "Cal.App.").replace("F. ", "F.")
        if compact != rep["pin"]:
            queries.append(f'"{compact}"')
    if wl:
        queries.append(wl.group(1))
        queries.append(f"WL {wl.group(1)}")
    # Name-only search is a last resort for reporter pins; for WL-only pins it
    # is too noisy (same party names, different decisions) — skip it.
    if name_guess and rep and not wl:
        queries.append(f'"{name_guess}"')

    best = None
    last_status = None
    tried = []
    for q in queries:
        url = CL_SEARCH + "?" + urllib.parse.urlencode({"type": "o", "q": q})
        status, ctype, body = http_get(url)
        last_status = status
        tried.append(q)
        if status != 200:
            time.sleep(0.25)
            continue
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            time.sleep(0.25)
            continue
        results = data.get("results") or []
        # Prefer citation-exact match when we have a reporter pin
        for r in results:
            cites = [str(c) for c in (r.get("citation") or [])]
            name = r.get("caseName") or ""
            abs_url = r.get("absolute_url") or ""
            full_url = (
                "https://www.courtlistener.com" + abs_url if abs_url.startswith("/") else abs_url
            )
            cite_match = False
            if rep:
                target = normalize_name(rep["pin"])
                cite_match = any(
                    normalize_name(c) == target or target in normalize_name(c) for c in cites
                )
            wl_match = False
            if wl:
                pin = wl.group(1)
                # Require a real Westlaw token (not a bare digit hit inside another WL year-pin).
                wl_rx = re.compile(rf"(?:^|[^0-9])(?:WL\s*)?{re.escape(pin)}(?:[^0-9]|$)", re.I)
                # Prefer citations that include 'WL' with this pin; year prefixes must not
                # create false friends like 1999 WL 1034838 vs 2021 WL 1034838 — those are
                # different pins that share the same trailing digits only if we strip the year.
                # CourtListener stores the full 'YYYY WL NNNNNNN', so match that whole form
                # when the query has a year, otherwise match 'WL NNNNNNN'.
                year_m = re.search(r"\b(19|20)\d{2}\b", citation)
                if year_m:
                    full = f"{year_m.group(0)} WL {pin}"
                    wl_match = any(full.lower() in str(c).lower() for c in cites)
                else:
                    wl_match = any(wl_rx.search(str(c)) and "WL" in str(c).upper() for c in cites)
            name_match = names_compatible(name_guess, name)

            # Accept rules:
            # - reporter pin: require cite_match (name-only is insufficient)
            # - WL-only: require wl_match
            # - neither: require name_match, flagged name_only (caps at PARTIAL)
            accept = False
            if rep and cite_match:
                accept = True
            elif wl and not rep and wl_match:
                accept = True
            elif not rep and not wl and name_match:
                accept = True
            name_only_hit = bool(accept and not rep and not wl)

            if accept:
                hit = SourceHit(
                    source="courtlistener",
                    found=True,
                    url=full_url,
                    case_name=name,
                    citations=cites,
                    notes=(
                        f"Search q={q!r}; cite_match={cite_match}; "
                        f"wl_match={wl_match}; name_match={name_match}"
                        + ("; NAME-ONLY (no pin behind this hit)" if name_only_hit else "")
                    ),
                    http_status=200,
                    name_only=name_only_hit,
                )
                if (cite_match or wl_match) and name_match:
                    return hit
                if best is None or (
                    (cite_match or wl_match)
                    and "cite_match=False" in (best.notes or "")
                    and "wl_match=False" in (best.notes or "")
                ):
                    best = hit
        time.sleep(0.55)

    if best:
        return best
    return SourceHit(
        source="courtlistener",
        found=False,
        url=CL_SEARCH,
        http_status=last_status,
        notes=f"No cite/name match in queries {tried}",
    )


def probe_justia(citation: str) -> SourceHit:
    rep = parse_reporter(citation)
    if rep and rep["slug"] == "us":
        url = f"https://supreme.justia.com/cases/federal/us/{rep['volume']}/{rep['page']}/"
    else:
        url = "https://law.justia.com/search?query=" + urllib.parse.quote(citation[:80])
    status, ctype, body = http_get(url, accept="text/html")
    if status == 200 and b"Cloudflare" not in body[:500] and b"Just a moment" not in body[:500]:
        return SourceHit(
            source="justia",
            found=True,
            url=url,
            http_status=status,
            notes="HTML reachable (parse not attempted)",
        )
    return SourceHit(
        source="justia",
        found=False,
        url=url,
        http_status=status if isinstance(status, int) else None,
        notes="Blocked or unreachable (Cloudflare/403 common in this environment)",
    )


def probe_scholar(citation: str) -> SourceHit:
    q = citation if len(citation) < 120 else (parse_reporter(citation) or {}).get("pin", citation[:80])
    url = "https://scholar.google.com/scholar?" + urllib.parse.urlencode(
        {"q": f'"{q}"', "hl": "en", "as_sdt": "2006"}
    )
    status, ctype, body = http_get(url, accept="text/html")
    if status == 200 and b"gs_rt" in body:
        return SourceHit(
            source="google_scholar",
            found=True,
            url=url,
            http_status=200,
            notes="Scholar HTML returned result markup (caption parse not asserted)",
        )
    return SourceHit(
        source="google_scholar",
        found=False,
        url=url,
        http_status=status if isinstance(status, int) else None,
        notes="Blocked, challenged, or empty (403/unusual HTML common)",
    )


# ---------------------------------------------------------------------------
# Extra probes — opt-in via --probe-extra. Live-confirmed 2026-09-19.
#
# See internal/docs/citation_verification_sources.json.
#
#   govinfo  — GPO Search Service. POST JSON. Ranking is not a citator:
#              name-match required before found=True. USCOURTS does not
#              host unbound U.S. Reports slips (*Horn* is supremecourt.gov).
#   ca9_cdn  — cdn.ca9.uscourts.gov. Docket-addressable. Two-step:
#              CourtListener search → strip "No. " → opinions PDF, then
#              memoranda PDF. Pre-~2010 published opinions often 404.
#
# Evidence only — consensus_for() is intentionally untouched.
# ---------------------------------------------------------------------------

GOVINFO_SEARCH = "https://api.govinfo.gov/search"
GOVINFO_API_KEY_ENV = "GOVINFO_API_KEY"
CA9_DATASTORE = "https://cdn.ca9.uscourts.gov/datastore"
CA9_OPINIONS = f"{CA9_DATASTORE}/opinions"
CA9_MEMORANDA = f"{CA9_DATASTORE}/memoranda"

_FEDERAL_REPORTER_SLUGS = {"us", "f2d", "f3d", "f4th", "f-supp-2d", "f-supp-3d", "s-ct"}
_UNBOUND_US_RE = re.compile(r"\bU\.?\s*S\.?\s*_{2,}\b")
_CA9_COURT_TAGS = {"ninth circuit", "ca9", "9th cir."}
_CA9_NO_PREFIX = re.compile(r"^(?:no\.?\s*)+", re.I)


def is_unbound_us(citation: str) -> bool:
    return bool(_UNBOUND_US_RE.search(citation))


def govinfo_api_key() -> str:
    """GOVINFO_API_KEY if set, else the public DEMO_KEY (rate-limited)."""
    return (
        (os.environ.get(GOVINFO_API_KEY_ENV) or "").strip()
        or _dotenv_value(GOVINFO_API_KEY_ENV)
        or "DEMO_KEY"
    )


def govinfo_search_payload(query: str) -> dict:
    """POST body for api.govinfo.gov/search (Search Service, 2023+)."""
    return {
        "query": query,
        "pageSize": 10,
        "offsetMark": "*",
        "historical": True,
        "resultLevel": "default",
    }


def govinfo_query_for(citation: str) -> str | None:
    """USCOURTS field query, or None when this probe should skip."""
    if is_unbound_us(citation):
        return None
    rep = parse_reporter(citation)
    if not rep or rep["slug"] not in _FEDERAL_REPORTER_SLUGS:
        return None
    return f'collection:(USCOURTS) "{rep["pin"]}"'


def govinfo_pick_named_hit(results: list, citation: str) -> dict | None:
    """First USCOURTS row whose title matches the caption. Not hits[0]."""
    name = guess_name(citation)
    if not name:
        return None
    for row in results or []:
        if (row.get("collectionCode") or "").upper() != "USCOURTS":
            continue
        title = row.get("title") or ""
        if title and names_compatible(name, title):
            return row
    return None


def probe_govinfo(citation: str) -> SourceHit:
    """POST the govinfo Search Service; FOUND only on a caption match."""
    if is_unbound_us(citation):
        return SourceHit(
            source="govinfo",
            found=False,
            url=GOVINFO_SEARCH,
            notes=(
                "skipped: unbound U.S. Reports — USCOURTS does not host slips; "
                "authoritative source is supremecourt.gov (see citation_verification_sources.json)"
            ),
        )
    query = govinfo_query_for(citation)
    if not query:
        rep = parse_reporter(citation)
        if rep:
            return SourceHit(
                source="govinfo",
                found=False,
                url=GOVINFO_SEARCH,
                notes=f"skipped: reporter slug {rep['slug']!r} is not a federal reporter",
            )
        return SourceHit(
            source="govinfo",
            found=False,
            url=GOVINFO_SEARCH,
            notes="skipped: no federal reporter pin",
        )
    payload = govinfo_search_payload(query)
    status, ctype, body = http_post_json(
        GOVINFO_SEARCH,
        payload,
        headers={"X-Api-Key": govinfo_api_key()},
    )
    if status != 200:
        return SourceHit(
            source="govinfo",
            found=False,
            url=GOVINFO_SEARCH,
            http_status=status if isinstance(status, int) else None,
            notes="govinfo POST search unreachable or errored",
        )
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return SourceHit(
            source="govinfo",
            found=False,
            url=GOVINFO_SEARCH,
            http_status=200,
            notes="govinfo returned non-JSON",
        )
    rows = data.get("results") or []
    # GET-shaped {message} with no results — the discarded sketch.
    if not rows and data.get("message") and "results" not in data:
        return SourceHit(
            source="govinfo",
            found=False,
            url=GOVINFO_SEARCH,
            http_status=200,
            notes="govinfo returned {message} with no results (GET-shaped; need POST JSON)",
        )
    uscourts_n = sum(
        1 for r in rows if (r.get("collectionCode") or "").upper() == "USCOURTS"
    )
    hit = govinfo_pick_named_hit(rows, citation)
    if not hit:
        return SourceHit(
            source="govinfo",
            found=False,
            url=GOVINFO_SEARCH,
            http_status=200,
            notes=(
                f"no caption match for {guess_name(citation)!r} among {uscourts_n} "
                f"USCOURTS hits (query={query!r}; ranking is not a citator)"
            ),
        )
    dl = hit.get("download") or {}
    pdf = dl.get("pdfLink") or ""
    return SourceHit(
        source="govinfo",
        found=True,
        url=pdf or hit.get("resultLink") or GOVINFO_SEARCH,
        case_name=hit.get("title") or "",
        http_status=200,
        notes=f"USCOURTS packageId={hit.get('packageId')!r}; query={query!r}; name-matched",
    )


def ca9_strip_docket(docket: str) -> str:
    """CourtListener docketNumber is often 'No. 13-35356'; CDN file is 13-35356.pdf."""
    s = (docket or "").strip()
    s = _CA9_NO_PREFIX.sub("", s)
    s = s.split(",")[0].strip()
    s = s.split(";")[0].strip()
    return s


def ca9_pdf_candidates(docket: str, year: str, month: str, day: str) -> list[tuple[str, str]]:
    """opinions first, then memoranda. Live 2026-09-19: Wicklund is memoranda."""
    slug = ca9_strip_docket(docket)
    y, m, d = year, month, day
    return [
        ("opinions", f"{CA9_OPINIONS}/{y}/{m}/{d}/{slug}.pdf"),
        ("memoranda", f"{CA9_MEMORANDA}/{y}/{m}/{d}/{slug}.pdf"),
    ]


def _ca9_resolve_docket(citation: str, name_guess: str):
    """citation → (docket, yyyy, mm, dd) via CourtListener search. 9th Cir. only."""
    rep = parse_reporter(citation)
    q = f'"{rep["pin"]}"' if rep else f'"{name_guess}"'
    url = CL_SEARCH + "?" + urllib.parse.urlencode({"type": "o", "q": q})
    status, ctype, body = http_get(url)
    if status != 200:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    for r in data.get("results") or []:
        court = str(r.get("court") or "").lower()
        if not any(tag in court for tag in _CA9_COURT_TAGS):
            continue
        raw = (r.get("docketNumber") or "").strip()
        docket = ca9_strip_docket(raw)
        filed = (r.get("dateFiled") or "")[:10]
        if docket and re.match(r"^\d{4}-\d{2}-\d{2}$", filed):
            y, m, d = filed.split("-")
            return docket, y, m, d
    return None


def probe_ca9(citation: str) -> SourceHit:
    """Fetch the 9th Circuit CDN PDF after resolving a docket on CourtListener."""
    rep = parse_reporter(citation)
    if not rep or rep["slug"] not in {"f2d", "f3d", "f4th"}:
        return SourceHit(
            source="ca9_cdn",
            found=False,
            url=CA9_OPINIONS,
            notes="skipped: needs a federal appellate reporter pin (name-only resolution is too noisy)",
        )
    name = guess_name(citation)
    resolved = _ca9_resolve_docket(citation, name)
    if not resolved:
        return SourceHit(
            source="ca9_cdn",
            found=False,
            url=CA9_OPINIONS,
            notes="could not resolve a 9th Circuit docket number via CourtListener search",
        )
    docket, y, m, d = resolved
    last_status = None
    last_url = CA9_OPINIONS
    tried = []
    for kind, pdf_url in ca9_pdf_candidates(docket, y, m, d):
        tried.append(kind)
        last_url = pdf_url
        status, ctype, body = http_get(pdf_url, accept="application/pdf")
        last_status = status if isinstance(status, int) else None
        if status == 200 and ((ctype or "").startswith("application/pdf") or body[:4] == b"%PDF"):
            return SourceHit(
                source="ca9_cdn",
                found=True,
                url=pdf_url,
                case_name=name,
                http_status=200,
                notes=f"docket {docket} resolved; {kind} PDF fetched from the 9th Circuit datastore",
            )
    return SourceHit(
        source="ca9_cdn",
        found=False,
        url=last_url,
        http_status=last_status,
        notes=(
            f"docket {docket} resolved but CDN PDF 404 after {', '.join(tried)} "
            f"(pre-~2010 published opinions often missing)"
        ),
    )


def consensus_for(result: LookupResult) -> str:
    pin = next((s for s in result.sources if s.source == "courtlistener_citation"), None)
    cl = next((s for s in result.sources if s.source == "courtlistener"), None)
    cap = next((s for s in result.sources if s.source == "case.law_static"), None)
    bulk = next((s for s in result.sources if s.source == "cl_bulk_offline"), None)

    def _skipped(s: SourceHit | None) -> bool:
        return s is None or "skipped" in (s.notes or "").lower()

    if pin and pin.found and pin.case_name and names_compatible(result.case_name_guess, pin.case_name):
        result.matched_name = pin.case_name
        result.matched_citations = pin.citations
        result.consensus = "FOUND"
        return result.consensus

    found_sources = [s for s in (pin, cl, cap, bulk) if s and s.found]
    if not found_sources:
        # NOT_FOUND only when live pin sources actually ran and missed.
        # A skipped probe (no token, volume metadata unavailable) is UNRESOLVED.
        # Bulk skip never blocks an explicit citation-lookup 404 — most
        # environments will not have the quarterly SQLite index.
        pin_404 = bool(pin and not pin.found and "404" in (pin.notes or ""))
        live_pin_sources = [s for s in (pin, cl, cap) if s is not None]
        any_skipped = any(_skipped(s) for s in live_pin_sources)
        if pin_404 and not any_skipped and (result.reporter_pin or result.wl_pin):
            result.consensus = "NOT_FOUND"
            return result.consensus
        result.consensus = "UNRESOLVED"
        return result.consensus

    if all(s.name_only for s in found_sources):
        primary = found_sources[0]
        result.matched_name = primary.case_name
        result.matched_citations = primary.citations
        result.consensus = "PARTIAL"
        return result.consensus

    # Prefer CAP/CL name that matches the query; otherwise surface mismatch.
    primary = found_sources[0]
    for s in found_sources:
        if s.case_name and names_compatible(result.case_name_guess, s.case_name):
            primary = s
            break
    result.matched_name = primary.case_name
    result.matched_citations = primary.citations

    name_ok = bool(primary.case_name) and names_compatible(
        result.case_name_guess, primary.case_name
    )
    if not name_ok and primary.case_name:
        # Reporter/WL pin resolves, but to a different caption — classic miscitation.
        result.consensus = "CAPTION_MISMATCH"
        return result.consensus

    if len(found_sources) >= 2:
        result.consensus = "FOUND"
        return result.consensus

    # Single-source hit (common for WL-only, where CAP has no pin).
    result.consensus = "PARTIAL"
    return result.consensus


def lookup_one(
    citation: str,
    *,
    include_blocked_probes: bool = False,
    include_extra_probes: bool = False,
    citation_lookup: str = "auto",
) -> LookupResult:
    name = guess_name(citation)
    rep = parse_reporter(citation)
    wl_m = WL_RE.search(citation)
    result = LookupResult(
        query=citation,
        case_name_guess=name,
        reporter_pin=rep["pin"] if rep else None,
        wl_pin=wl_m.group(1) if wl_m else None,
    )
    use_lookup = citation_lookup == "always" or (
        citation_lookup == "auto" and bool(courtlistener_token())
    )
    # Step 0: offline exact-triple existence check. A miss is not NOT_FOUND.
    result.sources.append(probe_bulk_offline(citation))
    cite_hit = None
    if use_lookup:
        cite_hit = lookup_courtlistener_citation(citation, name)
        result.sources.append(cite_hit)
    else:
        result.sources.append(
            SourceHit(
                source="courtlistener_citation",
                found=False,
                url=CL_CITATION_LOOKUP,
                notes="skipped (citation-lookup disabled or no COURTLISTENER_TOKEN)",
            )
        )
    result.sources.append(lookup_cap(citation, name))
    pin_resolved = bool(
        cite_hit
        and cite_hit.found
        and cite_hit.case_name
        and names_compatible(name, cite_hit.case_name)
    )
    if not pin_resolved:
        result.sources.append(lookup_courtlistener(citation, name))
    if include_blocked_probes:
        result.sources.append(probe_justia(citation))
        result.sources.append(probe_scholar(citation))
    if include_extra_probes:
        result.sources.append(probe_govinfo(citation))
        result.sources.append(probe_ca9(citation))
    consensus_for(result)
    return result


CONTROLS = [
    "Richardson v. McKnight, 521 U.S. 399 (1997)",
    "In re Leman, 66 Cal.App.5th 200",
]

HIGH_RISK = [
    "In re Hudson, 1 Cal.App. 4th 1 (2006)",
    "In re Hudson, 143 Cal.App.4th 1 (2006)",
    "Burrell v. Jackson, 2003 WL 23545858",
    "Swift v. Christian, 384 F. 3d 1184",
    "Swift v. California, 384 F.3d 1184",
    "Soranno's Gasco, Inc. v. Morgan Hill Unified, 874 F. 2d 1310",
    "Soranno's Gasco, Inc. v. Morgan, 874 F.2d 1310",
    "Lockley v. Law Office, 91 Cal.App. 4th 401 (2001)",
    "Lockley v. Law Office of Cantrell, 91 Cal.App.4th 875 (2001)",
    "California, Ltd. v. Dry Creek Joint Elementary Sch. Dist, 50 Cal.App. 4th 1",
    "Western/California, Ltd. v. Dry Creek, 50 Cal.App.4th 1461",
    "Home v. Dep't of Health Care Services, 204 Cal.App. 4th 676 (2012)",
    "California Ass'n for Health Services at Home v. State Department of Health Care Services, 204 Cal.App.4th 676 (2012)",
    "Unicorn Glob., Inc. v. Hillo Am., Inc, 2021 WL 1034838",
    "Los Angeles Cath. Worker v. Los Angeles Downtown Indus. Dist. Bus, 2015 WL 13650018",
    "California Highway Patrol v. Superior Court, 158 Cal.App. 4th 726 (2008)",
    "People v. Rizo, 22 Cal. 4th 681 (2000)",
    "Stump v. Sparkman, 435 U.S. 349 (1978)",
]


def cites_from_matter(matter: int) -> list[str]:
    index_path = DOCS / "citation_index.json"
    index = json.loads(index_path.read_text())
    out = []
    for c in index.get("citations") or []:
        if c.get("kind") != "authority":
            continue
        matters = {int(m) for m in (c.get("matters") or []) if str(m).isdigit()}
        if matter in matters:
            out.append(c["citation"])
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cite", action="append", default=[], help="Citation string (repeatable)")
    ap.add_argument(
        "--batch",
        choices=["controls", "high-risk", "all"],
        help="Built-in confirmation batches",
    )
    ap.add_argument(
        "--matter",
        type=int,
        action="append",
        default=[],
        help="Load authority citations for matter N from citation_index.json (repeatable)",
    )
    ap.add_argument(
        "--cites-file",
        type=Path,
        help="JSON file: array of citation strings, or {cites:[...]}",
    )
    ap.add_argument(
        "--probe-blocked",
        action="store_true",
        help="Also probe Justia + Google Scholar (usually 403)",
    )
    ap.add_argument(
        "--probe-extra",
        action="store_true",
        help="Also probe govinfo (POST + name-match) and CA9 CDN (opinions then memoranda). Evidence only; does not vote in consensus",
    )
    ap.add_argument(
        "--citation-lookup",
        choices=["auto", "always", "never"],
        default="auto",
        help="CourtListener citation-lookup pin API (needs COURTLISTENER_TOKEN)",
    )
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    cites: list[str] = list(args.cite)
    if args.batch in ("controls", "all"):
        cites.extend(CONTROLS)
    if args.batch in ("high-risk", "all"):
        cites.extend(HIGH_RISK)
    for m in args.matter:
        cites.extend(cites_from_matter(m))
    if args.cites_file:
        payload = json.loads(args.cites_file.read_text())
        if isinstance(payload, list):
            cites.extend(payload)
        else:
            cites.extend(payload.get("cites") or payload.get("citations") or [])
    if not cites:
        cites = CONTROLS + HIGH_RISK

    out_path = args.out
    if out_path is None:
        if len(args.matter) == 1 and not args.batch and not args.cite and not args.cites_file:
            out_path = DOCS / f"citation_lookup_matter{args.matter[0]:02d}.json"
        else:
            out_path = OUT_PATH

    # de-dupe preserving order
    seen = set()
    ordered = []
    for c in cites:
        if c not in seen:
            seen.add(c)
            ordered.append(c)

    results = []
    for i, c in enumerate(ordered):
        if not args.quiet:
            print(f"[{i+1}/{len(ordered)}] {c}", file=sys.stderr)
        results.append(
            lookup_one(
                c,
                include_blocked_probes=args.probe_blocked,
                include_extra_probes=args.probe_extra,
                citation_lookup=args.citation_lookup,
            )
        )

    # reachability summary (one-shot probes on controls if requested)
    reachability = {
        "courtlistener_search": "ok (unauthenticated /api/rest/v4/search/)",
        "case_law_api": "html docs only — JSON API not usable without auth/migration",
        "case_law_static": "ok (CasesMetadata.json + html/{file_name}.html)",
        "justia": "blocked (Cloudflare 403) in this environment",
        "google_scholar": "unreliable (often 403)",
        "courtlistener_citation_lookup": (
            "configured (COURTLISTENER_TOKEN)"
            if courtlistener_token()
            else "unset — citation-lookup skipped (set COURTLISTENER_TOKEN)"
        ),
        "govinfo": "opt-in --probe-extra (POST JSON + name-match; GOVINFO_API_KEY or DEMO_KEY)",
        "ca9_cdn": "opt-in --probe-extra (CL docket → strip No. → opinions then memoranda)",
        "cl_bulk_offline": (
            f"wired ({BULK_SNAPSHOT} SQLite)"
            if bulk_db_path()
            else "skipped — run internal/scripts/build-bulk-citation-index.py"
        ),
    }

    out = {
        "generatedBy": "internal/scripts/lookup-citations.py",
        "generatedDate": date.today().isoformat(),
        "matters": args.matter or None,
        "reachability": reachability,
        "resultCount": len(results),
        "results": [
            {
                **{k: getattr(r, k) for k in (
                    "query",
                    "case_name_guess",
                    "reporter_pin",
                    "wl_pin",
                    "consensus",
                    "matched_name",
                    "matched_citations",
                )},
                "sources": [asdict(s) for s in r.sources],
            }
            for r in results
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    if not args.quiet:
        print(json.dumps({
            "wrote": str(out_path),
            "counts": {
                c: sum(1 for r in results if r.consensus == c)
                for c in ("FOUND", "CAPTION_MISMATCH", "NOT_FOUND", "UNRESOLVED", "PARTIAL", "UNKNOWN")
            },
        }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
