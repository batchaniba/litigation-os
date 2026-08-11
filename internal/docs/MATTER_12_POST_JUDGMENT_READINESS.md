# Matter 12 — Post-Judgment Document Readiness

**Question presented:** The Aug. 12, 2026 hand-up default judgment packets for
Diamond Truck Sales, Inc. and Alpine Truck Sales, Inc. are finished. What is the
status of everything that has to follow — once default is officially entered — in
*Ngwa Nforbi v. Diamond Truck Sales, Inc. et al.*, No. STK-CV-UF-2026-0001094
(San Joaquin Sup. Ct.)?

**Short answer: the enforcement set is drafted but not usable, and the premise it
sits on is not yet true.** Nine post-judgment documents exist as drafts, four more
do not exist at all, and none of the drafts can be lodged as written. Two of the
defects are substantive rather than clerical: the Writ of Execution is directed to
**San Joaquin County**, while every asset identified in this matter is in
**Stanislaus County**, and one debtor-examination order was prepared for two
judgment debtors. Separately — and this is the item that outranks all of the
above — **the docket shows no default entered against either defendant.** The
June 15, 2026 CIV-100 was docketed *Not Entered*, the clerk rejected the renewed
packet on July 30, 2026, and the Aug. 12 setting is still calendared as a Case
Management Conference. Every document below is gated on two events, not one:
entry of default, then entry of default judgment.

**This memo is portfolio analysis of the record in this repository, not legal
advice.** The form-completeness findings are mechanical and reliable — they come
from reading the AcroForm field values in the PDFs. The statutory conclusions
should be confirmed against the current docket and, where possible, with counsel
before anything is lodged.

---

## 1. The gate: nothing has been entered yet

### 1.1 What the register of actions actually shows

The FullCourt ROA summary in this repository (`FullCourt Enterprise - Civil ROA
Summary (as of Aug 2 2026).pdf`) contains exactly one `DEFAULT`-coded event:

> 06/15/2026 — Request for Default against Diamond Truck Sales, Inc., a California
> corporation, Alpine Truck Sales, Inc., a California corporation (sued … as the
> successor in interest, mere continuation, and/or alter ego of Diamond Truck
> Sales, Inc.) **Not Entered**

There is no later event entering default against anyone. The most recent
scheduling event is still `SHSET` — "Hearing regarding: Case Management
Conference, set for 08/12/2026 at 8:30 AM before Hon. Robert T. Waters in
Department 11B." The conversion of that CMC into a prove-up rests on a clerk's
phone statement recorded in `timeline.json`, not on a docketed order.

The clerk's `Notice to Filing Party` dated 07/30/2026 (Stephanie Bohrer, Clerk,
by Deputy Natalie Bashaw) gives four independent reasons the default could not be
entered:

1. CIV-100 items 1A, 1B and 1C "all blank/incomplete";
2. item 6 on page 2 of the Default "is not a named Defendant";
3. "The Proof of Service as to Alpine Truck is invalid, as they were not served
   as sued, and there is no Proof of Service as to Diamond Truck";
4. "There are also documents missing if you are in fact requesting a Court
   Judgmnet [*sic*]."

Items 1, 2 and 4 are what PR #500 set out to cure. **Item 3 is not cured by
anything in the repository** — it is a service defect, and no re-service of either
defendant with the operative pleading is recorded after July 30, 2026. Note the
tension worth resolving with the clerk before the hearing: the ROA *does* carry
two Diamond proofs of service filed 03/17/2026 (service dates 03/10/2026 and
03/11/2026, one flagged "possible duplicate"), so the clerk's "no Proof of
Service as to Diamond Truck" most likely refers to the **Amended** Summons and
First Amended Complaint rather than the original.

### 1.2 The filed CM-110 states the opposite, and that has to be corrected

The Case Management Statement filed July 20, 2026 and docketed 07/27/2026 tells
the court, in two places, that default has already been entered:

> "Diamond Truck Sales, Inc. — served 05/12/2026; **default entered**."
>
> "**Default entered** against Diamond; prove-up anticipated at or after this CMC."

The docket does not support that. This is the single highest-priority item in
this memo, and it is not a post-judgment item at all — it is a correction to make
on the record at or before the Aug. 12 hearing. A default judgment entered on the
premise that default was already entered is exposed to attack under CCP § 473(d)
as beyond the court's power, and correcting it voluntarily costs far less than
having it found later.

`timeline.json` carried the same error at the May 12, 2026 entry ("DEFAULT
ENTERED against Diamond Truck Sales, Inc."). That entry has been corrected in
this branch to match the ROA; the CM-110 is a filed document and can only be
corrected by filing.

---

## 2. Inventory: what exists and how complete it is

Field counts are AcroForm `/V` values actually present in each PDF, so
"filled/total" measures real completeness rather than intent.

| Form | Document in repo | Fields filled | Status |
|---|---|---|---|
| CIV-100 §1 | Aug 12 hand-up packets (Diamond, Alpine) | packet complete | Ready to hand up; twice rejected on service grounds |
| JUD-100 | In each packet; standalone "ready to submit" copy | money items blank | Correct — the court completes and signs |
| CIV-110 | Dismissal of Does 1–20, executed Aug 12 2026 | complete | Ready; needed so the judgment disposes of all parties |
| EJ-001 | Abstract of Judgment (Draft, Pending Judgment Entry) | 29 / 145 | Blocked — see §4.1 |
| EJ-130 | Writ of Execution (Draft, Pending Judgment Entry) | 36 / 180 | **Wrong county** — see §4.2 |
| MC-012 | Memo of Costs After Judgment (Draft) | 18 / 93 | Caption only; correctly premature |
| AT-138/EJ-125 | Appearance & Examination (Draft) | 29 / 103 | One order, two debtors — see §4.3 |
| AT-167/EJ-152 | Memorandum of Garnishee × 4 (Draft, Pending Levy) | caption + garnishee | Misclassified — see §4.4 |
| EJ-160 | Claim of Exemption (Blank Form, Debtor-Filed Reference Copy) | n/a | Correctly labeled; nothing to do |
| MC-010 | — | — | Deliberately omitted; **not a gap** (see §2.1) |

Every money field in every enforcement draft is empty. That is expected — the
figures cannot be entered until the judgment is entered — but it means none of
these four forms is closer to filing than its caption.

### 2.1 MC-010 is correctly absent

Both hand-up packets state that "Plaintiff waives costs of suit on CIV-100 item
7f; no Memorandum of Costs (Form MC-010) is filed with this packet," consistent
with the FW-003 fee waiver granted 02/13/2026. That is a deliberate election, not
an oversight, and it does **not** waive post-judgment enforcement costs — those
run through MC-012 under CCP § 685.070, which remains available.

---

## 3. The four documents that do not exist

| Form | Purpose | Why it matters here |
|---|---|---|
| **JL-1** | Notice of Judgment Lien, filed with the Secretary of State (CCP §§ 697.510, 697.530) | The largest untapped item. It creates a lien on the debtors' **business personal property** — equipment, inventory, accounts receivable. Both debtors are truck dealerships whose inventory *is* the asset. Nothing in the portfolio pursues it. |
| **CIV-130** | Notice of Entry of Judgment or Order | Fixes the CRC 8.104 appeal clock and documents that the debtors know a judgment exists before any levy. See §5.2 for the trap. |
| **EJ-100** | Acknowledgment of Satisfaction of Judgment | Mandatory the moment the judgment is satisfied (CCP § 724.030). On a written demand, failure to comply within 15 days exposes the creditor to actual damages, a $100 forfeiture, and the debtor's attorney fees (CCP § 724.050). Cheap to stage now. |
| **EJ-130 Attachment 4** | Additional judgment debtors | The writ draft points at it in terms — "see Attachment 4 (to be prepared)" — and it was never prepared. |

Two diligence gaps sit alongside these. No real-property search is documented for
either defendant, so there is no basis yet for choosing the county in which to
**record** the abstract (recording, not issuance, is what creates the real-property
lien). And `DFPI Central Locations for Service of Legal Process (downloaded Jul 29
2026)` shows **no** central-service entry for either JPMorgan Chase or Bank of
Stockton, which means a bank levy has to be served at a branch — making the county
question in §4.2 decisive rather than cosmetic.

---

## 4. Defects in the drafts that do exist

### 4.1 Diamond's address is recorded as unknown, but the portfolio has it

Both the abstract and the writ carry the same placeholder:

> "Diamond Truck Sales, Inc., a California corporation [TBD -- confirm last known
> CA business address from original POS-010, served 3/11/26]"

The POS-010s are scanned images, so the address is not machine-readable from
them — which is presumably why it was left open. But it is already in the
portfolio in text form. The SER-001 executed for **Diamond** on Aug. 3, 2026 gives
Diamond's service address as:

> 1201 S Soderquist Road, Turlock, CA 95380

— the same address as Alpine, served on the same manager. That is the fact the
alter-ego theory depends on, and it resolves the TBD in both forms. It should
still be confirmed against the scanned POS-010 and the Secretary of State's
current record before it goes on an abstract, since the abstract is what gets
recorded against real property.

### 4.2 The writ is directed to the wrong county

`EJ-130 … li1[0].FillText74[0] = 'San Joaquin'` — the writ commands the Sheriff or
Marshal of **San Joaquin County**. Every asset identified anywhere in this matter
is in **Stanislaus County**:

| Asset / target | Location | County |
|---|---|---|
| Diamond and Alpine business premises | 1201 S Soderquist Rd, Turlock | Stanislaus |
| Bank of Stockton, Golden State Branch | 134 S Golden State Blvd, Turlock | Stanislaus |
| Prior service on both defendants | Turlock (Stanislaus Sheriff, SER-001) | Stanislaus |

CCP § 699.510(a) is explicit: a writ "shall be directed to the levying officer in
the county where the levy is to be made," and "**a separate writ shall be issued
for each county where a levy is to be made**." A San Joaquin writ cannot be
levied in Turlock. The Stanislaus writ is the one that does the work; a San Joaquin
writ is worth issuing only if assets are actually found there. The same subsection
also imposes a cost of guessing wrong — once a writ issues for a county, no new
writ issues for that county for 180 days unless the first is returned.

Note that the *court* county on the form is correctly San Joaquin. It is the
levying county in item 1 that is wrong.

### 4.3 One examination order for two judgment debtors, pointed at the wrong sheriff

The AT-138/EJ-125 draft leaves the debtor open — "[TBD -- insert judgment debtor
name(s) once Aug. 12 judgment enters]" — and there is only one of them. A debtor
examination is per-examinee: each of Diamond and Alpine needs its own order, its
own hearing date obtained from the clerk, and its own personal service. Item 2
(date, time, room, department) is blank in the draft and can only be filled from
the court's calendar.

Two further points:

- **Venue is fine.** The judgment will be entered in San Joaquin, which is the
  proper court under CCP § 708.160(a). Turlock to Stockton is well inside the
  150-mile limit in § 708.160(b), so no § 708.160(d) application to another county
  is needed.
- **The designated server is not.** The draft names "registered process server or
  **San Joaquin County Sheriff**." Service has to happen in Turlock, where the San
  Joaquin Sheriff has no authority. This needs the Stanislaus Sheriff — i.e. a
  fresh SER-001 plus FW-003 packet, the same route used on Aug. 3 — or a registered
  process server. Service must be personal and no less than **30 days** before the
  examination date, so the hearing date has to be set with that lead time in mind.
- Because both debtors are corporations, the order must be served on a natural
  person — an officer, director, or managing agent — for the entity to be examined
  (CCP § 708.150). That makes the name question in §4.5 operative.

### 4.4 The garnishee memoranda are not this desk's forms to file

Four AT-167/EJ-152 drafts exist, one per debtor per bank, each labeled "Draft,
Pending Levy," with the garnishee name, branch address, and judgment debtor
pre-filled. AT-167/EJ-152 is the form the **garnishee** — the bank — completes
under penalty of perjury and returns to the levying officer within 10 days of
being served with the writ and notice of levy (CCP § 701.030). It is not a
creditor filing, and the creditor pre-filling the declarant's identifying items
is at best pointless and at worst confusing.

These belong in the same category as the EJ-160 already in the folder, which is
correctly labeled "Blank Form, Debtor-Filed Reference Copy." Recommendation:
relabel rather than develop, and treat the absence of returned memoranda after a
levy as the thing to watch, since § 701.030 makes a non-responding garnishee
liable for the costs of getting the information.

### 4.5 One person, four spellings

The manager served for both corporations appears in the record as:

| Spelling | Where |
|---|---|
| Mustaqem **Usmani** | SER-001, Diamond and Alpine (Aug. 3, 2026) |
| Mustagem **Usmani** | EJ-001 Abstract of Judgment draft, item 16 |
| **Osmani** family ownership | CM-110 filed July 20, 2026 |

`matters/12.json` already flags the Osmani/Usmani inconsistency as an open
diligence item; the abstract draft adds a third variant by transposing `q` to `g`.
This stops being cosmetic at the enforcement stage. Name accuracy governs whether
a JL-1 filing is found by a searcher, whether an examination order can be enforced
against the person served, and whether a recorded abstract attaches to the right
owner's property. Pin the spelling from the Secretary of State's corporate record
and the returned POS-010 before any of the three is lodged.

---

## 5. Clocks that start at entry

None of these can be calendared yet, because they all run from an entry date that
does not exist. They are listed so they can be dated the day it does.

| Clock | Authority | Runs from |
|---|---|---|
| Postjudgment interest, **10% per annum** | CCP § 685.010(a)(1) | Entry. The reduced 5% rate needs a natural-person debtor; both debtors are corporations, and the claim is fraud-based, so 10% applies. |
| JL-1 must be **received** by the Secretary of State within 10 days of the notice date | SOS filing rule under CCP § 697.510 | The date on the notice — a short fuse that is easy to blow by mailing late. The lien then runs five years. |
| Costs after judgment must be reported within **2 years** of being incurred | CCP § 685.070 | Each cost as incurred (writ fees, levy fees, recording fees) |
| Examination order must be personally served **≥ 30 days** before the hearing | CCP § 708.110 / form AT-138 | The date the clerk gives |
| Relief from default: 6 months; § 473.5 relief up to 2 years | CCP §§ 473(b), 473.5 | Entry. Enforcement in this window carries set-aside risk, which is a further reason to cure §1.2 rather than leave it. |

### 5.1 The fee waiver becomes a lien on the recovery

Plaintiff's court fees were waived (FW-003, granted 02/13/2026). The CIV-100's own
"Declaration Concerning Waived Court Fees" page states the consequence: where a
party whose fees were waived recovers **$10,000 or more**, the court has a lien on
the judgment for the waived fees, which must be paid before the lien is satisfied
(Gov. Code § 68637). At $53,671.20 the threshold is crossed several times over.
Expect the clerk to assert it, and complete that declaration on the hand-up
packets rather than leaving it for the court to raise.

### 5.2 CIV-130 cannot be served by the plaintiff

Two things about the notice of entry, both easy to get wrong here:

- **There is probably no statutory duty.** CCP § 664.5(a) applies to *contested*
  actions where the prevailing party *is* represented by counsel. Neither
  defendant has appeared, and Plaintiff is in pro per, so subdivision (a) does not
  bind him and the clerk's duty under subdivision (b) — also keyed to a contested
  action — is unlikely to be triggered either. Serving CIV-130 anyway is the clean
  way to fix the CRC 8.104 date and to show the debtors had notice before a levy.
- **He cannot serve it himself.** The form's proof of service must be executed by
  someone at least 18 years old who is *not a party*. A self-executed CIV-130 is
  defective on its face. Line up a third-party mailer, or have the notice served
  alongside whatever else goes to the Stanislaus Sheriff.

---

## 6. One consequence of the compensatory-only election

PR #500 deliberately dropped punitive damages from both packets, seeking
$53,671.20 compensatory per defendant, joint and several. That choice retires the
Aug. 3, 2026 CCP § 425.115 notices ($25,000 per defendant) as to these
defendants: a default judgment is final, and punitive damages cannot be sought on
the same claims afterward. Flagged as a consequence of a decision already made,
not as a reason to revisit it — the § 425.115 service posture was itself
unresolved, and a clean compensatory judgment now is worth more than a contested
punitive claim later.

For the abstract, note that joint and several liability means item 6 takes
**$53,671.20** — the single judgment amount — not the sum of the two. The draft's
structure is already right on this: Diamond in item 1a, Alpine as an additional
debtor in item 16, one abstract.

---

## 7. Sequenced punch list

Ordered by dependency, not by importance. Steps 1–2 are pre-judgment and are the
only ones actionable today.

1. **Correct the default-entry representation** from the July 20 CM-110, at or
   before the Aug. 12 hearing (§1.2).
2. **Resolve the clerk's service objection** as to Alpine ("not served as sued")
   and as to Diamond on the amended pleading — the one July 30 rejection ground
   nothing in the repository addresses (§1.1).
3. Get default entered, then judgment entered. Obtain a conformed JUD-100 and the
   exact entry date.
4. Serve **CIV-130** through a non-party (§5.2).
5. Complete the **Gov. Code § 68637** waived-fee declaration (§5.1).
6. Finish **EJ-001**: Diamond's address (§4.1), item 6 = $53,671.20, item 8a =
   entry date; pin the manager's name (§4.5). Then apply to the clerk for
   issuance, and record it in each county where real property is found.
7. File **JL-1** with the Secretary of State — watch the 10-day receipt window
   (§5).
8. Issue **EJ-130 for Stanislaus County**, with Attachment 4 prepared (§4.2, §3).
9. Prepare a **separate AT-138/EJ-125 per debtor**, obtain hearing dates, and
   arrange Stanislaus Sheriff or registered-process-server personal service at
   least 30 days out (§4.3).
10. Relabel the four **AT-167/EJ-152** drafts as garnishee reference copies (§4.4).
11. Log enforcement costs to **MC-012** as incurred, within two years each (§5).
12. Stage **EJ-100** against satisfaction (§3).

---

## Appendix — how the field counts were produced

```bash
python3 - <<'PY'
from pypdf import PdfReader
import glob
for f in sorted(glob.glob('*.pdf')):
    if 'Draft' not in f: continue
    r = PdfReader(f)
    fields = r.get_fields() or {}
    filled = [k for k, v in fields.items() if v.get('/V') not in (None, '', '/Off')]
    print(f'{len(filled):>4} / {len(fields):<4}  {f}')
PY
```

Run from `internal/public/documents/matter-12/`. The machine-readable version of
this audit is `internal/docs/matter_12_post_judgment_readiness.json`.
