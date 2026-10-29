# Salvage record: PR #940 Sep. 24–25, 2026 catalog entries

Salvaged Oct. 28, 2026 from PR #940 (`catalog/sep-25-evening-updates`, closed). That PR registered the 9 documents below in the manifest, registry, and per-matter `documents.json`. **Their PDF bytes are not in the repo, the `documents` branch, or R2:** `GET /doc/<sha256>/meta` on the doc-api returned 404 for every one on Oct. 28, 2026. To avoid broken public links, they were **not** added to `manifest.json`. The PR's docket rows (M25 Dkt 10, M26 Dkt 15, M28 Dkt 24) and its past timeline events were salvaged into the matter files; those docket rows have `path: null`.

To restore: re-obtain each PDF (ECF or Gmail export), confirm the sha256 matches the value below or record the new one, then catalog it normally (`npm run q catalogDocument` / `documents:push`).

Other entries in that PR were deliberately excluded by owner instruction and are not recorded here.

| Matter | Path | sha256 | Bytes | Label (from PR registry) |
|---|---|---|---|---|
| matter-25 | `/documents/matter-25/Dkt 10 - Defendant's Status Report (Kray, Filed Sep 24 2026).pdf` | `bcb90fae499c5f8df1801f5a492a8a18a7363b5cc16360488cb3fa720fd2407d` | 235337 | Dkt 10 - FedEx status report (Kray, filed Sep 24 2026) |
| matter-25 | `/documents/matter-25/Rule 26(f) Meet-and-Confer - Zoom Invite from Kray (Sep 24 2026).pdf` | `47ae9aa3a4ebf120c66831c59b319b4aeee10ee499e4b2f2e9349e1fe75bffc7` | 57679 | Rule 26(f) Zoom invite from Kray (Sep 24 2026) |
| matter-25 | `/documents/matter-25/Email Thread - Rule 26(f) Conference Scheduling with Kray (Sep 24 2026).pdf` | `e7923c47114c65b4fb678520fe29ce7deb8c783c2d5cf85d1ce829ccb5c48a3d` | 81547 | Rule 26(f) scheduling thread with Kray (Sep 24 2026) |
| matter-26 | `/documents/matter-26/Dkt 15 - Minute Order Vacating Oct 7 MTD Hearing, Under Submission L.R. 230(g) (Sep 24 2026).pdf` | `d890b67a3968b182b09710781442b3523f01c7a3462c8d176a06980307d80dd5` | 136019 | Dkt 15 - Minute order: Oct 7 MTD hearing vacated, under submission (Sep 24 2026) |
| matter-28 | `/documents/matter-28/Dkt 24 - [Proposed] Order Denying Defendants' Motion to Dismiss, Lodged (Sep 24 2026).pdf` | `e542935384588b227e0900118100867a3a6c35e3ea0c1255b85dba865b256c8f` | 593972 | Dkt 24 - [Proposed] order denying MTD, lodged Sep 24 2026 |
| matter-33 | `/documents/matter-33/Email Thread with McMahon - Extension Request, FAC Service, Meet-and-Confer (Sep 25 2026).pdf` | `e53a39cd40d223398a7e2120059394993ee6090b586ce6dc967545403fd3334e` | 112507 | McMahon email: extension request, FAC service, meet-and-confer (Sep 25 2026) |
| matter-33 | `/documents/matter-33/Email to McMahon - Three-Week Extension Granted, MTS Opposition Due Oct 16 2026 (Sep 25 2026).pdf` | `7f66d49bfdf8017f2335d20fddd42403fa78e3cc582320892bcb64e0136ad14f` | 121213 | Extension granted: MTS opposition due Oct 16 2026 (Sep 25 2026) |
| matter-35 | `/documents/matter-35/Email from Musni (VMB) - Appearance and 15-Day Extension Request (Sep 25 2026).pdf` | `413e73728042bf99ad3b6bd973c9502bd7623d648763e1a1c8fbf176b76b69a5` | 135530 | Musni (VMB) appearance + 15-day extension request (Sep 25 2026) |
| matter-35 | `/documents/matter-35/Email Thread - Extension Granted Through Oct 15 2026, Confirmed (Sep 25 2026).pdf` | `ed2c38b2bfee53dafc059bd49cd14686074e031802111415074ed601e2079680` | 184096 | Extension granted through Oct 15 2026, confirmed (Sep 25 2026) |
