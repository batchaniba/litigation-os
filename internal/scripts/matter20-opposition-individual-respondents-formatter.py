# ==========================================================
# NEWANFORBI v. CALIFORNIA HIGHWAY PATROL, ET AL. (26CV191136)
# PETITIONER'S OPPOSITION TO INDIVIDUAL RESPONDENTS' DEMURRERS
# AND JOINDERS TO RESPONDENT CHP'S DEMURRER; MPA
# Alameda County Superior Court
# Reformatted onto the portfolio's standard pleading-paper engine
# (matches internal/scripts/pleading-paper-formatter-script.py,
# same visual convention as matter-20/Opposition to Demurrer.pdf)
# ==========================================================
import os, sys, re

try:
    import reportlab
except ImportError:
    os.system(f"{sys.executable} -m pip install reportlab")
    import reportlab

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

PAGE_W, PAGE_H = letter
MARGIN_LEFT = 1.0 * inch
MARGIN_RIGHT = 0.5 * inch
LINE_SPACING = 24
NUM_LINES = 28
FONT_SIZE = 12

TEXT_START_Y = PAGE_H - 1.05 * inch
TEXT_END_Y = TEXT_START_Y - (NUM_LINES - 1) * LINE_SPACING

VERT_LINE_LEFT = MARGIN_LEFT + 0.30 * inch
VERT_LINE_RIGHT = MARGIN_LEFT + 0.35 * inch
LINE_NUM_X = VERT_LINE_LEFT - 0.08 * inch

CONTENT_LEFT = VERT_LINE_RIGHT + 0.10 * inch
CONTENT_RIGHT = PAGE_W - MARGIN_RIGHT
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT

FOOTER_RULE_Y = TEXT_END_Y - 12
FOOTER_PAGE_Y = FOOTER_RULE_Y - 16
FOOTER_TITLE_Y = FOOTER_PAGE_Y - 18

DOC_TITLE_FOOTER = "OPPOSITION TO INDIVIDUAL RESPONDENTS' DEMURRERS — NEWANFORBI v. CHP, ET AL."
COURT_LINE1 = "SUPERIOR COURT OF THE STATE OF CALIFORNIA"
COURT_LINE2 = "COUNTY OF ALAMEDA"


class PleadingPaper:
    def __init__(self, filename):
        self.c = canvas.Canvas(filename, pagesize=letter)
        self.page_num = 0
        self.current_line = 0
        self.start_new_page()

    def start_new_page(self):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        self.current_line = 0
        self._draw_page_frame()

    def _draw_page_frame(self):
        c = self.c
        c.setStrokeColor(black)
        c.setLineWidth(0.5)
        c.line(VERT_LINE_LEFT, PAGE_H, VERT_LINE_LEFT, 0)
        c.line(VERT_LINE_RIGHT, PAGE_H, VERT_LINE_RIGHT, 0)
        c.line(CONTENT_RIGHT, PAGE_H, CONTENT_RIGHT, 0)
        c.setFont("Helvetica", 10)
        for i in range(NUM_LINES):
            y = TEXT_START_Y - i * LINE_SPACING
            c.drawRightString(LINE_NUM_X, y, str(i + 1))
        c.setLineWidth(0.5)
        c.line(VERT_LINE_RIGHT, FOOTER_RULE_Y, CONTENT_RIGHT, FOOTER_RULE_Y)
        center_x = (VERT_LINE_LEFT + CONTENT_RIGHT) / 2
        c.setFont("Helvetica", 10)
        c.drawCentredString(center_x, FOOTER_PAGE_Y, f"Page {self.page_num}")
        avail_footer_width = CONTENT_RIGHT - VERT_LINE_LEFT - 4
        footer_size = 9
        while footer_size > 6 and c.stringWidth(DOC_TITLE_FOOTER, "Helvetica", footer_size) > avail_footer_width:
            footer_size -= 0.5
        c.setFont("Helvetica", footer_size)
        c.drawCentredString(center_x, FOOTER_TITLE_Y, DOC_TITLE_FOOTER)

    def _line_y(self, idx):
        return TEXT_START_Y - idx * LINE_SPACING

    def _ensure_line(self):
        if self.current_line >= NUM_LINES:
            self.start_new_page()

    def ensure_space(self, n):
        if self.current_line + n > NUM_LINES:
            self.start_new_page()

    def write_line(self, text, bold=False, font="Times-Roman", size=FONT_SIZE,
                   italic=False, center=False, right=False, indent=0,
                   underline=False, right_margin_offset=0):
        self._ensure_line()
        y = self._line_y(self.current_line)
        c = self.c
        if bold and italic: fn = "Times-BoldItalic"
        elif bold: fn = "Times-Bold"
        elif italic: fn = "Times-Italic"
        else: fn = font
        c.setFont(fn, size)
        x = CONTENT_LEFT + indent
        if center:
            cx = CONTENT_LEFT + CONTENT_WIDTH / 2
            c.drawCentredString(cx, y, text)
        elif right:
            c.drawRightString(CONTENT_RIGHT - right_margin_offset, y, text)
        else:
            c.drawString(x, y, text)
        if underline:
            tw = c.stringWidth(text, fn, size)
            if center: ux = cx - tw / 2
            elif right: ux = (CONTENT_RIGHT - right_margin_offset) - tw
            else: ux = x
            c.setLineWidth(0.5)
            c.line(ux, y - 1.5, ux + tw, y - 1.5)
        self.current_line += 1

    def blank_line(self):
        self._ensure_line()
        self.current_line += 1

    def write_wrapped(self, text, bold=False, font="Times-Roman", size=FONT_SIZE,
                      italic=False, indent=0, first_indent=36):
        avail = CONTENT_WIDTH - indent
        segs = self._parse_segments(text)
        lines = self._wrap_segments(segs, avail, first_indent, size)
        c = self.c
        for i, parts in enumerate(lines):
            self._ensure_line()
            y = self._line_y(self.current_line)
            x = CONTENT_LEFT + indent
            if i == 0:
                x += first_indent
            for pt, ps in parts:
                if ps == "bi": pfn = "Times-BoldItalic"
                elif ps == "b": pfn = "Times-Bold"
                elif ps == "i": pfn = "Times-Italic"
                else: pfn = "Times-Roman"
                c.setFont(pfn, size)
                c.drawString(x, y, pt)
                x += c.stringWidth(pt, pfn, size)
            self.current_line += 1

    def _parse_segments(self, text):
        segs = []
        pat = r"<<(b|i|bi):([^>]*)>>"
        last = 0
        for m in re.finditer(pat, text):
            if m.start() > last:
                segs.append((text[last:m.start()], "r"))
            segs.append((m.group(2), m.group(1)))
            last = m.end()
        if last < len(text):
            segs.append((text[last:], "r"))
        return segs

    def _wrap_segments(self, segs, avail, fi, size):
        c = self.c
        lines, cur = [], []
        cw = fi
        def ffs(s):
            if s == "bi": return "Times-BoldItalic"
            elif s == "b": return "Times-Bold"
            elif s == "i": return "Times-Italic"
            return "Times-Roman"
        for st, ss in segs:
            fn = ffs(ss)
            words = st.split(" ")
            for wi, w in enumerate(words):
                if wi > 0:
                    w = " " + w
                ww = c.stringWidth(w, fn, size)
                if cw + ww > avail and cur:
                    lines.append(cur)
                    cur = []
                    cw = 0
                    if w.startswith(" "):
                        w = w[1:]
                        ww = c.stringWidth(w, fn, size)
                cur.append((w, ss))
                cw += ww
        if cur:
            lines.append(cur)
        return lines

    def draw_caption_block(self, left, right, caption_size=10, tight_lh=13, boxed=True):
        c = self.c
        box_left_x = CONTENT_LEFT
        box_right_x = CONTENT_LEFT + CONTENT_WIDTH * 0.52
        right_col_x = box_right_x + 10
        start_line = self.current_line
        self._ensure_line()
        first_y = self._line_y(self.current_line)
        box_top = first_y + 11
        left_x_pad = 6
        rows = max(len(left), len(right))
        for i in range(rows):
            y = first_y - i * tight_lh
            if y < TEXT_END_Y + 2:
                break
            if i < len(left):
                lt, lb, li = left[i]
                if lb and li: fn = "Times-BoldItalic"
                elif lb: fn = "Times-Bold"
                elif li: fn = "Times-Italic"
                else: fn = "Times-Roman"
                c.setFont(fn, caption_size)
                c.drawString(box_left_x + left_x_pad, y, lt)
            if i < len(right):
                rt, rb, ri = right[i]
                if rb and ri: fn = "Times-BoldItalic"
                elif rb: fn = "Times-Bold"
                elif ri: fn = "Times-Italic"
                else: fn = "Times-Roman"
                c.setFont(fn, caption_size)
                c.drawString(right_col_x, y, rt)
        last_left_y = first_y - (len(left) - 1) * tight_lh
        box_bottom = last_left_y - 8
        if boxed:
            c.setLineWidth(0.75)
            c.line(VERT_LINE_RIGHT, box_top, box_right_x, box_top)
            c.line(VERT_LINE_RIGHT, box_bottom, box_right_x, box_bottom)
            c.line(box_right_x, box_top, box_right_x, box_bottom)
        max_rows = max(len(left), len(right))
        true_bottom_y = first_y - (max_rows - 1) * tight_lh - 8
        consumed_height = box_top - true_bottom_y
        lines_consumed = int(consumed_height / LINE_SPACING) + 1
        self.current_line = start_line + lines_consumed

    def save(self):
        self.c.save()


# ==========================================================
# DOCUMENT CONTENT
# ==========================================================

CONTENT = [

    ("HEADER", "NOTICE OF OPPOSITION"),

    ("PARA", "TO ALL PARTIES AND THEIR COUNSEL OF RECORD:"),

    ("PARA", "PLEASE TAKE NOTICE that Petitioner Brendan Ngehsi Newanforbi, appearing in propria persona, hereby opposes the Demurrers and Joinders filed by individual Respondents Gerardo Serrato, Gary Paul, and Eric Dutra on July 30, 2026. This opposition is based on this notice, the accompanying Memorandum of Points and Authorities, the Verified Petition for Writ of Mandate and all exhibits incorporated therein, the files and records in this action, and any further evidence and argument the Court may receive at or before the hearing."),

    ("PARA", "Hearing Date: August 28, 2026, 9:00 a.m., Department 25, Superior Court of California, County of Alameda, 1221 Oak Street, Oakland, CA 94612."),

    # =====================================================
    ("HEADER", "MEMORANDUM OF POINTS AND AUTHORITIES"),

    ("HEADER", "I. INTRODUCTION"),

    ("PARA", "On July 30, 2026, individual Respondents Gerardo Serrato (Captain/Commander), Gary Paul (Lieutenant), and Eric Dutra (Sergeant) each filed a Notice of Joinder to Respondent California Highway Patrol's Demurrer, a separate Demurrer, and a supporting Memorandum of Points and Authorities. Each filing does two things. First, each individual Respondent joins and adopts CHP's core theory that certifying Form I-918, Supplement B is a discretionary act beyond the reach of ordinary mandamus under Code of Civil Procedure § 1085. Second, Respondents Paul and Dutra each raise an individualized argument not previously briefed: that the Petition fails to plead facts showing each of them personally qualifies as a “certifying official” within the meaning of Penal Code § 679.10(b), and that each is therefore not a proper respondent. Respondent Serrato's MPA does not independently challenge his certifying-official status but rather acknowledges that Petitioner has alleged he is a certifying official and has attached the denial letter he signed. (Serrato MPA at 2:20-24.)"),

    ("PARA", "As to the joinder-based arguments, Petitioner incorporates by reference in full the arguments and authorities set forth in Petitioner's Opposition to Respondent CHP's Demurrer, filed July 13, 2026, and the supporting Declaration of Petitioner. Those arguments apply with equal force to the individual Respondents, who merely adopt CHP's positions without independent analysis. Petitioner will not rebrief those arguments here."),

    ("PARA", "As to the “not a certifying official” argument raised by Respondents Paul and Dutra, it is independently meritless. As a threshold matter, the Petition does not merely support an inference on this point — Pet. ¶¶ 14–16 each expressly allege, in the statute's own words, that the respondent “is a 'certifying official' within the meaning of Penal Code § 679.10(b).” That allegation must be accepted as true on demurrer, together with the specific supporting facts and attached exhibits discussed below. Independent of that express allegation, the Petition also pleads specific supporting facts — including two exhibits attached to and incorporated by reference in the Petition itself — from which the Court can and must reasonably infer that each individual Respondent is a certifying official under one or more of the four categories in § 679.10(b). The Petition is not required to recite the statutory categories verbatim; it is required to plead facts, which it does, and it does so twice over. If the Court nonetheless finds any allegation insufficient, leave to amend should be granted because the deficiency, if any, is a readily curable pleading gap, not a substantive defect."),

    ("HEADER", "II. STANDARD OF REVIEW"),

    ("PARA", "A demurrer tests whether the complaint states facts sufficient to constitute a cause of action. (Code Civ. Proc., § 430.10, subd. (e).) In ruling on a demurrer, the court must “assume the truth of all facts properly pleaded by the plaintiff, as well as those that are judicially noticeable.” (<<i:Blank v. Kirwan>> (1985) 39 Cal.3d 311, 318.) The court “give[s] the complaint a reasonable interpretation, reading it as a whole and its parts in their context.” (Ibid.) A complaint need not plead facts in the precise language of the statute; it suffices if the facts alleged support a reasonable inference that each element of the claim is met. (<<i:Quelimane Co. v. Stewart Title Guaranty Co.>> (1998) 19 Cal.4th 26, 38-39 [“[w]e look to whether the factual allegations, liberally construed, state a cause of action on any available legal theory”].)"),

    ("PARA", "“[A] demurrer should not be sustained without leave to amend if the complaint, liberally construed, can reasonably be considered to state a cause of action on any theory, or if there is a reasonable possibility that the defect can be cured by amendment.” (Quelimane Co., supra, 19 Cal.4th at p. 38, citing Blank v. Kirwan, supra, 39 Cal.3d at p. 318.) The burden is on the demurring party to show that the complaint does not state facts sufficient to constitute a cause of action. (Ibid.)"),

    ("PARA", "On demurrer, the Court may also consider matters subject to judicial notice (Evid. Code, § 452) and documents incorporated by reference in the pleading. (<<i:Barnett v. Fireman's Fund Ins. Co.>> (2001) 90 Cal.App.4th 500, 505 [“a demurrer reaches exhibits attached to or incorporated by reference in the complaint”].) The Verified Petition incorporates fourteen exhibits, including the April 20, 2026 denial letter (Exhibit 1), the dashcam transcript (Exhibit 5), the CHP arrest report (Exhibit 6), and the Penal Code § 851.6 detention certificate (Exhibit 7). These are part of the pleading and accepted as true on demurrer."),

    ("HEADER", "III. ARGUMENT"),

    ("PARA", "Penal Code § 679.10(b) defines “certifying official” as: (1) the head of the certifying entity; (2) a person in a supervisory role who has been specifically designated by the head of the certifying entity to issue Form I-918 Supplement B certifications on behalf of that agency; (3) a judge; or (4) any other certifying official defined under § 214.14(a)(2) of Title 8 of the Code of Federal Regulations. (Pen. Code, § 679.10, subd. (b)(1)-(4).)"),

    ("PARA", "The question on demurrer is not whether the Petition recites these categories verbatim. It is whether the Petition alleges facts from which the Court can reasonably infer that each individual Respondent falls within one or more of these categories. (Quelimane Co., supra, 19 Cal.4th at pp. 38-39.) Here, the Petition does more than support an inference: Pet. ¶¶ 14, 15, and 16 each expressly allege that the respondent “is a 'certifying official' within the meaning of Penal Code § 679.10(b)” — using the statute's own operative phrase. As shown below, the Petition also independently pleads the specific supporting facts for each Respondent, backed by exhibits attached to and incorporated by reference in the Petition itself."),

    ("SUBHEAD", "A. Respondent Serrato Is a Certifying Official Under\n§ 679.10(b)(1) and/or (b)(2)"),

    ("PARA", "Respondent Serrato's challenge to the Petition is the weakest of the three — so weak that Serrato's own MPA does not even raise it. Unlike Respondents Paul and Dutra, whose MPAs each contain a section demurring “for one additional reason” (that the Petition does not adequately allege certifying-official status), Serrato's MPA contains no such section. Instead, it acknowledges that “Petitioner alleges that Capt. Serrato is a 'certifying official' within the meaning of Penal Code section 679.10(b) and has attached to his petition the certification denial letter signed by Capt. Serrato.” (Serrato MPA at 2:20-24.) The Court should overrule Serrato's demurrer on this ground alone: the argument was not raised and is therefore waived."),

    ("PARA", "Even if the argument were before the Court, it would fail on the merits. Pet. ¶ 14 alleges that Serrato, as Captain and Commander of the CHP Dublin Area, “authored, signed, and issued the April 20, 2026 denial letter on CHP Dublin Area letterhead under his name and title,” “exercises supervisory and final decisional authority over certifications processed out of the Dublin Area office,” and — in the statute's own words — “is a 'certifying official' within the meaning of Penal Code section 679.10(b).” (Pet., ¶ 14.) The denial letter itself, attached to the Petition as Exhibit 1, bears Serrato's signature and title."),

    ("PARA", "These facts establish certifying-official status under multiple subsections of § 679.10(b). As the area-level Commander exercising “final decisional authority” over certifications, Serrato is the functional head of the certifying entity at the operational unit level, satisfying subdivision (b)(1). At minimum, he is a person in a supervisory role who exercises certification authority on behalf of CHP, satisfying subdivision (b)(2). And Serrato's actual conduct — personally signing a certification denial under his name and title — is itself the strongest possible evidence that he holds the statutory role. A respondent who has exercised the very authority the Petition seeks to compel cannot credibly claim he lacks that authority."),

    ("PARA", "Respondents' own proposed order further confirms Serrato's status. The proposed order seeks to sustain the demurrers on the ground that certification is discretionary, not ministerial — a merits argument that presupposes Serrato is the official exercising the discretion in question. Respondents cannot simultaneously argue that Serrato exercised certification discretion and that he is not a certifying official."),

    ("SUBHEAD", "B. Respondent Paul Is a Certifying Official Under\n§ 679.10(b)(2)"),

    ("PARA", "As a threshold matter, Pet. ¶ 15 does not stop at the facts Respondent Paul quotes in his MPA — it goes on to expressly allege, in the statute's own words, that Paul “is a 'certifying official' within the meaning of Penal Code section 679.10(b).” That allegation, standing alone, must be accepted as true on demurrer. Respondent Paul's MPA does not address it, quoting only the sentence that precedes it."),

    ("PARA", "Respondent Paul argues that the Petition alleges only that he “is a CHP supervisory official with responsibility for processing the certification request” (Pet., ¶ 15) and that this does not satisfy any of the four categories in § 679.10(b). (Paul MPA at 2:24-3:5.) This argument ignores the full scope of the allegations and misapplies the demurrer standard."),

    ("PARA", "The Petition alleges far more than a bare label. Pet. ¶ 15 alleges that Paul “is the official who acknowledged receipt of Petitioner's April 9, 2026 certification request by return e-mail on April 10, 2026, and who is identified in the April 20, 2026 denial letter as the contact point for 'any additional questions.'” These are specific factual allegations — not conclusions — establishing that Paul personally received, processed, and was the designated point of contact for the certification request. Combined with the allegation that Paul is “a CHP supervisory official” (Lieutenant), these facts support the reasonable inference that Paul was specifically designated by CHP to process Form I-918, Supplement B certifications, satisfying § 679.10(b)(2)."),

    ("PARA", "The April 10, 2026 email from Lt. Paul — attached to the Petition as Exhibit 13 and incorporated by reference, and referenced at Pet. ¶ 15 — confirms this inference. In that email, Paul acknowledged receipt of the certification request and represented that he would ensure Petitioner was notified “by written correspondence.” This is not the conduct of an uninvolved bystander; it is the conduct of an official who has been designated to process certifications and who is performing the function the statute assigns to a certifying official. On demurrer, the Court must draw this reasonable inference in Petitioner's favor, and it need not draw any inference at all as to the email's authenticity or contents: Exhibit 13 is part of the pleading itself. (Blank v. Kirwan, supra, 39 Cal.3d at p. 318; Barnett v. Fireman's Fund Ins. Co., supra, 90 Cal.App.4th at p. 505.)"),

    ("PARA", "Paul's argument also proves too much. If a CHP lieutenant who personally receives a certification request, acknowledges it, processes it, and is identified in the denial letter as the contact person is not a “certifying official,” then the statute's inclusion of designated supervisory officials in subdivision (b)(2) is rendered a nullity. The Court should reject any construction that makes statutory language surplusage. (<<i:People v. Pieters>> (1991) 52 Cal.3d 894, 919 [courts should give effect to every word of a statute].)"),

    ("SUBHEAD", "C. Respondent Dutra Is a Certifying Official Under\n§ 679.10(b)(2) or, Alternatively, (b)(4)"),

    ("PARA", "As a threshold matter, Pet. ¶ 16 does not stop at the facts Respondent Dutra quotes in his MPA — it goes on to expressly allege, in the statute's own words, that Dutra “is a 'certifying official' within the meaning of Penal Code section 679.10(b).” That allegation, standing alone, must be accepted as true on demurrer. Respondent Dutra's MPA does not address it, quoting only the sentence that precedes it."),

    ("PARA", "Respondent Dutra argues that the Petition alleges only that he is “the assigned investigator and designated recipient on the Supplement B” (Pet., ¶ 16) and that this does not satisfy any of the four statutory categories. (Dutra MPA at 2:25-3:5.) This argument fails for several reasons."),

    ("PARA", "First, the Petition alleges that Dutra is “the investigator assigned to CHP Citizen Complaint File No. 390.18437.17620 by the March 26, 2026 correspondence of Respondent Serrato” and is “the official to whom Petitioner submitted the formal certification request on April 9, 2026.” (Pet., ¶ 16.) These allegations establish that Dutra was formally designated by Captain Serrato — a command-level officer — to handle the investigation and receive the Supplement B submission. The March 26, 2026 Complaint Assignment Letter documenting this formal assignment is attached to the Petition as Exhibit 11 and incorporated by reference — it is part of the pleading itself, not extrinsic evidence. (Barnett v. Fireman's Fund Ins. Co., supra, 90 Cal.App.4th at p. 505.)"),

    ("PARA", "This formal designation by a command-level supervisor satisfies § 679.10(b)(2), which covers “a person in a supervisory role who has been specifically designated by the head of the certifying entity to issue Form I-918 Supplement B certifications on behalf of that agency.” Dutra was specifically designated by the area commander to handle the complaint file and receive the Supplement B; he was the official to whom Petitioner submitted the form. On demurrer, these facts support the reasonable inference that Dutra's assignment encompassed the processing of the certification request. (Blank v. Kirwan, supra, 39 Cal.3d at p. 318.)"),

    ("PARA", "Second, the Petition's characterization of Dutra as the “designated recipient on the Supplement B” is itself significant. The word “designated” — drawn from the Petition's factual narrative, not from a bare statutory label — mirrors the operative language of subdivision (b)(2) (“specifically designated”). A respondent who is the “designated recipient” of the very form at issue in this litigation occupies precisely the role the statute contemplates."),

    ("PARA", "Third, alternatively, Dutra may qualify under subdivision (b)(4) as a “certifying official defined under Section 214.14(a)(2) of Title 8 of the Code of Federal Regulations,” which broadly defines certifying officials to include law enforcement officers who have responsibility for the investigation of qualifying criminal activity. Dutra was assigned as the investigator on the underlying complaint file and was the point of submission for the Supplement B. These facts support a reasonable inference under (b)(4) as well."),

    ("HEADER", "IV. IN THE ALTERNATIVE, LEAVE TO AMEND SHOULD BE GRANTED"),

    ("PARA", "If the Court finds the current allegations insufficient as to any individual Respondent, Petitioner respectfully requests leave to amend the Petition to add: (a) express cross-references to Exhibit 11 (the March 26, 2026 Complaint Assignment Letter) and Exhibit 13 (the April 10, 2026 email from Lt. Paul) within the body of Pet. ¶¶ 15–16; and (b) any additional facts regarding CHP's internal designation procedures for Form I-918, Supplement B certifications. Petitioner notes that Exhibits 11 and 13 themselves are already attached to and incorporated by reference in the Petition (see Section III, supra); any amendment on this point would be limited to adding clarifying cross-references within the body paragraphs, not to introducing new material into the record."),

    ("PARA", "A demurrer should not be sustained without leave to amend unless “there is no reasonable possibility that the defect can be cured by amendment.” (Blank v. Kirwan, supra, 39 Cal.3d at p. 318.) Here, the purported deficiency is not that the individual Respondents are not certifying officials — they are, as the record shows, including by their own express allegations at Pet. ¶¶ 14–16 and the exhibits already attached at Exhibits 11 and 13 — but, at most, that the body paragraphs do not separately cite those exhibits by number. That is, at most, a cosmetic cross-referencing gap, not a substantive defect, and amendment to add express exhibit citations and any additional designation facts would cure it. Leave to amend should be liberally granted, particularly to a self-represented litigant. (<<i:Jones v. Lodge at Torrey Pines Partnership>> (2008) 42 Cal.4th 1158, 1162 [leave to amend “is routinely and liberally granted”].)"),

    ("HEADER", "V. CONCLUSION"),

    ("PARA", "For the foregoing reasons, and for the reasons set forth in Petitioner's July 13, 2026 Opposition to Respondent CHP's Demurrer (incorporated herein by reference), Petitioner respectfully requests that the Court:"),

    ("LIST_ITEM", "1. Overrule the demurrers of individual Respondents Serrato, Paul, and Dutra in their entirety; or"),

    ("LIST_ITEM", "2. In the alternative, if the Court finds any allegation insufficient as to any individual Respondent, sustain the demurrer with leave to amend; and"),

    ("LIST_ITEM", "3. Deny Respondents' request that the demurrers be sustained without leave to amend."),

    ("SIGNATURE", "\nDated: ___________________\n\n\n___________________________________\nBRENDAN NGEHSI NEWANFORBI\nPetitioner, In Pro Per"),

    # =====================================================
    # PROOF OF SERVICE
    # =====================================================
    ("PAGEBREAK", ""),
    ("HEADER", "PROOF OF SERVICE"),

    ("PARA", "I, Brendan Ngehsi Newanforbi, declare:"),

    ("PARA", "I am the Petitioner in the above-captioned action, appearing in propria persona. I am over the age of eighteen and a resident of San Joaquin County, California. My mailing address is 1455 Cat Tail Drive, Stockton, California 95204, and my electronic service address is bnn.cdl@gmail.com."),

    ("PARA", "On ___________________, 2026, I served true and correct copies of the following document:"),

    ("LIST_ITEM", "1. PETITIONER'S OPPOSITION TO INDIVIDUAL RESPONDENTS' DEMURRERS AND JOINDERS TO RESPONDENT CHP'S DEMURRER; MEMORANDUM OF POINTS AND AUTHORITIES"),

    ("PARA", "on the following party by transmitting a true copy via electronic mail and by depositing a true copy in the United States mail, first-class postage prepaid, in a sealed envelope addressed as follows:"),

    ("PARA", "Vanessa Ing, Deputy Attorney General, Office of the Attorney General, 455 Golden Gate Avenue, Suite 11000, San Francisco, CA 94102-7004. E-mail: Vanessa.Ing@doj.ca.gov. Attorneys for Respondents California Highway Patrol, Gerardo Serrato, Gary Paul, and Eric Dutra."),

    ("PARA", "I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct."),

    ("SIGNATURE", "\nExecuted on ___________________, 2026,\nat Stockton, California.\n\n\n___________________________________\nBRENDAN NGEHSI NEWANFORBI"),
]


# ==========================================================
# MAIN
# ==========================================================

def main():
    out = "/tmp/claude-0/-home-user-interactive-litigation-portfolio/73ae914c-39d4-5df8-866c-f2328c2fe1c7/scratchpad/formatter/Opposition_to_Individual_Respondents_Demurrers_FORMATTED.pdf"
    d = PleadingPaper(out)

    # === TOP ATTORNEY BLOCK (matches matter-20/Opposition to Demurrer.pdf) ===
    c = d.c
    atty_y = d._line_y(0)
    atty_lh = 15
    atty_lines = [
        ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
        ("Petitioner In Pro Per", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12),
        ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
    ]
    for i, (txt, fn, sz) in enumerate(atty_lines):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()

    # === CAPTION BLOCK (party listing matches matter-20/Opposition to Demurrer.pdf) ===
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Petitioner,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("CALIFORNIA HIGHWAY PATROL;", True, False),
        ("G. SERRATO, in his official capacity", True, False),
        ("as Captain and Commander of the CHP", True, False),
        ("Dublin Area; GARY PAUL, in his", True, False),
        ("official capacity as Lieutenant of the", True, False),
        ("CHP Dublin Area; ERIC DUTRA, in his", True, False),
        ("official capacity as Sergeant of the", True, False),
        ("CHP Dublin Area; and DOES 1 through", True, False),
        ("10, inclusive,", True, False),
        ("", False, False),
        ("                          Respondents.", False, False),
    ]

    right = [
        ("Case No. 26CV191136", False, False),
        ("", False, False),
        ("PETITIONER'S OPPOSITION TO", True, False),
        ("INDIVIDUAL RESPONDENTS'", True, False),
        ("DEMURRERS AND JOINDERS TO", True, False),
        ("RESPONDENT CHP'S DEMURRER;", True, False),
        ("", False, False),
        ("MEMORANDUM OF POINTS", True, False),
        ("AND AUTHORITIES", True, False),
        ("", False, False),
        ("Date:  August 28, 2026", False, False),
        ("Time:  9:00 a.m.", False, False),
        ("Assigned for All Purposes to:", False, False),
        ("Hon. Jenna M. Whitman, Dept. 25", False, False),
        ("", False, False),
        ("Action Filed: May 29, 2026", False, False),
        ("Trial Date:   Not set", False, False),
    ]

    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)

    d.blank_line()

    # RENDER BODY
    for c_type, text in CONTENT:
        if c_type == "HEADER":
            d.ensure_space(4)
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=False)
            d.blank_line()
        elif c_type == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif c_type == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        elif c_type == "SIGNATURE":
            for line in text.split("\n"):
                d.write_line(line, right=True, right_margin_offset=20)
            d.blank_line()
        elif c_type == "PAGEBREAK":
            d.start_new_page()

    d.save()
    print(f"SUCCESS! Generated: {out}")


if __name__ == "__main__":
    main()
