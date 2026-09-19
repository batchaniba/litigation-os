#!/usr/bin/env python3
"""Render the Matter 28 Westlaw Patron Access run sheet.

Reads internal/docs/citation_sources_matter28_primary.json so the citations
on the run sheet cannot drift from the verification queue, and pairs each
item with what to type into Westlaw and what to bring back.

Westlaw Patron Access for Pro Se is a MANUAL source. The account's own
affirmations bar use on behalf of an organization and bar competitive
product development; the full licence terms are expected to bar automated
access and bulk extraction. Nothing here is automatable, and no credential
belongs anywhere near lookup-citations.py. What comes back is the reader's
own finding — status, holding, pin confirmed, KeyCite flag — recorded as a
round entry, never wholesale opinion text pasted into the repo.

Outputs:
  internal/docs/MATTER_28_WESTLAW_RUN_SHEET.md

Usage:
  python3 internal/scripts/build-matter28-westlaw-run-sheet.py
  python3 internal/scripts/build-matter28-westlaw-run-sheet.py --check
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "docs/citation_sources_matter28_primary.json"
OUT = ROOT / "docs/MATTER_28_WESTLAW_RUN_SHEET.md"

# item -> (tier, what to type, what to bring back)
PLAN: dict[str, tuple[int, str, str]] = {
    "1A": (1, "meinhardt v. city of sunnyvale",
           "The holding on when the appeal clock starts. Then search within the "
           "opinion for *demurrer* and for *res judicata*. Answer all five queue "
           "questions, especially whether preclusion is discussed at all. This "
           "item decides the shape of the opposition — do it first."),
    "1B": (1, "Estate of Esche v. Bunuel-Jordana  (or docket 24-6244)",
           "KeyCite flag. Then settle the disputed question: is the private-party "
           "qualified-immunity discussion the HOLDING or reasoning toward a "
           "jurisdictional holding? The ledger currently says MISCHARACTERIZED — "
           "confirm or overturn it on the record."),
    "5C": (1, "2016 WL 4761808",
           "Paste the bare WL number — Westlaw is the only source that resolves "
           "one. Then KeyCite for the subsequent history that has been unverified "
           "since the Sept. 18 memo: later state-action ruling, dismissal, "
           "settlement, or appeal."),
    "4.2": (2, "975 F.3d 742", "Confirm the quoted language sits at 753. KeyCite flag."),
    "4.3": (2, "326 F.3d 1088", "Confirm the four state-action tests are at 1092. KeyCite flag."),
    "4.4": (2, "590 F.3d 806",
            "Confirm the conduct-specific inquiry, AND record the actual outcome — "
            "was the charter school held a state actor for the conduct at issue? "
            "The queue flags this as likely cutting against us."),
    "4.8": (2, "398 F. Supp. 3d 700",
            "Confirm what the sentence at 713 actually says, and the full caption "
            "(the index has it truncated as 'Zetz v. Boston Scienti')."),
    "4.9": (2, "806 F.2d 1393",
            "Confirm 1400-01, and confirm the year is 1986 and that it REVERSED a "
            "RICO dismissal."),
    "4.10": (2, "96 F.4th 1223", "Confirm the sentence at 1233 and what proposition it supports."),
    "4.11": (2, "824 F.3d 858",
             "Confirm 867 and the full caption (indexed mangled as "
             "“Az. Students’ Ass. v. Ariz. Bd”)."),
    "2A": (3, "989 F.2d 362",
           "Quote on whether a California judgment after a general demurrer is on "
           "the merits, with the pin. Expect this to cut AGAINST us — record it "
           "plainly either way."),
    "2B": (3, "112 Cal.App.4th 1416", "The general-vs-special demurrer passage, with the pin."),
    "2C": (3, "14 Cal.2d 47",
           "The sentence at 52-53 conceding a general-demurrer judgment may NOT be "
           "on the merits where the defect is technical or formal. Cal.2d is a "
           "known gap in the free tooling — this is the lookup only Westlaw does."),
    "2D": (3, "67 Cal.App.3d 887",
           "Confirm 891-92 and footnote 3: until entry of judgment a demurrer "
           "ruling is not res judicata."),
    "2E": (3, "250 F.3d 668",
           "Settle the YEAR (2000 vs 2001 both appear in circulation) and pin the "
           "judicial-notice passage. Existence is already VERIFIED — this is a "
           "pin and year fix only."),
    "1C": (3, "623 F. App'x 338",
           "Published or unpublished memo? Disposition on each claim. First "
           "Amendment retaliation and qualified immunity rulings. CONFIRM the "
           "docket is No. 12-35294 — several other Wicklund actions exist and "
           "caption collision is the whole risk here."),
    "4.1": (4, "765 F.3d 999", "The 'obvious bar on the face of the complaint' sentence at 1004."),
    "4.5": (4, "521 U.S. 399",
            "Supply the missing pin for the 'systematically organized' private-firm "
            "language. Existence is settled; this is the pin only."),
    "4.6": (4, "708 F.2d 1376",
            "Confirm the footnote really is n.4 and the page really is 1380 — the "
            "queue doubts this pin."),
    "4.7": (4, "27 Cal.3d 875", "The prematurity / precondition passage at 882-83."),
    "4.12": (4, "604 U.S. 593",
             "Confirm the official U.S. Reports cite, and quote what the Court "
             "EXPRESSLY DECLINED to decide about 'business', 'property', and "
             "proximate cause."),
}

TIER_LABEL = {
    1: "Tier 1 — do these first (they change the argument)",
    2: "Tier 2 — the seven standing UNVERIFIED ledger rows (fast; pin confirmation only)",
    3: "Tier 3 — the preclusion battleground and the caption-collision risk",
    4: "Tier 4 — remaining pin confirmations",
}


def main() -> int:
    q = json.loads(QUEUE.read_text())
    by_item = {e["item"]: e for e in q["caseLaw"]}
    missing = sorted(set(PLAN) ^ set(by_item))
    if missing:
        print(f"run sheet and queue disagree on items: {missing}", file=sys.stderr)
        return 1

    L: list[str] = []
    w = L.append
    w("# Matter 28 — Westlaw Patron Access run sheet")
    w(f"## *Newanforbi v. Shannon Smith, LCSW, et al.*, {q['caseNo']}")
    w("")
    w("Generated by `internal/scripts/build-matter28-westlaw-run-sheet.py` from "
      "`citation_sources_matter28_primary.json` — edit the script, not this file. "
      "Citations are pulled from the queue so the two cannot drift.")
    w("")
    w("## Read this before you start")
    w("")
    w("**Westlaw Patron Access for Pro Se is a MANUAL source. It does not wire "
      "into the citation funnel.**")
    w("")
    w("The affirmations on the account bar use on behalf of a law firm, company, "
      "government or non-profit, and bar use for developing competing products or "
      "for benchmarking. The full License Terms are expected to bar automated "
      "access and bulk extraction — read that section once and treat it as "
      "controlling.")
    w("")
    w("- No credential goes near `lookup-citations.py`, `.env`, or any script.")
    w("- No scripted queries, no scraping, no bulk download.")
    w("- Do not paste opinion text wholesale into the repo.")
    w("- What you bring back is YOUR OWN FINDING — status, holding in your words, "
      "whether the pin checked out, the KeyCite flag. That is what "
      "`citation_verification_rounds.json` has always held.")
    w("")
    w("What this account uniquely closes, which no free source could: KeyCite "
      "negative treatment, `F. App'x`, `Cal.2d`, bare `WL` numbers, star "
      "pagination for pin confirmation, and docket-number search.")
    w("")
    w("## Standing instruction")
    w("")
    w("**KeyCite every authority already on `MATTER_28_SAFE_CITE_LIST.md`.** "
      "Existence was verified months ago; treatment never was. A red or yellow "
      "flag on a cite currently marked SAFE is the most valuable thing this "
      "session can produce.")
    w("")
    w("## What to record per item")
    w("")
    w("```")
    w("ITEM:            <queue item id>")
    w("KEYCITE FLAG:    green / yellow / red / none shown")
    w("PIN CONFIRMED:   yes (page seen in star pagination) / no / n-a")
    w("HOLDING:         <in your own words, one or two sentences>")
    w("DISPOSITION:     affirmed / reversed / dismissed / vacated")
    w("PUBLISHED:       published / unpublished")
    w("CUTS AGAINST US: <yes + how, or no>")
    w("```")
    w("")
    w("Anything that cuts against us is the point, not the failure. Record it.")
    w("")
    w("---")
    w("")
    for tier in (1, 2, 3, 4):
        items = [i for i in PLAN if PLAN[i][0] == tier]
        items.sort(key=lambda i: (len(i), i))
        w(f"## {TIER_LABEL[tier]}")
        w("")
        for item in items:
            _, query, capture = PLAN[item]
            e = by_item[item]
            pins = "; ".join(e["pinsToConfirm"])
            led = e["existingPortfolioStatus"].get("ledgerStatus")
            w(f"### {item} — *{e['caseName']}*")
            w("")
            w(f"- **Type:** `{query}`")
            w(f"- **Full cite:** {e['citation']}")
            if pins:
                w(f"- **Pin(s) to confirm:** {pins}")
            if led:
                w(f"- **Ledger now:** {led}")
            w(f"- **Bring back:** {capture}")
            w("")
        w("")
    w("## When you are back at the keyboard")
    w("")
    w("1. Write each finding into `internal/docs/citation_verification_rounds.json` "
      "as `{citation, status, source, notes, round}` with "
      "`round: \"12-matter28-westlaw-patron\"` and `source` naming Westlaw Patron "
      "Access plus the date you read it.")
    w("2. `npm run citations:verify && npm run citations:check && npm run generate:readme`")
    w("3. Promote to `MATTER_28_SAFE_CITE_LIST.md` only per legal-intel README rule 5 "
      "— the opinion has been opened, which after this session is true.")
    w("4. A red KeyCite flag on anything currently SAFE moves it to DO_NOT_USE "
      "immediately, before any drafting.")
    w("")
    return _emit("\n".join(L) + "\n")


def _emit(body: str) -> int:
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text() != body:
            print(f"drift: {OUT}", file=sys.stderr)
            return 1
        print("ok — run sheet matches the script")
        return 0
    OUT.write_text(body)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
