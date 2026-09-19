#!/usr/bin/env python3
"""Fold lookup-citations.py consensus into citation_verification_rounds.json.

Usage:
  python3 internal/scripts/overlay-citation-lookups.py \\
      internal/docs/citation_lookup_matter25.json \\
      internal/docs/citation_lookup_p0_25263233.json

Rules (citation-verify skill + this overlay):
  FOUND + prior UNVERIFIED → VERIFIED (existence only)
  PARTIAL with a CourtListener/CAP hit and compatible name → VERIFIED
    (single-source; CAP often lacks recent Cal. App. 5th volumes)
  CAPTION_MISMATCH + truncated/OCR name of the same case → VERIFIED
    (existence; official caption recorded in notes)
  CAPTION_MISMATCH with a wrong case at the pin → MISCITED
    (this script does not auto-detect that; mark those by hand)
  Devenpeck 543 U.S. 11 / 3 U.S. 146 → MISCITED (wrong or impossible pin)
  Prior MISCHARACTERIZED / proposition-MISCITED stays
  Never downgrade a table-page VERIFIED
  NOT_FOUND is left alone (a miss is not a fabrication)
  UNRESOLVED is left alone (pin sources were skipped or incomplete)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUNDS = ROOT / "docs" / "citation_verification_rounds.json"
LEDGER = ROOT / "docs" / "citation_verification.json"


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def key_of(citation: str) -> str:
    c = re.sub(r"^(See|see|SEE)\s+", "", (citation or "").strip())
    return slug(c)


def load_prior_status() -> dict[str, str]:
    if not LEDGER.exists():
        return {}
    data = json.loads(LEDGER.read_text())
    out = {}
    for row in data.get("authorities") or data.get("results") or []:
        cite = row.get("citation")
        status = row.get("status")
        if cite and status:
            out[key_of(cite)] = status
    return out


def sources_note(row: dict) -> str:
    urls = []
    for s in row.get("sources") or []:
        if s.get("found") and s.get("url"):
            urls.append(s["url"])
    return (" Sources: " + " ; ".join(urls) + ".") if urls else ""


def overlay_row(lookup: dict, prior: dict[str, str]) -> dict | None:
    query = lookup.get("query") or ""
    consensus = lookup.get("consensus")
    prior_status = prior.get(key_of(query))
    if prior_status in {"MISCHARACTERIZED", "MISCITED", "NOT_FOUND", "VERIFIED"}:
        return None
    matched = lookup.get("matched_name") or ""
    pin = lookup.get("reporter_pin") or lookup.get("wl_pin") or ""

    cap_notes = " ".join(
        s.get("notes") or ""
        for s in (lookup.get("sources") or [])
        if s.get("source") == "case.law_static"
    )
    # Volume exists on CAP but this first_page is not in it — the pin is wrong.
    if "No case with first_page=" in cap_notes and "Devenpeck" in query:
        return {
            "citation": query,
            "status": "MISCITED",
            "source": "Round 11 CAP volume check",
            "round": "11-p0-ocr-alias",
            "notes": (
                "Devenpeck v. Alford is 543 U.S. 146 (2004). This string points at a page "
                "that is not in that volume (543 U.S. 11) or at an impossible early U.S. "
                "Reports volume (3 U.S. 146). Do not brief this pin."
            ),
        }

    if consensus in {"FOUND", "CAPTION_MISMATCH"} or (
        consensus == "PARTIAL" and lookup.get("matched_name") and "Devenpeck" not in query
    ):
        official = matched or "the queried caption"
        src = (
            "Round 11 CourtListener + CAP lookup"
            if consensus == "FOUND"
            else (
                "Round 11 pin resolves; official caption differs from index string"
                if consensus == "CAPTION_MISMATCH"
                else "Round 11 single-source lookup (CourtListener or CAP)"
            )
        )
        extra = ""
        if consensus == "CAPTION_MISMATCH":
            extra = (
                f" Index string is truncated or OCR-variant; official caption is {official}."
            )
        return {
            "citation": query,
            "status": "VERIFIED",
            "source": src,
            "round": "11-p0-ocr-alias",
            "notes": (
                f"Existence only. Pin {pin or '(none)'} is {official}."
                f"{extra}{sources_note(lookup)} Characterization still needs opinion text."
            ),
        }
    return None


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: overlay-citation-lookups.py <lookup.json> [...]", file=sys.stderr)
        return 2
    prior = load_prior_status()
    rounds = json.loads(ROUNDS.read_text())
    existing_keys = {key_of(r["citation"]) for r in rounds.get("results") or []}
    added = []
    for path in argv:
        payload = json.loads(Path(path).read_text())
        for row in payload.get("results") or []:
            overlay = overlay_row(row, prior)
            if not overlay:
                continue
            k = key_of(overlay["citation"])
            if k in existing_keys:
                continue
            rounds.setdefault("results", []).append(overlay)
            existing_keys.add(k)
            added.append(overlay)
            prior[k] = overlay["status"]
    ROUNDS.write_text(json.dumps(rounds, indent=2) + "\n")
    print(json.dumps({"added": len(added), "byStatus": {
        s: sum(1 for r in added if r["status"] == s) for s in ("VERIFIED", "MISCITED")
    }}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
