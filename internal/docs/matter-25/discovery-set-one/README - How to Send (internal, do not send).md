# Matter 25 — Discovery Set One: how to send

Internal checklist. Do not send this file.

## Rebuilding the PDFs

The documents are on the portfolio's pleading paper (`internal/scripts/lib/pleading_paper.py`), with a proof of service from `proof_of_service.py` attached to docs 01, 02, 03 and 05. To change the date, city, or service method, rebuild:

```
python3 internal/scripts/matter25-discovery-set-one.py --date "September 25, 2026" --mailed-from "Stockton, California"
```

- `--by-email`: the proofs recite email service instead of mail. Use it only after Kray consents to email service in writing.
- `--stamp-signature`: applies your canonical signature stamp to the documents and proofs. Signature lines print blank by default because signing discovery is a Rule 26(g) certification. Review first, then either sign by hand or rebuild with this flag.
- Needs `reportlab`, `pypdf`, `numpy`, and `pillow`.

## After the Rule 26(f) call (Sep. 25, 2026)

Discovery opens when the Rule 26(f) conference ends (Fed. R. Civ. P. 26(d)(1)).

0. **Right after the call, send the memorial email** (`00a - 26(f) Memorial Email...`). Fill in what was actually agreed. It fixes the discovery-open date and any email-service consent in writing before anyone remembers it differently.
1. **Sign** docs 01, 02, 03 and 05 and their attached proofs of service: in ink, or rebuild with `--stamp-signature`. Rule 26(g) requires a signature on every discovery request.
2. **Serve 01–03 on Kray today**:
   - First-class mail to 2601 Main Street, Suite 1100, Irvine, CA 92614. The proof of service is already filled in (date, Stockton, Kray's address). Rebuild with `--date` / `--mailed-from` if either changes.
   - Email a courtesy copy with the cover email (`00 - Cover Email...`). Email counts as service only if Kray consents **in writing**. Ask for that on the call. If she consents, check the email box on the proofs instead of the mail box.
3. **Do not file** discovery requests with the court (E.D. Cal. L.R. 250.2–250.4). Keep the signed originals and proofs.
4. **Response deadlines:** 30 days after service, plus 3 days if served by mail. Served Sep. 25: 30 days lands on Sunday, Oct. 25, which rolls to **Mon., Oct. 26, 2026** (Rule 6(a)(1)(C)). That's the deadline if you emailed with written consent. If you mailed, Rule 6(d) adds 3 days after that, so the deadline is **Thu., Oct. 29, 2026**. Recount if you serve on a different day.
   - Requests for admission are **deemed admitted** if FedEx doesn't answer on time (Rule 36(a)(3)).
   - Calendar the date in `clocks.json` once served.

## Status (Sep. 25, 2026)

- Docs 01–03 were served Sep. 25 by mail from San Jose and by email. FedEx responses are due **Oct. 29, 2026**.
- The served proofs recited Stockton. Send **06 (Amended Proof of Service, San Jose)** with the `00b` email.
- The repo PDFs are the signed (stamped) San Jose versions:
  `python3 internal/scripts/matter25-discovery-set-one.py --stamp-signature --mailed-from "San Jose, California" --amended-pos`
- **Doc 05 (notice of subpoena) is dated Sep. 25 but isn't served yet.** Rebuild it with `--date "<the day you send it>"` (and `--mailed-from` if different) once the clerk issues the AO 88B, so its date and proof are accurate.

## Rule 45 subpoena to First Advantage (takes a few extra days)

A party without a lawyer cannot issue a subpoena. The clerk must (Rule 45(a)(3)).

1. **Get a signed blank AO 88B** ("Subpoena to Produce Documents, Information, or Objects…") from the E.D. Cal. clerk, Sacramento: Robert T. Matsui U.S. Courthouse, 501 I Street. Ask in person or by mail with a short request letter (confirm the room number and procedure with the clerk's office).
2. **Fill in the AO 88B:**
   - To: First Advantage Background Services Corp., c/o its registered agent. PR #935 lists CSC – Lawyers Incorporating Service, 2710 Gateway Oaks Drive, Suite 150N, Sacramento, CA 95833 (the same CSC office used for Randstad). **Confirm on the California Secretary of State bizfile site before service.** A courtesy copy by mail to First Advantage's Consumer Center, P.O. Box 105292, Atlanta, GA 30348-5292, is fine but is not service.
   - "Production": check the box and write "See Attachment A."
   - Place: 1455 Cat Tail Drive, Stockton, CA 95204, or electronic delivery to bnn.cdl@gmail.com.
   - Date/time: at least 14 days after you expect it to be served. Suggest about 30 days, e.g. **Nov. 2, 2026, 10:00 a.m.** This keeps the place of compliance within Rule 45(c)(2)(A); production by mail satisfies it.
   - Attach doc 04 (Attachments A and B).
3. **Notice first (Rule 45(a)(4)):** before serving First Advantage, serve Kray with doc 05 plus a copy of the completed subpoena and attachments. Mail it, or email if she consented.
4. **Serve First Advantage:** someone **18 or older who is not you** must deliver it (Rule 45(b)(1)), usually a registered process server. For a documents-only subpoena, no witness fee is required. That person completes the proof of service on page 2 of the AO 88B.
5. **Hold rule:** if Kray commits in writing to a date for producing the First Advantage report, you may hold the subpoena 48 hours against that commitment. The party requests (01–03) go out regardless.
6. **Identifiers:** never put your DOB or SSN in anything to Kray. If First Advantage needs them to locate your file, send them only to First Advantage, separately.
7. **If First Advantage objects or asks for a protective order,** don't argue by email. Meet and confer by phone, then use Judge Riordan's informal two-page letter procedure if needed.

## Numbers
- Interrogatories: 18. Counting discrete subparts (Nos. 2, 4, and 17), about 22–23, still under the 25 limit (Rule 33(a)(1)). Only 2–3 remain for a second set, so spend them carefully.
- Requests for admission: 26. Requests for production: 25. Subpoena requests: 9.
- Merged from PR #935: First Advantage account/search IDs, litigation hold, the § 290.46(j)(2)(E) contention interrogatory, jury-demand RFAs, prior-file RFA, Fair Chance Act and Workday in the RFPs, notice drafts and distribution lists, pricing redaction, the registered agent, the cc, the memorial email, and the 48-hour hold rule. Deliberately left out: #935's RFA on the PC 220(a)(1) conviction (it feeds the Labor Code § 432.7 argument), its pure-law RFAs (Rule 36 doesn't allow them), and its magistrate-consent interrogatory (the docket answers it).

## Reminder
Discovery runs both ways. FedEx will serve its own requests and notice your deposition. Pin down the facts on your prior FedEx applications before answering anything under oath.
