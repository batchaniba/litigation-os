# Matter 28 — Discovery Planning Scaffold

Starter grid only. Every "fact to prove" comes from `matter.json` key_facts (complaint
allegations), Dkt 28 (Joint CMS), or Plaintiff's Oct 14 initial disclosures. Nothing here is
a finding. Labels: **ALLEGED** (complaint/matter.json), **HELD** (evidence in Plaintiff's
possession), **NEEDED** (gap), **QUESTION**. Do not quote HOPE_000 content in anything
filed or sent until the stipulated PO is entered (or the San Joaquin PO otherwise permits it).

## 1. Timing gates

| Gate | Status | Basis |
|---|---|---|
| Discovery open? | **Yes, formally.** FRCP 26(d)(1) bars discovery only before the Rule 26(f) conference; the parties held it Sep 29, 2026 (Dkt 28 p.4). No stay order is in the repo; a pending Rule 12(b)(6) motion does not stay discovery by itself. QUESTION: confirm Judge Cisneros's standing order has no different rule. | Dkt 28; FRCP 26(d)(1) |
| Response clock | 30 days for RFP/ROG/RFA (FRCP 33(b)(2), 34(b)(2)(A), 36(a)(3)); FRCP 6(d) adds 3 days only for mail / clerk / Rule 5(b)(2)(F) service, not electronic service. Requests served Oct 16 by email → responses due Nov 16 (Nov 15 is a Sunday). | FRCP |
| Protective order | **[Proposed] Stipulated PO filed Oct 14, 2026; not yet entered.** Defendants will withhold confidential material until entry (Martinez, Oct 13). Plaintiff's disclosures say he will produce HOPE_000001–542 only after an order/agreement authorizes it. | Gmail Oct 13–14; Dkt 28; initial disclosures |
| Nov 13, 2026 re-production | **Plaintiff's *proposed* schedule only** ("Prior Discovery Re-Production or Authorization: Completed by November 13, 2026", Dkt 28 p.6). Not court-ordered; not in clocks.json. Becomes real only if the Court adopts it at the Oct 27 CMC. | Dkt 28 |
| Oct 27 CMC | Court sets the schedule. Defendants proposed fact cutoff May 1, 2027 / trial July 10, 2028; Plaintiff proposed Jan 29, 2027 / June 14, 2027. | Dkt 28; Dkt 29 |
| Rule 26(a)(1) | Plaintiff served Oct 14. Defendants due Oct 15. | Dkt 28 |
| Limits | 25 ROGs per party (FRCP 33(a)(1)); 10 depositions (FRCP 30(a)(2)(A)(i)); no RFA cap in FRCP. Check N.D. Cal. Civ. L.R. 26–37 and standing order before serving. | FRCP |

## 2. Claims → facts → evidence → discovery

### Count 1 — § 1983 Monell (HOPE) and Count 2 — § 1983 individual (Smith)

| Fact to prove | Held | Needed | Candidate discovery |
|---|---|---|---|
| HOPE acts under color of state law (CDCR vendor agreement, CASOMB certification) — ALLEGED | Research memos (`/documents/matter-28/research/`); Title 15 § 3574; NCR 25-01 | CDCR–HOPE contract(s), amendments, SOWs | RFP: all CDCR/DAPO contracts & amendments 20XX–present. Subpoena: CDCR (contract file). RFA: HOPE contracts with CDCR to provide SOMP treatment to parolees. |
| Blanket policy: no graduation before parole term ends — ALLEGED | HOPE_000225–349 Clinical Operational Manual; HOPE_000486–537 treatment manual; HOPE_000350–434 Maintenance Curriculum; HOPE_000224 audit; Matter 5 RFA 4/18 admissions | Completion/discharge criteria actually applied; statistics of completions before term end | ROG: identify every client who completed treatment before end of parole (count by year). RFP: discharge/completion policies, revisions, communications re policy. RFA: no written criterion permits completion before end of parole term (only if supported by manual — verify). 30(b)(6) topics: completion policy. |
| Smith personally directed policy / retaliatory reporting — ALLEGED | HOPE_000538–542 Clinical Director job description; HOPE_000139–199 collateral notes/comms | Smith's emails/directives; org chart | RFP: Smith communications re Plaintiff, completion policy, parole reporting. ROG: persons who decided Plaintiff's status reports. Deposition: Smith; Palacios. |
| False no-shows / adverse CDCR Form 3043 reports — ALLEGED (HOPE_000142, HOPE_000194 cited in matter.json) | HOPE_000139–199; HOPE_000105–138 and 200–223 homework | Attendance logs, telehealth logs (tech-error evidence), all 3043s sent | RFP: attendance & platform logs for Plaintiff; all Forms 3043/treatment reports sent to CDCR re Plaintiff. Subpoena: CDCR/DAPO parole file, agent notes re HOPE reports. RFA: genuineness of specific reports (FRCP 36(a)(1)(B)). |
| Causation / damages (lost CDL earnings) — ALLEGED | W-2s 2022–2024 (per matter.json); CDCR Form 1502-DR (Nov 14/19, 2025, per disclosures) | Proof that HOPE reports drove parole conditions | Subpoena: DAPO records of decisions citing HOPE reports. ROG: HOPE's contention re causation. |

### Count 3 — Bane Act (Civ. Code § 52.1)

| Fact | Held | Needed | Candidate discovery |
|---|---|---|---|
| Interference with rights by threat/intimidation/coercion — ALLEGED | Collateral notes; opposition brief | Specific communications threatening adverse reports | RFP: communications with Plaintiff and parole agents re non-compliance/reporting. ROG: each adverse report and its basis. |

### Count 4 — Fraud / negligent misrepresentation

| Fact | Held | Needed | Candidate discovery |
|---|---|---|---|
| Misrepresentations (to Plaintiff and/or CDCR) re treatment/progress — ALLEGED | Homework records; audit (HOPE_000224) | Representations made, to whom, when; reliance | ROG: identify statements made re Plaintiff's progress. RFA: specific statements (after reviewing text). |

### Count 5 — RICO § 1962(c)–(d)

| Fact | Held | Needed | Candidate discovery |
|---|---|---|---|
| Enterprise, billing to CDCR at listed rates (group $100, individual $200, polygraph $500, psych eval $1,800, etc.) — ALLEGED | Matter 28 research memos (`/documents/matter-28/research/`); insurance policies HOPE_000001–104 | Invoices/billing to CDCR for Plaintiff; rate sheets; revenue per parolee | RFP: all invoices to CDCR for Plaintiff's services; rate schedules. Subpoena: CDCR accounting/payments to HOPE. ROG: total billed for Plaintiff by service type. |
| Predicate acts (mail/wire fraud via billing and false reports) — ALLEGED | — | Transmission records | RFP: billing submission method/records. |
| Insurance (Rule 26(a)(1)(A)(iv)) | HOPE_000001–104 | Current policies for 2026 suit; reservation-of-rights | Confirm in Defendants' initial disclosures; RFP if absent. |

## 3. Immediate high-leverage moves (scaffold — Plaintiff decides)

1. Calendar the Oct 27 CMC asks: adopt Nov 13 authorization/re-production date; enter the stipulated PO.
2. Prepare RFP Set One (contracts, billing, completion policy, Plaintiff's full client file, Smith comms) for service now that discovery is open.
3. Prepare targeted RFAs on authenticity of HOPE_000001–542 (saves re-authentication) once PO is entered.
4. Draft CDCR/DAPO Rule 45 subpoena (parole file, Form 3043s, contract/payment records) — QUESTION: whether a CDCR Form 7385 records request is already pending (not catalogued in the repo).
5. Watch Defendants' Oct 15 disclosures; deficiency letter if confidential material is withheld without a timetable.

## 4. Open questions

- Is the San Joaquin PO's use restriction lifted by the federal stipulated PO, or is a separate stipulation needed? (Dkt 28 "Other" section.)
- Exact Dkt numbers 16–27 and whether any discovery-related order exists.
- Whether Defendants' Dkt 30 reply raises preclusion (Matter 5 demurrer) that affects discovery scope.
