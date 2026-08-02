# Legal review checklist — pre-launch

**Status: NOT REVIEWED. Do not point a live domain at this site until counsel has signed
off on the items below.**

This site makes public, consumer-facing claims about a fee arrangement tied to home equity
borrowing and digital asset acquisition. That combination touches several regulatory
regimes at once. Every substantive claim is inventoried here with its source in
`Equity2Bitcoin_Business_Plan.pdf` so counsel can review the site against the plan it
implements.

Reviewer: ______________________  Date: __________  Sign-off: __________

---

## 1. The highest-priority items

These are the three where the site's copy leans hardest on the business plan's own
reasoning, and where an adverse reading would be most consequential. Review these first.

### 1.1 The publisher's / Advisers Act exemption

**Where:** site-wide positioning; `/disclosures`; FAQ "Are you a registered
investment adviser?"
**Plan basis:** §IV.C, "Investment Advisers Act of 1940 — SEC Publisher's Exemption:
provides general education, not tailored financial advice."

**The question for counsel:** the publisher's exemption as construed in *Lowe v. SEC*
turns on publications being impersonal and of general and regular circulation. This
business delivers a **personalized** "Equity Profile Review," a customized written
"Readiness Report" built on an individual client's property and loan data, and one-on-one
consulting directed at a **specific asset**. Confirm whether the exemption reaches that
conduct, and if not, what registration or restructuring is required.

Downstream: if the exemption does not apply, most of this site's copy needs revision, not
just the disclaimer.

### 1.2 Fee contingent on loan closing

**Where:** `/pricing`; `/calculator` results; every milestone card; FAQ "The fee".
**Plan basis:** §III.C — 30% of extracted equity, triggered at verified loan funding.

**The question for counsel:** a fee payable only upon a consumer's mortgage loan closing
raises questions under, at minimum: RESPA §8 (fees for referral or for services not
actually performed) if any lender relationship exists; TILA/Reg Z loan originator
compensation rules; California Financing Law and CA Fin. Code §50000 et seq. re: whether
any activity constitutes brokering; and state mortgage broker licensing generally.
Confirm the fee is permissible as structured, in each state where clients will be served,
and confirm no compensation, referral, or marketing arrangement with any lender partner
alters the analysis.

### 1.3 UDAAP exposure on the fee itself

**Where:** entire site.
**Plan basis:** §III.C; §VII.F.

**The question for counsel:** a 30% fee on borrowed principal, secured by the consumer's
home, where the consumer is left immediately 30% underwater, is the kind of arrangement
the CFPB and state AGs examine under unfair/deceptive/abusive standards — particularly
"abusive," which reaches taking unreasonable advantage of a consumer's inability to
protect their interests. **The site has been built to disclose this as prominently as
possible** (the calculator subtracts the fee on screen, the homepage states it, the FAQ
states it) precisely because disclosure is the strongest available mitigation. Confirm
whether disclosure is sufficient here or whether the fee structure itself needs revisiting.

---

## 2. Claim inventory

| # | Claim | Where | Plan cite | Review |
|---|---|---|---|---|
| 2.1 | "Not a registered investment adviser / broker-dealer / mortgage broker / MLO / bank / lender / money transmitter" | Footer, `/disclosures`, `/book` | §IV.C | Confirm accurate and complete for every state served |
| 2.2 | "We never take custody of funds, loan proceeds, or digital assets" | Footer, homepage trust bar, FAQ | §III.A, §IV.C | Confirm operational reality matches; any deviation defeats the MTL position |
| 2.3 | "Clients apply to licensed third-party lenders independently" | `/how-it-works`, FAQ | §III.B Phase 3 | Confirm no arrangement makes this brokering in substance |
| 2.4 | 30% fee, charged once, at Milestone 3 | `/pricing`, `/calculator` | §III.C | See §1.2 above |
| 2.5 | "Fee is not contingent on Bitcoin performance" | `/pricing`, FAQ | §III.C | Confirm this distinction holds up |
| 2.6 | Historical Bitcoin cycle data (2012/2016/2020 halvings, price moves, drawdowns) | `/why-bitcoin` | §I | Verify each figure against a citable source; add citations or soften to ranges |
| 2.7 | "Bitcoin has declined more than 80% in every completed cycle" | Multiple | §I Volatility Acknowledgment | Verify accuracy — this is a risk disclosure and must be right |
| 2.8 | Calculator outputs (borrowable, fee, net, monthly cost) | `/calculator` | §II.C, §III.F | Confirm disclaimer language is adequate; confirm outputs cannot be read as pre-qualification under ECOA/Reg B |
| 2.9 | Worked pricing example | `/pricing` | §X.B | Confirm "illustrative" framing is sufficient |
| 2.10 | "You could lose your home" / foreclosure risk | FAQ, `/disclosures` | §VII.E | Confirm phrasing meets applicable disclosure standards |
| 2.11 | Tax comment re: interest deductibility depending on use of proceeds | `/fit`, FAQ | §55 tax discussion | Confirm accurate and adequately hedged; consider removing entirely |
| 2.12 | Terms of service | `/terms` | — | **Drafted by non-counsel. Full review required.** |
| 2.13 | Privacy policy | `/privacy` | — | **Drafted by non-counsel. Full review required.** CCPA/CPRA adequacy; update for any analytics or CRM added later |

---

## 3. Deliberately excluded from the public site

Recorded here so the decision is visible and reversible only on purpose.

| Excluded | Source | Why |
|---|---|---|
| BTC price projections ($500K by 2029, $1M by 2033) | Plan p.2 | Forward-looking asset price claims to a retail audience considering borrowing against their home. Highest-risk content in the document. |
| Treasury compounding projections ($600M–$2.37B) | Plan p.2 | Investor-facing; irrelevant and prejudicial on a consumer site |
| Revenue/client projections | §VI | Investor-facing |
| "Best-performing asset class in history" / +20,000,000% return | §I | Cherry-picked start date; reads as promotional |
| ARK Invest $700K–$1M price targets | §I | Third-party forecast; republishing adopts it |
| §III.F worked example as written | §III.F | Contains a math error — see §4 |

---

## 4. Two errors in the source document, corrected here

Flagged so nobody "fixes" the site back to match the plan.

**4.1 — Raw equity vs. tappable equity.** §III.F describes a $700,000 home with a
$400,000 mortgage as having "≈$300,000 in extractable equity." That is *raw* equity. At
the 80% LTV the plan itself cites on p.55, the borrowable figure is **$160,000**. The
site's calculator uses the LTV-based figure and displays raw equity separately, labelled
as such. Appendix B's example ($700K value, $300K mortgage, $200K draw) is internally
consistent at ~71% LTV and does not have this problem.

**4.2 — BTC quantity ignores the fee.** §III.F concludes the client "owns 3–5 BTC" from a
$300,000 draw. After the $90,000 fee only $210,000 reaches Bitcoin. The site subtracts
the fee before computing any illustrative BTC quantity.

**Commercial consequence, for the record:** because 4.1 corrects the borrowable figure
downward, typical clients will draw less than the $300,000 the revenue model assumes, and
the fee per client will be correspondingly lower. That is a business planning matter, not
a legal one, but it follows from the same correction.

---

## 5. Before launch

- [ ] Counsel sign-off on §1 (all three items)
- [ ] Counsel review and rewrite of `/terms` and `/privacy`
- [ ] Citations added or figures softened for every item in §2.6 and §2.7
- [ ] E&O insurance bound (§VII.B)
- [ ] Milestone agreement finalized and consistent with what `/pricing` describes
- [ ] Confirm state-by-state where services may be offered; add geographic limits if needed
- [ ] Replace both `PLACEHOLDER` Calendly URLs in `web/src/config/site.ts`
- [ ] Update `BTC_REFERENCE` price and `asOf` date together, or remove the BTC line
- [ ] Confirm `hello@equity2bitcoin.com` is monitored
- [ ] Re-review this file if any analytics, ad pixel, CRM, or email capture is added
