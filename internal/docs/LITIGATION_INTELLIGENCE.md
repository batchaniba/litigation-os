# Litigation intelligence OS

The portfolio already stores dockets, timelines, and documents. This layer **reasons** about them.

CourtListener remains an upstream event stream (`internal/docs/COURTLISTENER.md`). Confirmed facts still land in `timeline.json`. Deadlines still cannot silently enter next-actions. What changes is what happens *after* an event is known.

```
COURTLISTENER / PACER / filings
        │
        ▼
Litigation Event Bus
        │
        ├── deadline agent      (dependency clocks, not just dates)
        ├── matter-state agent  (Litigation Twin)
        ├── war-room agent
        ├── precedent agent     (shockwave against the issue graph)
        ├── citation agent      (CiteProof: existence + proposition + history)
        └── notification agent  (overnight brief)
```

`sync-dockets.mjs` stays a dispatcher. It classifies new entries and appends `internal/src/data/intelligence/events.json`. It does not become a 4,000-line monster.

## What this slice does

| Capability | What shipped | What is still catalog/seeded |
|---|---|---|
| Knowledge graph | Built at runtime from matters + catalog + cross-matter links | Issue/authority/counsel nodes |
| Litigation Twin | Per-matter controlling questions; QI anticipated → active on MTD | Coverage scores are **record coverage**, not win odds |
| Defense fingerprints | Profiles for Li, Van Dine, Mott; match a filing to repeated arguments | No RECAP scrape of 41 outside matters |
| Judge doctrine maps | Krishnan / Cisneros / Delaney research order | Not grant-rate statistics |
| Precedent shockwave | Issue overlap → affected matters | No opinion-NLP holdings extractor |
| Argument diff | Snapshot vs snapshot (Matter 24 Dkt. 18; Matter 26 reply) | No PDF section parser yet |
| Contradiction engine | Fact propositions with sources / contradicted_by | Grows as discovery is coded |
| Claim element matrix | Live federal matters 24, 25, 26, 28, 29, 32, 33 | Coverage detection only |
| Dependency deadlines | Serrato CMC = 14 days after Dkt. 18 final order; JCMS −7 | Trigger still needs the order |
| War room | Generated from MOTION_FILED / ORDER_ENTERED | CiteProof overlap is catalog-backed |
| Event bus | Typed events; court:sync emits | Webhook HTTP still not deployed |
| Opposing-party graph + systemic importance | Counsel sharing + graph degree + live motions | Not a dollar ranking |
| Domino simulator | “What if 24 survives the MTD?” / theory rejected | Deterministic graph walk |
| RECAP cost gate | retrieve / wait / skip | No automatic PACER purchase |
| CiteProof+ | existence, bindingness, posture, parenthetical overstatement (Lerma) | Proposition-in-opinion NLP later |
| Overnight analyst | Text brief from twins + events | No autonomous filing |

## Commands

```
npm run intel:brief     # text radar
```

UI: `/intelligence`, plus a Litigation Twin panel on each matter that has a twin.

## Scores

Every percentage on this surface is **coverage detection**: allegation / evidence / authority / defense slots filled. It is not a prediction of how a judge will rule.
