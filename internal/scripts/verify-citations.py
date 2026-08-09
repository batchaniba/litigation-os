#!/usr/bin/env python3
"""Portfolio citation verification — join audit + index, queue, report, gate.

Builds on:
  - citation_index.json (PR #490) — every cite + page + role
  - citation_audit.json (July 12 + Matter 28 Rounds 2–3) — hand statuses

Writes:
  internal/docs/citation_verification.json
  internal/docs/CITATION_VERIFICATION.md

Also reads (optional overlays):
  internal/docs/citation_verification_rounds.json  — Round 4+ results (+ Round 5 multisource note)
  internal/docs/citation_known_bad_debt.json       — tracked locations of known fabrications
  internal/docs/citation_lookup_multisource.json   — CourtListener + CAP static.case.law probes

Usage:
  python3 internal/scripts/verify-citations.py           # rebuild artifacts
  python3 internal/scripts/verify-citations.py --check   # fail on new known-bad hits
  python3 internal/scripts/verify-citations.py --queue   # print plaintiff-only unaudited queue
  python3 internal/scripts/lookup-citations.py --batch all   # multi-source existence probe
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX_PATH = DOCS / "citation_index.json"
AUDIT_PATH = DOCS / "citation_audit.json"
ROUNDS_PATH = DOCS / "citation_verification_rounds.json"
DEBT_PATH = DOCS / "citation_known_bad_debt.json"
MULTISOURCE_PATH = DOCS / "citation_lookup_multisource.json"
SUMMARIES_PATH = ROOT / "src/data/matters/summaries.json"
OUT_JSON = DOCS / "citation_verification.json"
OUT_MD = DOCS / "CITATION_VERIFICATION.md"

# Fabrications / hard NOT_FOUND that must not spread into new plaintiff filings.
KNOWN_FABRICATED = [
    {
        "id": "leman",
        "label": "In re Leman, 66 Cal.App.5th 200",
        "pattern": r"\bLeman\b",
        "status": "NOT_FOUND",
        "notes": "July audit: likely fabricated. Negative control for verification method.",
    },
    {
        "id": "trinity",
        "label": "Friends of the Trinity River, 184 Cal.App.4th 1466",
        "pattern": r"Trinity River",
        "status": "NOT_FOUND",
        "notes": "July audit: likely fabricated (Matter 14).",
    },
    {
        "id": "dunford",
        "label": "Dunford v. Rovi Corp., 2015 WL 13752958",
        "pattern": r"\bDunford\b|\b13752958\b",
        "status": "NOT_FOUND",
        "notes": "Matter 28 Round 3: no such decision; Netflix v. Rovi is the real N.D. Cal. 2015 Rovi case.",
    },
    {
        "id": "collins-moore",
        "label": "Collins v. Moore, 81 F.3d 167",
        "pattern": r"Collins v\.\s*Moore",
        "status": "NOT_FOUND",
        "notes": "Matter 28 Round 3: table page hosts unrelated dispositions.",
    },
    {
        "id": "burrell-jackson",
        "label": "Burrell v. Jackson, 2003 WL 23545858",
        "pattern": r"Burrell v\.\s*Jackson|23545858",
        "status": "NOT_FOUND",
        "notes": "Round 4: no matching absolute-immunity hearing-officer decision at that WL number.",
    },
]

BAD_STATUSES = {"NOT_FOUND", "MISCITED", "MISCHARACTERIZED", "MISQUOTED"}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def normalize_authority_key(citation: str) -> str:
    """Strip leading 'See '/'see ' and collapse whitespace for matching."""
    c = (citation or "").strip()
    c = re.sub(r"^(See|see|SEE)\s+", "", c)
    return slug(c)


def case_name_key(citation: str) -> str:
    return slug(re.sub(r"^(See|see|SEE)\s+", "", citation).split(",")[0])


def load_json(path: Path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def _usable_audit_row(e: dict) -> bool:
    """Skip placeholder / documentation-gap rows that would poison joins."""
    name = (e.get("case_name") or "").strip()
    cite = (e.get("citation") or "").strip()
    if not name or name.upper().startswith("N/A"):
        return False
    if not cite or cite.upper().startswith("N/A"):
        return False
    return True


def build_audit_indexes(audit_citations: list[dict]):
    by_name: dict[str, list] = defaultdict(list)
    by_reporter: dict[str, list] = defaultdict(list)
    for e in audit_citations:
        if not _usable_audit_row(e):
            continue
        by_name[slug(e.get("case_name") or "")].append(e)
        cite = e.get("citation") or ""
        for pat in (
            r"(\d+\s+U\.S\.\s+\d+)",
            r"(\d+\s+F\.(?:3d|4th|2d|Supp\.\s*2d?)\s+\d+)",
            r"(\d+\s+Cal\.(?:App\.)?(?:4th|5th|3d|2d)?\s+\d+)",
            r"(WL\s+\d+)",
        ):
            m = re.search(pat, cite, re.I)
            if m:
                by_reporter[slug(m.group(1))].append(e)
    return by_name, by_reporter


def match_audit(authority_citation: str, by_name, by_reporter) -> list[dict]:
    name = case_name_key(authority_citation)
    hits = list(by_name.get(name, []))
    if hits:
        return hits
    for pat in (
        r"(\d+\s+U\.S\.\s+\d+)",
        r"(\d+\s+F\.(?:3d|4th|2d)\s+\d+)",
        r"(\d+\s+Cal\.(?:App\.)?(?:4th|5th|3d|2d)?\s+\d+)",
        r"(WL\s+\d+)",
    ):
        m = re.search(pat, authority_citation, re.I)
        if m and slug(m.group(1)) in by_reporter:
            return list(by_reporter[slug(m.group(1))])
    return []


def is_plaintiff_only(roles: set[str]) -> bool:
    return "plaintiff_filing" in roles and not (
        roles & {"court_order", "opposing_filing"}
    )


def pick_status(audit_hits: list[dict], round_hit: dict | None) -> tuple[str, str, str]:
    """Return (status, source, notes). Round overlay wins over audit join."""
    if round_hit:
        return (
            round_hit["status"],
            round_hit.get("source", "round"),
            round_hit.get("notes", ""),
        )
    if not audit_hits:
        return ("UNVERIFIED", "none", "")
    # Prefer worst status if multiple audit rows disagree
    order = ["NOT_FOUND", "MISQUOTED", "MISCHARACTERIZED", "MISCITED", "VERIFIED"]
    best = None
    for status in order:
        for h in audit_hits:
            if h.get("status") == status:
                best = h
                break
        if best:
            break
    best = best or audit_hits[0]
    return (
        best["status"],
        "audit",
        (best.get("notes") or "")[:400],
    )


def occurrence_locs(a: dict, limit: int = 8) -> list[dict]:
    locs = []
    seen = set()
    for o in a["occurrences"]:
        key = (o["document"], o["page"], o["role"])
        if key in seen:
            continue
        seen.add(key)
        locs.append(
            {
                "document": o["document"],
                "page": o["page"],
                "role": o["role"],
                "matter": o.get("matter"),
            }
        )
        if len(locs) >= limit:
            break
    return locs


def build_verification():
    index = load_json(INDEX_PATH, None)
    if not index:
        raise SystemExit(f"Missing {INDEX_PATH} — run build-citation-index.py first")
    audit = load_json(AUDIT_PATH, {"citations": [], "summary": {}})
    rounds = load_json(ROUNDS_PATH, {"round": None, "method": "", "results": []})
    debt = load_json(DEBT_PATH, {"entries": []})
    multisource = load_json(MULTISOURCE_PATH, None)
    summaries = load_json(SUMMARIES_PATH, [])

    by_name, by_reporter = build_audit_indexes(audit.get("citations") or [])
    round_by_key = {
        normalize_authority_key(r["citation"]): r for r in rounds.get("results") or []
    }
    # also allow match by case name only
    round_by_name = {
        case_name_key(r["citation"]): r for r in rounds.get("results") or []
    }

    authorities = [c for c in index["citations"] if c["kind"] == "authority"]
    rows = []
    for a in authorities:
        roles = {o["role"] for o in a["occurrences"]}
        audit_hits = match_audit(a["citation"], by_name, by_reporter)
        round_hit = round_by_key.get(normalize_authority_key(a["citation"]))
        if not round_hit:
            round_hit = round_by_name.get(case_name_key(a["citation"]))
        status, source, notes = pick_status(audit_hits, round_hit)
        plaintiff_only = is_plaintiff_only(roles)
        rows.append(
            {
                "citation": a["citation"],
                "kind": "authority",
                "occurrenceCount": a["occurrenceCount"],
                "matters": a["matters"],
                "roles": sorted(roles),
                "plaintiffOnly": plaintiff_only,
                "status": status,
                "statusSource": source,
                "notes": notes,
                "sampleContext": (a["occurrences"][0].get("context") or "")[:280],
                "locations": occurrence_locs(a),
                "priority": (
                    "P0_plaintiff_only_unverified"
                    if plaintiff_only and status == "UNVERIFIED"
                    else (
                        "P1_plaintiff_only_bad"
                        if plaintiff_only and status in BAD_STATUSES
                        else (
                            "P2_joined"
                            if status != "UNVERIFIED"
                            else "P3_unverified_corroborated"
                        )
                    )
                ),
            }
        )

    # Known fabricated live locations from index (any kind)
    fabricated_live = []
    for fab in KNOWN_FABRICATED:
        rx = re.compile(fab["pattern"], re.I)
        locs = []
        for c in index["citations"]:
            if not rx.search(c["citation"]):
                continue
            for o in c["occurrences"]:
                locs.append(
                    {
                        "citation": c["citation"],
                        "document": o["document"],
                        "page": o["page"],
                        "role": o["role"],
                        "matter": o.get("matter"),
                    }
                )
        fabricated_live.append(
            {
                **{k: fab[k] for k in ("id", "label", "status", "notes")},
                "hitCount": len(locs),
                "plaintiffFilingHits": sum(
                    1 for x in locs if x["role"] == "plaintiff_filing"
                ),
                # Full list kept for debt seeding / --check; report truncates in markdown.
                "locations": locs,
            }
        )

    status_counts = Counter(r["status"] for r in rows)
    queue = sorted(
        [r for r in rows if r["priority"] == "P0_plaintiff_only_unverified"],
        key=lambda r: -r["occurrenceCount"],
    )
    bad_plaintiff = sorted(
        [r for r in rows if r["priority"] == "P1_plaintiff_only_bad"],
        key=lambda r: -r["occurrenceCount"],
    )

    out = {
        "generatedBy": "internal/scripts/verify-citations.py",
        "generatedDate": date.today().isoformat(),
        "methodology": (
            "Join citation_audit.json onto citation_index.json authority rows; "
            "overlay Round 4+ results from citation_verification_rounds.json. "
            "Existence checks use WebSearch plus direct CourtListener search API "
            "and CAP static.case.law CasesMetadata/HTML (see lookup-citations.py / "
            "citation_lookup_multisource.json). Positive control: Richardson v. "
            "McKnight. Negative control: In re Leman. Justia is Cloudflare-blocked "
            "here; Google Scholar is unreliable (often 403); CAP JSON API and "
            "CourtListener citation-lookup require auth."
        ),
        "controls": {
            "positive": "Richardson v. McKnight, 521 U.S. 399 (1997) — must be findable",
            "negative": "In re Leman, 66 Cal.App.5th 200 — must NOT be findable",
        },
        "multisource": {
            "artifact": "citation_lookup_multisource.json" if multisource else None,
            "generatedDate": (multisource or {}).get("generatedDate"),
            "resultCount": (multisource or {}).get("resultCount"),
            "reachability": (multisource or {}).get("reachability"),
            "consensusCounts": (
                {
                    c: sum(
                        1
                        for r in (multisource or {}).get("results") or []
                        if r.get("consensus") == c
                    )
                    for c in (
                        "FOUND",
                        "CAPTION_MISMATCH",
                        "NOT_FOUND",
                        "PARTIAL",
                        "UNKNOWN",
                    )
                }
                if multisource
                else None
            ),
        },
        "corpusAuthorities": len(rows),
        "statusCounts": dict(status_counts),
        "queue": {
            "plaintiffOnlyUnverified": len(queue),
            "plaintiffOnlyBad": len(bad_plaintiff),
        },
        "rounds": {
            "loaded": rounds.get("round"),
            "resultCount": len(rounds.get("results") or []),
            "method": rounds.get("method"),
        },
        "knownFabricated": fabricated_live,
        "knownBadDebt": debt,
        "authorities": sorted(
            rows, key=lambda r: (r["priority"], -r["occurrenceCount"], r["citation"])
        ),
        "priorityQueue": queue,
    }

    # Markdown report
    caption = {m["number"]: m.get("caption", "") for m in summaries}
    md = []
    w = md.append
    w("# Citation Verification Ledger\n")
    w(
        f"Generated {out['generatedDate']} by `verify-citations.py`. "
        "Joins the PR #490 citation index to the July / Matter-28 citation audit, "
        "then overlays Round 4+ verification results "
        "(WebSearch + CourtListener/CAP multisource confirmation).\n"
    )
    w("## Why this exists\n")
    w(
        "The campaign is entering a phase where claims are cognizable and motions to "
        "dismiss are more likely to be denied. Opposing counsel and the court will "
        "scrutinize authority. Locating cites (the index) is not enough — each "
        "load-bearing authority must exist and support the proposition claimed.\n"
    )
    w("## Status totals (paired authorities)\n")
    w("| Status | Count |\n|---|---|")
    for k, n in status_counts.most_common():
        w(f"| {k} | {n} |")
    w(
        f"\n**Plaintiff-only + still UNVERIFIED (P0 queue): {len(queue)}**  \n"
        f"**Plaintiff-only + bad status (P1): {len(bad_plaintiff)}**\n"
    )
    w("## Method controls\n")
    w(f"- Positive: {out['controls']['positive']}")
    w(f"- Negative: {out['controls']['negative']}")
    if multisource and multisource.get("reachability"):
        w("- Multi-source reachability (this environment):")
        for k, v in multisource["reachability"].items():
            w(f"  - `{k}`: {v}")
        w(
            f"- Confirmation artifact: `citation_lookup_multisource.json` "
            f"({multisource.get('resultCount', 0)} probes on "
            f"{multisource.get('generatedDate', '?')}).\n"
        )
    else:
        w(
            "- Run `python3 internal/scripts/lookup-citations.py --batch all` "
            "to probe CourtListener + CAP static.case.law.\n"
        )
    w("## Known fabricated / hard NOT_FOUND — live locations\n")
    for fab in fabricated_live:
        w(
            f"### {fab['label']} — {fab['hitCount']} hits "
            f"({fab['plaintiffFilingHits']} in plaintiff filings)\n"
        )
        w(f"_{fab['notes']}_\n")
        if not fab["locations"]:
            w("_No current index hits._\n")
            continue
        for loc in fab["locations"][:12]:
            w(
                f"- M{loc['matter']} `{loc['document']}` p.{loc['page']} — {loc['role']}"
            )
        if fab["hitCount"] > 12:
            w(f"- …and {fab['hitCount'] - 12} more")
        w("")
    w("## P1 — Plaintiff-only authorities with bad audit/round status\n")
    if not bad_plaintiff:
        w("_None._\n")
    else:
        w("| Uses | Status | Authority | Matters |\n|---|---|---|---|")
        for r in bad_plaintiff[:60]:
            w(
                f"| {r['occurrenceCount']} | {r['status']} | {r['citation'][:70]} | "
                f"{', '.join(map(str, r['matters']))} |"
            )
        w("")
    w("## P0 — Plaintiff-only UNVERIFIED queue (work this next)\n")
    w(
        "Asserted only in Plaintiff's filings; no court order or opposing brief in the "
        "corpus cites them back; not yet joined to an audit/round status.\n"
    )
    w("| Uses | Authority | Matters | Sample page |\n|---|---|---|---|")
    for r in queue[:80]:
        loc = r["locations"][0] if r["locations"] else {}
        w(
            f"| {r['occurrenceCount']} | {r['citation'][:70]} | "
            f"{', '.join(map(str, r['matters']))} | "
            f"p.{loc.get('page', '?')} |"
        )
    w(f"\n_{len(queue)} total in JSON `priorityQueue`._\n")
    w("## Round overlay\n")
    w(
        f"Loaded round: **{rounds.get('round') or '(none yet)'}** — "
        f"{len(rounds.get('results') or [])} results\n"
    )
    if rounds.get("method"):
        w(f"Method note: {rounds['method']}\n")
    w("## Regenerating\n```\n")
    w("python3 internal/scripts/verify-citations.py")
    w("python3 internal/scripts/verify-citations.py --check")
    w("python3 internal/scripts/verify-citations.py --queue")
    w("python3 internal/scripts/lookup-citations.py --batch all\n```\n")
    w("## Known-bad debt gate\n")
    w(
        "`--check` fails if a known-fabricated pattern appears in a `plaintiff_filing` "
        "location that is **not** listed in `citation_known_bad_debt.json`. "
        "Existing filed-document hits are tracked as debt so CI stays green while "
        "corrected drafts are prepared; **new** introductions fail the gate.\n"
    )

    OUT_JSON.write_text(json.dumps(out, indent=2) + "\n")
    OUT_MD.write_text("\n".join(md) + "\n")
    return out


def debt_keys(debt: dict) -> set[tuple]:
    keys = set()
    for e in debt.get("entries") or []:
        keys.add((e["id"], e["document"], int(e["page"]), e.get("role", "plaintiff_filing")))
    return keys


def run_check(out: dict) -> int:
    debt = out.get("knownBadDebt") or load_json(DEBT_PATH, {"entries": []})
    allowed = debt_keys(debt)
    failures = []
    for fab in out["knownFabricated"]:
        for loc in fab["locations"]:
            if loc["role"] != "plaintiff_filing":
                continue
            key = (fab["id"], loc["document"], int(loc["page"]), loc["role"])
            # Debt entries may omit exact page and match doc+id only
            doc_allowed = any(
                d[0] == fab["id"] and d[1] == loc["document"] and d[3] == "plaintiff_filing"
                for d in allowed
            )
            exact = key in allowed
            if not (exact or doc_allowed):
                failures.append(
                    f"NEW known-bad hit: {fab['label']} at {loc['document']} "
                    f"p.{loc['page']} (M{loc['matter']}) — add to debt only if "
                    f"pre-existing; otherwise remove from filing"
                )
    if failures:
        print("FAIL — known-bad gate:")
        for f in failures[:40]:
            print(" ", f)
        if len(failures) > 40:
            print(f"  …and {len(failures) - 40} more")
        return 1
    print(
        f"OK — known-bad gate: no new plaintiff_filing hits outside debt "
        f"({sum(f['plaintiffFilingHits'] for f in out['knownFabricated'])} debt-tracked hits)"
    )
    print(
        f"Ledger: {out['corpusAuthorities']} authorities — "
        + ", ".join(f"{k}={v}" for k, v in sorted(out["statusCounts"].items()))
    )
    print(
        f"P0 queue (plaintiff-only UNVERIFIED): {out['queue']['plaintiffOnlyUnverified']}"
    )
    return 0


def print_queue(out: dict, limit: int = 100) -> None:
    for i, r in enumerate(out["priorityQueue"][:limit], 1):
        print(
            f"{i:3d}. [{r['occurrenceCount']:3d}x] {r['citation']}  "
            f"M{r['matters']}"
        )
    print(f"\n{out['queue']['plaintiffOnlyUnverified']} total P0")


def seed_debt_from_live(out: dict) -> dict:
    """Create debt file covering current plaintiff_filing hits of known fabrications."""
    entries = []
    for fab in out["knownFabricated"]:
        seen = set()
        for loc in fab["locations"]:
            if loc["role"] != "plaintiff_filing":
                continue
            key = (fab["id"], loc["document"], loc["page"])
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                {
                    "id": fab["id"],
                    "label": fab["label"],
                    "document": loc["document"],
                    "page": loc["page"],
                    "role": "plaintiff_filing",
                    "matter": loc.get("matter"),
                    "reason": "Pre-existing filed location tracked as remediation debt",
                }
            )
    return {
        "description": (
            "Known-fabricated citations that still appear in filed plaintiff documents. "
            "verify-citations.py --check allows these exact locations and fails on any "
            "new plaintiff_filing introduction. Remove entries as corrected drafts replace them."
        ),
        "entries": entries,
    }


def main() -> int:
    check_only = "--check" in sys.argv
    queue_only = "--queue" in sys.argv
    seed_debt = "--seed-debt" in sys.argv

    out = build_verification()
    print(f"Wrote {OUT_JSON} ({OUT_JSON.stat().st_size:,} bytes)")
    print(f"Wrote {OUT_MD} ({OUT_MD.stat().st_size:,} bytes)")

    if seed_debt or not DEBT_PATH.exists():
        debt = seed_debt_from_live(out)
        DEBT_PATH.write_text(json.dumps(debt, indent=2) + "\n")
        print(f"Wrote {DEBT_PATH} ({len(debt['entries'])} debt entries)")
        # rebuild so out.knownBadDebt is current
        out = build_verification()

    if queue_only:
        print_queue(out)
        return 0
    if check_only:
        return run_check(out)
    return run_check(out)


if __name__ == "__main__":
    sys.exit(main())
