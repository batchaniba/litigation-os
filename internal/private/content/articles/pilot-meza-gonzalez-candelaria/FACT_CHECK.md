# FACT_CHECK — pilot Meza-Gonzalez / Candelaria article

**Draft:** `ARTICLE.md` (PILOT, not published).
**Checked:** 2026-11-01 (updated same day for Breyer reassignment).
**Record cutoff in the article:** portfolio `last_updated` 2026-10-28 for Matters 32 and 33; identity files for Matters 1, 2, 7, and 8 last updated 2026-09-16; user statement Oct. 31, 2026 that Matter 32 was reassigned to Senior District Judge Charles R. Breyer.
**Rule:** every factual sentence in the article maps to a filed paper, a public order, or a graph row that itself cites those papers. Advocacy, settlement numbers, sealed material, and excluded topics are out of the article and listed in RISK_NOTES if they sat nearby in the repo.

Status key:

| Status | Meaning |
|---|---|
| SUPPORTED | Filed paper or public order in the repo, or a graph field that restates one |
| ALLEGATION | True that the complaint/petition alleges it; not an adjudicated fact |
| GRAPH-ONLY | Portfolio identity / clocks / events; no independent PDF quote in this check |
| USER REPORT | Plaintiff’s statement in this chat; not yet a clerk PDF in the graph |
| GAP | Article avoided the claim, or stated the gap |

---

## FACT_CHECK table

| # | Claim in ARTICLE.md | Source file(s) | Status | Notes |
|---|---|---|---|---|
| 1 | Subject is Brendan Ngehsi Newanforbi; captions use Newanforbi and Nforbi | `internal/private/research/jurisdictions/NGEHSI_NEWANFORBI_JURISDICTIONS.md` (branch `cursor/ngehsi-newanforbi-jurisdictions-7b3e`); `internal/src/data/matters/01/matter.json`; `02/matter.json`; `07/matter.json`; `08/matter.json`; `32/matter.json`; `33/matter.json` | SUPPORTED | Catalog treats 32/33 as Nforbi-form captions; 1/2/7/8 as Newanforbi-form |
| 2 | Last graph-supported Meza-Gonzalez number is N.D. Cal. 4:26-cv-08271-ASK (formerly 3:26-cv-08271-PHK) | `internal/src/data/matters/32/matter.json`; `internal/src/data/index/matters.json` (number 32) | SUPPORTED | CourtListener object `nforbi-v-meza-gonzalez`. Graph still `-ASK` / Krishnan as of Oct. 28. `-CRB` is **not** written because no clerk notice is in the repo |
| 3 | Live Candelaria docket is N.D. Cal. 3:26-cv-08272-RFL (formerly LJC), San Francisco, Hon. Rita F. Lin (unchanged) | `internal/src/data/matters/33/matter.json`; index row 33 | SUPPORTED | User confirmed Candelaria stays with Judge Lin |
| 4 | Portfolio last_updated October 28, 2026 for Matters 32/33; Breyer assignment is an Oct. 31 user report layered on that cutoff | `32/matter.json` `last_updated`; `33/matter.json` `last_updated`; index `today` 2026-10-28; this chat, Oct. 31, 2026 | SUPPORTED (cutoff) / USER REPORT (judge) | |
| 5 | Officers Santiago Meza-Gonzalez (023295) and Jose Melano (023054) contacted plaintiff Nov. 1, 2024, I-580 East shoulder near Isabel Avenue, Livermore; CHP RJ68845 / CAD 241101GG0064 | `32/matter.json` `key_facts`; `33/matter.json` `key_facts`; `32/claims.json`; operative FACs Dkt. 5 / Dkt. 6 | ALLEGATION | Stated in the article as what the FACs allege |
| 6 | Stationary vehicle, engine off; treated as DUI investigation | `07/matter.json` `key_facts`; `32/prose.json` `key_facts` | ALLEGATION | Drawn from FAC/key_facts, not from an officer admission |
| 7 | Warrantless door opening, interior search, arrest under Veh. Code § 23152(a) | `32/claims.json` counts 1–3; `07/matter.json` `key_facts` | ALLEGATION | |
| 8 | On-scene audio identified the only liquid as urine, not alcohol; no contemporaneous alcohol-odor statement | `07/matter.json` `key_facts`; `08/matter.json` `key_facts` | ALLEGATION | Article does not use crude transcript quotes |
| 9 | Blood-draw warrant later obtained and blood drawn; later form designated a chemical-test refusal | `07/matter.json` `key_facts`; `33/matter.json` `key_facts` (DS-367) | ALLEGATION | Warrant number WAR913372 and phlebotomist name omitted from article as unnecessary |
| 10 | Nov. 5, 2024 Detention Certificate, Pen. Code § 849(b)(1), Dublin CHP-01991 / File 202400898, “detention only, not an arrest” | `07/matter.json` `key_facts`; `08/matter.json` `key_facts`; `33/matter.json` `key_facts` | ALLEGATION | Certificate is described in the pleadings; article does not call it a judicial finding |
| 11 | Alameda County DA declined to file charges | `07/matter.json` `key_facts`; `01/matter.json` `key_facts` | ALLEGATION | No DA declination letter independently quoted in this check |
| 12 | Live Meza-Gonzalez defendants are the two officers individually, plus Does; no State/CHP | `32/parties.json`; `32/claims.json` | SUPPORTED | |
| 13 | Six live § 1983 counts (entry, search, arrest, Franks, fabrication, First Amendment retaliation / PAS) | `32/claims.json` | SUPPORTED | |
| 14 | Alameda caption *Newanforbi v. Meza-Gonzalez et al.*, 26CV168913; claims false imprisonment, battery, Bane Act; filed Feb. 4, 2026; Hon. Marc Fickes | `02/matter.json`; `02/claims.json`; `02/parties.json` | SUPPORTED | |
| 15 | Alameda action dismissed without prejudice Aug. 15, 2026, CCP § 581(b)(1), (c) | `02/matter.json` `status`; `02/events.jsonl` Aug. 15, 2026; `/documents/matter-32/from-02/Request for Dismissal Without Prejudice (Draft, Aug 11 2026).pdf` | SUPPORTED | CIV-110 entered copy also cataloged: `CIV-110 Request for Dismissal Entered - Meza Alameda 26CV168913 (Aug 21 2026).pdf` on the jurisdictions branch |
| 16 | State-law theories and State/CHP defendant are not in the live N.D. Cal. Meza complaint | `32/parties.json`; `32/claims.json`; `02/events.jsonl` Aug. 15 flagged note | SUPPORTED | Article states the docket fact only; does not discuss limitations strategy |
| 17 | E.D. Cal. predecessor *Newanforbi v. CHP et al.*, 2:25-cv-01460-DC-CSK, filed May 27, 2025; Fourth Amendment / due process / Monell; dismissed without prejudice Aug. 15, 2026, FRCP 41(a)(1)(A)(i) | `01/matter.json`; `01/claims.json`; `/documents/matter-32/from-01/Notice of Voluntary Dismissal Without Prejudice (Aug 11 2026).pdf` | SUPPORTED | |
| 18 | APS Case 34739340; Teams hearing Jan. 24, 2025; Candelaria decision Feb. 11, 2025; one-year Class A suspension Feb. 20, 2025–Feb. 19, 2026; reissue fee; SR-22 | `33/matter.json` `key_facts`; `07/matter.json` `key_facts`; `33/claims.json` | ALLEGATION as to characterization of the hearing; the decision date/case number are pleaded as record facts | Article does not quote dollar reissue/SR-22 figures |
| 19 | Live Candelaria defendants: Diana Candelaria individually; Steve Gordon, DMV Director, official capacity | `33/parties.json`; `33/claims.json` | SUPPORTED | |
| 20 | Four live Candelaria counts (impartial adjudicator; fair hearing; declaratory vacatur; Ex parte Young injunction) | `33/claims.json` | SUPPORTED | |
| 21 | E.D. Cal. *Newanforbi v. Candelaria*, 2:26-cv-00983-DC-CSK; identity filed Apr. 27, 2026; FAC adding Gordon; Mag. Kim F&R June 15, 2026; dismissed without prejudice Aug. 15, 2026 before a district-judge ruling | `07/matter.json`; `07/claims.json`; `07/events.jsonl` Aug. 15; `/documents/matter-33/from-07/Notice of Voluntary Dismissal Without Prejudice (Aug 11 2026).pdf` | SUPPORTED / GRAPH-ONLY on F&R contents | Article does not quote the F&R. Catalog notes dismissal paper recites initiation Mar. 19, 2026 — article discloses that discrepancy |
| 22 | Veh. Code §§ 13353 / 13353.2 “lawful arrest” predicate theory | `07/claims.json` Count II; `08/claims.json` Count I | ALLEGATION | |
| 23 | Sacramento *Newanforbi v. Candelaria, et al.*, 26WM000135, filed May 18, 2026; CCP § 1094.5 / Veh. Code § 13559; fee waiver denied as incomplete; later hearing did not go forward; fee deadline ~July 27, 2026; abandoned | `08/matter.json`; `08/claims.json`; `08/events.jsonl` May 18, May 19, July 17, July 27 | SUPPORTED | Article omits the parole-transfer explanation recorded in events |
| 24 | Published cases *California DUI Lawyers Ass'n v. DMV*, 77 Cal. App. 5th 517 (2022), and *Knudsen v. DMV*, 101 Cal. App. 5th 186 (2024), are invoked by the pleadings | `07/matter.json` `key_facts`; `08/claims.json` Count IV | SUPPORTED as citations in the pleadings | Article does not say they control |
| 25 | Alameda Jan. 30, 2026 filing rejected for pleading paper; accepted Feb. 4, 2026 | `02/events.jsonl` Jan. 30 and Feb. 4 | GRAPH-ONLY | One Legal order numbers in events; complaint PDF `Newanforbi v. Meza Gonzalez et al.pdf` on jurisdictions branch |
| 26 | Service extension; State/CHP and Melano served March 2026; DAG meet-and-confer; Apr. 14, 2026 stay stipulation | `02/events.jsonl` Mar. 20, Mar. 25, Apr. 2, Apr. 9, Apr. 14; `02/prose.json` `procedural_status` | SUPPORTED as portfolio chronology of filed/served events | Stay stipulation PDF not independently re-read in this check |
| 27 | N.D. Cal. packets signed Aug. 7, 2026; both cases docketed Aug. 10, 2026 as 3:26-cv-08271-PHK (Kang) and 3:26-cv-08272-LJC (Cisneros) | `32/matter.json` `filed`; `33/matter.json` `filed`; `32/events.jsonl` Aug. 10–11 CourtListener rows; `33/events.jsonl` Aug. 10 | SUPPORTED | |
| 28 | Predecessors dismissed Aug. 15, 2026, after the N.D. Cal. refiles; new complaints disclosed the planned dismissals | `01`, `02`, `07`, `32`, `33` Aug. 15 events; Dkt. 1 complaints | SUPPORTED | Sequence is a public docket fact; article does not argue claim-splitting |
| 29 | Meza FAC Dkt. 6 filed Aug. 14; Dkt. 5 filed Aug. 17 and is operative | `32/matter.json`; `32/docket.json`; `32/events.jsonl` Aug. 14 / Aug. 17 | SUPPORTED | Numbering is inverted; article says so |
| 30 | Candelaria FAC Dkt. 5 filed Aug. 14; Dkt. 6 filed Aug. 17 and is operative; Dkt. 10 identifies Dkt. 6 | `33/matter.json`; `33/docket.json`; `33/events.jsonl` Aug. 14 / Aug. 17 / Aug. 26 | SUPPORTED | |
| 31 | Summonses Aug. 10; sheriff requests Aug. 13; Candelaria/Gordon served Aug. 14 at DMV Legal Affairs (Dkt. 7) | `33/parties.json` `serviceTracking`; `33/events.jsonl` Aug. 14; `33/docket.json` Dkt. 2, SER-001 rows | SUPPORTED | |
| 32 | Melano POS Dkt. 5-1 filed Aug. 17; clerk-stamped original scanned Aug. 31 | `32/docket.json`; `32/parties.json`; `32/events.jsonl` Aug. 17 / Aug. 31 | SUPPORTED | |
| 33 | Meza-Gonzalez substitute service Aug. 27; Rule 4(l) return Dkt. 16 / 16-1 filed Sep. 14 | `32/parties.json`; `32/events.jsonl` Aug. 27 / Sep. 14; `32/clocks.json` `32-deadline-1` | SUPPORTED | |
| 34 | Admin motion for DAG to accept service, Dkt. 13, filed Sep. 3 | `32/docket.json` Dkt. 13; `32/events.jsonl` Sep. 3 | SUPPORTED | Article correctly does not treat it as an officer appearance |
| 35 | Civil L.R. 3-15 certifications: Meza Dkt. 15 (Sep. 9); Candelaria Dkt. 16 (Sep. 10) | `32/docket.json` Dkt. 15; `33/docket.json` Dkt. 16; matching events | SUPPORTED | |
| 36 | Two PACER name forms; clerk would not merge e-filing accounts | `32/events.jsonl` Sep. 1 Help Desk correspondence; jurisdictions catalog N.D. Cal. section | GRAPH-ONLY / correspondence | Help Desk email is not a court order; article states the operational fact only |
| 37 | Candelaria name-correction stipulation Dkt. 18 (Sep. 14) granted Dkt. 19 (Sep. 16) | `33/docket.json` Dkt. 18; `33/events.jsonl` Sep. 14 / Sep. 16 | SUPPORTED | Stamped Dkt. 19 PDF not pulled in this check |
| 38 | Aug. 24, 2026 order related Serrato (then 4:26-cv-05953-ASK) to Meza-Gonzalez; reassigned to Mag. Krishnan as 4:26-cv-08271-ASK | `/documents/matter-24/Order Granting Administrative Motion to Relate Cases - Serrato and Meza (Aug 24 2026).pdf`; `32/events.jsonl` Aug. 24 | SUPPORTED | Article does not describe Serrato claims |
| 39 | Sep. 8, 2026 order: Candelaria not related to Serrato (Candelaria Dkt. 13) | `/documents/matter-33/ndcal/Dkt 13 - Related Case Order - Candelaria Not Related to Serrato (Filed Sep 8 2026).pdf`; `33/events.jsonl` Sep. 8 | SUPPORTED | |
| 40 | Candelaria declined magistrate jurisdiction and was reassigned to Judge Lin (-RFL) | `33/matter.json` `judge` / `case_no`; `33/clocks.json` `33-deadline-1` retired_reason | SUPPORTED | |
| 41 | Candelaria Dkt. 11 answer Sep. 4; Dkt. 17 motion to strike; Dkt. 24 granted Oct. 13 without hearing; struck Dkt. 11; required response to FAC | `33/docket.json`; `33/clocks.json` `33-deadline-6`, `33-deadline-7`; `/documents/matter-33/ndcal/Dkt 24 - Order Granting Motion to Strike (Filed Oct 13 2026).pdf` | SUPPORTED | PDF exists; text not extracted in this environment |
| 42 | Candelaria Dkt. 26 answer to amended complaint filed Oct. 27, 2026 | `33/clocks.json` `33-deadline-7` retired_reason; `33/events.jsonl` Oct. 28 PACER row | GRAPH-ONLY | PDF not ingested as of Oct. 28 — article says so |
| 43 | Meza Dkt. 22 MTD/strike filed Oct. 26; Dkt. 23 declination same day; responses Nov. 9, replies Nov. 16; Dec. 9 hearing later vacated | `32/docket.json` Dkts. 22–23; `32/clocks.json` `32-deadline-mtd-opposition`, `32-mtd-reply`, `32-mtd-hearing` | SUPPORTED | Article does not characterize MTD grounds (motion PDF not quoted) |
| 44 | Dkt. 25 clerk notice of impending reassignment Oct. 28 vacated magistrate hearing dates | `32/clocks.json` `32-mtd-hearing`, `32-reassignment-watch`; `32/events.jsonl` Oct. 28 | GRAPH-ONLY | Text-only NEF; PDF not stored. Precursor to the Oct. 31 Breyer report |
| 44a | Meza-Gonzalez reassigned to Senior District Judge Charles R. Breyer | User statement Oct. 31, 2026; Dkt. 25 impending-reassignment watch; related Serrato already before Breyer as 3:26-cv-05953-CRB (`24/matter.json`, Dkt. 29) | USER REPORT + GRAPH precursor | Article keeps `4:26-cv-08271-ASK` and TODOs the `-CRB` suffix. No `08271-CRB` string exists in the matter graph. The “new judge not in graph” gap is closed as to the judge’s name |
| 45 | Courtesy email of a Meza opposition is not an ECF filing; no opposition on NEFs through Oct. 28 | `32/clocks.json` `32-deadline-mtd-opposition`; `32/events.jsonl` Oct. 28 | GRAPH-ONLY | |
| 46 | Open Candelaria clocks: 26(f)/ADR Nov. 18; CMS/disclosures Dec. 2; CMC Dec. 9, 2026, 10:00 a.m. | `33/clocks.json` `33-deadline-2`, `33-deadline-3`, `33-hearing-4`; index `next_clock` | SUPPORTED | |
| 47 | Meza CMS Nov. 25 may reset before Judge Breyer | `32/clocks.json` `32-deadline-cms` | SUPPORTED | Clock note still says “until the new judge's order issues” |
| 48 | CourtListener slugs listed in the sources table | `01`, `07`, `32`, `33` `matter.json` `courtlistener` | SUPPORTED | |
| 49 | *California DUI Lawyers* / *Knudsen* existence | Standard published reporters; also recited in `07/matter.json` | SUPPORTED as published law | Not independently re-pulled from CourtListener in this draft |
| 50 | No settlement amounts, sealed files, registry, criminal history, Hertz/HireRight/other non-party employers, or strategy memos appear in ARTICLE.md | This FACT_CHECK; grep of ARTICLE.md | SUPPORTED by exclusion | See RISK_NOTES |

---

## Gaps (what the article does not claim, and why)

| Gap | Why |
|---|---|
| Grounds of Dkt. 22 (Meza MTD/strike) | PDF is on disk; this draft does not quote defense arguments |
| Text of Dkt. 24 (Candelaria strike order) | PDF is on disk; `pdftotext` / pypdf were unavailable in this environment. Substance taken from `clocks.json` / events |
| Clerk suffix / division after the Breyer reassignment | User named Judge Breyer on Oct. 31, 2026. The graph still has `4:26-cv-08271-ASK`. Article TODOs `-CRB` and the `4:` prefix; it does **not** invent `08271-CRB`. This is not a “new judge unknown” gap |
| Text of Dkt. 26 | Answer PDF not ingested as of Oct. 28. Dkt. 25 remains a text-only clerk notice (impending reassignment) |
| E.D. Cal. Candelaria F&R (June 15, 2026) wording | Identity files summarize Mag. Kim’s recommendation (IFP denial / dismissal). Article states that an F&R issued and was mooted; it does not quote it |
| Alameda stay-stipulation PDF | Events and `prose.json` record the Apr. 14, 2026 filing; the stipulation PDF was not re-read here |
| Exact E.D. Cal. Candelaria initiation date | Identity says Apr. 27, 2026; jurisdictions catalog says the dismissal paper recites Mar. 19, 2026. Article flags both |
| Whether default was entered on Meza Dkt. 17 | A Rule 55(a) request was filed Sep. 18; defendants later appeared by Dkt. 22. Article does not discuss default |
| Blood-alcohol number, medical condition, vehicle owner, employer, wage rates | Present in some `key_facts` fields; excluded as unnecessary or as non-party employer / medical detail |
| Any dollar demand, SR-22 premium, or settlement figure | Hard exclusion |

Private-matters front door `internal/private/matters/` has no Meza-Gonzalez or Candelaria workspace. Matter 0 is unrelated and was not used.

---

## RISK_NOTES

These cases are pending. The article is an unpublished internal draft. The following items are **in the repo** and were **kept out of ARTICLE.md**. Do not add them in a public revision without a separate decision.

1. **Pending-case prejudice.** A public narrative of a live stop and a live APS challenge can be attached to a motion, a CMC statement, or press. The draft is labeled PILOT / NOT FOR PUBLICATION for that reason.
2. **Settlement figures and terms.** `33/events.jsonl` (Sep. 18 and Sep. 25, 2026) and `internal/docs/settlement/SETTLEMENT_REANCHOR_MEMO.md` / `internal/private/negotiation/32.jsonl` and `33.jsonl` contain numbers and walk-aways. Hard exclusion. Do not put ledger figures in anything defense counsel or the public sees.
3. **Parole, custody, and criminal history.** Matter 2 and Matter 1 `key_facts` / events mention a multi-day hold. The jurisdictions catalog lists a Santa Clara criminal number and an Aurora immigration proceeding. The user forbade criminal-history and registry content. The article does not mention parole, holds, convictions, or registry.
4. **Sex-offender registry / CASOMB / PC 290.** Nearby cluster files mention these. Excluded.
5. **Hertz, HireRight, and other non-party employers.** `07/matter.json` names a commercial carrier and a rental-registration owner. Matter 29 / employment files are outside these captions. Excluded.
6. **U-visa / I-918 certification motion** in Alameda 26CV168913 (briefed June 2026; unruled; dismissed with the case). Public on that docket, but immigration-sensitive. Omitted.
7. **Medical detail** (pre-diabetes) in `07/matter.json` `key_facts`. Omitted.
8. **Home address, phone, and email** on caption blocks and notices of change of address. Omitted.
9. **Work product / strategy.** `prose.json` `risk` fields, SOL backstop discussion (Matter 2 `clocks.json` Nov. 1, 2026), claim-splitting flags, immunity forecasts, “do not start the Rule 12 clock” notes, and `internal/private/research/parole-habeas/` are internal. The article states only public sequence (refile then dismiss) without advising a limitations or amendment move.
10. **Citation-correction history.** `33/prose.json` discusses a *Burrell v. Jackson* passage on Dkt. 1 that does not appear in Dkt. 6. Internal. Not for a public piece.
11. **Serrato merits.** Related-case orders necessarily name *Newanforbi v. Serrato*. The article names the caption and the relate/not-relate results only.
12. **Defamation / character.** Officers and the hearing officer are described by badge, title, and what the complaints allege. No motive adjectives. “Fabrication” appears only as the name of a pleaded count.
13. **Name-form confusion.** Publishing both *Newanforbi* and *Nforbi* is accurate and also makes the person easier to search. A public version should keep the caption rule and the draft banner.
14. **Docket drift.** Matter 32: user reports reassignment to Senior District Judge Charles R. Breyer (Oct. 31, 2026); the graph still lists `-ASK`. Confirm the clerk suffix and any reset hearing/CMS dates on PACER before a public version. Matter 33 stays with Judge Lin; clocks run in November–December 2026.
15. **No GitHub / document-store URLs** in any outbound version (standing lock). Internal `/documents/...` paths in the sources table are for editors, not for a public page.

---

## Exclusion scan (ARTICLE.md)

| Term | In ARTICLE.md? |
|---|---|
| Settlement / offer / $50,000 / $250,000 / walk-away | No |
| Parole / hold / CDCR / registry / Megan / PC 290 | No |
| Hertz / HireRight / Centerline / PV Holding / Accurate / Amazon / FedEx / UPS | No |
| U-visa / I-918 / immigration court | No |
| Home address / phone / email | No |
| GitHub / raw.githubusercontent | No |
| Immunity prediction / “will win” / “should lose” | No |
