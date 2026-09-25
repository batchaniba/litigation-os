#!/usr/bin/env python3
"""Generate Matter 25 first-wave discovery (HTML -> PDF via headless Chromium)."""
import html, pathlib, subprocess

OUT = pathlib.Path("/home/user/interactive-litigation-portfolio/internal/docs/matter-25/discovery-set-one")
OUT.mkdir(parents=True, exist_ok=True)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DATE = "September 25, 2026"
CASE = "Case No. 2:26-cv-02881-DAD-SCR"

CSS = """
@page{size:Letter;margin:1in 1in 1in 1.1in}
body{font-family:"Times New Roman",Times,serif;font-size:12pt;line-height:1.55;color:#000}
.hdr{line-height:1.25;margin-bottom:18pt}
.court{text-align:center;font-weight:bold;margin:10pt 0 14pt;line-height:1.3}
table.cap{width:100%;border-collapse:collapse;margin-bottom:16pt}
table.cap td{vertical-align:top;padding:4pt 8pt}
table.cap td.l{width:52%;border-right:1px solid #000;border-bottom:1px solid #000}
.ttl{font-weight:bold}
h2{font-size:12pt;text-align:center;margin:16pt 0 8pt;text-transform:uppercase}
h3{font-size:12pt;margin:12pt 0 4pt}
p{margin:0 0 9pt;text-align:justify}
.req{margin:0 0 10pt}
.req b{display:block}
.sig{margin-top:26pt;line-height:1.3}
.pb{page-break-before:always}
.small{font-size:10.5pt}
"""

def esc(s): return html.escape(s, quote=False)

def caption(title, extra_right=""):
    return f"""
<div class="hdr">BRENDAN NGEHSI NEWANFORBI<br>1455 Cat Tail Drive<br>Stockton, CA 95204<br>Telephone: (209) 801-4442<br>Email: bnn.cdl@gmail.com<br>Plaintiff, In Propria Persona</div>
<div class="court">UNITED STATES DISTRICT COURT<br>EASTERN DISTRICT OF CALIFORNIA</div>
<table class="cap"><tr><td class="l">BRENDAN NGEHSI NEWANFORBI,<br><br>&nbsp;&nbsp;&nbsp;&nbsp;Plaintiff,<br><br>&nbsp;&nbsp;v.<br><br>FEDERAL EXPRESS CORPORATION, and DOES 1 through 10, inclusive,<br><br>&nbsp;&nbsp;&nbsp;&nbsp;Defendants.</td>
<td>{CASE}<br><br><span class="ttl">{title}</span>{extra_right}<br><br>Magistrate Judge: Hon. Sean C. Riordan<br>District Judge: Hon. Dale A. Drozd</td></tr></table>
"""

def sig(label="Plaintiff, In Propria Persona"):
    return f"""<div class="sig">Dated: {DATE}<br><br><br>____________________________________<br>BRENDAN NGEHSI NEWANFORBI<br>{label}</div>"""

def pos(docs, note_email=True):
    items = "".join(f"<li>{esc(d)}</li>" for d in docs)
    return f"""
<div class="pb"></div>
<h2>Proof of Service</h2>
<p>I am the Plaintiff in this action, over the age of eighteen. My address is 1455 Cat Tail Drive, Stockton, California 95204. On the date below I served the following document(s):</p>
<ol>{items}</ol>
<p>on the person below, by the method checked:</p>
<p>&#9744; <b>U.S. Mail</b> (Fed. R. Civ. P. 5(b)(2)(C)): by placing a true copy in a sealed envelope, first-class postage fully prepaid, deposited with the United States Postal Service at ______________________, California, addressed as below.</p>
<p>&#9744; <b>Email</b> (Fed. R. Civ. P. 5(b)(2)(E)): by transmitting a PDF copy to the email address below. Counsel consented in writing to email service on ______________ (date).</p>
<p style="margin-left:24pt">Allison A. Kray, Esq.<br>Federal Express Corporation<br>2601 Main Street, Suite 1100<br>Irvine, California 92614<br>allison.kray@fedex.com<br><i>Attorney for Defendant Federal Express Corporation</i></p>
<p>I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct. Executed on ______________, 2026, at ______________________, California.</p>
<div class="sig"><br>____________________________________<br>BRENDAN NGEHSI NEWANFORBI</div>
"""

DEFS = """
<h2>Definitions</h2>
<p>1. <b>"FedEx," "Defendant," "You," and "Your"</b> mean Defendant Federal Express Corporation and, to the extent it acted for or with Federal Express Corporation in connection with Plaintiff's applications, background screening, or hiring decisions, any parent, subsidiary, or affiliate (including FedEx Ground Package System, Inc. and any unit identified as "FEDEX GROUND HR"), and their officers, employees, agents, and vendors.</p>
<p>2. <b>"Plaintiff"</b> means Brendan Ngehsi Newanforbi, including under any variation of that name (for example, Brendan Ngwa Nforbi, Brendan Ngwanforbi, or Ngwa-Nforbi).</p>
<p>3. <b>"First Advantage"</b> means First Advantage Background Services Corp. and any affiliate that prepared or furnished a background report about Plaintiff to FedEx.</p>
<p>4. <b>"Report"</b> means every consumer report, investigative consumer report, background report, and update or version of one, concerning Plaintiff that First Advantage or any other consumer reporting agency furnished to FedEx, including the report FedEx admits (Answer, ECF No. 4, &para;&para; 17, 20, 34) was provided to it on or before March 10, 2025.</p>
<p>5. <b>"Adverse Action"</b> means FedEx's decision to deny Plaintiff employment, and to withdraw any conditional offer of employment, in or about March 2025, including the adverse-action notice dated on or about March 19, 2025.</p>
<p>6. <b>"Registry Information"</b> means any information identifying Plaintiff as a registered sex offender, from any source, including the California Department of Justice Megan's Law website (Cal. Penal Code &sect; 290.46), the National Sex Offender Public Website (NSOPW), any state registry, or any database compiled from them.</p>
<p>7. <b>"Prior Employment"</b> means each period, before January 2025, in which FedEx hired or employed Plaintiff, and each application Plaintiff submitted to FedEx before January 2025.</p>
<p>8. <b>"Document"</b> and <b>"communication"</b> have the broadest meaning allowed by Fed. R. Civ. P. 34(a)(1)(A), and include electronically stored information such as email, chat and instant messages, applicant-tracking-system records (including Paradox), portal records, notes, and audit logs.</p>
<p>9. <b>"Identify,"</b> for a person, means full name, job title, employer, and last known business address; for a document, its date, author, recipients, type, and Bates number if produced.</p>
<p>10. Unless otherwise stated, the relevant period is <b>January 1, 2024 through the present</b>, except that requests about Prior Employment cover any time.</p>
"""

def build(fname, body, title):
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{esc(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"
    h = OUT / f"{fname}.html"
    h.write_text(doc)
    pdf = OUT / f"{fname}.pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", f"file://{h}"], check=True, capture_output=True, timeout=120)
    h.unlink()
    print("wrote", pdf.name)

# ---------------- INTERROGATORIES ----------------
ROGS = [
 "Identify each person who participated in, recommended, reviewed, or approved the Adverse Action, and describe each person's role.",
 "Identify the legal entity that (a) received Plaintiff's January 2025 application, (b) ordered the Report from First Advantage, and (c) made the Adverse Action, and state whether that entity was Federal Express Corporation, FedEx Ground Package System, Inc., or another entity.",
 "State every reason for the Adverse Action, and for each reason identify the documents and the persons with knowledge that support it.",
 "State all facts supporting Your contention (Status Report, ECF No. 10, at 2) that Plaintiff's application \"contained material misrepresentations that independently justified the hiring decision,\" including, for each alleged misrepresentation: the exact wording of the question; Plaintiff's answer; the date the question was presented; whether it was presented before or after any conditional offer of employment; and the date FedEx first contended the answer was a misrepresentation.",
 "State whether FedEx would have taken the Adverse Action if the Report had contained no Registry Information, and state all facts supporting Your answer.",
 "Describe each search or component FedEx ordered from First Advantage concerning Plaintiff (including the package name and any sex offender registry search), identify who selected that package for the position, and state the source First Advantage searched for any Registry Information (for example, NSOPW, the California Megan's Law website, or another database).",
 "Describe the adjudication or scoring criteria (including any \"client criteria\" or eligibility matrix) applied to the Report, including how Registry Information is scored, and identify who applied the criteria to Plaintiff's Report.",
 "Identify each position and period of Prior Employment (title, facility, start and end dates, and reason employment ended), and state whether FedEx or its vendor conducted a background check in connection with each.",
 "For each background check identified in response to Interrogatory No. 8, state whether it disclosed Registry Information about Plaintiff and what, if anything, FedEx did in response.",
 "Describe each policy, procedure, guideline, or training in effect between January 1, 2024 and March 31, 2025 concerning the use of Registry Information in hiring decisions in California, including any that refers to California Penal Code section 290.46.",
 "Identify each communication between FedEx and First Advantage concerning Plaintiff, by date, participants, and substance.",
 "Describe the position for which Plaintiff was considered in 2025, including title, facility, shift, duties, and whether the position involved supervising, or unsupervised contact with, minors or elder or dependent adults.",
 "State all facts supporting Your Eighth Affirmative Defense (that any use of Registry Information was to protect a person at risk under Cal. Penal Code § 290.46(j)(1)), and identify each person at risk You contend was protected.",
 "Describe any conditional offer of employment extended to Plaintiff in or about 2025, including its date, the position, hourly wage, expected weekly hours, and benefits.",
 "Identify each person who drafted, approved, or sent the adverse-action notice dated on or about March 19, 2025, and state the source of that notice's reference to the National Sex Offender Public Website and the California sex offender website (Answer ¶ 26).",
 "State whether any FedEx employee or agent accessed the California Megan's Law website or NSOPW concerning Plaintiff, and if so identify who, when, and for what purpose.",
 "State whether any document or electronically stored information concerning Plaintiff's applications, the Report, or the Adverse Action has been deleted, discarded, or lost since March 1, 2025, and if so describe it and the circumstances.",
 "Identify each person, other than Your counsel, who assisted in answering these interrogatories, and the interrogatory numbers each assisted with.",
]

rog_body = caption("PLAINTIFF'S FIRST SET OF INTERROGATORIES TO DEFENDANT FEDERAL EXPRESS CORPORATION", "<br><br>Set No.: One<br>Propounding Party: Plaintiff<br>Responding Party: Defendant Federal Express Corporation")
rog_body += f"""
<p>TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:</p>
<p>Under Federal Rules of Civil Procedure 26 and 33, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant Federal Express Corporation answer each interrogatory below separately and fully, in writing and under oath, and serve its answers on Plaintiff within thirty (30) days after service (plus three days if service is by mail under Rule 6(d)).</p>
<h2>Instructions</h2>
<p>1. Answer each interrogatory on the basis of all information available to You, including information held by Your employees, affiliates, agents, and vendors. If You cannot answer fully, answer to the extent possible and explain why.</p>
<p>2. Any objection must be stated with specificity (Rule 33(b)(4)). If You object to part of an interrogatory, answer the rest.</p>
<p>3. If You answer by reference to business records under Rule 33(d), identify the records by Bates number in enough detail for Plaintiff to locate them as readily as You could.</p>
<p>4. If You withhold information on a claim of privilege, describe it as required by Rule 26(b)(5)(A).</p>
<p>5. These interrogatories are continuing. Supplement Your answers as required by Rule 26(e).</p>
{DEFS}
<h2>Interrogatories</h2>
"""
for i, q in enumerate(ROGS, 1):
    rog_body += f"<div class='req'><b>INTERROGATORY NO. {i}:</b>{esc(q)}</div>"
rog_body += sig() + pos(["Plaintiff's First Set of Interrogatories to Defendant Federal Express Corporation"])
build("01 - Plaintiff First Set of Interrogatories to FedEx (Set One)", rog_body, "Interrogatories Set One")

# ---------------- RFAs ----------------
RFAS = [
 "Admit that You engaged First Advantage to prepare a background report on Plaintiff in connection with his application for employment with You in 2025.",
 "Admit that the Report provided to You on or before March 10, 2025 identified Plaintiff as a registered sex offender.",
 "Admit that the Report identified the California sex offender registry as the source of the registry record concerning Plaintiff.",
 "Admit that You reviewed the Registry Information in the Report before taking the Adverse Action.",
 "Admit that You considered the Registry Information in deciding to take the Adverse Action.",
 "Admit that the Registry Information was a reason for the Adverse Action.",
 "Admit that You extended Plaintiff a conditional offer of employment before March 10, 2025.",
 "Admit that You withdrew Plaintiff's conditional offer of employment on or about March 19, 2025.",
 "Admit that the adverse-action notice sent to Plaintiff on or about March 19, 2025 referenced the National Sex Offender Public Website.",
 "Admit that the adverse-action notice sent to Plaintiff on or about March 19, 2025 referenced the California sex offender website.",
 "Admit that the adverse-action notice sent to Plaintiff on or about March 19, 2025 did not state that any answer on Plaintiff's application was a reason for the Adverse Action.",
 "Admit that, before March 19, 2025, You did not inform Plaintiff in writing that You believed any answer on his application was false.",
 "Admit that the position for which Plaintiff was considered in 2025 did not involve supervising minors.",
 "Admit that the position for which Plaintiff was considered in 2025 did not involve unsupervised contact with minors.",
 "Admit that the position for which Plaintiff was considered in 2025 did not involve caring for elder or dependent adults.",
 "Admit that, before taking the Adverse Action, You did not identify any specific person at risk whom the Adverse Action was intended to protect.",
 "Admit that no federal, state, or local law required You to conduct a criminal background check for the position for which Plaintiff was considered in 2025.",
 "Admit that no federal, state, or local law required You to search any sex offender registry for the position for which Plaintiff was considered in 2025.",
 "Admit that You employed Plaintiff at least once before January 2025.",
 "Admit that You conducted, or caused First Advantage to conduct, a background check on Plaintiff in connection with at least one period of Prior Employment.",
 "Admit that You hired Plaintiff at least once before January 2025 after receiving a background report about him.",
 "Admit that You did not send Plaintiff a copy of the Report within three business days after You received it.",
 "Admit that You have no written policy, in effect between January 1, 2024 and March 31, 2025, that prohibits using Registry Information in hiring decisions for positions in California.",
]
rfa_body = caption("PLAINTIFF'S FIRST SET OF REQUESTS FOR ADMISSION TO DEFENDANT FEDERAL EXPRESS CORPORATION", "<br><br>Set No.: One<br>Propounding Party: Plaintiff<br>Responding Party: Defendant Federal Express Corporation")
rfa_body += f"""
<p>TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:</p>
<p>Under Federal Rules of Civil Procedure 26 and 36, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant Federal Express Corporation admit the truth of each matter below, in writing, within thirty (30) days after service (plus three days if service is by mail under Rule 6(d)).</p>
<p><b>Notice under Rule 36(a)(3):</b> each matter is admitted unless, within the time allowed, You serve a written answer or objection addressed to it, signed by You or Your attorney.</p>
<h2>Instructions</h2>
<p>1. If You do not admit a matter, specifically deny it or state in detail why You cannot truthfully admit or deny it (Rule 36(a)(4)). A denial must fairly respond to the substance of the matter; when good faith requires, specify the part admitted and qualify or deny only the rest.</p>
<p>2. You may assert lack of knowledge or information as a reason for failing to admit or deny only if You state that You have made reasonable inquiry and that the information You know or can readily obtain is insufficient.</p>
<p>3. The Definitions in Plaintiff's First Set of Interrogatories, served with these requests, apply here and are restated below.</p>
{DEFS}
<h2>Requests for Admission</h2>
"""
for i, q in enumerate(RFAS, 1):
    rfa_body += f"<div class='req'><b>REQUEST FOR ADMISSION NO. {i}:</b>{esc(q)}</div>"
rfa_body += sig() + pos(["Plaintiff's First Set of Requests for Admission to Defendant Federal Express Corporation"])
build("02 - Plaintiff First Set of Requests for Admission to FedEx (Set One)", rfa_body, "RFAs Set One")

# ---------------- RFPs ----------------
RFPS = [
 "All documents concerning each application Plaintiff submitted to You at any time, including the application reflected in the July 17, 2024 confirmation from fedex@paradox.ai and the application You describe as submitted in January 2025, together with all forms Plaintiff completed, including the forms dated on or about January 8, 2025.",
 "Plaintiff's complete personnel, onboarding, and separation files for each period of Prior Employment.",
 "Each Report, in every version and in the form furnished to You, including all attachments, component results, and updates.",
 "All communications between You and First Advantage concerning Plaintiff, including portal messages, emails, adjudication notes, and status updates.",
 "All documents reflecting the adjudication, scoring, or eligibility determination applied to each Report, including any \"client criteria,\" eligibility matrix, or adjudication guideline used.",
 "Each conditional offer of employment, offer letter, or offer communication extended to Plaintiff at any time.",
 "Each pre-adverse action notice and adverse-action notice sent to Plaintiff at any time, with all enclosures, in the form sent, and documents showing the dates and method of delivery.",
 "All documents You relied on, reviewed, or considered in taking the Adverse Action.",
 "All internal communications (including email, chat, and instant messages) concerning Plaintiff's 2025 application, the Report, or the Adverse Action.",
 "All documents supporting Your contention that Plaintiff's application \"contained material misrepresentations that independently justified the hiring decision\" (ECF No. 10 at 2).",
 "All documents supporting Your Eighth Affirmative Defense (use of information to protect a person at risk).",
 "All policies, procedures, guidelines, and training materials in effect at any time from January 1, 2024 through March 31, 2025 concerning the use of criminal history or Registry Information in hiring decisions for positions in California.",
 "All policies, procedures, guidelines, and training materials in effect at any time from January 1, 2024 through March 31, 2025 that refer to California Penal Code section 290.46 or the Megan's Law website.",
 "The portions of each agreement, statement of work, or package configuration between You and First Advantage in effect during 2024 or 2025 that govern the searches ordered for California applicants, any sex offender registry search, or compliance with California law.",
 "The job posting, job description, and documents sufficient to show the duties of each position for which Plaintiff applied or was considered in 2024 or 2025.",
 "Documents sufficient to show the hourly wage, expected hours, and benefits of the position for which Plaintiff was considered in 2025.",
 "All applicant-tracking-system records concerning Plaintiff (including Paradox and any successor or related system), including status histories, notes, and audit logs.",
 "All disclosure and authorization forms concerning background reports that Plaintiff signed or acknowledged at any time, and all documents showing whether Plaintiff requested a copy of any Report.",
 "Documents sufficient to show the date and time You received each Report.",
 "All documents concerning any background check performed on Plaintiff in connection with any period of Prior Employment.",
 "All documents identified, referred to, or relied on in Your answers to Plaintiff's First Set of Interrogatories.",
 "All written or recorded statements of any witness concerning the facts of this action.",
 "All documents You obtain from any third party, by subpoena or otherwise, concerning Plaintiff or this action.",
]
rfp_body = caption("PLAINTIFF'S FIRST SET OF REQUESTS FOR PRODUCTION OF DOCUMENTS TO DEFENDANT FEDERAL EXPRESS CORPORATION", "<br><br>Set No.: One<br>Propounding Party: Plaintiff<br>Responding Party: Defendant Federal Express Corporation")
rfp_body += f"""
<p>TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:</p>
<p>Under Federal Rules of Civil Procedure 26 and 34, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant Federal Express Corporation serve a written response within thirty (30) days after service (plus three days if service is by mail under Rule 6(d)), and produce the documents requested below at that time or by another reasonable date stated in the response.</p>
<p><b>Place and manner of production:</b> by delivery of copies to Plaintiff at 1455 Cat Tail Drive, Stockton, California 95204, or by secure electronic delivery to bnn.cdl@gmail.com.</p>
<h2>Instructions</h2>
<p>1. Produce documents in Your possession, custody, or control, including documents held by Your affiliates, agents, and vendors (including First Advantage) that You have the legal right or practical ability to obtain.</p>
<p>2. Produce electronically stored information as searchable PDF, except that spreadsheets, audit logs, and applicant-tracking-system data should be produced in native or other reasonably usable form with metadata showing dates and authors (Rule 34(b)(1)(C), (b)(2)(E)).</p>
<p>3. Organize and label documents to correspond to the requests, or produce them as kept in the usual course of business (Rule 34(b)(2)(E)(i)). Bates-number each page.</p>
<p>4. For each request, state whether responsive documents are being withheld on the basis of any objection (Rule 34(b)(2)(C)). For any document withheld as privileged, provide the information required by Rule 26(b)(5)(A) at the time of production.</p>
<p>5. If a responsive document no longer exists, identify it and explain the circumstances of its loss or destruction.</p>
<p>6. The Definitions in Plaintiff's First Set of Interrogatories, served with these requests, apply here and are restated below.</p>
{DEFS}
<h2>Documents Requested</h2>
"""
for i, q in enumerate(RFPS, 1):
    rfp_body += f"<div class='req'><b>REQUEST FOR PRODUCTION NO. {i}:</b>{esc(q)}</div>"
rfp_body += sig() + pos(["Plaintiff's First Set of Requests for Production of Documents to Defendant Federal Express Corporation"])
build("03 - Plaintiff First Set of Requests for Production to FedEx (Set One)", rfp_body, "RFPs Set One")

# ---------------- Rule 45: Attachment A ----------------
FA_REQS = [
 "Each consumer report and investigative consumer report concerning Plaintiff that You prepared for, or furnished to, Federal Express Corporation, FedEx Ground Package System, Inc., or any other FedEx entity (together, \"FedEx\") at any time from January 1, 2019 through the present, in every version and in the form furnished, including all component results and updates.",
 "For each report in Request No. 1, all records of each search performed, including for any sex offender registry search: the database or website queried (for example, the National Sex Offender Public Website, the California Department of Justice Megan's Law website, or another source); the raw result returned; the \"source of record\" information; and the date and time retrieved.",
 "Order records for each report in Request No. 1, including the package ordered, each component, the requesting FedEx user or account, and the dates ordered and completed.",
 "All records of any adjudication, scoring, or eligibility determination applied to each report in Request No. 1, including the \"client criteria\" or matrix applied and the resulting score.",
 "All communications with FedEx concerning Plaintiff, including portal messages, emails, adjudication notes, and status updates.",
 "Each pre-adverse action and adverse-action notice sent to Plaintiff on behalf of FedEx, with enclosures, and records showing when each was sent and when Plaintiff accessed any portal link.",
 "All disclosure and authorization forms concerning Plaintiff that You received or maintain in connection with any FedEx order, and records of any request by Plaintiff for a copy of a report.",
 "Documents sufficient to show, for the period January 1, 2024 through March 31, 2025, how the search labeled \"National Sex Offender Registry\" or \"National Sex Offender Registry Search - Department of Justice Web Site\" retrieves records of California registrants, including whether it queries the National Sex Offender Public Website, the California Megan's Law website, or a database compiled from either.",
 "Documents sufficient to show the terms of any agreement between You and FedEx in effect during 2024 or 2025 that govern sex offender registry searches for California applicants or compliance with California Penal Code section 290.46.",
]
att_body = f"""
<h2>Attachment A to Subpoena to Produce Documents<br>First Advantage Background Services Corp.</h2>
<p style="text-align:center"><i>Newanforbi v. Federal Express Corporation</i>, E.D. Cal. {CASE}</p>
<h3>Definitions</h3>
<p>1. "You" and "Your" mean First Advantage Background Services Corp. and its affiliates that prepared or furnished background reports to FedEx.</p>
<p>2. "Plaintiff" means Brendan Ngehsi Newanforbi, including under any variation of that name (for example, Brendan Ngwa Nforbi, Brendan Ngwanforbi, Brendan Ngehsi Ngwa-Nforbi, or Ngwa-Nforbi).</p>
<p>3. "Document" has the broadest meaning allowed by Fed. R. Civ. P. 34(a)(1)(A) and includes electronically stored information.</p>
<h3>Instructions</h3>
<p>1. Produce responsive documents in Your possession, custody, or control. Produce electronically stored information as searchable PDF, or in native form for logs and data.</p>
<p>2. <b>No appearance is required.</b> You may comply by mailing or securely emailing true copies of the documents, with the completed Declaration of Custodian of Records (Attachment B), to: Brendan Ngehsi Newanforbi, 1455 Cat Tail Drive, Stockton, California 95204; bnn.cdl@gmail.com, on or before the date stated on the subpoena.</p>
<p>3. Plaintiff is the consumer to whom these records relate. Plaintiff consents to Your disclosure of his own consumer file and report records to him for purposes of this action.</p>
<p>4. If You withhold any document on a claim of privilege or protection, provide the information required by Fed. R. Civ. P. 45(e)(2)(A).</p>
<p>5. Plaintiff will reimburse the reasonable copying costs of production on request. Please contact Plaintiff at bnn.cdl@gmail.com with any question about the scope or format of production before the compliance date.</p>
<h3>Documents to Be Produced</h3>
"""
for i, q in enumerate(FA_REQS, 1):
    att_body += f"<div class='req'><b>REQUEST NO. {i}:</b>{esc(q)}</div>"
att_body += f"""
<div class="pb"></div>
<h2>Attachment B<br>Declaration of Custodian of Records<br>(Fed. R. Evid. 902(11), 803(6))</h2>
<p style="text-align:center"><i>Newanforbi v. Federal Express Corporation</i>, E.D. Cal. {CASE}</p>
<p>I, ____________________________________, declare:</p>
<p>1. I am employed by First Advantage Background Services Corp. as ____________________________________, and I am a custodian of records, or am otherwise qualified by my position, to make this declaration.</p>
<p>2. The records produced with this declaration, consisting of ________ pages (Bates or other identification: ______________________), are true copies of records that were (a) made at or near the time of the acts, events, or conditions they record, by, or from information transmitted by, someone with knowledge; (b) kept in the course of a regularly conducted activity of First Advantage; and (c) made as a regular practice of that activity.</p>
<p>3. &#9744; A diligent search was made, and no records responsive to Request No(s). ______________ were found.</p>
<p>I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct.</p>
<p>Executed on ______________, 20___, at ______________________.</p>
<div class="sig"><br>____________________________________<br>Signature<br><br>____________________________________<br>Printed name and title</div>
"""
build("04 - Rule 45 Subpoena Attachments A and B - First Advantage", att_body, "Subpoena Attachments")

# ---------------- Rule 45(a)(4) notice ----------------
notice_body = caption("NOTICE OF SUBPOENA TO PRODUCE DOCUMENTS TO NONPARTY FIRST ADVANTAGE BACKGROUND SERVICES CORP.", "<br><br>(Fed. R. Civ. P. 45(a)(4))")
notice_body += f"""
<p>TO DEFENDANT FEDERAL EXPRESS CORPORATION AND ITS ATTORNEY OF RECORD:</p>
<p>PLEASE TAKE NOTICE that, under Federal Rule of Civil Procedure 45(a)(4), Plaintiff Brendan Ngehsi Newanforbi will serve the attached Subpoena to Produce Documents, Information, or Objects (Form AO 88B), with its Attachments A and B, on nonparty First Advantage Background Services Corp. The subpoena commands production of the documents described in Attachment A on or before the date stated on the subpoena, by mail or secure electronic delivery to Plaintiff at 1455 Cat Tail Drive, Stockton, California 95204. No appearance or deposition is commanded.</p>
<p>A copy of the subpoena and its attachments is served with this notice, before the subpoena is served on the nonparty. Plaintiff will make any documents produced in response available to Defendant for copying on request.</p>
{sig()}
{pos(["Notice of Subpoena to Produce Documents to Nonparty First Advantage Background Services Corp., with a copy of the Subpoena (AO 88B) and Attachments A and B"])}
"""
build("05 - Rule 45(a)(4) Notice of Subpoena to FedEx", notice_body, "Notice of Subpoena")
