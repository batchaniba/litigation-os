# FACT_CHECK — pilot Meza-Gonzalez / Candelaria article

**Draft:** `ARTICLE.md` (PILOT, not published). **Hold: do not publish before the Nov 9 Meza opposition is filed.**
**Checked:** 2026-11-02 (ChatGPT 27 edits + Claude line edits; more protective version on overlap).
**Record cutoff in the article:** Meza-Gonzalez Dkt. 29 NEF filed Oct. 30, 2026; portfolio `last_updated` 2026-10-28 for other Matter 32/33 graph fields; identity files for Matters 1, 2, 7, and 8 last updated 2026-09-16. Narrative of the stop follows Exhibit A (00:54:36–01:57:10) without announcing conflicts with the FACs.
**Rule:** every factual sentence in the article maps to a filed paper, a public order, Exhibit A (timestamp and internal page), or a graph row that itself cites those papers. Advocacy, settlement numbers, sealed material, and excluded topics are out of the article and listed in RISK_NOTES if they sat nearby in the repo. User decision 2026-11-01 (still in force): KEEP the drinking questions, the denials, the empty can, and Melano's "This is pee" quote verbatim. User decision 2026-11-02: apply both critiques; delete the "Neither?"/"Yep." exchange; do not publish Exhibit A vs. FAC contradictions.

Status key:

| Status | Meaning |
|---|---|
| SUPPORTED | Filed paper or public order in the repo, or a graph field that restates one |
| ALLEGATION | True that the complaint/petition alleges it; not an adjudicated fact |
| RECORDING | Plaintiff's Exhibit A transcript (not a stipulated CHP transcript); timestamp and internal "Page N of 19" cited |
| GRAPH-ONLY | Portfolio identity / clocks / events; no independent PDF quote in this check |
| UNVERIFIED | Could not re-open the cited PDF or native video in this pass; flagged, not deleted |
| GAP | Article avoided the claim, or stated the gap |

---

## FACT_CHECK table

| # | Claim in ARTICLE.md | Source file(s) | Status | Notes |
|---|---|---|---|---|
| 1 | Subject is Brendan Ngehsi Newanforbi; captions use Newanforbi and Nforbi | `internal/private/research/jurisdictions/NGEHSI_NEWANFORBI_JURISDICTIONS.md` (branch `cursor/ngehsi-newanforbi-jurisdictions-7b3e`); `internal/src/data/matters/01/matter.json`; `02/matter.json`; `07/matter.json`; `08/matter.json`; `32/matter.json`; `33/matter.json` | SUPPORTED | Catalog treats 32/33 as Nforbi-form captions; 1/2/7/8 as Newanforbi-form |
| 2 | Live Meza-Gonzalez number is N.D. Cal. 4:26-cv-08271-CRB (formerly 4:26-cv-08271-ASK; 3:26-cv-08271-PHK) | Dkt. 29 NEF Case Number field; `NEF-Dkt-29-Order-Reassigning-Case-to-Breyer-2026-10-30.pdf`. Graph row `32/matter.json` still `-ASK` as of Oct. 28 | SUPPORTED | Clerk number on the NEF controls over the stale graph |
| 3 | Live Candelaria docket is N.D. Cal. 3:26-cv-08272-RFL (formerly LJC), San Francisco, Hon. Rita F. Lin (unchanged) | `internal/src/data/matters/33/matter.json`; index row 33 | SUPPORTED | |
| 4 | Portfolio last_updated October 28, 2026 for Matters 32/33; Dkt. 29 filed October 30, 2026 | `32/matter.json` `last_updated`; `33/matter.json` `last_updated`; Dkt. 29 NEF (“entered on 10/30/2026 at 2:26 PM and filed on 10/30/2026”) | SUPPORTED | |
| 5 | Officers Santiago Meza-Gonzalez and Jose Melano identified as the officers in the Nov. 1, 2024 Livermore encounter; CHP RJ68845 / CAD 241101GG0064 | Operative FACs Dkt. 5 / Dkt. 6; `32/claims.json` | ALLEGATION | Badge numbers removed from the article |
| 6 | Stationary vehicle, engine off; treated as DUI investigation | `07/matter.json` `key_facts`; `32/prose.json` `key_facts` | ALLEGATION | Drawn from FAC/key_facts, not from an officer admission |
| 7 | Warrantless door opening, interior search, arrest under Veh. Code § 23152(a) | `32/claims.json` counts 1–3; `07/matter.json` `key_facts` | ALLEGATION | |
| 8 | Officers identified the contents of a cup as urine; Melano quoted verbatim: "Is it water? No this is piss. This is pee." / "I'm telling you it's piss. It smells like piss." | Ex. A 00:58:49–00:58:59 (p. 3); M-FAC 5:28–6:4 (¶17); C-FAC 10:24–25 | RECORDING / ALLEGATION | KEEP verbatim. Article no longer says "only liquid." Brand of the empty can, 21+ wristband, and any test result remain out |
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
| 21 | E.D. Cal. *Newanforbi v. Candelaria*, 2:26-cv-00983-DC-CSK; identity filed Apr. 27, 2026; FAC adding Gordon; Mag. Kim F&R June 15, 2026; dismissed without prejudice Aug. 15, 2026 before a district-judge ruling | `07/matter.json`; `07/claims.json`; `07/events.jsonl` Aug. 15; `/documents/matter-33/from-07/Notice of Voluntary Dismissal Without Prejudice (Aug 11 2026).pdf` | SUPPORTED / GRAPH-ONLY on F&R contents | Article does not quote the F&R. Dismissal paper's Mar. 19 date is noted without calling it a forum-switch |
| 22 | Veh. Code §§ 13353 / 13353.2 “lawful arrest” predicate theory | `07/claims.json` Count II; `08/claims.json` Count I | ALLEGATION | |
| 23 | Sacramento *Newanforbi v. Candelaria, et al.*, 26WM000135, filed May 18, 2026; CCP § 1094.5 / Veh. Code § 13559; petition did not proceed | `08/matter.json`; `08/claims.json`; `08/events.jsonl` May 18, May 19, July 17, July 27 | SUPPORTED | Article no longer says "abandoned" or recites the lapsed-fee sequence |
| 24 | Published cases *California DUI Lawyers Ass'n v. DMV*, 77 Cal. App. 5th 517 (2022), and *Knudsen v. DMV*, 101 Cal. App. 5th 186 (2024), are invoked by the pleadings | `07/matter.json` `key_facts`; `08/claims.json` Count IV | SUPPORTED as citations in the pleadings | Article frames them as addressing when a dual role requires a new hearing. Reporter page 101 Cal. App. 5th 186 remains UNVERIFIED as a pinpoint |
| 25 | Alameda Jan. 30, 2026 filing rejected for pleading paper; accepted Feb. 4, 2026 | `02/events.jsonl` Jan. 30 and Feb. 4 | GRAPH-ONLY | One Legal order numbers in events; complaint PDF `Newanforbi v. Meza Gonzalez et al.pdf` on jurisdictions branch |
| 26 | Service extension; State/CHP and Melano served March 2026; DAG meet-and-confer; Apr. 14, 2026 stay stipulation | `02/events.jsonl` Mar. 20, Mar. 25, Apr. 2, Apr. 9, Apr. 14; `02/prose.json` `procedural_status` | SUPPORTED as portfolio chronology of filed/served events | Stay stipulation PDF not independently re-read in this check |
| 27 | N.D. Cal. packets signed Aug. 7, 2026; both cases docketed Aug. 10, 2026 as 3:26-cv-08271-PHK (Kang) and 3:26-cv-08272-LJC (Cisneros) | `32/matter.json` `filed`; `33/matter.json` `filed`; `32/events.jsonl` Aug. 10–11 CourtListener rows; `33/events.jsonl` Aug. 10 | SUPPORTED | |
| 28 | Northern District complaints docketed Aug. 10, 2026; predecessors dismissed without prejudice Aug. 15, 2026 | `01`, `02`, `07`, `32`, `33` Aug. 10 / Aug. 15 events | SUPPORTED | Claim-splitting and "docketing choice" sentences removed |
| 29 | Roadside FAC Dkt. 5 is operative | `32/matter.json`; `32/docket.json` | SUPPORTED | Article no longer describes the two FAC stamps |
| 30 | Candelaria FAC Dkt. 5 filed Aug. 14; Dkt. 6 filed Aug. 17 and is operative; Dkt. 10 identifies Dkt. 6 | `33/matter.json`; `33/docket.json`; `33/events.jsonl` Aug. 14 / Aug. 17 / Aug. 26 | SUPPORTED | |
| 31 | Summonses Aug. 10; sheriff requests Aug. 13 | `33/docket.json` Dkt. 2; `33/events.jsonl` Aug. 10 / Aug. 13 | SUPPORTED | Agency-mail-room service sentence removed from the article |
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
| 42 | Candelaria Dkt. 26 answer to amended complaint filed Oct. 27, 2026 | `33/clocks.json` `33-deadline-7` retired_reason; `33/events.jsonl` Oct. 28 PACER row | GRAPH-ONLY | Article states only that an answer is on file; PDF still not reviewed |
| 43 | Meza Dkt. 22 MTD/strike filed Oct. 26; Dkt. 23 declination same day; responses Nov. 9, replies Nov. 16; Dec. 9 hearing later vacated | `32/docket.json` Dkts. 22–23; `32/clocks.json` `32-deadline-mtd-opposition`, `32-mtd-reply`, `32-mtd-hearing` | SUPPORTED | Article does not characterize MTD grounds (motion PDF not quoted) |
| 44 | Dkt. 25 clerk notice of impending reassignment Oct. 28 vacated magistrate hearing dates | `32/clocks.json` `32-mtd-hearing`, `32-reassignment-watch`; `32/events.jsonl` Oct. 28 | GRAPH-ONLY | Text-only NEF; precursor to Dkt. 29 |
| 44a | Dkt. 29 (Oct. 30, 2026, 2:26 p.m.) directly assigned the case to Judge Charles R. Breyer; Judge Araceli Martinez-Olguin no longer assigned; number 4:26-cv-08271-CRB; all hearing and trial dates vacated; briefing schedules unchanged; motions must be renoticed | `internal/private/content/articles/pilot-meza-gonzalez-candelaria/NEF-Dkt-29-Order-Reassigning-Case-to-Breyer-2026-10-30.pdf` (text-only ECF entry; “No document attached”) | SUPPORTED | Replaces the Oct. 31 user-report row. Prior district judge named on the order is Martinez-Olguin, not Krishnan |
| 45 | Nov. 9 opposition / Nov. 16 reply deadlines unchanged after Dkt. 29 | Dkt. 29 NEF; `32/clocks.json` `32-deadline-mtd-opposition`, `32-mtd-reply` | SUPPORTED | Courtesy-email and missing-opposition sentences removed |
| 46 | Open Candelaria clocks: 26(f)/ADR Nov. 18; CMS/disclosures Dec. 2; CMC Dec. 9, 2026, 10:00 a.m. | `33/clocks.json` `33-deadline-2`, `33-deadline-3`, `33-hearing-4`; index `next_clock` | SUPPORTED | |
| 47 | Dkt. 29 vacates hearing/trial dates; other deadlines unchanged | Dkt. 29 NEF docket text | SUPPORTED | Article no longer cites a Nov. 25 CMS "clock list" |
| 48 | CourtListener slugs listed in the sources table | `01`, `07`, `32`, `33` `matter.json` `courtlistener` | SUPPORTED | |
| 49 | *California DUI Lawyers* / *Knudsen* existence | Standard published reporters; also recited in `07/matter.json` | SUPPORTED as published law | Knudsen opinion confirmed; 101 Cal. App. 5th 186 pinpoint UNVERIFIED |
| 50 | No settlement amounts, sealed files, registry, criminal history, Hertz/HireRight/other non-party employers, or strategy memos appear in ARTICLE.md | This FACT_CHECK; grep of ARTICLE.md | SUPPORTED by exclusion | See RISK_NOTES. Drinking questions, denials, empty can, and the "This is pee" quote are in by user decision |

---

## Narrative claims (Passages A–E)

Exhibit A page numbers are the internal "Page N of 19" stamp. Complaint cites are page:line on the conformed N.D. Cal. FACs. This environment could not re-open `Exhibit_A_CHP_Video_Transcript.pdf` (sha256 `3750927a…1b6660`) or `DMV Decision.pdf` on the public Worker; recording rows below rest on the approved proposal's line-by-line read of that PDF, cross-checked against M-FAC / C-FAC where those papers quote the same lines. The article no longer states that Exhibit A contradicts the FACs.

| # | Claim in ARTICLE.md | Source (timestamp, page, line) | Status | Notes |
|---|---|---|---|---|
| N1 | Nov. 1, 2024, early morning, eastbound I-580, Livermore | Ex. A p. 1 caption; Ex. A 00:54:36 (p. 2) "heading eastbound on I-580" | RECORDING | |
| N2 | Cruiser stopped at 00:55:37; "12:55" | Ex. A 00:55:25, 00:55:37 (p. 2); APS Dec. p. 1 ("on 11/01/2024 at 12:55 AM") | RECORDING / UNVERIFIED | APS page not re-opened here |
| N3 | Dirt shoulder; gray Tesla Model Y | Ex. A 00:55:57 (p. 2, "dirt shoulder"); 01:07:12 (p. 9, "Tesla Model Y"); M-FAC 4:15–16 | RECORDING / ALLEGATION (color) | Rental owner / Hertz excluded |
| N4 | Commercial truck driver was asleep; he says he had stopped to rest | Ex. A 01:01:21 (p. 7); M-FAC 4:15–19 | RECORDING / ALLEGATION | Narrator no longer says he "pulled off the freeway to sleep" |
| N5 | "It's a rental. Huh." before the officers exited | Ex. A 00:55:53; exit at 00:55:57 (p. 2); M-FAC 5:3–4 (¶14) | RECORDING | |
| N6 | Handcuffed approximately sixteen minutes after the cruiser stopped | Ex. A 00:55:37 (stop); 01:11:33 (cuffs, p. 12) | RECORDING | 00:55:37 → 01:11:33 is 15 min 56 sec. Back-seat stamp no longer combined with the cuffing |
| N7 | Suspension began Feb. 20, 2025 (within four months) | APS Dec. p. 1; C-FAC 2:24–3:1 (¶3) | ALLEGATION / UNVERIFIED | Decision date confirmed in C-FAC; APS PDF not re-opened |
| N8 | Alleges suspension ended his work as a driver | C-FAC 4:18–20 (¶6); 27:14–20 (¶79) | ALLEGATION | No employer named |
| N9 | Transcript window 00:54:36–01:57:10, about 62 minutes | Ex. A p. 1 ("Recording Duration: 00:54:36 – 01:57:10") | RECORDING | Article no longer contrasts that window with the FACs' "two hours" |
| N10 | Plaintiff prepared and signed the transcript; speaker IDs and brackets are his | Ex. A p. 1 Certificate of Accuracy; p. 19 Declaration of Authenticity (executed Mar. 21, 2026) | UNVERIFIED | Certificate/declaration pages not re-opened here |
| N11 | Filed as Exhibit A in his cases | Supp. Decl. ¶10 (6:13–15); Ex. A p. 1 caption (E.D. Cal. 2:25-cv-01460); 26CV168913 Reply 5:1 ("Motion, Exh. A") | UNVERIFIED | Face of the PDF does not prove it is the Fickes lodge. See Open flags |
| N12 | Times are the recording's clock; Tesla dash 12:57 a.m. | Ex. A p. 1; Ex. A 00:57:51 (p. 3) | RECORDING | Lodging Decl. is Matter 20 — not cited in the article |
| N13 | Passenger side, flashlights, shining through windows | Ex. A 00:55:57, 00:56:00, 00:56:05 (p. 2) | RECORDING | Bracket "appearing to search the interior" not used |
| N14 | "It wasn't here earlier when we passed by," then "I think it's booze." | Ex. A 00:56:07; 00:56:09 (p. 2); M-FAC 5:5–10 (¶¶14–15) | RECORDING | Quote order corrected to timestamp order |
| N15 | Meza-Gonzalez knocked and kept knocking | Ex. A 00:56:07, 00:56:30 (p. 2) | RECORDING | |
| N16 | "Oh look at this." / "Open the window." at 00:56:40 | Ex. A 00:56:30, 00:56:40 (p. 2) | RECORDING | |
| N17 | At 00:56:43, a plaintiff-authored bracket identifies Melano as opening the passenger door | Ex. A 00:56:43 (p. 2) bracket | RECORDING (bracket) | Qualified as the plaintiff's description. Native video not reviewed |
| N18 | Melano: "Hello." Newanforbi: "Uh-huh." "Are you okay?" "Yeah, we good." | Ex. A 00:56:46–00:56:48 (p. 2) | RECORDING | Speakers now attributed |
| N19 | "We're coming from uh, uh, a party." | Ex. A 00:57:05–00:57:11 (pp. 2–3) | RECORDING | |
| N20 | "This is not a parking lot."; dash 12:57 a.m.; "like 5-7 minutes" | Ex. A 00:57:46, 00:57:51, 00:58:06 (p. 3) | RECORDING | |
| N21 | "How much have you had to drink…" / "Zero." | Ex. A 00:58:30–00:58:36 (p. 3) | RECORDING | Kept by user decision |
| N22 | "What's in that cup right there?" / "Don't drink it. Yeah don't drink it," spoken by Newanforbi | Ex. A 00:58:34, 00:58:46 (p. 3) | RECORDING | Both lines attributed to Newanforbi |
| N23 | Melano cup quotes, including "This is pee." | Ex. A 00:58:49–00:58:59 (p. 3); M-FAC 5:28–6:4 | RECORDING | Kept verbatim |
| N24 | Meza-Gonzalez: "No I'm not gonna smell that." | Ex. A 00:58:59 bracket (p. 3); 00:59:02 (p. 4) | RECORDING | |
| N25 | "OK. Leave it there. Put it back." Step-out at 00:59:12 | Ex. A 00:59:07, 00:59:12 (p. 4) | RECORDING | |
| N26 | Walked to patrol car; spelled "NEW-WAN-FOR-BI" | Ex. A 00:59:40, 00:59:53, 00:59:57 (p. 4) | RECORDING | |
| N27 | Bracketed description: Melano opened a rear passenger door during the escort, then appeared with an empty can | Ex. A 00:59:46 bracket (p. 5); 01:00:06 (p. 5) | RECORDING (bracket) | Article no longer independently calls it a "search" |
| N28 | Empty can; "Did you drink that?" "No."; "You haven't drank anything since you've been parked?" "No." | Ex. A 01:00:06–01:00:14 (p. 5) | RECORDING | KEEP the can and denials. Article does not contrast the timestamp with the Alameda pleading. Brand at 01:00:09 withheld |
| N29 | "Right now, Livermore."; sign "Isabella Avenue, Portola Avenue"; "Correct." | Ex. A 01:00:40–01:00:46 (pp. 5–6); bracket at 01:00:44 ("about 50 yards away") | RECORDING | |
| N30 | During questioning about his presence in the vehicle, "I was in the driver's seat, yes sir." | Ex. A 01:03:47–01:03:50 (p. 8) | RECORDING | Officer's exact question not recovered in this pass. Article does not paraphrase it as "asked whether he had been driving" |
| N31 | Truck-driver fatigue explanation (verbatim, with ellipsis) | Ex. A 01:01:16–01:01:21 (pp. 6–7) | RECORDING | |
| N32 | Exhibit A attributes eye and time-estimation test instructions to Meza-Gonzalez | Ex. A 01:05:22–01:07:04 (p. 9); 01:07:42–01:08:45 (p. 10) | RECORDING | Speaker IDs not confirmed against native video. Article does not announce a conflict with M-FAC ¶53 |
| N33 | "It seems as though I'm passing them…I just wanna know if I've passed your test." | Ex. A 01:08:58, 01:09:14, 01:09:23 (p. 10) | RECORDING | |
| N34 | Melano: "Yeah there's not pass or fail." Meza-Gonzalez: "I go through all of them regardless…" | Ex. A 01:09:52 (p. 10); 01:09:58 (p. 11) | RECORDING | Contradicts Ala. Compl. 6:3–5 (attributes the remark to Meza-Gonzalez at 01:08:20–40) |
| N35 | Balance doubt on one knee; "It's fine if you don't. You don't have to." | Ex. A 01:09:20 (p. 10); 01:10:12 (p. 11) | RECORDING | Article now uses "knee" |
| N36 | "I mean I think we can do that." / "It's kind of sketch here bro." / "uneven ground. I wouldn't do that one." / "Alright then." | Ex. A 01:10:14–01:10:30 (p. 11) | RECORDING | |
| N37 | PAS request at 01:10:33; "You may refuse to take this test" | Ex. A 01:10:33 (p. 12) | RECORDING | |
| N38 | Required/not required exchange; "up to my discretion whether I put you under arrest for DUI or not" | Ex. A 01:10:51–01:11:03 (p. 12); M-FAC 7:2–5 (¶22) | RECORDING | |
| N39 | "Yes or no?"; "I don't consent to that." at 01:11:15 | Ex. A 01:11:11 bracket, 01:11:13, 01:11:15 (p. 12) | RECORDING | |
| N40 | "OK. Brendan. Alright then. I'm gonna have you just turn around please…" at 01:11:16; cuffs by 01:11:33 | Ex. A 01:11:16, 01:11:31, 01:11:33 (p. 12); M-FAC 7:11–13 (¶24) | RECORDING | |
| N41 | Search of person; back seat; cuffs attached to vehicle frame | Ex. A 01:12:54 (p. 12); 01:13:14 (p. 13); 01:15:06 bracket (p. 13) | RECORDING (bracket on frame) | |
| N42 | Breath-or-blood question; "I don't know. It seems like torture." | Ex. A 01:15:54, 01:16:04, 01:16:19 (p. 13) | RECORDING | |
| N43 | "Right now you're not refusing…don't want to choose"; one-year-at-least admonition, even if sober | Ex. A 01:16:37, 01:16:59 (p. 14); 01:19:18 bracket; 01:20:49 (p. 14) | RECORDING | Scare quotes removed from the paraphrase |
| N44 | "Even as a truck commercial driver…force the DMV's hand?" / "I'm not forcing the DMV to do it, that's their rule." | Ex. A 01:21:41, 01:21:50 (p. 14) | RECORDING | |
| N45 | Exhibit A transcribes no audible response between "So you're refusing to take a test?" and "OK." | Ex. A 01:22:15, 01:22:21 (p. 15) | UNVERIFIED | Qualified as transcript silence |
| N46 | "We just have to write what time we last passed him…" / "But he said he was here for seven minutes." / "you want to start your warrant?" | Ex. A 01:23:11, 01:23:16, 01:23:33 (p. 15) | RECORDING | 01:23:20 omitted (supervision status — excluded) |
| N47 | Implied-consent advisement at 01:36:47; Miranda exchange; "We already have everything we need right?" | Ex. A 01:36:47–01:37:08, 01:37:45 (p. 16) | RECORDING | |
| N48 | Implied-consent / warrant lines at 01:36:47 ff.; "OK so we're getting a warrant" | Ex. A 01:36:47–01:38:10 (pp. 16–17) | RECORDING | "Neither?" / "Yep." deleted from the article |
| N49 | Alternator exchange; "I don't think electric vehicles have alternators" / "Just like your phone gets charged." | Ex. A 01:44:21–01:45:01 (p. 17) | RECORDING | |
| N50 | Left at 01:52:05; arrived at 01:57:10, "Dublin CHP transfer" | Ex. A 01:52:05, 01:57:10 brackets (p. 18) | RECORDING (bracket) | Bracket also says "Santa Rita Jail"; article uses only "Dublin CHP transfer" |
| N51 | Officer's account as quoted and characterized in the Candelaria complaint | C-FAC quotations of APS Dec.; APS Dec. not re-opened | ALLEGATION / UNVERIFIED | Article no longer presents the decision's contents as independently verified |
| N52 | DS-367 and arrest report signed under penalty of perjury; used for warrant, APS, DA referral | M-FAC 2:11–15 (¶2); 7:18–21 (¶25) | ALLEGATION | |
| N53 | Four entries the complaint alleges are unsupported, including "Beverage Present: Yes," which the complaint disputes | M-FAC 7:23–8:15 (¶26(a)–(d)); C-FAC 12:2–20 (¶29) | ALLEGATION | Narrator no longer vouches that the recording "does not support" the entries. Empty can remains in the transcript section |
| N54 | Complaint acknowledges odor, speech, and orientation are "experiential observations"; alleges the recording is inconsistent with those entries | M-FAC 8:22–27 (¶28) | ALLEGATION | "Concedes" removed |
| N55 | The complaint alleges that a magistrate issued the warrant and that blood was drawn at the CHP Dublin Area office | M-FAC 9:3–5 (¶29) | ALLEGATION | Both facts attributed to the complaint |
| N56 | MTD Dkt. 22 pending; no admission | ARTICLE current-status; FACT_CHECK row 43 | SUPPORTED | |
| N57 | Temporary license "through the outcome of hearing," barring "driving commercially" | C-FAC 16:12–18 (¶42) (quoting DS 2030/2030A) | ALLEGATION | Forms themselves not opened |
| N58 | Dec. 9, 2024 five-page response; certificate and transcript offered | C-FAC 17:6–15 (¶45); 17:17–20 (¶46) | ALLEGATION | |
| N59 | "The Hearing Officer will develop the facts and render a final decision on your matter." | C-FAC 16:25–28 (¶44); 3:14–15 (quoting Form DS 2304) | ALLEGATION | Form itself not opened |
| N60 | Teams, 9:00 a.m., Jan. 24, 2025; testified under penalty of perjury | C-FAC 16:16–18 (¶42); 18:4–7 (¶48); APS Dec. p. 1 | ALLEGATION / UNVERIFIED | Hearing time confirmed in C-FAC; APS PDF not re-opened |
| N61 | Marshaled/offered exhibits, ruled on objections, decided; "from neutral fact development into advocacy" | C-FAC 22:25–23:4 (¶65); 18:18–23 (¶50) | ALLEGATION | Confirmed on C-FAC Worker text |
| N62 | As quoted in the Candelaria complaint, the decision states: "It is presumed official duty has been regularly performed. No evidence was presented to the contrary." | C-FAC 22:9–13 (¶63) | ALLEGATION | "Because" causal reading removed. APS PDF not re-opened |
| N63 | Complaint alleges the written decision failed to address the Detention Certificate and the recording discrepancies the plaintiff identified | C-FAC 19:27–20:3 (¶55) | ALLEGATION | Absolute "does not mention" removed |
| N64 | Suspension Feb. 20, 2025 – Feb. 19, 2026 | C-FAC 2:24–3:1 (¶3); APS Dec. p. 1 | ALLEGATION | C-FAC confirmed |
| N65 | Dkt. 26 answer filed; not ingested | ARTICLE.md; FACT_CHECK row 42 | GRAPH-ONLY | |
| N66 | Two federal judges (Breyer; Lin) | Dkt. 29 NEF; `33/matter.json` | SUPPORTED | |
| N67 | Complaints allege a Detention Certificate dated Nov. 5, 2024; date and contents not independently verified | M-FAC 9:26 (¶32); C-FAC 2:14–17 (¶2) | ALLEGATION | Article now says the certificate was not independently verified. Ala. Compl. May 12 date is not used |
| N68 | State is not a defendant in live Meza | `32/parties.json`; M-FAC caption | SUPPORTED | |
| N69 | After Dkt. 23/25, Judge Martinez-Olguin was the assigned district judge; Dkt. 29 reassigned to Judge Breyer | Dkt. 25; Dkt. 29 NEF ("Judge Araceli Martinez-Olguin no longer assigned") | SUPPORTED | Article now states the missing assignment step. Dkt. assigning her was not separately pulled |

---

## Gaps (what the article does not claim, and why)

| Gap | Why |
|---|---|
| Grounds of Dkt. 22 (Meza MTD/strike) | PDF is on disk; this draft does not quote defense arguments |
| Text of Dkt. 24 (Candelaria strike order) | PDF is on disk; `pdftotext` / pypdf were unavailable in this environment. Substance taken from `clocks.json` / events |
| Matter 32 graph still lists `-ASK` / Krishnan | Dkt. 29 NEF is the controlling clerk record. The article uses `4:26-cv-08271-CRB`. Updating `32/matter.json` is outside this draft task |
| Text of Dkt. 26 | Answer PDF not ingested as of Oct. 28. Dkt. 25 remains a text-only clerk notice (impending reassignment) |
| E.D. Cal. Candelaria F&R (June 15, 2026) wording | Identity files summarize Mag. Kim’s recommendation (IFP denial / dismissal). Article states that an F&R issued and was mooted; it does not quote it |
| Alameda stay-stipulation PDF | Events and `prose.json` record the Apr. 14, 2026 filing; the stipulation PDF was not re-read here |
| Exact E.D. Cal. Candelaria initiation date | Identity says Apr. 27, 2026; jurisdictions catalog says the dismissal paper recites Mar. 19, 2026. Article flags both |
| Whether default was entered on Meza Dkt. 17 | A Rule 55(a) request was filed Sep. 18; defendants later appeared by Dkt. 22. Article does not discuss default |
| Blood-alcohol number, medical condition, vehicle owner, employer, wage rates | Present in some `key_facts` fields; excluded as unnecessary or as non-party employer / medical detail |
| Any dollar demand, SR-22 premium, or settlement figure | Hard exclusion |
| Can brand / "source alcohol" at Ex. A 01:00:09 | Alcohol-product exclusion. The empty can itself is in |
| Orange 21-and-over wristband (APS Dec. p. 2) | Alcohol-detail exclusion |
| Toxicology / blood-test results | None in the reviewed papers; excluded if they appear later |
| "Still asleep" at the door opening (M-FAC ¶¶16, 56) | Not used. Article does not announce a conflict with the FAC |
| Locked-door allegation (Ala. Compl. 4:27–5:3) | Ex. A is silent on a lock |
| Cup-explanation allegation (Ala. Compl. 5:14–16) | Ex. A records only "Don't drink it" and "I don't know what that is" |
| "Neither?" / "Yep." chemical-test exchange | Deleted as a refusal concession |
| Claim-splitting / Rule 41 / courtesy-email / abandoned-writ sentences | Deleted as pending-case risk |
| Badge numbers; officers' names in title, H1, and JSON-LD headline | Removed |

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
14. **Docket drift.** Matter 32 is 4:26-cv-08271-CRB before Judge Breyer (Dkt. 29). Hearing/trial dates are vacated; Dkt. 22 must be renoticed; briefing dates unchanged. The Oct. 28 graph row is stale (`-ASK` / Krishnan). Matter 33 stays with Judge Lin; clocks run in November–December 2026.
15. **No GitHub / document-store URLs** in any outbound version (standing lock). Internal `/documents/...` paths in the sources table are for editors, not for a public page.
16. **Crude transcript language.** Melano's "piss" / "This is pee" lines are now in the article by express user decision (P14 KEEP). Do not expand into other excluded audio (registry, medical, brand).
17. **Exhibit A is the plaintiff's transcription.** Speaker labels and bracketed actions are his. Native video was not replayed in this pass.

---

## Open verification flags

These are not article deletions. They are the items still unverified after this integration.

1. **Native video not reviewed.** Every recording-based detail rests on Plaintiff's Exhibit A. Spot-check 00:55:50–00:57:05, 00:59:40–01:00:20, 01:11:10–01:11:40, and 01:22:00–01:22:30 before publication. The silence after "So you're refusing to take a test?" (N45) is transcript silence.
2. **Exhibit A PDF not re-opened in this environment.** Public Worker returned 404 for sha256 `3750927a…1b6660`. Citations follow the approved proposal's read of that file, cross-checked against M-FAC quotes.
3. **Fickes-lodge identity.** The repo copy is captioned E.D. Cal. 2:25-cv-01460 and declared March 21, 2026. The Alameda U-visa Motion with its Exhibit A is not in the repo. Dialogue matches the June 18, 2026 alternate copy line for line. Pull the file-stamped 26CV168913 Motion Exhibit A to confirm the hash.
4. **APS Decision PDF not re-opened** (sha256 `2bdd43b6…aac90c8`, Worker 404). Officer-account quotes in Passage C and the presumption sentence in Passage D are from the proposal's read plus C-FAC.
5. **DS-367 and arrest report not read directly.** The four contested entries are quoted as M-FAC pleads them. Supp. Decl. / Ala. Compl. / APS Dec. have small odor-quote variances.
6. **Detention Certificate itself not reviewed.** Article uses November 5, 2024 (M-FAC 9:26; C-FAC 2:14–17). Ala. Compl. 3:7–9 says May 12, 2025.
7. **Blood-draw location and booking.** Passage C attributes the Dublin Area office to the complaint. Passage B ends at "Dublin CHP transfer." Warrant and booking records not reviewed.
8. **"Joselyn Melano"** in the Ex. A 00:56:43 bracket — treated as a typo.
9. **DMV forms DS 2030A and DS 2304** quoted from C-FAC, not from the forms.
10. **Dkt. 22, Dkt. 23, and Dkt. 26** not read for a competing door-opening or odor account.
11. **Matter 32 graph** still lists `-ASK` / Krishnan as of Oct. 28.

---

## Exclusion scan (ARTICLE.md)

| Term | In ARTICLE.md? |
|---|---|
| Settlement / offer / $50,000 / $250,000 / walk-away | No |
| Parole / hold / CDCR / registry / Megan / PC 290 | No |
| Hertz / HireRight / Centerline / PV Holding / Accurate / Amazon / FedEx / UPS | No |
| U-visa / I-918 / immigration court | No |
| Home address / phone / email | No |
| GitHub / raw.githubusercontent | No (sources-table warning only) |
| Immunity prediction / “will win” / “should lose” | No |
| Mike's / brand of the empty can / 21+ wristband / BAC figure | No |
| Melano "This is pee" / drinking questions / denials / empty can | Yes — kept by user decision |
| Officers' names in title / H1 / JSON-LD headline | No |
| Badge numbers | No |
| "Neither?" / "Yep." | No |
