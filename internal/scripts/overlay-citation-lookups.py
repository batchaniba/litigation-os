#!/usr/bin/env python3
"""Fold lookup-citations.py consensus into citation_verification_rounds.json.

Usage:
  python3 internal/scripts/overlay-citation-lookups.py FILE.json [...]
  python3 internal/scripts/overlay-citation-lookups.py --existing

Rules (citation-verify skill + this overlay):
  FOUND + prior UNVERIFIED → VERIFIED (existence only)
  PARTIAL with a CourtListener/CAP hit and compatible name → VERIFIED
    (single-source; CAP often lacks recent Cal. App. 5th volumes)
  CAPTION_MISMATCH + truncated/OCR name of the same case → VERIFIED
    (existence; official caption recorded in notes)
  CAPTION_MISMATCH with a wrong case at the pin, from a pin API
    (citation-lookup or CAP) → MISCITED
  CAPTION_MISMATCH from search-only → left alone (table-page hazard)
  Devenpeck 543 U.S. 11 / 3 U.S. 146 → MISCITED (wrong or impossible pin)
  Prior MISCHARACTERIZED / proposition-MISCITED stays
  Never downgrade a table-page VERIFIED
  NOT_FOUND is left alone (a miss is not a fabrication)
  Web-search-only PARTIAL is left alone (allowlisted SERP is not a pin match)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from lib.citation_keys import case_name_key, names_overlap, normalize_authority_key, reporter_pin_key

ROOT = Path(__file__).resolve().parents[1]
ROUNDS = ROOT / "docs" / "citation_verification_rounds.json"
LEDGER = ROOT / "docs" / "citation_verification.json"
DOCS = ROOT / "docs"
ROUND_ID = "13-cl-token"
PIN_OVERLAY_SOURCES = {"courtlistener_citation", "case.law_static"}

SKIP_PRIOR = {"MISCHARACTERIZED", "MISCITED", "NOT_FOUND", "VERIFIED"}


def load_prior() -> tuple[dict[str, str], dict[str, str], dict[str, list[str]]]:
    """Maps: full key → status, pin → status, pin → ledger citation strings."""
    by_key: dict[str, str] = {}
    by_pin: dict[str, str] = {}
    cites_by_pin: dict[str, list[str]] = {}
    if not LEDGER.exists():
        return by_key, by_pin, cites_by_pin
    data = json.loads(LEDGER.read_text())
    for row in data.get("authorities") or data.get("results") or []:
        cite = row.get("citation")
        status = row.get("status")
        if not cite or not status:
            continue
        by_key[normalize_authority_key(cite)] = status
        pin = reporter_pin_key(cite)
        if pin:
            by_pin.setdefault(pin, status)
            cites_by_pin.setdefault(pin, []).append(cite)
    return by_key, by_pin, cites_by_pin


def sources_note(row: dict) -> str:
    urls = []
    for source in row.get("sources") or []:
        if not isinstance(source, dict):
            continue
        if source.get("found") and source.get("url"):
            urls.append(source["url"])
    return (" Sources: " + " ; ".join(urls) + ".") if urls else ""


def prior_status_for(lookup: dict, by_key: dict[str, str], by_pin: dict[str, str]) -> str | None:
    query = lookup.get("query") or ""
    status = by_key.get(normalize_authority_key(query))
    if status:
        return status
    pin = reporter_pin_key(query) or reporter_pin_key(str(lookup.get("reporter_pin") or lookup.get("wl_pin") or ""))
    if pin and pin in by_pin:
        return by_pin[pin]
    return None


def ledger_citation_for(lookup: dict, cites_by_pin: dict[str, list[str]]) -> str:
    query = lookup.get("query") or ""
    pin = reporter_pin_key(query) or reporter_pin_key(str(lookup.get("reporter_pin") or lookup.get("wl_pin") or ""))
    if pin:
        cites = cites_by_pin.get(pin) or []
        if len(cites) == 1:
            return cites[0]
        query_name = case_name_key(query)
        for cite in cites:
            if case_name_key(cite) == query_name or query_name in case_name_key(cite) or case_name_key(cite) in query_name:
                return cite
    return query


def pin_source_found(lookup: dict) -> bool:
    return any(
        isinstance(s, dict) and s.get("found") and s.get("source") in PIN_OVERLAY_SOURCES
        for s in (lookup.get("sources") or [])
    )


def web_only_partial(lookup: dict) -> bool:
    if lookup.get("consensus") != "PARTIAL":
        return False
    found = [s for s in (lookup.get("sources") or []) if isinstance(s, dict) and s.get("found")]
    if not found:
        return True
    return all(s.get("source") == "web_search" for s in found)


def overlay_row(
    lookup: dict,
    by_key: dict[str, str],
    by_pin: dict[str, str],
    cites_by_pin: dict[str, list[str]],
) -> dict | None:
    query = lookup.get("query") or ""
    consensus = lookup.get("consensus")
    prior_status = prior_status_for(lookup, by_key, by_pin)
    if prior_status in SKIP_PRIOR:
        return None
    if web_only_partial(lookup):
        return None
    matched = lookup.get("matched_name") or ""
    pin = lookup.get("reporter_pin") or lookup.get("wl_pin") or ""
    query_name = query

    cap_notes = " ".join(
        (s.get("notes") or "")
        for s in (lookup.get("sources") or [])
        if isinstance(s, dict) and s.get("source") == "case.law_static"
    )
    if "No case with first_page=" in cap_notes and "Devenpeck" in query:
        return {
            "citation": ledger_citation_for(lookup, cites_by_pin),
            "status": "MISCITED",
            "source": "Round 12 CAP volume check",
            "round": ROUND_ID,
            "notes": (
                "Devenpeck v. Alford is 543 U.S. 146 (2004). This string points at a page "
                "that is not in that volume (543 U.S. 11) or at an impossible early U.S. "
                "Reports volume (3 U.S. 146). Do not brief this pin."
            ),
        }

    # Pin API resolved a different case at this reporter page.
    if consensus == "CAPTION_MISMATCH" and matched and not names_overlap(query_name, matched):
        if pin_source_found(lookup):
            return {
                "citation": ledger_citation_for(lookup, cites_by_pin),
                "status": "MISCITED",
                "source": "Round 13 CourtListener citation-lookup / CAP pin",
                "round": ROUND_ID,
                "notes": (
                    f"Pin {pin or '(none)'} resolves to {matched}, not the queried caption. "
                    f"Do not brief this pin as {query_name}.{sources_note(lookup)}"
                ),
            }
        return None

    if consensus in {"FOUND", "CAPTION_MISMATCH"} or (
        consensus == "PARTIAL" and lookup.get("matched_name") and "Devenpeck" not in query
    ):
        official = matched or "the queried caption"
        src = (
            "Round 13 CourtListener citation-lookup + CAP"
            if consensus == "FOUND"
            else (
                "Round 13 pin resolves; official caption differs from index string"
                if consensus == "CAPTION_MISMATCH"
                else "Round 13 single-source pin (citation-lookup or CAP)"
            )
        )
        extra = ""
        if consensus == "CAPTION_MISMATCH":
            extra = (
                f" Index string is truncated or OCR-variant; official caption is {official}."
            )
        return {
            "citation": ledger_citation_for(lookup, cites_by_pin),
            "status": "VERIFIED",
            "source": src,
            "round": ROUND_ID,
            "notes": (
                f"Existence only. Pin {pin or '(none)'} is {official}."
                f"{extra}{sources_note(lookup)} Characterization still needs opinion text."
            ),
        }
    return None


def existing_lookup_files() -> list[Path]:
    return sorted(DOCS.glob("citation_lookup*.json"))


def main(argv: list[str]) -> int:
    args = list(argv)
    use_existing = False
    if "--existing" in args:
        use_existing = True
        args = [a for a in args if a != "--existing"]
    paths = [Path(a) for a in args]
    if use_existing:
        paths.extend(existing_lookup_files())
    if not paths:
        print(
            "usage: overlay-citation-lookups.py [--existing] <lookup.json> [...]",
            file=sys.stderr,
        )
        return 2
    by_key, by_pin, cites_by_pin = load_prior()
    rounds = json.loads(ROUNDS.read_text())
    existing_keys = {normalize_authority_key(r["citation"]) for r in rounds.get("results") or []}
    existing_pins = {
        reporter_pin_key(r["citation"])
        for r in rounds.get("results") or []
        if reporter_pin_key(r["citation"])
    }
    added = []
    for path in paths:
        payload = json.loads(path.read_text())
        for row in payload.get("results") or []:
            overlay = overlay_row(row, by_key, by_pin, cites_by_pin)
            if not overlay:
                continue
            k = normalize_authority_key(overlay["citation"])
            pin = reporter_pin_key(overlay["citation"])
            if k in existing_keys or (pin and pin in existing_pins):
                continue
            rounds.setdefault("results", []).append(overlay)
            existing_keys.add(k)
            if pin:
                existing_pins.add(pin)
            added.append(overlay)
            by_key[k] = overlay["status"]
            if pin:
                by_pin[pin] = overlay["status"]
    if added:
        method = rounds.get("method") or ""
        note = (
            " Round 13: CourtListener citation-lookup (COURTLISTENER_API_TOKEN) is a pin "
            "source; same-case OCR CAPTION_MISMATCH stays existence VERIFIED; wrong case "
            "at a pin-API hit is MISCITED; web-search-only hits are not overlaid."
        )
        if "Round 13:" not in method:
            rounds["method"] = (method.rstrip() + note).strip()
    ROUNDS.write_text(json.dumps(rounds, indent=2) + "\n")
    print(json.dumps({"added": len(added), "byStatus": {
        s: sum(1 for r in added if r["status"] == s) for s in ("VERIFIED", "MISCITED")
    }}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
