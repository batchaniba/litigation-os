# Matter 20 — CHP Production Set One: Video (MP4) Descriptions

**Case:** *Newanforbi v. California Highway Patrol, et al.*, No. 26CV191136 (Alameda Superior, Dept. 25, Judge Whitman)
**Production:** Respondent's Responses to Petitioner's Requests for Production of Documents, Set One, served October 23, 2026, by Huihong Su (DOJ) via DOJ FileXchange
**Companion memo:** `internal/docs/Matter 20 - CHP Production Set One Map vs Answer (Oct 23 2026).md` (timeline, CHP 202, tox, map vs. the Answer, privilege log, substantive read)

## Why the videos themselves are not in this folder

The four MP4s total ~2.87 GB and the largest is 2.47 GB — far beyond GitHub's 100 MB per-file limit. They are held instead in the author's Google Drive (My Drive root, private, unshared; Drive file IDs below) and locally at `~/workspace/user/files/chp-production-set-one/`. The SHA-256 values below are the integrity record: any copy that does not match is not the produced file. All four were verified against DOJ's printed checksums on receipt, October 23, 2026.

The Dashcam Videos Coversheet PDF (in this folder) is CHP's own index of these files.

## The four videos

| File | Camera / span | Size | SHA-256 | Google Drive ID |
|---|---|---|---|---|
| `7659@20241101005536-0.mp4` | Forward dashcam, 00:54:36–~01:59:51, Nov 1, 2024 | 2,652,758,419 bytes (2.47 GB) | `ae5da7e970720d26d076ad36fb32543429ef60b3a79fc1c274b647b06fd1d6b4` | `1Rqv371jHmjY8B8T4lflu1lzkEamUK9W4` |
| `7659@20241101013330-1.mp4` | Back-seat camera, ~01:33, Nov 1, 2024 | 56,926,885 bytes (54.3 MB) | `30aac4eae73188ba82b2e7916f70097f59f2f493a1e0b3d6f46ebcb93e1352e9` | `19ZJo9qPwny6smaW2iyUT7Fmk2_c5KYB0` |
| `7659@20241101024702-0.mp4` | Forward dashcam, 02:46:03–02:49:53, Nov 1, 2024 | 152,917,057 bytes (146 MB) | `921025565fd7baaff762ab51a8328548ddbb2290b28cd6c1e358de6cad4720c0` | `1geAHpVDDL_2VG9yXhq4J9yHo26duOfHX` |
| `7659@20241101024704-1.mp4` | Back-seat camera, ~02:47, Nov 1, 2024 | 8,426,310 bytes (8.04 MB) | `359fc627805a4bdcf72cf11945548742c8b29e446eedafa35346cf07dd3f75fb` | `1owz99B20IIaCs7v24RyhObMtw01_hlpQ` |

## What each video shows

### 1. Forward dashcam, 00:54:36–~01:59:51 (the roadside record)

Unit 023295 (Meza-Gonzales), MVARS ID 3901633363. This is the usable record of the stop:

- **00:54:36** — Patrol car approaching the parked gray Tesla Model Y on the I-580 East shoulder, west of Isabel Ave, Livermore, at night.
- **01:04:36** — Subject out of the car, standing roadside with an officer, talking. Tesla on the shoulder, hazards on.
- **01:24:36** — Tesla on the shoulder with trunk open and door open (vehicle inventory stage).
- **01:34:36** — Officer standing by the Tesla holding a light-colored object; door open.
- **01:39:36** — Officer and subject near the Tesla in headlight glare (detail hard to discern).
- **01:49:36** — Tesla loaded on a tow truck; officer walking roadside with papers.
- **01:59:36** — Patrol car in a parking lot with parked cars and a wall; the clip ends ~01:59:51.

**Gap:** no forward video exists for 01:59:51–02:46:03 (Dublin processing and blood-draw lead-up). The roadside audio on this clip is transcribed — see [Transcripts of this recording already in the repo](#transcripts-of-this-recording-already-in-the-repo) below. The Answer's admissions turn on what was and was not said aloud (neither officer stated aloud on the recording that they smelled alcohol; neither told the subject his speech was slurred or impaired), and the transcript is where those admissions are tested.

### 2. Back-seat camera, ~01:33 — no signal, no sound

The frame shows the literal on-screen text "No Signal." A 30-second audio sample measures −91 dB mean/max — effectively silent. There is no in-car picture or sound of the subject during this period, including during transport. The file carries an AAC audio stream, but the sampled audio is silent.

### 3. Forward dashcam, 02:46:03–02:49:53 (facility arrival)

- **02:46:03** — Patrol car at a facility entrance with a canopy.
- **02:49:33** — Driving through a fenced compound with razor wire and buildings, consistent with the Santa Rita Jail arrival (booking recorded 03:25).

### 4. Back-seat camera, ~02:47 — no signal, no sound

Same as video 2: "No Signal" on screen, no in-car picture or sound of the subject. Together, videos 2 and 4 mean half the video record — the entire back-seat camera — is blank.

## Transcripts of this recording already in the repo

The forward (Camera 1) audio **is** transcribed. The transcript is a verbatim, timestamped transcription of the CHP dashcam video and audio recording for this incident — November 1, 2024, I-580 East, Livermore, CHP Case RJ68845, window **00:54:36–01:57:10** — with a speaker legend (Meza-Gonzalez, badge 023295; Melano, badge 023054) and sections including pre-FST questioning (01:01:21–01:05:07). It covers the whole roadside encounter on video 1 above, through the tow phase; it does not cover the 01:59:51–02:46:03 gap (no video exists there) or the 02:46–02:49 arrival clip, and there is no back-seat audio to transcribe (videos 2 and 4 are silent).

### Where the transcript lives

- **Hand-extract sidecar (live file in this repo):** `internal/public/documents/matter-33/incident/Exhibit_A_CHP_Video_Transcript.txt`, with `Exhibit_A_CHP_Video_Transcript.meta.json` alongside it. It is filed under matter-33 in the repo tree although the incident is Matter 20's. It extracts the four proof points, with citable anchors `RJ68845#t=00:54:36` (encounter window opens) and `RJ68845#t=01:12:04` (odor of alcohol never verbalized on the recording):
  1. "Strong distinct odor of an alcoholic beverage" — never verbalized during the 62-minute encounter.
  2. "Slurred" speech — contradicted by coherent, articulate speech throughout.
  3. "Seemed very confused and disoriented" — the subject correctly identified his location and read highway signs.
  4. "BEVERAGE PRESENT: YES" — the only liquid found was urine in a cup.
- **Full transcript text (in the repo's document index):** `internal/docs/document_index.jsonl` carries the extracted text of two full versions — the 15-page standalone `CHP Transcript.pdf` (document-store path `/documents/matter-33/from-07/CHP Transcript.pdf`) and the 19-page Exhibit A version filed in the E.D. Cal. Meza-Gonzalez case, No. 2:25-cv-01460-DC-CSK (document-store path `/documents/matter-33/incident/Exhibit_A_CHP_Video_Transcript.pdf`). Note: those PDFs themselves are not files in the repo tree — only their extracted text is in the index, and the sidecar itself notes "Replace with pdftotext when the documents branch is pulled."
- **As an exhibit to the Verified Petition:** the Matter 20 Verified Petition for Writ of Mandate (153 pp; document-store paths `/documents/matter-32/from-20/`) attaches the transcript as an exhibit and cites it at Petition ¶¶ 35–38, 44–48, 63.
- **Timestamped quotes embedded in the filed papers:** the briefs quote the transcript directly, including the cup exchange (00:58:51–00:59:05, "This is piss"; Meza-Gonzalez: "No I'm not gonna smell that"), the FST discussion (01:08:20–01:08:40; 01:10:14–01:10:30, environmental conditions), and the PAS advisement (01:10:54, "You're not required to do this"; 01:11:03, arrest left to the officer's discretion on refusal).

### What this changes

An earlier draft of this file — and of the companion memo — said the roadside audio was untranscribed. That was wrong: the transcript above already exists, and the companion memo's "transcribe the audio" next step is superseded by working from this transcript and logging only the narrow gap between the transcript's 01:57:10 end and the forward clip's ~01:59:51 end.

## Production PDFs in this folder

The eight PDFs of Production Set One are committed alongside this file:

- Dashcam Videos Coversheet (AGO 000022–000024)
- Exhibit 3, Incident Log 241101GG0064
- Exhibit 4, Beat sheet 10-31-2024 (AGO 000025)
- Exhibit 5, CHP 202 / DS 367 / Warrant Affidavit packet (AGO 000029–000053)
- Exhibit 8, CHP 415, Meza-Gonzales 10-31-2024 (AGO 000054)
- Exhibit 11, CHP 415, Melano 10-31-2024 (AGO 000061)
- Privilege Log (10 items withheld)
- Proof of Service (Su, October 23, 2026)

Their SHA-256 values, as verified against DOJ's printed checksums on receipt:

- Dashcam Videos Coversheet: `c8472a9d6c15f76a99e9e67097d1e35ffbfd7ab0a7d0d72df1051820337c4dc0`
- Exhibit 3: `201cacaed9a228daa17b579e1a46b72b66706304f93c0b6de0dd868809140aa8`
- Exhibit 4: `e1814786b9a8210608f574b17249bdfa83f6efd5d6d83c6d05151603a9423ded`
- Exhibit 5: `320533ac9d50323cf49abd59506b0a8bd0db3e42fc9f895ac8c7d055259aa012`
- Exhibit 8: `36781c9e379c04e9e602162505f7c4ed7e80e6219040e44fa6be8f2d0cd1d166`
- Exhibit 11: `f6c013637f82aa9143c7271653111c1ae0a8253eeda4fcc3c5316f7ee3d0b664`
- Privilege Log: `cabad17f0d00dcd92c9ebcdabb1955b2442b9c96e53c2e755d2cebbe30991063`
- Proof of Service: `c15d4fa96e4a398ed1562261e2b0080efe58c04165719a7b8276349bf2e89ef8`
