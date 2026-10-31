# Matter 29 — Accurate discovery analysis workspace

**Newanforbi v. Amazon.com Services LLC & Accurate Background LLC**  
N.D. Cal. **4:26-cv-09249-ASK** (Hon. Ajay S. Krishnan, U.S. Magistrate Judge, Oakland; all-consent case).  
Removed from Alameda Superior Court **26CV201554** (filed July 28, 2026; both defendants served July 31; removed August 31).

This folder is a self-contained room for further pointed analysis of Accurate Background discovery. It is meant to be read by an outside LLM pointed at this GitHub branch. Private working analysis. Nothing here has been filed, served, or adopted by the Court.

**Start here**

1. [`00-ANALYSIS.md`](00-ANALYSIS.md) — foundation analysis (Oct. 31, 2026), kept verbatim.
2. [`INDEX.md`](INDEX.md) — full file map with relative links and suggested follow-up questions.
3. [`sources/`](sources/) — new source files (served Accurate RFP Set One; Oct. 28 closing letter; Oct. 27 file-disclosure text).
4. [`extracts/`](extracts/) — pdftotext helpers for a few key repo PDFs that lacked sidecars.

Live calendar truth is [`clocks.json`](../../../src/data/matters/29/clocks.json), not this README.

## How an outside model should work this room

Read in this order unless the prompt names a narrower task:

1. This README (identity, posture, rules).
2. `00-ANALYSIS.md` (the working thesis).
3. `sources/RFP_Accurate_Set1.txt` and `sources/Closing_Letter_1028.txt`.
4. `sources/Accurate_File_Disclosure_Oct27.txt` (202-page file; search, do not dump).
5. The linked pleading texts in [`INDEX.md`](INDEX.md) (complaint via Dkt. 2 extract; Accurate Answer Dkt. 21; Amazon MTD Dkt. 19).
6. Only then the comparator dockets (*Varela*, *Santee*, *Rangel*, *Lerma*) and the existing discovery-set drafts.

Prefer the `.txt` / `.md` sidecar over the PDF. The PDF controls if they conflict. Do not invent a docket number. If `dkt` is null, say so.

## What this case is

Plaintiff applied in early July 2026 for Seasonal XL Warehouse Associate at Amazon's Fremont fulfillment center (44051 Osgood Rd.). Conditional offer July 3. Accurate Background (shortcode 45996; order **Y94611404** / ref **496623722**) began screening July 7. The assigned July 28 training shift disappeared from Simple Hire on July 27 while the background check was still "Pending." No formal adverse-action notice is in the ingested file.

The operative complaint (Alameda filing, Exhibit 1 to Dkt. 2) pleads seven counts against Amazon and Accurate: (1) Cal. Penal Code § 290.46(j); (2) Fair Chance Act, Gov. Code § 12952; (3) FCRA; (4) ICRAA; (5) invasion of privacy; (6) UCL § 17200; (7) IIED.

Against Accurate, the pleaded FCRA theory is **§ 1681b(b)(1)** (furnishing without employer certification) plus **§ 1681n** willfulness. **Not pleaded:** §§ 1681e(b), 1681i, 1681g, 1681k. No CCRAA count.

Accurate answered (Dkt. 21, Sept. 22) with twelve defenses. Amazon moved to dismiss only Claims 5–7 (Dkt. 19). Claims 1–4 are live as to both defendants.

Oct. 14, 2026: Accurate issued a completed consumer report that included a **NEWANSORBI** alias (labeled "Provided by Applicant") and a National Sex Offender Database Search result of **NO RECORD FOUND**. Plaintiff disputed both and requested the complete file. Oct. 28: Accurate closed the reinvestigation, removed the alias, confirmed no reported sex-offender information, and said it sent an amended report to Amazon. Oct. 30: Seyfarth transmitted a 202-page file disclosure dated Oct. 27. The cover says Accurate **received a request** for Amazon on July 7, 2026. That sentence is the order date, not proof the report was furnished that day. The original 34 MB PDF is in Plaintiff's Gmail from Seyfarth (Oct. 30, 2026); only the text extract is in this room. The text extract includes an October 28 letter near the end. Whether the PDF bytes do is unchecked.

## Posture and key dates

From live [`clocks.json`](../../../src/data/matters/29/clocks.json) and Dkt. 9. Vacated clocks are not live.

| Date | Event | Status |
|---|---|---|
| Fri. Nov. 6, 2026, 1:00–1:30 p.m. PT | Rule 26(f) / ADR L.R. 3-5 conference (Teams): Brown & Frederick (Morgan Lewis / Amazon); Drury & Stanzick (Seyfarth / Accurate) | open |
| Mon. Nov. 10 | ADR certification (Dkt. 9). The Nov. 6 call satisfies the meet-and-confer piece | open |
| Fri. Nov. 13 | Optional last day to request Zoom for the Nov. 18 MTD (Krishnan standing order: law-and-motion is in person; 3 business days + good cause) | contingent |
| Wed. Nov. 18, 1:30 p.m. PT | Hearing on Amazon Dkt. 19 MTD (Claims 5–7), Courtroom 4, 3rd Floor, Oakland | open |
| Mon. Nov. 24 | Initial disclosures (Rule 26(a)(1)) and Joint CMC Statement | open |
| Sat. Nov. 28 | Watch: Amazon CCPA request-to-know response (45 days from the Oct. 14 letter) | open |
| Tue. Dec. 1, 1:30 p.m. PT | Initial CMC by Zoom (`cand.uscourts.gov/ask`) | open |
| ~Mon. Dec. 7 | Illustrative Accurate RFP Set One response date if deemed served Nov. 6 (Dec. 9–10 if a 3-day mail add applies) | not a stored clock |

No scheduling order, fact cutoff, or protective order yet. Early Rule 34 is the only formal discovery now pending. Interrogatories and RFAs wait until after Nov. 6.

The as-of-right amendment window closed Oct. 13. Further amendment is Rule 15(a)(2) (leave or stipulation). Krishnan requires a redline against the last pleading.

## Counsel

| Party | Firm | Appearances in this file |
|---|---|---|
| Plaintiff | In propria persona | Brendan Ngwa Nforbi |
| Amazon.com Services, LLC | Morgan, Lewis & Bockius LLP | Andrew P. Frederick, Douglass G. Brown, Suga A. Ikeda |
| Accurate Background, LLC | Seyfarth Shaw LLP | Jasmine J. Stanzick, John Drury |

Two-desk research (do not email counsel about it; not Civil L.R. 3-12 related cases): [`internal/docs/counsel/frederick-stanzick/`](../../../docs/counsel/frederick-stanzick/).

## Working rules for this room

- Keep allegations, evidence, judicial findings, and proposed drafts distinct. Label **FACT**, **INFERENCE**, **UNVERIFIED**, **QUESTION**, **MISSING**.
- Never invent a docket number. Plaintiff's opposition to Dkt. 19 has **no ingested ECF number**.
- Live calendar: `internal/src/data/matters/29/clocks.json`. Do not rebuild dates from README prose.
- **Do not include, quote, or compute settlement figures, walk-aways, or ledger contents.** Skip demand letters, Rule 68 papers, and negotiation files. If a comparator docket mentions a settlement, say that it settled and stop.
- Never write that Amazon settled the identical § 290.46 claim. *Lerma* Dkt. 36 dismissed that theory; the later settlement was on the surviving Fair Chance Act claim against Amazon.
- Do not put GitHub or repo URLs in anything Plaintiff would send or file.
- This directory stays under `internal/private/`. Do not register it in the public SPA, Worker/D1, or R2 merely because it was collected here.
- A research revision is not user approval, operative status, or filing readiness.

## Missing from the repo (do not invent)

- The original **202-page / ~34 MB Oct. 27 file-disclosure PDF**. Text extract is in `sources/Accurate_File_Disclosure_Oct27.txt`. Original: Plaintiff's Gmail from Seyfarth, Oct. 30, 2026.
- The Oct. 14 **preservation letters** to Amazon (Morgan Lewis) and Accurate (Seyfarth). Calendar and clocks treat them as sent that afternoon; the letter PDFs are not ingested. Do not reconstruct their text.
- Krishnan Civil Standing Order PDF (Aug. 20, 2026). Court URL: `https://cand.uscourts.gov/sites/default/files/standing-orders/ASK-CivilStandingOrder_8.20.26.pdf`. Dossier: [`ajay-s-krishnan-2026.md`](../../../docs/legal-intel/judges/ajay-s-krishnan-2026.md). Dkt. 10 is only the proof of service.
- Standalone as-filed complaint PDF (`Complaint for Damages - AS FILED…`). The complaint text is Exhibit 1 to Dkt. 2; helper extract: [`extracts/Dkt_02_Removal_Exhibits.txt`](extracts/Dkt_02_Removal_Exhibits.txt).

## Sibling rooms (read after this one)

| Room | Role |
|---|---|
| [`../matter-29/`](../matter-29/) | Broader Oct. 28 research room (26(f) prep, claims matrix, reinvestigation analysis). Historical snapshots; some dates are stale. |
| [`../../../docs/matter-29/discovery-set-one/`](../../../docs/matter-29/discovery-set-one/) | Oct. 19 draft packet (Amazon RFPs, Accurate RFPs, ROGs, RFAs, ESI proposal). The **served** Accurate RFP PDF is `sources/RFP_Accurate_Set1.pdf`. |

## Suggested first prompts

Copy a question from [`INDEX.md` § Questions for further analysis](INDEX.md#questions-for-further-analysis). Typical first asks: strengthen RFPs 8 / 16 / 19; draft RFP Set Two; ROGs and RFAs after Nov. 6; Rule 15 amendment theories; Rule 45 subpoenas to Tauxbe / InformData-SJV / Infinity Court Research; the Nov. 6 26(f) agenda; willfulness / punitive discovery that does not recite settlement numbers.


## Independent critical review and proposed next wave (Oct. 31)

Three private reviews, none served or filed. The consolidated plan is [`SYNTHESIS-3-MODEL.md`](SYNTHESIS-3-MODEL.md). Where a review and the synthesis differ, follow the synthesis.

| Review | Start here |
|---|---|
| Foundation (unchanged) | [`00-ANALYSIS.md`](00-ANALYSIS.md) |
| ChatGPT | [`review-2026-10-31/00-START-HERE.md`](review-2026-10-31/00-START-HERE.md) |
| Claude (uploaded work product, copied in) | [`claude-review-2026-10-31/claude-work-response.md`](claude-review-2026-10-31/claude-work-response.md) |
| Grok (written before the other two were opened) | [`grok-review-2026-10-31/00-START-HERE.md`](grok-review-2026-10-31/00-START-HERE.md) |
| **Consolidated plan** | [`SYNTHESIS-3-MODEL.md`](SYNTHESIS-3-MODEL.md) |

ChatGPT's package re-rates all twenty RFPs, with supplemental RFPs 21–44, twenty-two interrogatories, thirty-six RFAs, a Rule 15 analysis, vendor subpoenas, and a timed Rule 26(f) agenda. Some authentication RFAs require the absent original disclosure PDF before service. The synthesis narrows Set Two to requests 21–33, holds a duplicate ICRAA accuracy count because of Civil Code § 1786.52(a), and treats "did not re-run" as an inference rather than a fact.
