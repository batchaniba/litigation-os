from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from pypdf import PdfReader, PdfWriter


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[1]
OUT = ROOT / "internal" / "docs" / "matter-25" / "discovery" / "first-wave-2026-09-25"
OUT.mkdir(parents=True, exist_ok=True)

CASE = "2:26-cv-02881-DAD-SCR"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
DEFENDANT = "FEDERAL EXPRESS CORPORATION"


def set_cell_margins(cell, top=60, start=80, bottom=60, end=80):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, val in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)


def add_page_field(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run("Page ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    paragraph._p.append(fld)


def configure(doc):
    sec = doc.sections[0]
    sec.top_margin = Inches(0.72)
    sec.bottom_margin = Inches(0.72)
    sec.left_margin = Inches(0.85)
    sec.right_margin = Inches(0.85)
    sec.header_distance = Inches(0.3)
    sec.footer_distance = Inches(0.35)
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08
    for name in ["Title", "Heading 1", "Heading 2"]:
        st = styles[name]
        st.font.name = "Times New Roman"
        st._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        st.font.color.rgb = None
    styles["Title"].font.size = Pt(13)
    styles["Title"].font.bold = True
    styles["Heading 1"].font.size = Pt(11)
    styles["Heading 1"].font.bold = True
    styles["Heading 1"].paragraph_format.space_before = Pt(10)
    styles["Heading 1"].paragraph_format.space_after = Pt(5)
    add_page_field(sec.footer.paragraphs[0])


def add_contact(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    for line in [
        "BRENDAN NGEHSI NEWANFORBI",
        "Plaintiff, In Pro Per",
        "1455 Cat Tail Drive",
        "Stockton, California 95204",
        "Telephone: (209) 801-4442",
        "Email: bnn.cdl@gmail.com",
    ]:
        r = p.add_run(line + "\n")
        r.font.size = Pt(10)
    return p


def add_caption(doc, title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run("UNITED STATES DISTRICT COURT")
    r.bold = True
    r.font.size = Pt(11)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(9)
    r = p.add_run("EASTERN DISTRICT OF CALIFORNIA")
    r.bold = True
    r.font.size = Pt(11)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(3.1)
    table.columns[1].width = Inches(3.65)
    left, right = table.rows[0].cells
    left.width = Inches(3.1)
    right.width = Inches(3.65)
    for c in (left, right):
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
        set_cell_margins(c, top=80, start=90, bottom=80, end=90)
    lp = left.paragraphs[0]
    lp.add_run("BRENDAN NGEHSI NEWANFORBI,\n\n").bold = True
    lp.add_run("                     Plaintiff,\n\nv.\n\n")
    lp.add_run("FEDERAL EXPRESS CORPORATION,\n").bold = True
    lp.add_run("and DOES 1 through 10, inclusive,\n\n                     Defendants.")
    rp = right.paragraphs[0]
    rp.add_run(f"Case No. {CASE}\n\n").bold = True
    t = rp.add_run(title.upper())
    t.bold = True
    rp.add_run("\n\nAssigned to Hon. Dale A. Drozd\nMagistrate Judge Sean C. Riordan")
    # use solid black caption borders
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = OxmlElement(f"w:{edge}")
        tag.set(qn("w:val"), "single")
        tag.set(qn("w:sz"), "8")
        tag.set(qn("w:color"), "000000")
        borders.append(tag)
    tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def add_title(doc, title):
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    p.add_run(title)


def add_numbered_items(doc, items, label):
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.22)
        p.paragraph_format.first_line_indent = Inches(-0.22)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(f"{label} NO. {i}: ")
        r.bold = True
        p.add_run(text)


def add_signature(doc, date="September 25, 2026"):
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run(f"Dated: {date}\n\n")
    p.add_run("/s/ Brendan Ngehsi Newanforbi\n").bold = True
    p.add_run("BRENDAN NGEHSI NEWANFORBI\nPlaintiff, In Pro Per")


def add_certificate(doc, document_title):
    doc.add_page_break()
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Certificate of Service")
    p = doc.add_paragraph()
    p.add_run("I declare that on September 25, 2026, I served a true copy of ").bold = False
    p.add_run(document_title).bold = True
    p.add_run(" on counsel for Defendant Federal Express Corporation as indicated below:")
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    p.add_run("Allison A. Kray, Senior Attorney\nFederal Express Corporation Legal Department\n2601 Main Street, Suite 1100\nIrvine, California 92614\nallison.kray@fedex.com")
    p = doc.add_paragraph()
    p.add_run("[  ] By email, pursuant to the parties' written agreement to electronic service.\n")
    p.add_run("[  ] By first-class United States mail, postage fully prepaid.")
    p = doc.add_paragraph()
    p.add_run("I declare under penalty of perjury under the laws of the United States that the foregoing is true and correct. Executed on September 25, 2026, at ____________________, California.\n\n")
    p.add_run("__________________________________\nBRENDAN NGEHSI NEWANFORBI")


def add_definitions(doc):
    doc.add_paragraph("These requests use the following definitions solely for discovery:")
    defs = [
        ("You, Your, Defendant, or FedEx", "Federal Express Corporation and its employees, agents, representatives, departments, databases, and persons acting on its behalf concerning Plaintiff's application or background screening."),
        ("Plaintiff", "Brendan Ngehsi Newanforbi."),
        ("2025 Application", "Plaintiff's application completed on or about January 8, 2025, associated with FEDEX GROUND HR, the March 10, 2025 pre-adverse-action notice, and the March 19, 2025 adverse action."),
        ("Report", "every consumer report, investigative consumer report, background-screening result, component result, source record, attachment, score, adjudication result, notice, and updated version concerning Plaintiff that First Advantage prepared, maintained, or transmitted in connection with the 2025 Application."),
        ("Registry Information", "information identifying or describing Plaintiff as a sex-offender registrant, or referring to NSOPW, the National Sex Offender Public Website, a national sex-offender-registry search, the California Sex Offender Registry, California's Megan's Law website, Penal Code section 220(a)(1), or registration status."),
        ("Prior FedEx Application", "every application by Plaintiff before the 2025 Application for employment or engagement with Defendant or a FedEx-affiliated entity whose records are in Defendant's possession, custody, or control."),
        ("Document", "the broad meaning in Federal Rule of Civil Procedure 34(a), including electronically stored information, native files, email, messaging, database entries, audit logs, metadata, reports, notes, and paper records."),
        ("Identify a person", "state the person's name, title, employer, role concerning the subject matter, and last known business contact information."),
        ("Identify a document", "state its date, author, recipients, title or description, custodian, and Bates number if produced."),
    ]
    for term, meaning in defs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.add_run(term + ": ").bold = True
        p.add_run(meaning)


def make_discovery(title, intro, items, label, filename, include_definitions=True):
    doc = Document()
    configure(doc)
    add_contact(doc)
    add_caption(doc, title)
    add_title(doc, title)
    p = doc.add_paragraph(intro)
    p.paragraph_format.first_line_indent = Inches(0.3)
    if include_definitions:
        doc.add_paragraph("Definitions", style="Heading 1")
        add_definitions(doc)
    doc.add_paragraph("Instructions", style="Heading 1")
    for s in [
        "Respond separately and fully in writing within 30 days after service, subject to any different deadline fixed by rule, stipulation, or court order.",
        "If you object to any portion, state the specific ground and respond to every unobjectionable portion. Do not withhold responsive material based only on a general objection.",
        "If information is unavailable after a reasonable inquiry, describe the inquiry and state what information remains unavailable.",
        "These requests are continuing to the extent required by Federal Rule of Civil Procedure 26(e).",
    ]:
        p = doc.add_paragraph(style=None)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.add_run("- ")
        p.add_run(s)
    doc.add_paragraph(title, style="Heading 1")
    add_numbered_items(doc, items, label)
    add_signature(doc)
    add_certificate(doc, title)
    path = OUT / filename
    doc.save(path)
    return path


interrogatories = [
    "State verbatim each question, instruction, certification, or statement in the 2025 Application that Defendant contends Plaintiff answered falsely or misleadingly, state Plaintiff's answer, and state the complete factual basis for the contention that the answer was false, misleading, and material.",
    "State the date on which Defendant first learned of each alleged misrepresentation identified in response to Interrogatory No. 1 and identify each person who first learned of it.",
    "Identify every person who participated in, recommended, approved, reviewed, or communicated about the decision to issue the March 10, 2025 pre-adverse-action notice or the March 19, 2025 final adverse action.",
    "State every reason Defendant considered or relied upon in deciding not to hire Plaintiff in connection with the 2025 Application.",
    "Identify every contemporaneous document that records, reflects, or communicates a reason for the adverse action on the 2025 Application.",
    "State whether Defendant contends it would have taken the same adverse action if the Report had contained no Registry Information, and state every fact supporting that contention.",
    "Identify each Prior FedEx Application, including the approximate date, position, facility, employing or engaging FedEx entity, outcome, and whether Plaintiff began work.",
    "For each Prior FedEx Application that resulted in Plaintiff being hired or beginning work, state whether Defendant contends Plaintiff gave the same or a materially similar answer to the application question at issue in Interrogatory No. 1.",
    "Identify every First Advantage product, package, search component, database, and adjudication service Defendant ordered or caused to be ordered in connection with the 2025 Application.",
    "Describe all information from the Report that any FedEx person or system accessed, displayed, downloaded, reviewed, transmitted, or used before the March 19, 2025 adverse action.",
    "Identify every person who accessed, reviewed, downloaded, or received the Report or any component result, and state the date and purpose of each access known to Defendant.",
    "State Defendant's understanding of the relationship, if any, between the NSOPW or national sex-offender search result and the California sex-offender-registry or Megan's Law information referenced in Plaintiff's Report.",
    "State every fact supporting Defendant's affirmative defense that Registry Information was used to protect a person at risk under California Penal Code section 290.46(j)(1), including the identity or description of the person allegedly at risk and the particular risk asserted.",
    "Identify every federal, state, or local law that Defendant contends required or authorized it to obtain or use Registry Information for the position associated with the 2025 Application.",
    "Identify each policy, guideline, matrix, instruction, training material, or decision rule in effect from January through March 2025 concerning sex-offender-registry information, application misrepresentations, criminal history, or adjudication of FedEx Ground applicants.",
    "Describe each communication between Defendant and First Advantage concerning Plaintiff, the 2025 Application, the Report, adjudication, pre-adverse action, final adverse action, or any dispute or reinvestigation.",
    "Identify the FedEx entity, business unit, and department that made the conditional offer and adverse-action decision, and explain the role of FEDEX GROUND HR in those decisions.",
    "State the position title, facility, anticipated start date, pay rate, expected weekly hours, shift, benefits, and duration associated with the conditional employment opportunity withdrawn in March 2025.",
    "Describe the steps Defendant has taken to preserve documents and electronically stored information concerning Plaintiff's applications, prior FedEx work, the 2025 Application, the Report, and the adverse-action decision, without disclosing privileged communications.",
    "State the complete factual basis for Defendant's seventh affirmative defense, including its assertion that Plaintiff answered 'NO' to questions concerning sex-based offenses.",
    "State the complete factual basis for Defendant's eighth affirmative defense under Penal Code section 290.46(j)(1).",
]

rfas = [
    "Admit that Plaintiff completed an employment application associated with FEDEX GROUND HR in January 2025.",
    "Admit that Defendant caused First Advantage to conduct a background screening concerning Plaintiff in connection with the 2025 Application.",
    "Admit that First Advantage provided a Report concerning Plaintiff to Defendant on or before March 10, 2025.",
    "Admit that Plaintiff received a pre-adverse-action notice on or about March 10, 2025 because Defendant was considering information in the Report.",
    "Admit that Defendant withdrew Plaintiff's conditional employment opportunity on or about March 19, 2025.",
    "Admit that the Report referenced the National Sex Offender Public Website or a national sex-offender-registry search.",
    "Admit that the Report referenced the California sex-offender website or California Sex Offender Registry.",
    "Admit that the Report identified a conviction under California Penal Code section 220(a)(1).",
    "Admit that the Report identified Plaintiff as a person required to register as a sex offender in California.",
    "Admit that at least one FedEx employee or agent reviewed Registry Information concerning Plaintiff before the March 19, 2025 adverse action.",
    "Admit that Registry Information was considered in connection with the 2025 Application.",
    "Admit that Defendant was not required by law to conduct a sex-offender-registry search for the position associated with the 2025 Application.",
    "Admit that no law categorically prohibited Defendant from hiring Plaintiff for the position associated with the 2025 Application.",
    "Admit that the position associated with the 2025 Application did not require Plaintiff to work directly and unaccompanied with minor children on more than an incidental basis.",
    "Admit that neither the pre-adverse-action notice nor the final adverse-action notice identified a particular person allegedly at risk from Plaintiff's employment.",
    "Admit that neither the pre-adverse-action notice nor the final adverse-action notice stated that Plaintiff was rejected because of an application misrepresentation.",
    "Admit that Defendant's Answer alleges that Plaintiff answered 'NO' to an application question concerning sex-based offenses.",
    "Admit that Defendant did not ask Plaintiff to explain or correct the alleged application misrepresentation before taking final adverse action.",
    "Admit that Plaintiff had previously applied for employment or engagement with a FedEx entity before the 2025 Application.",
    "Admit that Plaintiff had previously been hired or permitted to begin work for a FedEx entity before the 2025 Application.",
    "Admit that Defendant or a FedEx-affiliated entity possesses records of Plaintiff's prior FedEx applications or work.",
    "Admit that First Advantage performed the 2025 background screening at Defendant's request and for Defendant's employment purposes.",
    "Admit that Defendant possesses no contemporaneous document created before March 19, 2025 stating that an application misrepresentation, standing alone, required rejection of Plaintiff.",
    "Admit that Defendant contends it would have rejected Plaintiff even if the Report had contained no Registry Information.",
    "Admit that the assertion in Request No. 24 depends on information Defendant knew before the March 19, 2025 adverse action.",
    "Admit that Defendant has not identified any person to Plaintiff who was allegedly protected from risk by denying Plaintiff the position.",
    "Admit that Defendant's September 24, 2026 status report states that Plaintiff's application contained material misrepresentations that independently justified the hiring decision.",
    "Admit that Defendant's claim of an independent justification can be evaluated from Defendant's application, screening, adjudication, and decision records.",
]

rfps = [
    "Produce the complete 2025 Application in native form and in a readable export, including every question, answer, certification, timestamp, revision, audit field, and attachment.",
    "Produce every Prior FedEx Application and every associated offer, onboarding, hiring, screening, assignment, work, separation, and rehire-eligibility record concerning Plaintiff.",
    "Produce Plaintiff's complete recruiting, applicant-tracking, candidate, personnel, contractor, vendor, and human-resources files maintained by Defendant or FEDEX GROUND HR.",
    "Produce the complete Report exactly as Defendant received or accessed it, including every version, page, component, attachment, source record, warning, disclaimer, score, status, and adjudication result.",
    "Produce all documents reflecting the First Advantage products, packages, searches, databases, adjudication rules, client configurations, and instructions ordered or applied to the 2025 Application.",
    "Produce all source records, raw results, underlying hits, links, screenshots, or data furnished with or accessible through the Report, including records referencing NSOPW, a national registry, the California registry, California's Megan's Law website, Penal Code section 220(a)(1), or registration status.",
    "Produce all communications between Defendant and First Advantage concerning Plaintiff, the 2025 Application, the Report, screening status, adjudication, pre-adverse action, final adverse action, or any dispute or reinvestigation.",
    "Produce all audit logs showing when, how, and by whom the Report or any component result was ordered, received, displayed, accessed, opened, downloaded, transmitted, evaluated, or changed.",
    "Produce all documents identifying or recording every reason code, decision code, score, matrix result, workflow status, recommendation, or explanation associated with Plaintiff's conditional offer or adverse action.",
    "Produce all internal communications, notes, messages, memoranda, tickets, and meeting records concerning Plaintiff's application, background screening, conditional offer, alleged misrepresentation, Registry Information, or adverse action.",
    "Produce every document supporting Defendant's assertion that Plaintiff's application contained one or more material misrepresentations.",
    "Produce every policy, standard, rubric, training material, instruction, or decision rule in effect from January through March 2025 defining a material application misrepresentation or prescribing consequences for one.",
    "Produce all documents showing when Defendant first discovered each alleged misrepresentation and what action Defendant took because of it.",
    "Produce all documents comparing or relating the alleged misrepresentation in the 2025 Application to any answer Plaintiff gave in a Prior FedEx Application.",
    "Produce every policy, guideline, instruction, training material, or compliance communication in effect from January through March 2025 concerning sex-offender-registry information, NSOPW, California's Megan's Law website, Penal Code section 290.46, or the use of registry data in employment decisions.",
    "Produce the background-screening and adjudication policies, matrices, workflows, and client instructions applied to applicants for the position associated with the 2025 Application.",
    "Produce all nonprivileged warnings, notices, compliance materials, or terms supplied by First Advantage to Defendant concerning permissible or prohibited uses of the Report or Registry Information.",
    "Produce the job posting, job description, essential functions, location, shift, pay rate, expected hours, benefits, anticipated start date, and reporting structure for the position associated with the 2025 Application.",
    "Produce every document supporting Defendant's contention that denying Plaintiff the position protected a person at risk, including any document identifying the person, class of persons, or particular risk.",
    "Produce every document identifying a federal, state, or local law that Defendant contends required or authorized obtaining or using Registry Information for the position.",
    "Produce every pre-adverse-action and adverse-action notice concerning Plaintiff, together with all enclosures, report copies, rights summaries, transmission records, delivery logs, portal-access logs, and expiration records.",
    "Produce every disclosure, authorization, consent, request-for-copy record, and copy of an investigative consumer report provided or made available to Plaintiff in connection with the 2025 Application.",
    "Produce all documents concerning any open position or replacement hire for the position Plaintiff sought, including the date filled, pay rate, expected hours, and duration of employment, with personal identifiers of any nonparty applicant redacted.",
    "Produce all nonprivileged documents supporting any affirmative defense that Defendant presently contends bars or reduces Plaintiff's recovery.",
    "Produce any insurance policy or agreement under which an insurer may be liable to satisfy or reimburse all or part of a judgment in this action, subject to Federal Rule of Civil Procedure 26(a)(1)(A)(iv).",
]


make_discovery(
    "Plaintiff's First Set of Interrogatories to Defendant Federal Express Corporation",
    "Pursuant to Federal Rules of Civil Procedure 26 and 33, Plaintiff serves these interrogatories on Defendant Federal Express Corporation. Each answer must be made separately and fully under oath and signed as required by Rule 33(b).",
    interrogatories,
    "INTERROGATORY",
    "01_Plaintiff_Interrogatories_Set_One_to_FedEx.docx",
)

make_discovery(
    "Plaintiff's First Set of Requests for Admission to Defendant Federal Express Corporation",
    "Pursuant to Federal Rules of Civil Procedure 26 and 36, Plaintiff requests that Defendant Federal Express Corporation admit or deny the following matters. If Defendant cannot truthfully admit or deny a matter in full, it must admit the portion that is true and specifically deny or qualify the remainder.",
    rfas,
    "REQUEST FOR ADMISSION",
    "02_Plaintiff_Requests_for_Admission_Set_One_to_FedEx.docx",
)

make_discovery(
    "Plaintiff's First Set of Requests for Production to Defendant Federal Express Corporation",
    "Pursuant to Federal Rules of Civil Procedure 26 and 34, Plaintiff requests that Defendant Federal Express Corporation produce the following documents and electronically stored information. Production may be made by secure electronic transfer in searchable PDF form, with spreadsheets, databases, audit logs, and structured data produced in reasonably usable native form.",
    rfps,
    "REQUEST FOR PRODUCTION",
    "03_Plaintiff_Requests_for_Production_Set_One_to_FedEx.docx",
)


def make_notice():
    title = "Plaintiff's Notice of Intent to Serve Rule 45 Subpoena on First Advantage Background Services Corp."
    doc = Document()
    configure(doc)
    add_contact(doc)
    add_caption(doc, title)
    add_title(doc, title)
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(0.3)
    p.add_run("PLEASE TAKE NOTICE ").bold = True
    p.add_run("that, pursuant to Federal Rule of Civil Procedure 45(a)(4), Plaintiff intends to serve the attached subpoena duces tecum on nonparty First Advantage Background Services Corp. after the subpoena has been issued by the Clerk. The subpoena seeks Plaintiff's own March 2025 FedEx background-screening report, source and audit records, notices, and communications concerning that screening. A copy of the proposed subpoena and Attachment A is served with this notice before service on the nonparty.")
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(0.3)
    p.add_run("The proposed compliance date is October 23, 2026. Production may be made securely and electronically. No appearance or testimony is commanded.")
    add_signature(doc)
    add_certificate(doc, title)
    path = OUT / "04_Notice_of_Intent_to_Serve_First_Advantage_Subpoena.docx"
    doc.save(path)
    return path


def make_attachment():
    doc = Document()
    configure(doc)
    add_contact(doc)
    add_caption(doc, "Attachment A to Rule 45 Subpoena to First Advantage Background Services Corp.")
    add_title(doc, "Attachment A Document Requests and Production Instructions")
    doc.add_paragraph("Consumer identification", style="Heading 1")
    for line in [
        "Name: Brendan Ngehsi Newanforbi",
        "Date of birth: September 16, 1996",
        "Email used for the application: bnn.cdl@gmail.com",
        "Client or employer: FEDEX GROUND HR / Federal Express Corporation",
        "Application completed: on or about January 8, 2025",
        "Pre-adverse-action notice: on or about March 10, 2025",
        "Final adverse action: on or about March 19, 2025",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.add_run(line)
    doc.add_paragraph("Definitions and instructions", style="Heading 1")
    for text in [
        "Report means every consumer report, investigative consumer report, background-screening result, component result, attachment, source record, updated report, score, status, and adjudication result concerning the identified consumer and the FedEx screening described above.",
        "Produce records as kept in the ordinary course of business. Produce searchable PDFs for documents and reasonably usable native files for spreadsheets, databases, structured exports, and audit logs. Preserve metadata showing creation, modification, access, transmission, and status-change dates.",
        "Personal identifiers may be transmitted through a secure portal or encrypted transfer. No records concerning another consumer are requested.",
        "If any responsive record no longer exists, produce any retention, deletion, purge, or destruction record sufficient to identify what was removed and when.",
        "Production may be made by secure electronic transfer to bnn.cdl@gmail.com. Please contact Plaintiff at (209) 801-4442 to arrange a secure transfer if necessary.",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.add_run("- ")
        p.add_run(text)
    doc.add_paragraph("Documents to be produced", style="Heading 1")
    reqs = [
        "The complete Report exactly as furnished or made available to FEDEX GROUND HR or Federal Express Corporation, including every version, page, component, attachment, warning, disclaimer, score, status, and adjudication result.",
        "Every source record, raw result, data return, screenshot, link, or underlying hit used to create the Report, including records referencing NSOPW, a national sex-offender-registry search, the California Sex Offender Registry, California's Megan's Law website, Penal Code section 220(a)(1), or registration status.",
        "All records identifying the source, vendor, database, jurisdiction, query, search term, search date, retrieval method, and chain of transmission for each criminal-history or sex-offender-registry component of the Report.",
        "The complete order record and client configuration for the screening, including products and packages ordered, search components, adjudication criteria, client-specific rules, instructions, and result or eligibility codes applied.",
        "All audit logs showing when the screening was ordered, searched, completed, changed, delivered, displayed, accessed, opened, downloaded, or transmitted, including the identity or account identifier of each FedEx or First Advantage user involved.",
        "All communications with FEDEX GROUND HR, Federal Express Corporation, or any FedEx-affiliated user concerning the consumer, the application, the Report, any component result, adjudication, pre-adverse action, final adverse action, dispute, or reinvestigation.",
        "Every pre-adverse-action and final adverse-action notice generated, transmitted, hosted, or maintained by First Advantage, including all enclosures, rights summaries, report copies, transmission records, delivery records, portal-access logs, and expiration records.",
        "Every disclosure, authorization, consent, certification, request-for-copy record, and record showing whether or when a copy of the Report was provided or made available to the consumer.",
        "Every record reflecting any manual review, quality-control review, matching decision, suppression, dispute, reinvestigation, correction, update, or communication concerning the Report.",
        "Every nonprivileged warning, disclaimer, compliance notice, instruction, or term supplied to FedEx with the Report concerning permissible or prohibited employment use of criminal-history or sex-offender-registry information, including California Penal Code section 290.46.",
        "Records sufficient to identify every person or organizational unit at First Advantage that collected, reviewed, approved, transmitted, or maintained the Report.",
        "The consumer's complete file maintained by First Advantage concerning the March 2025 FedEx screening, including the recipients of each report or file disclosure.",
    ]
    add_numbered_items(doc, reqs, "REQUEST")
    doc.add_paragraph("Optional custodian certification", style="Heading 1")
    doc.add_paragraph("If First Advantage elects to provide one, Plaintiff requests a declaration from a qualified records custodian authenticating the production under Federal Rules of Evidence 803(6), 902(11), and 902(13). This request does not require creation of a declaration if First Advantage does not ordinarily provide one.")
    path = OUT / "05_First_Advantage_Subpoena_Attachment_A.docx"
    doc.save(path)
    return path


def make_clerk_request():
    doc = Document()
    configure(doc)
    add_contact(doc)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.add_run("September 25, 2026")
    p = doc.add_paragraph()
    p.add_run("Clerk of Court\nUnited States District Court\nEastern District of California\n501 I Street, Room 4-200\nSacramento, California 95814")
    p = doc.add_paragraph()
    p.add_run(f"Re: Newanforbi v. Federal Express Corporation, Case No. {CASE}").bold = True
    add_title(doc, "Request for Issuance of AO 88B Subpoena")
    for text in [
        "Dear Clerk:",
        "I am the self-represented Plaintiff in the above-captioned action. Under Federal Rule of Civil Procedure 45(a)(3), I respectfully request issuance of the enclosed AO 88B subpoena directed to First Advantage Background Services Corp.",
        "The subpoena seeks documents only and does not command attendance. I have enclosed the proposed subpoena, its Attachment A, and a self-addressed stamped envelope for return of the issued subpoena. If the Clerk requires an otherwise blank signed subpoena instead, please issue and return the enclosed AO 88B so that I may complete it before service.",
        "Thank you for your assistance.",
    ]:
        p = doc.add_paragraph(text)
        if text not in ("Dear Clerk:", "Thank you for your assistance."):
            p.paragraph_format.first_line_indent = Inches(0.3)
    add_signature(doc)
    doc.add_paragraph("Enclosures:\n1. AO 88B subpoena\n2. Attachment A\n3. Self-addressed stamped return envelope")
    path = OUT / "06_Request_to_Clerk_for_Issuance_of_AO88B_Subpoena.docx"
    doc.save(path)
    return path


make_notice()
make_attachment()
make_clerk_request()


def fill_ao88b():
    src = ROOT / "internal" / "public" / "documents" / "_form-library" / "AO88B-Subpoena-to-Produce-Documents.pdf"
    dst = OUT / "07_Proposed_AO88B_First_Advantage_Subpoena_UNSIGNED.pdf"
    reader = PdfReader(src)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    values = {
        "District Information": "         Eastern District of California",
        "Attorney_Information": "BRENDAN NGEHSI NEWANFORBI, Plaintiff In Pro Per\n1455 Cat Tail Drive, Stockton, CA 95204\n(209) 801-4442 | bnn.cdl@gmail.com",
        "Plaintiff": "BRENDAN NGEHSI NEWANFORBI",
        "Defendant": "FEDERAL EXPRESS CORPORATION, et al.",
        "Case_Num": CASE,
        "Subpoena_To": "FIRST ADVANTAGE BACKGROUND SERVICES CORP.\nAttn: Legal Department / Custodian of Records\n1 Concourse Parkway NE, Suite 200\nAtlanta, GA 30328",
        "check_1": "/Production",
        "Sampling_Material": "See Attachment A, incorporated into this subpoena.",
        "Production_Place": "First Advantage Legal Dept., 1 Concourse Pkwy NE, Ste. 200, Atlanta, GA 30328; secure electronic production permitted.",
        "Production_DateTime": "10/23/2026 5:00 pm ET",
    }
    writer.update_page_form_field_values(None, values, auto_regenerate=True)
    writer.set_need_appearances_writer(True)
    with dst.open("wb") as f:
        writer.write(f)
    return dst


fill_ao88b()
