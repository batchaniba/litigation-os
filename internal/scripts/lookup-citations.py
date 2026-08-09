#!/usr/bin/env python3
"""Multi-source citation existence lookup (CourtListener + CAP static.case.law).

Probes reporter pins against:
  1. CourtListener REST search API (unauthenticated /api/rest/v4/search/)
  2. Caselaw Access Project bulk metadata at static.case.law (CasesMetadata.json)

Also records reachability for Justia and Google Scholar (usually blocked).

This does NOT mark portfolio statuses by itself — it produces evidence for
manual / round-overlay confirmation. Characterization still needs opinion text.

Usage:
  python3 internal/scripts/lookup-citations.py
  python3 internal/scripts/lookup-citations.py --cite "521 U.S. 399"
  python3 internal/scripts/lookup-citations.py --batch controls
  python3 internal/scripts/lookup-citations.py --batch high-risk
  python3 internal/scripts/lookup-citations.py --matter 28
  python3 internal/scripts/lookup-citations.py --cites-file /tmp/cites.json
"""

from __future__ import annotations

import argparse
import json
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
CAP_STATIC = "https://static.case.law"

# reporter slug on static.case.law → regex capturing (volume, page)
REPORTER_MAP = [
    (r"(\d+)\s+U\.?\s*S\.?\s+(\d+)", "us", "U.S."),
    (r"(\d+)\s+F\.\s*R\.\s*D\.\s+(\d+)", "frd", "F.R.D."),
    (r"(\d+)\s+F\.\s*2d\s+(\d+)", "f2d", "F.2d"),
    (r"(\d+)\s+F\.\s*3d\s+(\d+)", "f3d", "F.3d"),
    (r"(\d+)\s+F\.\s*4th\s+(\d+)", "f4th", "F.4th"),
    (r"(\d+)\s+F\.\s*Supp\.\s*2d\s+(\d+)", "f-supp-2d", "F. Supp. 2d"),
    (r"(\d+)\s+F\.\s*Supp\.\s*3d\s+(\d+)", "f-supp-3d", "F. Supp. 3d"),
    (r"(\d+)\s+M\.?\s*J\.?\s+(\d+)", "mj", "M.J."),
    (r"(\d+)\s+Cal\.\s*App\.\s*5th\s+(\d+)", "cal-app-5th", "Cal. App. 5th"),
    (r"(\d+)\s+Cal\.\s*App\.\s*4th\s+(\d+)", "cal-app-4th", "Cal. App. 4th"),
    (r"(\d+)\s+Cal\.\s*App\.\s*3d\s+(\d+)", "cal-app-3d", "Cal. App. 3d"),
    (r"(\d+)\s+Cal\.\s*5th\s+(\d+)", "cal-5th", "Cal. 5th"),
    (r"(\d+)\s+Cal\.\s*4th\s+(\d+)", "cal-4th", "Cal. 4th"),
    (r"(\d+)\s+Cal\.\s*3d\s+(\d+)", "cal-3d", "Cal. 3d"),
    (r"(\d+)\s+S\.\s*Ct\.\s+(\d+)", "s-ct", "S. Ct."),
    (r"(\d+)\s+L\.\s*Ed\.\s*2d\s+(\d+)", "l-ed-2d", "L. Ed. 2d"),
]

WL_RE = re.compile(r"(?:WL|Westlaw)\s*(\d{7,})", re.I)
NAME_RE = re.compile(
    r"^(?:See\s+)?(.+?),\s+\d+\s+(?:U\.S\.|F\.|Cal\.)",
    re.I,
)


@dataclass
class SourceHit:
    source: str
    found: bool
    url: str = ""
    case_name: str = ""
    citations: list[str] = field(default_factory=list)
    notes: str = ""
    http_status: int | None = None


@dataclass
class LookupResult:
    query: str
    case_name_guess: str
    reporter_pin: str | None
    wl_pin: str | None
    sources: list[SourceHit] = field(default_factory=list)
    consensus: str = "UNKNOWN"  # FOUND / NOT_FOUND / PARTIAL / BLOCKED / UNKNOWN
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
            accept = False
            if rep and cite_match:
                accept = True
            elif wl and not rep and wl_match:
                accept = True
            elif not rep and not wl and name_match:
                accept = True

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
                    ),
                    http_status=200,
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


def consensus_for(result: LookupResult) -> str:
    cl = next((s for s in result.sources if s.source == "courtlistener"), None)
    cap = next((s for s in result.sources if s.source == "case.law_static"), None)
    found_sources = [s for s in (cl, cap) if s and s.found]
    if not found_sources:
        if result.wl_pin and not result.reporter_pin:
            result.consensus = "NOT_FOUND"
            return result.consensus
        if result.reporter_pin:
            result.consensus = "NOT_FOUND"
            return result.consensus
        result.consensus = "UNKNOWN"
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


def lookup_one(citation: str, *, include_blocked_probes: bool = False) -> LookupResult:
    name = guess_name(citation)
    rep = parse_reporter(citation)
    wl_m = WL_RE.search(citation)
    result = LookupResult(
        query=citation,
        case_name_guess=name,
        reporter_pin=rep["pin"] if rep else None,
        wl_pin=wl_m.group(1) if wl_m else None,
    )
    result.sources.append(lookup_courtlistener(citation, name))
    result.sources.append(lookup_cap(citation, name))
    if include_blocked_probes:
        result.sources.append(probe_justia(citation))
        result.sources.append(probe_scholar(citation))
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
        results.append(lookup_one(c, include_blocked_probes=args.probe_blocked))

    # reachability summary (one-shot probes on controls if requested)
    reachability = {
        "courtlistener_search": "ok (unauthenticated /api/rest/v4/search/)",
        "case_law_api": "html docs only — JSON API not usable without auth/migration",
        "case_law_static": "ok (CasesMetadata.json + html/{file_name}.html)",
        "justia": "blocked (Cloudflare 403) in this environment",
        "google_scholar": "unreliable (often 403)",
        "courtlistener_citation_lookup": "requires API token (401)",
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
                for c in ("FOUND", "CAPTION_MISMATCH", "NOT_FOUND", "PARTIAL", "UNKNOWN")
            },
        }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
