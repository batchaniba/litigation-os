# Legal intel layer

Research input for briefs. Not a brief. If a page does not change a sentence about to be filed, it is a notebook.

## Rules

1. Each **active** matter has one card: `matters/NN.md`. Four headings only: Clock, People, Safe cites, Impeachment watch.
2. Cluster contradictions live in `clusters/`, not in the matter card. Generators read the cluster file first.
3. One counsel record per person: the `counsel/*-hand.md` file if it exists. Stub `.md` / `.json` pairs are not cited.
4. One judge file per judge. If the assignment moved, mark the old file `prior` and point the card at the live assignment.
5. Authorities go on the matter **Safe cites** list before they go in a generator. `MATTER_28_SAFE_CITE_LIST.md` is the model.
6. Dated `recon/` surveys are appendices. Do not open them to draft.
7. Update the card when the assignment changes, counsel changes, a motion is filed, or a locked fact is decided.

## Live index

| Matter | Card | Cluster lock | Next clock (as of 2026-09-15) |
|---|---|---|---|
| 12 Diamond / Alpine | [12](matters/12.md) | — | Re-serve Saliman Osmani; Alpine Kern; CMC Dec. 11 |
| 19 (if open) | *not yet* | [02](clusters/02-hope-parole-locked-facts.md) | Eagan quote rule |
| 20 CHP writ | [20](matters/20.md) | [01](clusters/01-nov1-locked-facts.md) | Count 4 optional amend Sep. 20; CMC Oct. 28 |
| 24 Serrato | [24](matters/24.md) | [01](clusters/01-nov1-locked-facts.md) | MTD Nov. 20, 10:00 a.m. Zoom (Breyer); opposition is Dkt. 20 |
| 25 FedEx | *not yet* | [05](clusters/05-screening-locked-facts.md) | No UPS Exhibit A language |
| 26 UPS | [26](matters/26.md) | [05](clusters/05-screening-locked-facts.md) | MTD hearing Oct. 7 |
| 27 Randstad / RK | [27](matters/27.md) | [05](clusters/05-screening-locked-facts.md) | Randstad response Sep. 15; $25k global expires Sep. 18 5:00 p.m. PT |
| 28 Smith / HOPE | [28](matters/28.md) | [02](clusters/02-hope-parole-locked-facts.md) | Answer Sep. 21 |
| 29 Amazon | [29](matters/29.md) | [05](clusters/05-screening-locked-facts.md) | Answers Sep. 22 |
| 30 Moua | *not yet* | [02](clusters/02-hope-parole-locked-facts.md) | Pre-filing; GCA window |
| 31 First Advantage | *not yet* | [05](clusters/05-screening-locked-facts.md) | Limitations diary only |
| 32 Officers | [32](matters/32.md) | [01](clusters/01-nov1-locked-facts.md) | Meza service clean-up; send Li the return |
| 33 Candelaria | [33](matters/33.md) | [01](clusters/01-nov1-locked-facts.md) | MJ consent Sep. 22; Dkt. 17 opp. Sep. 23 |
| 35 Ross | [35](matters/35.md) | — | Caption request; serve CT Corp ~Oct. 25 |
| 36–39 unfiled | [36–39](matters/36-39.md) | [05](clusters/05-screening-locked-facts.md) | Shared card until each has a case number |
| 22 Pilot | archive | [05](clusters/05-screening-locked-facts.md) | Settled Jul. 14, 2026 |

Closed shells (1, 2, 5, 7, 8, 15) stay off this table. They appear only on the cluster lock as “do not cite as pending.”

## Existing research (appendices)

- Counsel hands: `counsel/`
- Frederick–Stanzick Playbook (Matter 29 two-desk + *Lerma* / *Carrillo* papers): [`../counsel/frederick-stanzick/`](../counsel/frederick-stanzick/)
- Judge memos: `judges/` — check assignment before using
- Dated surveys: `recon/`
- Matter 28 MTD stack: [`recon/2026-09-12-matter-28-UNIFIED.md`](recon/2026-09-12-matter-28-UNIFIED.md) (briefing spine — rebuilt 2026-09-19 on Track A + unique #879 files; do not merge old #879 as-is). Draft from UNIFIED. Do not open the dated supplements to draft. Primary-source ITEM log: [`recon/2026-09-19-matter-28-primary-source-verification.md`](recon/2026-09-19-matter-28-primary-source-verification.md). Gap-fill pins remain at [`recon/2026-09-18-matter-28-mtd-gap-fill.md`](recon/2026-09-18-matter-28-mtd-gap-fill.md).
- Portfolio impeachment map: [`../CROSS_MATTER_RISK_INDEX.md`](../CROSS_MATTER_RISK_INDEX.md) (dated Jul. 11, 2026 — refresh against live captions)
- 28 cite whitelist: [`../MATTER_28_SAFE_CITE_LIST.md`](../MATTER_28_SAFE_CITE_LIST.md)

## New card template

Copy [`matters/_TEMPLATE.md`](matters/_TEMPLATE.md).
