# Matter 35 — Plaintiff's Outbound Discovery Drafts

Prepared October 15, 2026 for *Brendan Ngwa Nforbi v. Ross Stores, Inc., et al.*, Santa Clara County Superior Court No. 26CV501995.

This folder contains the first-wave plaintiff discovery package developed after Ross Stores, Inc. and Ross Dress for Less, Inc. served their verified answer and written discovery on October 15, 2026.

## Draft package

| File | Purpose |
|---|---|
| `M35_Standalone_Evidence_Preservation_Demand_DRAFT.pdf` / `.docx` | Immediate standalone demand focused on surveillance video, metadata, audit logs, witness identity, incident records, communications, schedules, training and preservation history. |
| `M35_Discovery_Set_One_to_Ross_Stores_Inc_DRAFT.pdf` / `.docx` | Defendant-specific packet containing 34 RFAs, the planned DISC-001 selections, 35 special interrogatories and 40 RFPs. |
| `M35_Discovery_Set_One_to_Ross_Dress_for_Less_Inc_DRAFT.pdf` / `.docx` | Parallel defendant-specific packet directed to Ross Dress for Less, Inc. |
| `README_SERVICE_ASSEMBLY.txt` | Pre-service assembly checklist and unresolved fields. |
| `OUTBOUND_DISCOVERY_STRATEGY.md` | Objectives, sequencing, leverage points and follow-up plan. |

## Service status

All documents are unsigned drafts. Nothing in this folder has been served or filed.

Before service:

1. Complete a separate current Judicial Council Form DISC-001 for each responding defendant. The packet's selection sheet is a drafting aid and is not a substitute for the official form.
2. Check DISC-001 Nos. 1.1, 4.1, 4.2, 12.1–12.7, 13.1–13.2, 14.1–14.2, 15.1 and 17.1.
3. Replace the bracketed RFP production date with a definite compliant date calculated from the actual service date.
4. Add separate proofs of service executed by a nonparty adult.
5. Recheck counsel's service addresses and the operative email-service arrangement.

## Architecture

The two corporate defendants receive separate sets. The requests are organized to:

- lock the answer's most useful admissions and denials;
- identify DOE 1, the cashier, the manager on duty, the verifier and surveillance custodians;
- obtain native video, metadata and access/export/deletion history;
- test the factual basis for any merchant-detention defense;
- obtain store policies, training, schedules, incident records and focused comparator evidence; and
- force facts, witnesses and documents supporting denials and affirmative defenses through Form Interrogatories 15.1 and 17.1.

The source generator is `internal/scripts/matter35-outbound-discovery-drafts.py`.
