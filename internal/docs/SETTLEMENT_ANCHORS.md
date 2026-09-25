# Settlement Anchors — Portfolio Negotiation Policy

Effective September 25, 2026. Applies to every settlement demand, counter, and call in the portfolio until Plaintiff changes it. Brackets are negotiation positions, not verdict predictions. Live dates stay in each matter's `clocks.json`; this file does not create clocks.

## Why this exists — Matter 27 post-mortem

Randstad / RK closed at a **$25,000 global** agreement in principle (Sep. 17, 2026). The number came from Plaintiff moving alone, not from a trade:

| Date | Plaintiff move | Defense move |
|---|---|---|
| Aug. 19 | $55,000 Randstad-only / $85,000 global | — |
| Aug. 28 | Restated same figures | Williams: needs more time (no number) |
| Sep. 9 | Withdrew both figures, **no replacement** | — |
| Sep. 12 | Sent **$25,000 global** + extension to Sep. 18 (the $40,000 house draft that held the Sep. 14/15 clocks was not sent) | — |
| Sep. 16–17 | Default entered, then vacated by stipulation for a Sep. 25 answer date and a PJ/service waiver | Accepted $25,000 |

The file's own default prove-up for Randstad alone was **$45,543.70**. Two defendants settled for ~55% of the conservative one-defendant figure, with no defense counter on the record.

## Rules

1. **After the opening, no move without their number.** Silence, "conferring with client," and requests for time are not counters.
2. **Never withdraw a figure without a replacement on the table,** and never pair a price cut with extra defense time.
3. **Every concession buys something:** a defense number, a document, a held clock, or a narrower release.
4. **No demand while their dispositive motion is pending,** unless Plaintiff would hold that figure after winning it.
5. **Write the walk-away before each call or email** (in the matter's `events.jsonl` or eval folder). If a drafted figure is higher than what is about to go out, stop and reconcile.
6. **Do not trade a default, a clock, or a waiver for procedure alone.** Trade it for money or a counter.
7. **Settlements are separate.** Do not cite Randstad's number anywhere (it will likely be confidential, and $25,000 is a low anchor). Do not release other matters, other defendants, or unrelated claims to close one deal.
8. **Allocate shared losses once.** SLB's May 23, 2026 rejection already argued Plaintiff's Matter 1 declaration ties lost employment to the CHP DUI arrest. Wage loss claimed in one matter is not re-claimed in another.

## Brackets

| Track | Opening | Target | Walk-away | When a number goes out |
|---|---|---|---|---|
| **Accurate** (29) | $150,000 (re-anchored Sep. 25 by Plaintiff; was $60,000) | $25,000–$35,000 | ~$15,000 — weigh any Rule 68 offer above it against trial-after-costs before rejecting | Now, after the FCRA file request |
| **FedEx** (25) | $150,000 | $60,000–$90,000; $90,000–$125,000 if the First Advantage report shows registry as the sole basis | $40,000 (file's conservative) | Settlement conference requested for the week of Nov. 2, or earlier if FedEx asks |
| **UPS** (26) | $150,000 | $60,000–$90,000 | $40,000 | Only after the Oct. 7 ruling, and only if the MTD is denied; reprice down if granted with leave |
| **Amazon** (29) | $250,000 (Aug. 31 demand stands) | $50,000–$90,000; $100,000+ if the Accurate report shows registry sourcing | $30,000 | After its responsive motion is decided |
| **Smith / HOPE** (28) | $350,000–$500,000 | $150,000–$250,000 if core claims survive; $50,000–$100,000 if narrowed | Set after ruling | After the Oct. 20 MTD ruling |
| **Serrato** (20 state, 24 federal) | Completed I-918 Supplement B certification + $150,000 | Certification + modest cash | Certification itself | Push certification now (Count 1 survived Aug. 29); federal cash after the Nov. 20 ruling |
| **Candelaria** (33) | Vacatur / corrected record first | Cash only after wage loss is allocated across the DMV-related matters | Not set | After the Nov. 12 motion-to-strike ruling; the $50,000 offer expiring Sep. 25 is not renewed |

Not in the settlement wave: Matter 12 (default judgment / collection), Matter 35 (unserved), Matter 32 (service still being perfected), Matter 19 (habeas).

## Track notes

- **Accurate and Amazon negotiate separately.** Different counsel (Seyfarth / Morgan Lewis) and different speeds: Accurate's desk exits fast after the answer (*Santee*: $10,000 Rule 68 the next day; *Williams*: ~5 weeks), Amazon after a ruling narrows the case (*Lerma*). A combined figure lets Accurate wait behind Amazon. Accurate's release must name Accurate only; track any settlement credit against Amazon. Mechanics: [`counsel/frederick-stanzick/PLAYBOOK.md`](counsel/frederick-stanzick/PLAYBOOK.md).
- **The report decides the § 290.46 premium.** In *Lerma*, the Megan's Law claim died because Accurate's report showed ordinary court-record sourcing and a "NO RECORD FOUND" sex-offender search. Get Matter 29's actual report before pricing that theory: see [`fcra-file-requests/`](fcra-file-requests/).
- **FedEx and UPS are the one real linked pair.** Same theory, same court, same district judge. The FedEx answer (Dkt. 4) admits First Advantage flagged registration and the adverse-action letter cited the registry websites; UPS's Dkt. 7 Exhibit A is a First Advantage report and its Dkt. 14 reply admits registry-based use. Do not return to UPS's $85,000 pre-filing figure; the $250,000 demand (Aug. 31) lapsed Sep. 14 with no counter.
- **Serrato's leverage is the linkage.** The certification is worth more to Plaintiff than cash from an individual officer asserting qualified immunity with the AG defending. The federal case may be what buys the certification.

## Remedies — what the brackets assume

- **Pen. Code § 290.46(j)(4)(A):** actual damages, an additional amount of at least $250 up to treble actuals, attorney's fees, and exemplary damages **or** a civil penalty **up to** $25,000. The $25,000 is a cap, not a floor.
- **ICRAA, Civ. Code § 1786.50:** actual damages or $10,000, whichever is greater (non-class), plus costs/fees; punitive damages for grossly negligent or willful violations. The violation still has to be proved.
- **FCRA:** $100–$1,000 statutory damages per consumer only for willful noncompliance (15 U.S.C. § 1681n), plus punitive damages; actual damages for negligent noncompliance (§ 1681o).
- **Pro se:** Plaintiff's own time is not recoverable as attorney's fees. Every comparable that includes plaintiff-side fees (e.g. *Santee* ~$17,240 all-in) overstates what a pro se plaintiff takes home.
- **Unverified:** a claim that 2026 California appellate decisions let a plaintiff pursue ICRAA's $10,000 alternative without additional actual injury arrived without case names. Do not put it in a demand until named and cleared through the citation funnel (`citation-verify`).

## Deal terms to hold in every agreement

- Release limited to the named defendant(s), this case, and the claims pleaded in it.
- Written confirmation of authority for every releasing defendant before signature (Matter 27: RK / Garcia).
- Allocation stated in the agreement (wage vs. non-wage), with tax treatment reviewed before signing.
- Payment within a fixed number of days after execution; dismissal filed only after funds clear.
- Confidentiality, non-disparagement, no-rehire, and tax-indemnity clauses are concessions: narrow or price them.
