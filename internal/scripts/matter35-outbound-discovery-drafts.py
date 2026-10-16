from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt


OUT = Path("output/discovery")
OUT.mkdir(parents=True, exist_ok=True)

PLAINTIFF = "Brendan Ngwa Nforbi"
CASE = "26CV501995"
COURT = "SUPERIOR COURT OF CALIFORNIA\nCOUNTY OF SANTA CLARA"
CAPTION = "BRENDAN NGWA NFORBI, Plaintiff,\nv.\nROSS STORES, INC.; ROSS DRESS FOR LESS, INC.; DOE 1; and DOES 2 through 20, inclusive, Defendants."


RFAS = [
    "Admit that YOU operated the STORE on August 25, 2026.",
    "Admit that DOE 1 was working at the STORE during the INCIDENT.",
    "Admit that DOE 1 was employed by YOU during the INCIDENT.",
    "Admit that DOE 1 was performing services for YOUR benefit during the INCIDENT.",
    "Admit that DOE 1 was acting within the course and scope of duties performed for YOU during the INCIDENT.",
    "Admit that the cashier who observed the INCIDENT was employed by YOU.",
    "Admit that YOU controlled, operated, or had access to the surveillance system that recorded the INCIDENT.",
    "Admit that the beverage carried by Plaintiff was the sole merchandise-related basis for DOE 1's interaction with Plaintiff.",
    "Admit that DOE 1 did not observe Plaintiff select the beverage from merchandise displayed for sale at the STORE.",
    "Admit that DOE 1 did not observe Plaintiff conceal the beverage.",
    "Admit that DOE 1 did not observe Plaintiff remove the beverage from a shelf, display, refrigerator, or other merchandise area at the STORE.",
    "Admit that no employee reported observing Plaintiff take the beverage from the STORE.",
    "Admit that YOU have no record establishing that the beverage carried by Plaintiff was merchandise belonging to YOU.",
    "Admit that no electronic article-surveillance alarm sounded as Plaintiff approached the customer exit.",
    "Admit that no Ross merchandise was recovered from Plaintiff.",
    "Admit that no employee searched Plaintiff during the INCIDENT.",
    "Admit that no employee requested a receipt from Plaintiff during the INCIDENT.",
    "Admit that no employee contacted law enforcement concerning Plaintiff during the INCIDENT.",
    "Admit that no police report was created concerning the INCIDENT.",
    "Admit that no employee checked inventory records before DOE 1 initiated the interaction with Plaintiff.",
    "Admit that no employee checked sales records before DOE 1 initiated the interaction with Plaintiff.",
    "Admit that YOU do not contend that Plaintiff possessed unpaid merchandise belonging to YOU during the INCIDENT.",
    "Admit that Plaintiff was proceeding toward the customer exit when DOE 1 initiated the interaction.",
    "Admit that DOE 1 positioned herself between Plaintiff and the nearest customer exit during at least part of the INCIDENT.",
    "Admit that DOE 1 questioned Plaintiff about whether he had paid for the beverage.",
    "Admit that the interaction continued after Plaintiff stated that the beverage came from another store.",
    "Admit that surveillance cameras recorded Plaintiff entering the STORE on August 25, 2026.",
    "Admit that surveillance cameras recorded the interaction between Plaintiff and DOE 1.",
    "Admit that surveillance cameras recorded Plaintiff leaving the STORE.",
    "Admit that YOU possessed RESPONSIVE VIDEO when YOU first received notice of this lawsuit.",
    "Admit that YOU have preserved all RESPONSIVE VIDEO in native format with available metadata.",
    "Admit that no written policy in effect during the INCIDENT authorized an employee to question a customer solely because the customer possessed an openly carried beverage.",
    "Admit that no incident report concerning Plaintiff was prepared before YOU received notice of this lawsuit.",
    "Admit that YOU have not identified any item of unpaid Ross merchandise that Plaintiff possessed during the INCIDENT.",
]


SROGS = [
    "IDENTIFY DOE 1.",
    "IDENTIFY the entity that employed DOE 1 during the INCIDENT.",
    "State DOE 1's job title during the INCIDENT.",
    "State DOE 1's principal duties during the INCIDENT.",
    "IDENTIFY DOE 1's immediate supervisor during the INCIDENT.",
    "IDENTIFY the cashier who observed the INCIDENT.",
    "IDENTIFY the manager on duty at the STORE during the INCIDENT.",
    "IDENTIFY the person responsible for loss-prevention supervision at the STORE during the INCIDENT.",
    "IDENTIFY each person who communicated with DOE 1 about Plaintiff before Plaintiff left the STORE.",
    "IDENTIFY the person most knowledgeable about the surveillance system operating at the STORE during the INCIDENT.",
    "IDENTIFY each third-party vendor that maintained, hosted, stored, or exported surveillance recordings for the STORE during the INCIDENT.",
    "State Rachel De la Cruz's job title on October 8, 2026.",
    "IDENTIFY Rachel De la Cruz's employer on October 8, 2026.",
    "State the authority under which Rachel De la Cruz verified YOUR Answer in this action.",
    "State whether Rachel De la Cruz was present at the STORE during the INCIDENT.",
    "State every observation DOE 1 made of Plaintiff before initiating the interaction.",
    "State the words DOE 1 used to initiate the interaction with Plaintiff.",
    "State the words DOE 1 used concerning the beverage carried by Plaintiff.",
    "State the words Plaintiff used to explain where he obtained the beverage.",
    "State DOE 1's position relative to the nearest customer exit during the interaction.",
    "State how the interaction between Plaintiff and DOE 1 ended.",
    "State the duration YOU contend the interaction lasted.",
    "State every fact supporting YOUR contention that Plaintiff remained free to leave throughout the interaction.",
    "State every objective fact that YOU contend supported suspicion that the beverage carried by Plaintiff was unpaid merchandise from the STORE.",
    "State whether any employee checked STORE inventory records before DOE 1 initiated the interaction.",
    "State whether any employee checked STORE sales records before DOE 1 initiated the interaction.",
    "State whether the STORE offered any Celsius-branded beverage for sale on August 25, 2026.",
    "IDENTIFY each Celsius-branded product offered for sale at the STORE on August 25, 2026.",
    "State the number of Celsius-branded units recorded as sold at the STORE on August 25, 2026.",
    "State whether the STORE recorded a shortage of any Celsius-branded product on August 25, 2026.",
    "State the ordinary retention period on August 25, 2026, for surveillance recordings made at the STORE.",
    "State the date on which YOU first preserved or exported RESPONSIVE VIDEO.",
    "IDENTIFY each person who preserved, exported, copied, or downloaded RESPONSIVE VIDEO.",
    "State whether any portion of RESPONSIVE VIDEO is unavailable.",
    "IDENTIFY each person who viewed RESPONSIVE VIDEO before YOUR Answer was served on October 15, 2026.",
]


RFPS = [
    "Produce each native-format recording from any camera depicting Plaintiff entering the STORE on August 25, 2026.",
    "Produce each native-format recording from any camera depicting the interaction between Plaintiff and DOE 1.",
    "Produce each native-format recording from any camera depicting Plaintiff leaving the STORE on August 25, 2026.",
    "Produce each exported, converted, clipped, enhanced, or transmitted version of RESPONSIVE VIDEO.",
    "Produce each still image created from RESPONSIVE VIDEO.",
    "Produce all available metadata associated with RESPONSIVE VIDEO, including creation time, camera identifier, export time, codec, frame rate, resolution, and file hash information.",
    "Produce surveillance-system audit logs showing access, viewing, export, copying, modification, deletion, or overwrite activity involving RESPONSIVE VIDEO.",
    "Produce DOCUMENTS sufficient to identify the location, direction, and field of view of each camera that may have recorded Plaintiff during the INCIDENT.",
    "Produce each surveillance-recording retention policy in effect at the STORE on August 25, 2026.",
    "Produce DOCUMENTS reflecting any deletion, overwrite, loss, corruption, editing, or unavailability of any portion of RESPONSIVE VIDEO.",
    "Produce DOCUMENTS sufficient to identify the surveillance hardware, software, cloud host, and vendor used at the STORE on August 25, 2026.",
    "Produce nonprivileged DOCUMENTS sufficient to show the date on which a litigation hold or preservation instruction concerning the INCIDENT was implemented and the categories of information included.",
    "Produce each incident report, security report, loss-prevention report, customer-contact report, or similar report concerning Plaintiff or the INCIDENT.",
    "Produce each contemporaneous log entry concerning Plaintiff or the INCIDENT.",
    "Produce DOCUMENTS sufficient to show each customer stop, detention, or merchandise inquiry recorded at the STORE on August 25, 2026.",
    "Produce each written, recorded, transcribed, or summarized witness statement concerning the INCIDENT.",
    "Produce communications among STORE employees concerning Plaintiff or the INCIDENT.",
    "Produce communications between STORE management and corporate personnel concerning Plaintiff or the INCIDENT.",
    "Produce nonprivileged communications concerning Plaintiff's request that evidence of the INCIDENT be preserved.",
    "Produce each photograph, diagram, sketch, or reconstruction concerning the INCIDENT.",
    "Produce DOCUMENTS sufficient to show the layout of the entrance, customer exit, registers, and adjacent sales-floor area as they existed during the INCIDENT.",
    "Produce employee schedules, time records, and assignment records sufficient to identify personnel working at the STORE from 8:30 p.m. through 9:30 p.m. on August 25, 2026.",
    "Produce DOCUMENTS sufficient to identify DOE 1, the cashier who observed the INCIDENT, and the manager on duty.",
    "Produce each job description applicable to DOE 1 during the INCIDENT.",
    "Produce DOCUMENTS sufficient to show DOE 1's employer, job title, dates of work at the STORE, and immediate supervisor during the INCIDENT.",
    "Produce each contract or agreement under which a third party supplied security, loss-prevention, or customer-monitoring personnel to the STORE during the INCIDENT.",
    "Produce each policy, procedure, directive, checklist, or training document governing merchant detentions in effect during the INCIDENT.",
    "Produce each policy, procedure, directive, checklist, or training document governing questioning customers about suspected unpaid merchandise in effect during the INCIDENT.",
    "Produce each policy, procedure, directive, checklist, or training document governing customers who enter the STORE carrying outside food, beverages, bags, or merchandise in effect during the INCIDENT.",
    "Produce each receipt-check policy in effect at the STORE during the INCIDENT.",
    "Produce each anti-discrimination, racial-profiling, equal-service, or implicit-bias policy applicable to DOE 1 during the INCIDENT.",
    "Produce each de-escalation or customer-interaction training document applicable to DOE 1 during the INCIDENT.",
    "Produce DOCUMENTS sufficient to show DOE 1's completion, acknowledgment, or receipt of the policies and training requested in Requests Nos. 27 through 32.",
    "Produce DOCUMENTS sufficient to identify each Celsius-branded product or SKU offered for sale at the STORE on August 25, 2026.",
    "Produce DOCUMENTS sufficient to show sales, returns, inventory adjustments, shrink, or reported shortage involving Celsius-branded products at the STORE on August 25, 2026.",
    "Produce DOCUMENTS sufficient to show each customer stop, detention, or merchandise inquiry recorded at the STORE from August 25, 2024, through August 25, 2026, including the date, stated reason, disposition, and any demographic information actually recorded.",
    "Produce each complaint received from August 25, 2021, through August 25, 2026, alleging racial profiling, race discrimination, or unequal customer treatment at the STORE.",
    "Produce each complaint received from August 25, 2021, through August 25, 2026, alleging an unreasonable detention, blocked exit, or unsupported theft inquiry by DOE 1.",
    "Produce nonprivileged DOCUMENTS reflecting any investigation, finding, discipline, counseling, corrective action, or remedial training arising from a complaint responsive to Request No. 37 or 38.",
    "Produce each insurance policy, self-insurance agreement, indemnity agreement, or reservation-of-rights document that may provide coverage for any claim asserted in this action.",
]


DEFINITIONS = [
    ("YOU and YOUR", "the responding defendant and its officers, employees, agents, representatives, departments, divisions, subsidiaries, contractors, and persons acting on its behalf."),
    ("STORE", "the Ross Dress for Less retail location at 119 E. El Camino Real, Sunnyvale, California."),
    ("INCIDENT", "the interaction alleged in the Complaint between Plaintiff and the person identified as DOE 1 at the STORE on August 25, 2026."),
    ("DOE 1", "the person alleged in the Complaint to have questioned or stopped Plaintiff near the customer exit during the INCIDENT."),
    ("RESPONSIVE VIDEO", "every surveillance, security, mobile-device, or other video or audiovisual recording that depicts Plaintiff at the STORE on August 25, 2026, including native recordings, exports, clips, still images, and associated metadata."),
    ("DOCUMENT", "a writing or electronically stored information within the meaning of Evidence Code section 250, including emails, text messages, internal messages, reports, logs, databases, photographs, video, audio, and metadata."),
    ("IDENTIFY", "when used as to a natural person, state the person's full name, employer, job title, business address, business telephone number, and business email address, if known."),
]


def set_cell_margins(cell, top=80, start=100, bottom=80, end=100):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def set_run_font(run, name="Times New Roman", size=12, bold=None, italic=None):
    run.font.name = name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def add_field(paragraph, field_code):
    run = paragraph.add_run()
    fld_char = OxmlElement("w:fldChar")
    fld_char.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = field_code
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char, instr, sep, text, end])
    set_run_font(run, size=9)


def base_doc(draft_footer=True):
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.68)
    sec.bottom_margin = Inches(0.68)
    sec.footer_distance = Inches(0.30)
    sec.left_margin = Inches(0.82)
    sec.right_margin = Inches(0.82)
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
    normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    normal.font.size = Pt(12)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.05
    for sty in ("Title", "Heading 1", "Heading 2"):
        s = styles[sty]
        s.font.name = "Times New Roman"
        s._element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman")
        s._element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
        s.font.color.rgb = None
    if draft_footer:
        p = sec.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run("DRAFT - NOT SERVED   |   Page ")
        set_run_font(r, size=9, italic=True)
        add_field(p, "PAGE")
    return doc


def add_caption(doc, case_title):
    attorney = doc.add_paragraph()
    attorney.paragraph_format.space_after = Pt(5)
    for i, line in enumerate([
        "BRENDAN NGWA NFORBI",
        "1455 Cat Tail Drive",
        "Stockton, California 95204",
        "Telephone: (209) 801-4442",
        "E-mail: bnn.cdl@gmail.com",
        "Plaintiff in Pro Per",
    ]):
        r = attorney.add_run(line)
        set_run_font(r, size=11, bold=(i == 0))
        r.add_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(COURT)
    set_run_font(r, size=12, bold=True)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(3.35)
    table.columns[1].width = Inches(3.35)
    left, right = table.rows[0].cells
    left.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    right.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    set_cell_margins(left, 100, 120, 100, 120)
    set_cell_margins(right, 100, 120, 100, 120)
    lp = left.paragraphs[0]
    lr = lp.add_run(CAPTION)
    set_run_font(lr, size=11)
    rp = right.paragraphs[0]
    rr = rp.add_run(f"Case No. {CASE}\n\n{case_title}")
    set_run_font(rr, size=11, bold=True)
    for cell in (left, right):
        tcPr = cell._tc.get_or_add_tcPr()
        borders = tcPr.first_child_found_in("w:tcBorders")
        if borders is None:
            borders = OxmlElement("w:tcBorders")
            tcPr.append(borders)
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            tag = OxmlElement(f"w:{edge}")
            tag.set(qn("w:val"), "single")
            tag.set(qn("w:sz"), "8")
            tag.set(qn("w:color"), "000000")
            borders.append(tag)
    doc.add_paragraph()


def add_service_meta(doc, responding):
    for label, value in [
        ("PROPOUNDING PARTY:", PLAINTIFF),
        ("RESPONDING PARTY:", responding),
        ("SET NUMBER:", "ONE"),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(label + " ")
        set_run_font(r, size=11, bold=True)
        r = p.add_run(value)
        set_run_font(r, size=11)
    doc.add_paragraph()


def add_definitions(doc, include_identify=True):
    h = doc.add_paragraph(style="Heading 1")
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run("Definitions")
    set_run_font(r, size=12, bold=True)
    for term, definition in DEFINITIONS:
        if term == "IDENTIFY" and not include_identify:
            continue
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        r = p.add_run(term + " means ")
        set_run_font(r, size=11, bold=True)
        r = p.add_run(definition)
        set_run_font(r, size=11)


def add_numbered_items(doc, heading, items, label):
    h = doc.add_paragraph(style="Heading 1")
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run(heading)
    set_run_font(r, size=12, bold=True)
    for i, text in enumerate(items, 1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_together = True
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.left_indent = Inches(0.30)
        p.paragraph_format.first_line_indent = Inches(-0.30)
        r = p.add_run(f"{label} NO. {i}: ")
        set_run_font(r, size=11, bold=True)
        r = p.add_run(text)
        set_run_font(r, size=11)


def add_signature(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    r = p.add_run("Dated: October 15, 2026")
    set_run_font(r, size=11)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run("__________________________________\nBrendan Ngwa Nforbi\nPlaintiff in Pro Per")
    set_run_font(r, size=11)


def start_discovery_part(doc, responding, title):
    add_caption(doc, title)
    add_service_meta(doc, responding)


def add_intro(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(text)
    set_run_font(r, size=11)


def page_break(doc):
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


def create_discovery_packet(responding, slug):
    doc = base_doc()

    # Requests for Admission
    start_discovery_part(doc, responding, "PLAINTIFF'S REQUESTS FOR ADMISSION, SET ONE")
    add_intro(doc, f"Plaintiff Brendan Ngwa Nforbi requests that {responding} admit the truth of the following matters under Code of Civil Procedure section 2033.010 et seq. Each request is directed only to the responding party. Responses must be served within the time prescribed by law.")
    add_definitions(doc, include_identify=False)
    add_numbered_items(doc, "Requests for Admission", RFAS, "REQUEST FOR ADMISSION")
    add_signature(doc)

    # Form Interrogatories selection sheet
    page_break(doc)
    start_discovery_part(doc, responding, "PLAINTIFF'S FORM INTERROGATORIES GENERAL, SET ONE")
    add_intro(doc, f"Plaintiff Brendan Ngwa Nforbi propounds Judicial Council Form Interrogatories-General, DISC-001, Set One, to {responding}. The service version should include the current official DISC-001 form with the following interrogatories checked. This selection sheet identifies the intended questions and is included for review.")
    checks = ["1.1", "4.1", "4.2", "12.1", "12.2", "12.3", "12.4", "12.5", "12.6", "12.7", "13.1", "13.2", "14.1", "14.2", "15.1", "17.1"]
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Selected interrogatories: " + ", ".join(checks))
    set_run_font(r, size=11, bold=True)
    h = doc.add_paragraph(style="Heading 1")
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run("Core Contention Interrogatories")
    set_run_font(r, size=12, bold=True)
    p = doc.add_paragraph()
    r = p.add_run("15.1 ")
    set_run_font(r, size=11, bold=True)
    r = p.add_run("Identify each denial of a material allegation and each special or affirmative defense in YOUR pleadings and for each: state all supporting facts; identify all persons with knowledge of those facts; and identify all documents and tangible things supporting the denial or defense and the person who has them.")
    set_run_font(r, size=11)
    p = doc.add_paragraph()
    r = p.add_run("17.1 ")
    set_run_font(r, size=11, bold=True)
    r = p.add_run("For each response to Plaintiff's concurrently served Requests for Admission that is not an unqualified admission: identify the request; state all facts supporting the response; identify all persons with knowledge of those facts; and identify all documents and tangible things supporting the response and the person who has them.")
    set_run_font(r, size=11)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    r = p.add_run("Service assembly note: attach the current official Judicial Council form DISC-001 bearing the case caption, party designations, Set One designation, INCIDENT definition, and the boxes listed above. Do not serve this review sheet as a substitute for DISC-001.")
    set_run_font(r, size=10, italic=True)
    add_signature(doc)

    # Special Interrogatories
    page_break(doc)
    start_discovery_part(doc, responding, "PLAINTIFF'S SPECIAL INTERROGATORIES, SET ONE")
    add_intro(doc, f"Plaintiff Brendan Ngwa Nforbi propounds the following Special Interrogatories, Set One, to {responding} under Code of Civil Procedure section 2030.010 et seq. Each interrogatory is directed only to the responding party. Responses must be answered separately and fully in writing under oath within the time prescribed by law.")
    add_definitions(doc, include_identify=True)
    add_numbered_items(doc, "Special Interrogatories", SROGS, "SPECIAL INTERROGATORY")
    add_signature(doc)

    # Requests for Production
    page_break(doc)
    start_discovery_part(doc, responding, "PLAINTIFF'S REQUESTS FOR PRODUCTION, SET ONE")
    add_intro(doc, f"Plaintiff Brendan Ngwa Nforbi demands that {responding} produce the following documents, electronically stored information, and tangible things under Code of Civil Procedure section 2031.010 et seq. Each request is directed only to the responding party. Production must occur within the time prescribed by law.")
    p = doc.add_paragraph()
    r = p.add_run("INSPECTION AND PRODUCTION: ")
    set_run_font(r, size=11, bold=True)
    r = p.add_run("[INSERT A DEFINITE DATE NO EARLIER THAN THE STATUTORY RESPONSE DEADLINE], at 10:00 a.m., by secure electronic transfer to bnn.cdl@gmail.com. The parties may agree in writing to another reasonable production method or location for tangible items.")
    set_run_font(r, size=11)
    add_definitions(doc, include_identify=False)
    h = doc.add_paragraph(style="Heading 1")
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run("Production Format")
    set_run_font(r, size=12, bold=True)
    for text in [
        "Produce documents as kept in the usual course of business or organize and label them to correspond with each request.",
        "Produce video and audio in native format together with available metadata and a standard playable copy. Do not reduce resolution, frame rate, timestamps, audio channels, or metadata.",
        "Produce spreadsheets, databases, emails, and internal messages in native or reasonably usable form preserving formulas, fields, headers, attachments, sender, recipient, date, and time information.",
        "Identify each static document with a unique production number and provide a production index showing the request number or numbers to which each item responds.",
    ]:
        p = doc.add_paragraph(style="List Number")
        r = p.add_run(text)
        set_run_font(r, size=11)
    add_numbered_items(doc, "Requests for Production", RFPS, "REQUEST FOR PRODUCTION")
    add_signature(doc)

    out = OUT / f"M35_Discovery_Set_One_to_{slug}_DRAFT.docx"
    doc.save(out)
    return out


def create_preservation_letter():
    doc = base_doc()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.8)
    p = doc.add_paragraph()
    for i, line in enumerate([
        "BRENDAN NGWA NFORBI",
        "1455 Cat Tail Drive",
        "Stockton, California 95204",
        "Telephone: (209) 801-4442",
        "E-mail: bnn.cdl@gmail.com",
        "Plaintiff in Pro Per",
    ]):
        r = p.add_run(line)
        set_run_font(r, size=11, bold=(i == 0))
        r.add_break()
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("October 15, 2026")
    set_run_font(r, size=11)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("VIA E-MAIL")
    set_run_font(r, size=11, bold=True)
    p = doc.add_paragraph()
    for line in [
        "E. Forrest Shryock, Jr., Esq.",
        "Raenalene C. Musni, Esq.",
        "Vogl Meredith Burke & Streza LLP",
        "456 Montgomery Street, Suite 1300",
        "San Francisco, California 94104",
        "fshryock@vmbllp.com",
        "rmusni@vmbllp.com",
    ]:
        r = p.add_run(line)
        set_run_font(r, size=11)
        r.add_break()
    p = doc.add_paragraph()
    r = p.add_run(f"Re: {PLAINTIFF} v. Ross Stores, Inc., et al., Santa Clara County Superior Court No. {CASE} - Evidence Preservation Demand")
    set_run_font(r, size=11, bold=True)
    p = doc.add_paragraph()
    r = p.add_run("Dear Mr. Shryock and Ms. Musni:")
    set_run_font(r, size=11)

    paragraphs = [
        "This letter supplements Plaintiff's prior preservation notice and requests immediate confirmation that Ross Stores, Inc., Ross Dress for Less, Inc., and their agents, vendors, insurers, employees, and custodians have suspended any deletion, overwrite, recycling, modification, or destruction process affecting evidence concerning the August 25, 2026 incident at the Ross Dress for Less store located at 119 E. El Camino Real, Sunnyvale, California.",
        "Defendants' Verified Answer states that surveillance cameras covered the entrance and captured the incident. The recordings are central to the disputed issues of Plaintiff's entry with the beverage, the employee's position relative to the exit, the words and duration of the interaction, the conduct of nearby employees and customers, and Plaintiff's departure. Please preserve complete recordings rather than selected clips.",
        "The preservation obligation includes information held by third-party surveillance vendors, cloud hosts, security contractors, claims administrators, insurers, and other service providers within Defendants' possession, custody, or control. Please transmit preservation instructions to those custodians immediately.",
    ]
    for text in paragraphs:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.5)
        r = p.add_run(text)
        set_run_font(r, size=11)

    h = doc.add_paragraph(style="Heading 1")
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = h.add_run("Evidence to Preserve")
    set_run_font(r, size=12, bold=True)
    preservation = [
        "All native surveillance video and audio from every camera covering the entrance, exterior approach, exit, registers, queue, adjacent sales floor, and employee work areas from 8:30 p.m. through 9:30 p.m. on August 25, 2026, including pre-event buffers and continuous footage.",
        "All exports, clips, transcodes, still images, enhanced copies, mobile-device recordings, and copies transmitted to counsel, insurers, claims administrators, employees, vendors, or investigators.",
        "Associated metadata, timestamps, camera identifiers, file names, frame rates, resolution, codec information, audio channels, hash values, access history, audit logs, export logs, deletion logs, overwrite logs, and chain-of-custody information.",
        "Camera maps, system diagrams, photographs, configuration records, maintenance records, retention settings, and documents identifying the hardware, software, cloud host, and surveillance vendor.",
        "Incident reports, loss-prevention reports, customer-contact reports, daily logs, stop logs, security logs, manager logs, claim notes, witness statements, photographs, diagrams, and investigative materials concerning the incident.",
        "Employee schedules, time records, assignments, rosters, and records sufficient to identify DOE 1, the cashier, the manager on duty, loss-prevention supervision, and every employee who observed or discussed the incident.",
        "Emails, text messages, internal messages, Teams or similar communications, voice messages, and other communications concerning Plaintiff, the incident, the beverage, the preservation demand, surveillance footage, or this lawsuit.",
        "Policies, procedures, manuals, directives, checklists, job descriptions, and training materials concerning merchant detentions, suspected theft, customer questioning, outside merchandise, receipt checks, racial profiling, equal customer service, implicit bias, and de-escalation.",
        "DOE 1's training acknowledgments, completion records, supervision records, and records of prior complaints or corrective action involving customer stops, blocked exits, unsupported theft inquiries, or alleged discriminatory treatment.",
        "Point-of-sale, inventory, SKU, sales, return, shrink, shortage, and adjustment records concerning Celsius-branded beverages at the STORE on August 25, 2026.",
        "Documents sufficient to show other customer stops, detentions, or merchandise inquiries at the STORE and complaints alleging racial profiling, unequal treatment, or unreasonable detention.",
        "Insurance, indemnity, claim, and notice records concerning this incident, while preserving any legitimately privileged material in place rather than deleting it.",
    ]
    for i, text in enumerate(preservation, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_together = True
        r = p.add_run(f"{i}. ")
        set_run_font(r, size=11, bold=True)
        r = p.add_run(text)
        set_run_font(r, size=11)

    closing = [
        "Please preserve original evidence and forensic-quality copies. Do not edit, annotate, compress, crop, change file format, reduce resolution, strip metadata, or rely solely on a screen recording or convenience export. If any responsive evidence has already been deleted, overwritten, lost, corrupted, or altered, preserve all information showing when, how, why, and by whom that occurred.",
        "Please confirm in writing by October 20, 2026, that preservation measures are in place; identify the surveillance custodian and any third-party vendor; state the ordinary video-retention period; and state whether all responsive video remains available. This request seeks preservation only and does not require immediate production or waive Plaintiff's forthcoming discovery demands.",
    ]
    for text in closing:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.5)
        r = p.add_run(text)
        set_run_font(r, size=11)
    p = doc.add_paragraph()
    r = p.add_run("Respectfully,")
    set_run_font(r, size=11)
    p = doc.add_paragraph()
    r = p.add_run("\n__________________________________\nBrendan Ngwa Nforbi\nPlaintiff in Pro Per")
    set_run_font(r, size=11)
    out = OUT / "M35_Standalone_Evidence_Preservation_Demand_DRAFT.docx"
    doc.save(out)
    return out


if __name__ == "__main__":
    files = [
        create_preservation_letter(),
        create_discovery_packet("ROSS STORES, INC.", "Ross_Stores_Inc"),
        create_discovery_packet("ROSS DRESS FOR LESS, INC.", "Ross_Dress_for_Less_Inc"),
    ]
    for path in files:
        print(path.resolve())
