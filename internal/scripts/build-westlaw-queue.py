#!/usr/bin/env python3
"""Build the portfolio Westlaw / KeyCite queue from the verification ledger.

Westlaw Patron Access is treatment + unresolved-pin only (see
WESTLAW_PATRON_ACCESS.md). This script does not mark anything VERIFIED.
It collapses OCR / 'See ' variants of the same reporter pin into one
library search string, tags the 27 UNIFIED cites already KeyCited on
2026-09-19, and ranks the rest for 20-view sessions.

Writes:
  internal/docs/westlaw_portfolio_queue.json
  internal/docs/WESTLAW_PORTFOLIO_QUEUE.md
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LEDGER = DOCS / "citation_verification.json"
OUT_JSON = DOCS / "westlaw_portfolio_queue.json"
OUT_MD = DOCS / "WESTLAW_PORTFOLIO_QUEUE.md"

# Matter 28 UNIFIED KeyCite (recon 2026-09-19-matter-28-keycite-westlaw.md).
# Most of these never entered the PDF citation index — still skip them.
UNIFIED_KEYCITE = [
    (("cal2d", "14", "47"), "Goddard v. Security Title, 14 Cal.2d 47"),
    (("cal2d", "43", "856"), "Berri v. Superior Court, 43 Cal.2d 856"),
    (("calapp3d", "67", "887"), "Valvo v. USC, 67 Cal.App.3d 887"),
    (("us", "553", "880"), "Taylor v. Sturgell, 553 U.S. 880"),
    (("us", "449", "90"), "Allen v. McCurry, 449 U.S. 90"),
    (("us", "465", "75"), "Migra v. Warren City Sch. Dist., 465 U.S. 75"),
    (("us", "531", "497"), "Semtek Int'l Inc. v. Lockheed Martin, 531 U.S. 497"),
    (("us", "365", "265"), "Costello v. United States, 365 U.S. 265"),
    (("cal4th", "61", "813"), "DKN Holdings LLC v. Faerber, 61 Cal.4th 813"),
    (("cal4th", "48", "788"), "Boeken v. Philip Morris USA, 48 Cal.4th 788"),
    (("cal2d", "39", "826"), "Keidatz v. Albany, 39 Cal.2d 826"),
    (("cal2d", "59", "577"), "Beazell v. Schrader, 59 Cal.2d 577"),
    (("calapp3d", "136", "322"), "Sartor v. Superior Court, 136 Cal.App.3d 322"),
    (("cal4th", "15", "288"), "Sullivan v. Delta Air Lines, 15 Cal.4th 288"),
    (("cal3d", "27", "875"), "Perez v. City of San Bruno, 27 Cal.3d 875"),
    (("f4th", "12", "978"), "Chavez v. Robinson, 12 F.4th 978"),
    (("f3d", "817", "1162"), "Chavez v. Robinson, 817 F.3d 1162"),
    (("f3d", "420", "897"), "Diaz v. Gates, 420 F.3d 897"),
    (("f3d", "504", "803"), "Kay v. City of Rancho Palos Verdes, 504 F.3d 803"),
    (("f3d", "325", "1078"), "Kildare v. Saenz, 325 F.3d 1078"),
    (("f3d", "131", "818"), "Neal v. Shimoda, 131 F.3d 818"),
    (("f3d", "739", "1226"), "Gonzales v. California Dep't of Corr., 739 F.3d 1226"),
    (("f3d", "838", "1019"), "Furnace v. Giurbino, 838 F.3d 1019"),
    (("calapp4th", "85", "1168"), "Franklin & Franklin v. 7-Eleven, 85 Cal.App.4th 1168"),
    (("us", "547", "451"), "Anza v. Ideal Steel Supply, 547 U.S. 451"),
    (("us", "533", "158"), "Cedric Kushner Promotions v. King, 533 U.S. 158"),
    (("f3d", "384", "1184"), "Swift v. California, 384 F.3d 1184"),
]
DONE_PINS = {pin for pin, _ in UNIFIED_KEYCITE}

# Hard NOT_FOUND — search to confirm absence; do not KeyCite a ghost.
FABRICATED_PATTERNS = (
    (r"\bleman\b", "In re Leman, 66 Cal.App.5th 200"),
    (r"trinity river", "Friends of the Trinity River, 184 Cal.App.4th 1466"),
    (r"\bdunford\b|\b13752958\b", "Dunford v. Rovi Corp., 2015 WL 13752958"),
    (r"collins v\.?\s*moore", "Collins v. Moore, 81 F.3d 167"),
    (r"burrell v\.?\s*jackson|\b23545858\b", "Burrell v. Jackson, 2003 WL 23545858"),
)

LIVE_BRIEFING = {12, 19, 20, 24, 25, 26, 27, 28, 29, 32, 33, 35}
BAD = {"NOT_FOUND", "MISCITED", "MISCHARACTERIZED", "MISQUOTED"}

PREFIX = re.compile(
    r"^(see|cf\.?|accord|citing|quoting|under|under the|"
    r"due process clause\.?|conclusion table of authorities cases|"
    r"table of authorities cases|cases|plaintiff.?s opposition\.?)\s+",
    re.I,
)

PIN_RE = re.compile(
    r"(?P<vol>\d+)\s+"
    r"(?P<rep>"
    r"U\.?\s*S\.|"
    r"S\.?\s*Ct\.|"
    r"F\.?\s*R\.?\s*D\.|"
    r"F\.?\s*App(?:'?x|\.?x)?|"
    r"Fed\.?\s*Appx|"
    r"F\.?\s*Supp\.?\s*(?:2d|3d)?|"
    r"F\.?\s*(?:2d|3d|4th)|"
    r"Cal\.?\s*Rptr\.?\s*(?:2d|3d)?|"
    r"Cal\.?\s*App\.?\s*(?:2d|3d|4th|5th)?|"
    r"Cal\.?\s*(?:2d|3d|4th|5th)|"
    r"M\.?\s*J\."
    r")\s+"
    r"(?P<page>\d+)",
    re.I,
)
WL_RE = re.compile(r"(?P<year>\d{4})\s+WL\s+(?P<num>\d+)", re.I)
US_BARE = re.compile(r"(?P<vol>\d+)\s+US\s+(?P<page>\d+)", re.I)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def strip_lead(citation: str) -> str:
    c = (citation or "").strip()
    while True:
        nxt = PREFIX.sub("", c)
        if nxt == c:
            return c
        c = nxt


def norm_reporter(raw: str) -> str:
    r = re.sub(r"[^a-z0-9]+", "", raw.lower())
    aliases = {
        "us": "us",
        "sct": "sct",
        "f2d": "f2d",
        "f3d": "f3d",
        "f4th": "f4th",
        "fappx": "fappx",
        "fedappx": "fappx",
        "fsupp": "fsupp",
        "fsupp2d": "fsupp2d",
        "fsupp3d": "fsupp3d",
        "frd": "frd",
        "cal": "cal",
        "cal2d": "cal2d",
        "cal3d": "cal3d",
        "cal4th": "cal4th",
        "cal5th": "cal5th",
        "calapp": "calapp",
        "calapp2d": "calapp2d",
        "calapp3d": "calapp3d",
        "calapp4th": "calapp4th",
        "calapp5th": "calapp5th",
        "calrptr": "calrptr",
        "calrptr2d": "calrptr2d",
        "calrptr3d": "calrptr3d",
        "mj": "mj",
    }
    return aliases.get(r, r)


def extract_pin(citation: str) -> tuple[str, str, str] | None:
    wl = WL_RE.search(citation)
    if wl:
        return ("wl", wl.group("year"), wl.group("num"))
    m = PIN_RE.search(citation)
    if m:
        return (norm_reporter(m.group("rep")), m.group("vol"), m.group("page"))
    m = US_BARE.search(citation)
    if m:
        return ("us", m.group("vol"), m.group("page"))
    return None


def case_name(citation: str) -> str:
    c = strip_lead(citation)
    head = c.split(",")[0].strip()
    return re.sub(r"\s+", " ", head)


def search_string(citation: str, pin: tuple[str, str, str] | None) -> str:
    c = strip_lead(citation)
    if pin and pin[0] == "wl":
        return f"{pin[1]} WL {pin[2]}"
    if pin:
        pretty = {
            "us": "U.S.",
            "sct": "S. Ct.",
            "f2d": "F.2d",
            "f3d": "F.3d",
            "f4th": "F.4th",
            "fappx": "F. App'x",
            "fsupp": "F. Supp.",
            "fsupp2d": "F. Supp. 2d",
            "fsupp3d": "F. Supp. 3d",
            "frd": "F.R.D.",
            "cal": "Cal.",
            "cal2d": "Cal.2d",
            "cal3d": "Cal.3d",
            "cal4th": "Cal.4th",
            "cal5th": "Cal.5th",
            "calapp": "Cal. App.",
            "calapp2d": "Cal.App.2d",
            "calapp3d": "Cal.App.3d",
            "calapp4th": "Cal.App.4th",
            "calapp5th": "Cal.App.5th",
            "mj": "M.J.",
        }.get(pin[0], pin[0])
        name = case_name(c)
        pin_s = f"{pin[1]} {pretty} {pin[2]}"
        keep = name and len(name) < 90 and (
            " v." in name.lower()
            or name.lower().startswith("in re ")
            or name.lower().startswith("in ")
        )
        if keep:
            return f"{name}, {pin_s}"
        return pin_s
    return c


def fabricated_label(citation: str) -> str | None:
    for pat, label in FABRICATED_PATTERNS:
        if re.search(pat, citation, re.I):
            return label
    return None


def worst_status(statuses: list[str]) -> str:
    order = ["NOT_FOUND", "MISQUOTED", "MISCHARACTERIZED", "MISCITED", "UNVERIFIED", "VERIFIED"]
    for s in order:
        if s in statuses:
            return s
    return statuses[0] if statuses else "UNVERIFIED"


def score(row: dict) -> tuple:
    """Lower is sooner. Load-bearing plaintiff work first."""
    bucket = {
        "confirm_absent": 0,
        "p0": 1,
        "p1": 2,
        "live_plaintiff": 3,
        "other_plaintiff": 4,
        "joined": 5,
        "done": 9,
    }[row["bucket"]]
    live = 0 if any(m in LIVE_BRIEFING for m in row["matters"]) else 1
    return (bucket, live, -row["occurrenceCount"], row["search"])


def build() -> dict:
    ledger = json.loads(LEDGER.read_text())
    rows = ledger.get("authorities") or []
    groups: dict[str, dict] = {}

    for r in rows:
        cite = r["citation"]
        pin = extract_pin(cite)
        if pin:
            key = f"{pin[0]}|{pin[1]}|{pin[2]}"
        else:
            key = f"name|{slug(case_name(cite))}"
        g = groups.get(key)
        if not g:
            g = {
                "key": key,
                "pin": list(pin) if pin else None,
                "search": search_string(cite, pin),
                "display": strip_lead(cite),
                "variants": [],
                "matters": set(),
                "roles": set(),
                "statuses": [],
                "priorities": [],
                "occurrenceCount": 0,
                "plaintiffOnly": True,
                "notes": [],
            }
            groups[key] = g
        g["variants"].append(cite)
        g["matters"].update(r.get("matters") or [])
        g["roles"].update(r.get("roles") or [])
        g["statuses"].append(r.get("status") or "UNVERIFIED")
        g["priorities"].append(r.get("priority") or "")
        g["occurrenceCount"] += int(r.get("occurrenceCount") or 0)
        if not r.get("plaintiffOnly"):
            g["plaintiffOnly"] = False
        if r.get("notes"):
            g["notes"].append(r["notes"])
        cand = strip_lead(cite)
        junk = "table of authorities" in cand.lower() or cand.lower().startswith("cases ")
        named = " v." in cand.lower() or " v " in cand.lower()
        current_named = " v." in g["display"].lower() or " v " in g["display"].lower()
        if not junk and (
            (named and not current_named)
            or (named == current_named and len(cand) < len(g["display"]))
        ):
            g["display"] = cand
            g["search"] = search_string(cite, pin)

    out_rows = []
    for g in groups.values():
        pin = tuple(g["pin"]) if g["pin"] else None
        fab = fabricated_label(g["display"]) or next(
            (fabricated_label(v) for v in g["variants"] if fabricated_label(v)), None
        )
        done = bool(pin and pin in DONE_PINS)
        status = worst_status(g["statuses"])
        has_plaintiff = "plaintiff_filing" in g["roles"]
        live_hit = bool(set(g["matters"]) & LIVE_BRIEFING)

        verified_exists = "VERIFIED" in g["statuses"]
        if fab:
            bucket = "confirm_absent"
        elif done:
            bucket = "done"
        elif (
            "P0_plaintiff_only_unverified" in g["priorities"]
            and not verified_exists
            and status == "UNVERIFIED"
        ):
            bucket = "p0"
        elif (g["plaintiffOnly"] and status in BAD) and not verified_exists:
            bucket = "p1"
        elif has_plaintiff and live_hit:
            bucket = "live_plaintiff"
        elif has_plaintiff or g["plaintiffOnly"]:
            bucket = "other_plaintiff"
        else:
            bucket = "joined"

        action = {
            "confirm_absent": "SEARCH ONLY — confirm the pin is empty; do not KeyCite a ghost",
            "p0": "KeyCite — plaintiff-only UNVERIFIED (existence still open)",
            "p1": "KeyCite — plaintiff-only bad status (treatment does not clear MISCITED / MISCHARACTERIZED)",
            "live_plaintiff": "KeyCite — appears in a plaintiff filing on a live matter",
            "other_plaintiff": "KeyCite — plaintiff filing, closed/archived matter",
            "joined": "KeyCite if time — court / opposing / research only so far",
            "done": "SKIP — KeyCite already recorded 2026-09-19 (UNIFIED / Round 12)",
        }[bucket]

        out_rows.append(
            {
                "search": g["search"],
                "display": g["display"],
                "pin": g["pin"],
                "bucket": bucket,
                "action": action,
                "status": status,
                "plaintiffOnly": g["plaintiffOnly"],
                "hasPlaintiffFiling": has_plaintiff,
                "liveBriefing": live_hit,
                "occurrenceCount": g["occurrenceCount"],
                "matters": sorted(g["matters"]),
                "roles": sorted(g["roles"]),
                "variantCount": len(set(g["variants"])),
                "variants": sorted(set(g["variants"]))[:8],
                "fabricated": fab,
                "keycited": done,
            }
        )

    seen_done = {tuple(r["pin"]) for r in out_rows if r.get("pin")}
    for pin, label in UNIFIED_KEYCITE:
        if pin in seen_done:
            continue
        out_rows.append(
            {
                "search": label,
                "display": label,
                "pin": list(pin),
                "bucket": "done",
                "action": "SKIP — KeyCite already recorded 2026-09-19 (UNIFIED / Round 12)",
                "status": "VERIFIED",
                "plaintiffOnly": False,
                "hasPlaintiffFiling": False,
                "liveBriefing": True,
                "occurrenceCount": 0,
                "matters": [28],
                "roles": ["research"],
                "variantCount": 0,
                "variants": [],
                "fabricated": None,
                "keycited": True,
                "indexMiss": True,
            }
        )

    out_rows.sort(key=score)
    for i, r in enumerate(out_rows, 1):
        r["n"] = i

    todo = [r for r in out_rows if r["bucket"] not in {"done", "confirm_absent"}]
    sessions = []
    for i in range(0, len(todo), 20):
        chunk = todo[i : i + 20]
        sessions.append(
            {
                "session": len(sessions) + 1,
                "from": chunk[0]["n"],
                "to": chunk[-1]["n"],
                "count": len(chunk),
                "searches": [c["search"] for c in chunk],
            }
        )

    payload = {
        "generatedDate": date.today().isoformat(),
        "source": "internal/docs/citation_verification.json",
        "method": (
            "Unique reporter/WL pins from ledger kind=authority rows. "
            "Statutes, rules, and constitutional provisions are not in this file. "
            "KeyCite is treatment, not existence. Yellow ≠ MISCITED. "
            "Round 12 UNIFIED 27 already tagged done. "
            "20-view session budget: flag-glance the batch, deep-read only yellow/red "
            "that could touch the cited proposition."
        ),
        "counts": {
            "ledgerAuthorities": len(rows),
            "uniquePins": len(out_rows),
            **dict(Counter(r["bucket"] for r in out_rows)),
            "todoKeyCite": len(todo),
            "sessionsOf20": len(sessions),
        },
        "alreadyKeycited": len(UNIFIED_KEYCITE),
        "rows": out_rows,
        "sessions": sessions,
    }
    return payload


def md_table(rows: list[dict], cols: list[tuple[str, str]]) -> str:
    head = "| " + " | ".join(h for h, _ in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    body = []
    for r in rows:
        cells = []
        for _, key in cols:
            val = r.get(key, "")
            if isinstance(val, list):
                val = ", ".join(str(x) for x in val)
            val = str(val).replace("|", "/")
            if len(val) > 90:
                val = val[:87] + "…"
            cells.append(val)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([head, sep, *body])


def write_md(payload: dict) -> str:
    c = payload["counts"]
    rows = payload["rows"]
    by = {b: [r for r in rows if r["bucket"] == b] for b in (
        "confirm_absent", "p0", "p1", "live_plaintiff", "other_plaintiff", "joined", "done"
    )}
    lines = [
        "# Westlaw portfolio queue",
        "",
        f"Generated {payload['generatedDate']} from `citation_verification.json` "
        "(kind=`authority` only). Not a brief. KeyCite is **treatment**, not existence. "
        "Yellow ≠ MISCITED. Do not mark VERIFIED from a flag color.",
        "",
        "Door: [WESTLAW_PATRON_ACCESS.md](WESTLAW_PATRON_ACCESS.md). "
        "20 document views / session. Flag-glance the batch first; deep-read only "
        "yellow/red that could touch the proposition you are citing.",
        "",
        "## Counts",
        "",
        f"- Ledger authority rows (OCR variants included): **{c['ledgerAuthorities']}**",
        f"- Unique reporter / WL / name pins: **{c['uniquePins']}**",
        f"- Already KeyCited (UNIFIED / Round 12): **{c.get('done', 0)}**",
        f"- Confirm-absent (known fabrications): **{c.get('confirm_absent', 0)}**",
        f"- Still to KeyCite: **{c['todoKeyCite']}** "
        f"({c.get('p0', 0)} P0 + {c.get('p1', 0)} P1 + {c.get('live_plaintiff', 0)} live-plaintiff "
        f"+ {c.get('other_plaintiff', 0)} other-plaintiff + {c.get('joined', 0)} court/opposing)",
        f"- Sessions at 20 views: **{c['sessionsOf20']}**",
        "",
        "## What this is not",
        "",
        "- Statutes, regulations, court rules, and constitutional provisions — Westlaw "
        "statute books are a different trip; they are not in this queue.",
        "- Existence. Run `npm run citations:lookup` first. Westlaw time is for flags "
        "and pins the free funnel left UNRESOLVED.",
        "- A clean bill. *Chavez*, 12 F.4th 978 is KeyCite NONE and still MISCHARACTERIZED.",
        "",
        "## Session 1 — do these first (20)",
        "",
        "P0 + P1 + the first live-plaintiff leftovers, in that order. "
        "Search the **Search** column. Record flag color and, on yellow/red, whether "
        "the treatment goes to **your** proposition.",
        "",
    ]
    first20 = [r for r in rows if r["bucket"] not in {"done", "confirm_absent"}][:20]
    lines.append(
        md_table(
            first20,
            [
                ("#", "n"),
                ("Search", "search"),
                ("Bucket", "bucket"),
                ("Status", "status"),
                ("Matters", "matters"),
            ],
        )
    )
    lines += [
        "",
        "## Confirm-absent (search only)",
        "",
        "Known fabrications. A miss is the point. Do not open KeyCite. "
        "Do not introduce these into a new plaintiff filing.",
        "",
        md_table(
            by["confirm_absent"],
            [
                ("Search / label", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
                ("Uses", "occurrenceCount"),
            ],
        )
        if by["confirm_absent"]
        else "_none_",
        "",
        "## P0 — plaintiff-only UNVERIFIED",
        "",
        md_table(
            by["p0"],
            [
                ("#", "n"),
                ("Search", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
                ("Uses", "occurrenceCount"),
            ],
        )
        if by["p0"]
        else "_none_",
        "",
        "## P1 — plaintiff-only bad status",
        "",
        "Treatment does not clear MISCITED / MISCHARACTERIZED. Use Westlaw to "
        "confirm the real caption/pin and whether anything is still citable at all.",
        "",
        md_table(
            by["p1"],
            [
                ("#", "n"),
                ("Search", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
                ("Uses", "occurrenceCount"),
            ],
        )
        if by["p1"]
        else "_none_",
        "",
        "## Live-matter plaintiff filings (not yet KeyCited)",
        "",
        "Matters 12, 19, 20, 24–29, 32, 33, 35. Load-bearing first by use count.",
        "",
        md_table(
            by["live_plaintiff"],
            [
                ("#", "n"),
                ("Search", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
                ("Uses", "occurrenceCount"),
            ],
        )
        if by["live_plaintiff"]
        else "_none_",
        "",
        "## Other plaintiff filings (closed / archived matters)",
        "",
        md_table(
            by["other_plaintiff"],
            [
                ("#", "n"),
                ("Search", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
                ("Uses", "occurrenceCount"),
            ],
        )
        if by["other_plaintiff"]
        else "_none_",
        "",
        "## Court / opposing / research only",
        "",
        "Flag-glance if a session has leftover views. Do not spend deep-reads here "
        "until the plaintiff buckets are empty.",
        "",
        md_table(
            by["joined"],
            [
                ("#", "n"),
                ("Search", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
                ("Uses", "occurrenceCount"),
            ],
        )
        if by["joined"]
        else "_none_",
        "",
        "## Already KeyCited — skip",
        "",
        "UNIFIED memo, 2026-09-19. Recon: "
        "`legal-intel/recon/2026-09-19-matter-28-keycite-westlaw.md`. "
        "*Chavez* 12 F.4th stays MISCHARACTERIZED.",
        "",
        md_table(
            by["done"],
            [
                ("Search", "search"),
                ("Status", "status"),
                ("Matters", "matters"),
            ],
        )
        if by["done"]
        else "_none_",
        "",
        "## 20-view session map",
        "",
        "| Session | Rows | First search | Last search |",
        "|---|---|---|---|",
    ]
    for s in payload["sessions"]:
        lines.append(
            f"| {s['session']} | {s['from']}–{s['to']} ({s['count']}) | "
            f"{s['searches'][0][:60]} | {s['searches'][-1][:60]} |"
        )
    lines += [
        "",
        "## Regenerating",
        "",
        "```",
        "python3 internal/scripts/build-westlaw-queue.py",
        "```",
        "",
        "Does not touch the verification ledger. Feed flags back through a dated "
        "recon + a later Round overlay the way Round 12 did.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    payload = build()
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n")
    OUT_MD.write_text(write_md(payload))
    c = payload["counts"]
    print(
        f"Wrote {OUT_JSON} and {OUT_MD} — "
        f"{c['uniquePins']} unique pins, {c['todoKeyCite']} still to KeyCite, "
        f"{c['sessionsOf20']} sessions of 20"
    )


if __name__ == "__main__":
    main()
