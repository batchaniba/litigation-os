# ==========================================================
# NEWANFORBI v. RANDSTAD US, LLC et al.
# COMPLAINT FOR DAMAGES — REVISED (v2)
# San Joaquin County Superior Court
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
 
DOC_TITLE_FOOTER = "COMPLAINT -- NEWANFORBI v. RANDSTAD US, LLC ET AL."
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
        c.setFont("Helvetica", 9)
        c.drawCentredString(center_x, FOOTER_TITLE_Y, DOC_TITLE_FOOTER)
 
    def _line_y(self, idx):
        return TEXT_START_Y - idx * LINE_SPACING
 
    def _ensure_line(self):
        if self.current_line >= NUM_LINES:
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
# COMPLAINT CONTENT
# ==========================================================
 
CONTENT = [
 
    ("HEADER", "COMPLAINT FOR DAMAGES"),
 
    ("PARA", "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in pro per, alleges as follows:"),
 
    # =====================================================
    # PARTIES
    # =====================================================
    ("HEADER", "PARTIES"),
 
    ("PARA", "1. Plaintiff BRENDAN NGEHSI NEWANFORBI (hereinafter \"Plaintiff\") is, and at all times relevant herein was, an individual residing in the County of San Joaquin, State of California."),
 
    ("PARA", "2. Defendant RANDSTAD US, LLC (hereinafter \"Randstad\") is, and at all times relevant herein was, a Delaware limited liability company doing business in the State of California under the trade names \"Randstad,\" \"Randstad General Staffing,\" and \"Randstad Inhouse Services.\" Randstad General Staffing and Randstad Inhouse Services are trade names and division brands of Randstad US, LLC, not separate legal entities. Randstad is a temporary staffing and employment agency that recruits, hires, and assigns employees to work at client companies throughout California, including in San Joaquin County. Randstad was Plaintiff's employer of record at all times relevant herein. Plaintiff has an established prior employment history with Randstad."),
 
    ("PARA", "3. Defendant THE RK LOGISTICS GROUP, INC. (hereinafter \"RK Logistics\") is, and at all times relevant herein was, a California corporation incorporated on April 23, 2004, with its principal place of business at 47020 Kato Road, Fremont, California 94538. RK Logistics is a third-party logistics (3PL) company specializing in semiconductor, electric vehicle, and high-tech logistics, operating multiple warehousing and distribution facilities throughout the San Francisco Bay Area, including facilities in Fremont, Newark, Hayward, and Livermore. RK Logistics was the client company to which Plaintiff was assigned by Randstad and was the entity that established the background screening criteria that resulted in Plaintiff's termination."),
 
    ("PARA", "4. At all times relevant herein, Defendants operated under a staffing arrangement whereby Randstad, through its Randstad Inhouse Services division, embedded a dedicated site manager within RK Logistics' facility to manage the recruitment, onboarding, and employment of Randstad temporary employees assigned to RK Logistics. Each Defendant was the agent, employee, partner, joint venturer, alter ego, and/or co-conspirator of each other Defendant and was acting within the course and scope of said agency, employment, partnership, joint venture, and/or conspiracy. Each Defendant ratified and approved the acts alleged herein of each other Defendant."),
 
    ("PARA", "5. The true names and capacities, whether individual, corporate, associate, or otherwise, of DOES 1 through 20, inclusive, are unknown to Plaintiff at this time. Plaintiff will amend this Complaint to allege their true names and capacities when ascertained. Each DOE Defendant is responsible in some manner for the acts, omissions, and damages alleged herein."),
 
    # =====================================================
    # JURISDICTION AND VENUE
    # =====================================================
    ("HEADER", "JURISDICTION AND VENUE"),
 
    ("PARA", "6. This Court has jurisdiction over this action pursuant to Article VI, Section 10 of the California Constitution and Code of Civil Procedure section 410.10. The amount in controversy exceeds the jurisdictional minimum of this Court."),
 
    ("PARA", "7. Venue is proper in this Court pursuant to Code of Civil Procedure sections 395(a) and 395.5 because a substantial part of the events and omissions giving rise to this action occurred in the County of Alameda, where Plaintiff was assigned to work at Defendant RK Logistics' facility in Fremont and where the adverse employment decision was made and implemented."),
 
    # =====================================================
    # FACTUAL ALLEGATIONS
    # =====================================================
    ("HEADER", "FACTUAL ALLEGATIONS"),
 
    ("SUBHEAD", "A. Plaintiff's Application and Recruitment"),
 
    ("PARA", "8. On June 30, 2026, Plaintiff submitted an employment application via the Indeed platform for the position of \"Class C Driver - Bobtail (Mon-Fri 2:30pm-11:00pm)\" listed by RK Logistics Group, Inc. at its Newark, California facility. At all times relevant herein, Plaintiff held a valid California Class C driver's license. Plaintiff also possessed a temporary Class C license and receipts of procurement issued by the California Department of Motor Vehicles while the DMV processed and mailed the physical license card to Plaintiff. Plaintiff was fully qualified and licensed to operate the bobtail vehicle required for the position."),
 
    ("PARA", "9. At 8:26 PM on June 30, 2026, RK Logistics transmitted to Plaintiff an automated SMS acknowledgment from telephone number +1 (762) 795-5146 stating: \"Thanks for your interest in RK Logistics Group, Inc jobs.\" This communication confirms that RK Logistics was independently recruiting for CDL driver positions through the Indeed platform and received Plaintiff's application directly."),
 
    ("PARA", "10. The following morning, July 1, 2026, at 8:08 AM -- approximately 12 hours after Plaintiff's Indeed application -- Randstad recruiter Dishon Bryant contacted Plaintiff via text message from telephone number +1 (609) 901-1636, stating: \"Hi Brendan, This is Dishon with Randstad. I'm contacting you regarding the class C driver position you applied for at RK Logistics. Give me a call when you get a chance.\" This communication establishes the direct nexus between Plaintiff's Indeed application to RK Logistics and Randstad's inhouse staffing pipeline: Randstad's outreach was triggered by, and explicitly referenced, the Indeed application submitted to RK Logistics less than 12 hours earlier."),
 
    ("PARA", "11. On July 2, 2026, recruiter Dishon Bryant followed up by text message, providing Plaintiff with the identity and direct contact number of the Randstad site manager embedded at the RK Logistics facility: \"Site Manger / Danyea Watkins -5106955468.\" Danyea Watkins (danyea.watkins@randstadusa.com; 510-695-5468) is a Randstad Inhouse Services Site Manager II assigned to the RK Logistics Fremont location -- the same individual who, five days later, emailed Plaintiff requesting completion of a Motor Vehicle Record (\"MVR\") authorization form, confirming Plaintiff's placement in a CDL commercial driving role."),
 
    ("PARA", "12. The Bryant-to-Watkins referral chain documents the complete pre-onboarding pipeline: Plaintiff's June 30, 2026 Indeed application to RK Logistics triggered Randstad recruiter outreach within hours; the Randstad recruiter then referred Plaintiff to the embedded RK Logistics site manager; and five days later the site manager completed onboarding paperwork with the MVR form."),
 
    ("SUBHEAD", "B. Onboarding and Background Investigation"),
 
    ("PARA", "13. On July 7, 2026, Defendant Randstad transmitted to Plaintiff a formal notification from noreply@randstadusa.com stating: \"Your employee status has changed to Rehired.\" The notification, signed \"Randstad General Staffing,\" advised Plaintiff regarding weekly paycheck processing and directed Plaintiff to Randstad's self-service portal at workplace.randstad.com to review and confirm personal and payroll information, including name and address, federal and state tax information, and direct deposit account information."),
 
    ("PARA", "14. That same day, at 2:45 PM, Randstad Inhouse Services Site Manager II Danyea Watkins -- operating inside the RK Logistics Fremont facility -- emailed Plaintiff from danyea.watkins@randstadusa.com requesting completion of an MVR (Motor Vehicle Record) authorization form, confirming that Plaintiff was being placed in a CDL commercial driving role at the RK Logistics facility."),
 
    ("PARA", "15. At 6:22 PM on July 7, 2026, Defendants caused a background investigation to be submitted through InfoMart LLC, a consumer reporting agency headquartered at 1582 Terrell Mill Road, SE, Marietta, Georgia 30067, for the placement designated as \"Randstad App\" (Order No. 15780719). The InfoMart report header confirms: Billing Code: \"RK LOGISTICS\"; Business Unit: \"RIS RK Logistics Fremont\"; Client Package: \"RK Logistics.\" These designations establish that RK Logistics is the billing client, configured the screening package criteria, and is the decision-making entity for the placement."),
 
    ("SUBHEAD", "C. The InfoMart Background Report"),
 
    ("PARA", "16. On July 13, 2026, InfoMart completed and transmitted its background screening report (Order No. 15780719) to Defendants. The report's purpose was designated as \"Pre-Employment.\" The report's Decision Date is July 13, 2026. The report's overall status was designated as \"NEEDS APPROVAL, PER CLIENT CRITERIA\" -- confirming that RK Logistics had established predetermined screening criteria that automatically flagged certain results for adverse action review."),
 
    ("PARA", "17. The InfoMart report is now in Plaintiff's possession. The report conducted criminal history searches across seven jurisdictions, every one of which returned \"No Record\":"),
 
    ("LIST_ITEM", "a. Fresno County, California: No Record;"),
    ("LIST_ITEM", "b. San Joaquin County, California: No Record;"),
    ("LIST_ITEM", "c. Santa Clara County, California: No Record;"),
    ("LIST_ITEM", "d. Stanislaus County, California: No Record;"),
    ("LIST_ITEM", "e. Clark County, Nevada: No Record;"),
    ("LIST_ITEM", "f. State of New York: No Record;"),
    ("LIST_ITEM", "g. Sheridan County, Wyoming: No Record."),
 
    ("PARA", "18. The report's Federal Criminal History search (National Federal) likewise returned \"No Record.\" The OFAC Watch List Search returned \"No name match found.\" The OIG Exclusions List Search returned \"not found.\" The GSA Procurement Exclusion Search returned \"not found.\""),
 
    ("PARA", "19. The sole item of adverse information identified in the entire 15-page report was a result from a National Sex Offender Search, conducted as part of a National Criminal Search. The search returned a \"Record\" for the jurisdiction \"County: Sex Offender, State: California,\" with the name on file listed as \"Newanforbi, Brendan Ngehsi.\" The record contained no case number, no case date, no charge description, no classification, and no disposition. The report's conclusion stated: \"Subject is a registered Sex Offender in California.\""),
 
    ("PARA", "20. The California Sex Offender Registry is therefore confirmed as the sole basis for the report's \"NEEDS APPROVAL\" flag and Defendants' subsequent adverse employment action. This is not a claim pled on information and belief -- Plaintiff possesses the actual InfoMart report, which conclusively demonstrates that every criminal search returned clear and that the sex offender registry listing was the only adverse item."),
 
    ("SUBHEAD", "D. The Pre-Adverse Action Notice"),
 
    ("PARA", "21. On July 13, 2026, at 1:31 PM, InfoMart transmitted to Plaintiff a \"Notice to Consumer for Employment Purposes\" pursuant to Section 607(b) of the Fair Credit Reporting Act (15 U.S.C. section 1681e(b)). The notice stated: \"The purpose of this message is to notify you that InfoMart, a consumer reporting agency, is reporting the criminal or other public record information that may be adverse about you to: Randstad App.\" The notice further stated that the \"above listed employer has certified that it uses such public record information to determine your eligibility for employment, promotion, reassignment, retention, placement and/or volunteering.\""),
 
    ("PARA", "22. The InfoMart notice explicitly identified the information being reported as \"criminal or other public record information.\" The \"other public record information\" referenced in the notice was sex offender registry information disclosed pursuant to Penal Code section 290.46 -- the only item of adverse information in the entire background report."),
 
    ("PARA", "23. The notice provided the following contact information: Randstad telephone: 1-888-990-9209; InfoMart dispute address: P.O. Box 2209, Alpharetta, GA 30023."),
 
    ("SUBHEAD", "E. The Termination"),
 
    ("PARA", "24. On or about July 15, 2026 -- only two business days after the July 13, 2026 pre-adverse action notice -- Defendant Randstad terminated Plaintiff's employment by telephone."),
 
    ("PARA", "25. Defendants terminated Plaintiff a mere two business days after InfoMart transmitted the pre-adverse action notice on Monday, July 13, 2026, without affording Plaintiff a reasonable opportunity to review and dispute the contents of the background report. No written adverse action notice was provided to Plaintiff before, concurrent with, or after the termination."),
 
    ("PARA", "26. The InfoMart report's \"NEEDS APPROVAL, PER CLIENT CRITERIA\" designation confirms that Defendants had established predetermined screening criteria that automatically flagged sex offender registry results for adverse action. The termination was not the product of an individualized assessment of Plaintiff's qualifications, job duties, or fitness for the position; it was the mechanical application of a categorical exclusion triggered by registry status alone."),
 
    ("SUBHEAD", "F. The Statutory Prohibition"),
 
    ("PARA", "27. California Penal Code section 290.46, subdivision (j)(1), provides that \"[a] person is authorized to use information disclosed pursuant to this section only to protect a person at risk.\" Subdivision (j)(2) further provides: \"Except as authorized under paragraph (1) or any other provision of law, use of any information that is disclosed pursuant to this section for purposes relating to any of the following is prohibited: ... (E) Employment.\""),
 
    ("PARA", "28. Subdivision (j)(4)(B) provides that \"[a]ny other misuse of information disclosed pursuant to this section is a misdemeanor,\" punishable by a fine not exceeding twenty-five thousand dollars ($25,000), imprisonment in a county jail not exceeding six months, or both. These criminal penalties confirm the Legislature's determination that the prohibition on employment-related use of registry information reflects a fundamental public policy of the State of California."),
 
    ("PARA", "29. Subdivision (j)(5) provides that any use of information disclosed pursuant to Penal Code section 290.46 for purposes relating to employment \"shall make the user liable for the actual damages, and any amount that may be determined by a jury or a court sitting without a jury, not exceeding three times the amount of actual damage, and not less than two hundred fifty dollars ($250), and attorney's fees, exemplary damages, or a civil penalty not exceeding twenty-five thousand dollars ($25,000).\""),
 
    ("PARA", "30. Defendants' termination of Plaintiff based on sex offender registry information violated each of the foregoing provisions. The termination was not undertaken \"to protect a person at risk\" within the meaning of subdivision (j)(1), and no other provision of law authorized Defendants' use of the registry information for employment purposes. No exception to the statutory prohibition applies to a CDL commercial driving placement."),
 
    ("SUBHEAD", "G. Damages"),
 
    ("PARA", "31. As a direct and proximate result of Defendants' unlawful conduct, Plaintiff has suffered and continues to suffer damages including, but not limited to: loss of wages and employment benefits; loss of earning capacity; emotional distress, humiliation, embarrassment, anxiety, and mental anguish; and other consequential damages. The precise amount of Plaintiff's damages will be established at trial."),
 
    ("PARA", "32. Defendants' conduct was willful, oppressive, and malicious. Defendants maintained a systematic background screening protocol that categorically excluded individuals based on sex offender registry status in direct contravention of Penal Code section 290.46, subdivision (j)(2)(E). The InfoMart report's \"NEEDS APPROVAL, PER CLIENT CRITERIA\" designation demonstrates that the exclusion was automated and predetermined, reflecting a deliberate corporate policy of registry-based employment discrimination rather than an isolated or inadvertent decision."),
 
    # =====================================================
    # FIRST CAUSE OF ACTION
    # =====================================================
    ("HEADER", "FIRST CAUSE OF ACTION"),
    ("SUBHEAD", "Violation of California Penal Code Section 290.46, Subdivision (j)(2)(E)\n(Against All Defendants)"),
 
    ("PARA", "33. Plaintiff incorporates by reference paragraphs 1 through 32 as though fully set forth herein."),
 
    ("PARA", "34. Defendants used information disclosed pursuant to California Penal Code section 290.46 -- specifically, sex offender registry information maintained on the California Department of Justice's public sex offender registry -- for purposes relating to Plaintiff's employment, in violation of Penal Code section 290.46, subdivision (j)(2)(E)."),
 
    ("PARA", "35. Defendants' use of the registry information was not authorized under subdivision (j)(1) (protection of a person at risk) or any other provision of law."),
 
    ("PARA", "36. Pursuant to Penal Code section 290.46, subdivision (j)(5), Plaintiff is entitled to recover: actual damages; an amount not exceeding three times actual damages and not less than $250; attorney's fees; exemplary damages; and/or a civil penalty not exceeding $25,000."),
 
    # =====================================================
    # SECOND CAUSE OF ACTION
    # =====================================================
    ("HEADER", "SECOND CAUSE OF ACTION"),
    ("SUBHEAD", "Wrongful Termination in Violation of Public Policy (Tameny)\n(Against All Defendants)"),
 
    ("PARA", "37. Plaintiff incorporates by reference paragraphs 1 through 32 as though fully set forth herein."),
 
    ("PARA", "38. California Penal Code section 290.46, subdivision (j)(2)(E), establishes a fundamental public policy of the State of California prohibiting the use of sex offender registry information for employment purposes. This public policy is: (a) tethered to a constitutional or statutory provision; (b) designed to benefit the public at large rather than serve a purely private interest; (c) well-established at the time of the termination; and (d) sufficiently substantial and fundamental. (See <<i:Tameny v. Atlantic Richfield Co.>> (1980) 27 Cal.3d 167; <<i:Gantt v. Sentry Insurance>> (1992) 1 Cal.4th 1083, 1090.)"),
 
    ("PARA", "39. Defendants terminated Plaintiff's employment in violation of this fundamental public policy by basing the termination on sex offender registry information disclosed pursuant to Penal Code section 290.46."),
 
    ("PARA", "40. As a direct and proximate result of Defendants' wrongful termination, Plaintiff has suffered and continues to suffer damages including, but not limited to: loss of wages and employment benefits; loss of earning capacity; emotional distress, humiliation, embarrassment, anxiety, and mental anguish; and other consequential damages."),
 
    ("PARA", "41. Defendants' conduct was willful, oppressive, and malicious, entitling Plaintiff to punitive damages pursuant to Civil Code section 3294."),
 
    # =====================================================
    # THIRD CAUSE OF ACTION
    # =====================================================
    ("HEADER", "THIRD CAUSE OF ACTION"),
    ("SUBHEAD", "Violation of the Investigative Consumer Reporting Agencies Act\n(Civil Code Section 1786 et seq.)\n(Against All Defendants)"),
 
    ("PARA", "42. Plaintiff incorporates by reference paragraphs 1 through 32 as though fully set forth herein."),
 
    ("PARA", "43. The InfoMart background screening report procured by Defendants constitutes an \"investigative consumer report\" within the meaning of Civil Code section 1786.2, subdivision (c), in that it was obtained through personal interviews and/or inquiry of public records for the purpose of evaluating Plaintiff's eligibility for employment."),
 
    ("PARA", "44. Defendants violated the Investigative Consumer Reporting Agencies Act (\"ICRAA\") in one or more of the following respects:"),
 
    ("LIST_ITEM", "a. Defendants failed to provide Plaintiff with a clear and conspicuous written disclosure, in a document consisting solely of the disclosure, that an investigative consumer report would be obtained for employment purposes, as required by Civil Code section 1786.16, subdivision (a)(2)(B);"),
 
    ("LIST_ITEM", "b. Defendants failed to provide Plaintiff with a written adverse action notice, as required by Civil Code section 1786.40, subdivision (b), prior to or concurrent with the termination;"),
 
    ("LIST_ITEM", "c. Defendants used the investigative consumer report for a purpose not permitted under the ICRAA, specifically by relying on sex offender registry information that California law categorically prohibits employers from using for employment purposes."),
 
    ("PARA", "45. Pursuant to Civil Code section 1786.50, Plaintiff is entitled to recover: actual damages sustained, or $10,000, whichever is greater, for each violation; punitive damages as the Court may allow; costs of the action; and reasonable attorney's fees as determined by the Court."),
 
    # =====================================================
    # FOURTH CAUSE OF ACTION
    # =====================================================
    ("HEADER", "FOURTH CAUSE OF ACTION"),
    ("SUBHEAD", "Invasion of Privacy\n(California Constitution, Article I, Section 1)\n(Against All Defendants)"),
 
    ("PARA", "46. Plaintiff incorporates by reference paragraphs 1 through 32 as though fully set forth herein."),
 
    ("PARA", "47. Article I, Section 1 of the California Constitution provides that all people have an inalienable right to privacy. This right protects against the improper use of personal information for purposes the law has declared off-limits. (See <<i:Hill v. National Collegiate Athletic Assn.>> (1994) 7 Cal.4th 1.)"),
 
    ("PARA", "48. Plaintiff had a legally protected privacy interest in his sex offender registry information, which the Legislature has expressly prohibited from use in employment decisions through Penal Code section 290.46, subdivision (j)(2)(E). Plaintiff had a reasonable expectation that this information would not be used for employment purposes, given the categorical statutory prohibition."),
 
    ("PARA", "49. Defendants' procurement, review, and use of Plaintiff's sex offender registry information to terminate his employment constituted a serious invasion of Plaintiff's constitutionally protected privacy interest. The invasion was not justified by any competing interest, and the means employed were not the least intrusive available."),
 
    ("PARA", "50. As a direct and proximate result of Defendants' invasion of Plaintiff's privacy, Plaintiff has suffered and continues to suffer damages including, but not limited to: emotional distress, humiliation, embarrassment, anxiety, and mental anguish."),
 
    # =====================================================
    # FIFTH CAUSE OF ACTION
    # =====================================================
    ("HEADER", "FIFTH CAUSE OF ACTION"),
    ("SUBHEAD", "Negligence Per Se\n(Evidence Code Section 669)\n(Against All Defendants)"),
 
    ("PARA", "51. Plaintiff incorporates by reference paragraphs 1 through 32 as though fully set forth herein."),
 
    ("PARA", "52. California Penal Code section 290.46, subdivision (j)(2)(E), establishes a standard of conduct prohibiting the use of sex offender registry information for employment purposes. Subdivision (j)(4)(B) makes the misuse of such information a misdemeanor, establishing that the statutory prohibition carries the force of criminal law."),
 
    ("PARA", "53. Plaintiff is within the class of persons for whose protection the statute was enacted. Employees and job applicants whose names appear on the sex offender registry are the direct and intended beneficiaries of the prohibition on employment-related use of registry information."),
 
    ("PARA", "54. The harm suffered by Plaintiff -- termination of employment based on registry information -- is the type of harm the statute was designed to prevent."),
 
    ("PARA", "55. Defendants violated Penal Code section 290.46, subdivision (j)(2)(E), by using sex offender registry information to terminate Plaintiff's employment. Pursuant to Evidence Code section 669, this violation constitutes negligence per se."),
 
    ("PARA", "56. As a direct and proximate result of Defendants' negligence per se, Plaintiff has suffered and continues to suffer the damages alleged herein."),
 
    # =====================================================
    # SIXTH CAUSE OF ACTION
    # =====================================================
    ("HEADER", "SIXTH CAUSE OF ACTION"),
    ("SUBHEAD", "Unlawful Business Practices\n(Business and Professions Code Section 17200 et seq.)\n(Against All Defendants)"),
 
    ("PARA", "57. Plaintiff incorporates by reference paragraphs 1 through 32 as though fully set forth herein."),
 
    ("PARA", "58. California Business and Professions Code section 17200 defines \"unfair competition\" to include \"any unlawful, unfair or fraudulent business act or practice.\" Defendants' use of sex offender registry information to terminate Plaintiff's employment constitutes an \"unlawful\" business practice because it violates California Penal Code section 290.46, subdivision (j)(2)(E), and the Investigative Consumer Reporting Agencies Act (Civil Code section 1786 et seq.)."),
 
    ("PARA", "59. Defendants' conduct also constitutes an \"unfair\" business practice because the harm caused by using categorically prohibited information to make employment decisions substantially outweighs any purported utility, and because such conduct violates the policy and spirit of the Legislature's express prohibition."),
 
    ("PARA", "60. Defendants' unlawful and unfair business practices have caused Plaintiff to suffer injury in fact and loss of money or property, including but not limited to lost wages and employment benefits."),
 
    ("PARA", "61. Pursuant to Business and Professions Code sections 17203 and 17204, Plaintiff is entitled to restitution of all earnings and benefits lost as a result of Defendants' unlawful and unfair business practices, and to injunctive relief prohibiting Defendants from continuing to engage in the unlawful practices alleged herein."),
 
    # =====================================================
    # PRAYER FOR RELIEF
    # =====================================================
    ("HEADER", "PRAYER FOR RELIEF"),
 
    ("PARA", "WHEREFORE, Plaintiff prays for judgment against Defendants, and each of them, as follows:"),
 
    ("SUBHEAD", "On All Causes of Action:"),
 
    ("LIST_ITEM", "1. For compensatory damages, including lost wages and employment benefits, according to proof at trial;"),
 
    ("LIST_ITEM", "2. For general damages for emotional distress, humiliation, embarrassment, anxiety, and mental anguish, according to proof at trial;"),
 
    ("SUBHEAD", "On the First Cause of Action:"),
 
    ("LIST_ITEM", "3. For treble actual damages, or statutory minimum damages of $250, whichever is greater, pursuant to Penal Code section 290.46, subdivision (j)(5);"),
 
    ("LIST_ITEM", "4. For exemplary damages and/or a civil penalty not exceeding $25,000 per violation, pursuant to Penal Code section 290.46, subdivision (j)(5);"),
 
    ("SUBHEAD", "On the Second Cause of Action:"),
 
    ("LIST_ITEM", "5. For punitive damages pursuant to Civil Code section 3294;"),
 
    ("SUBHEAD", "On the Third Cause of Action:"),
 
    ("LIST_ITEM", "6. For statutory damages of $10,000 per violation, or actual damages, whichever is greater, pursuant to Civil Code section 1786.50;"),
 
    ("LIST_ITEM", "7. For punitive damages pursuant to Civil Code section 1786.50;"),
 
    ("SUBHEAD", "On the Sixth Cause of Action:"),
 
    ("LIST_ITEM", "8. For restitution of all earnings and benefits lost as a result of Defendants' unlawful business practices, pursuant to Business and Professions Code section 17203;"),
 
    ("LIST_ITEM", "9. For injunctive relief prohibiting Defendants from continuing to use sex offender registry information for employment purposes in violation of Penal Code section 290.46, subdivision (j)(2)(E);"),
 
    ("SUBHEAD", "On All Causes of Action:"),
 
    ("LIST_ITEM", "10. For attorney's fees and costs of suit as permitted by law, including Penal Code section 290.46, subdivision (j)(5), and Civil Code section 1786.50;"),
 
    ("LIST_ITEM", "11. For prejudgment interest as permitted by law;"),
 
    ("LIST_ITEM", "12. For such other and further relief as this Court deems just and proper."),
 
    # =====================================================
    # JURY DEMAND
    # =====================================================
    ("HEADER", "DEMAND FOR JURY TRIAL"),
 
    ("PARA", "Plaintiff hereby demands a trial by jury on all issues so triable."),
 
    # =====================================================
    # SIGNATURE
    # =====================================================
    ("SIGNATURE", "\nDated: July 20, 2026\n\n\n___________________________________\nBRENDAN NGEHSI NEWANFORBI\nPlaintiff, In Pro Per"),
 
    # =====================================================
    # VERIFICATION
    # =====================================================
    ("PAGEBREAK", ""),
    ("HEADER", "VERIFICATION"),
 
    ("PARA", "I, BRENDAN NGEHSI NEWANFORBI, declare:"),
 
    ("PARA", "I am the Plaintiff in the above-entitled action. I have read the foregoing Complaint for Damages and know its contents. The matters stated therein are true of my own knowledge, except as to those matters stated on information and belief, and as to those matters I believe them to be true."),
 
    ("PARA", "I declare under penalty of perjury under the laws of the State of California that the foregoing is true and correct."),
 
    ("SIGNATURE", "\nExecuted on July 20, 2026,\nat Stockton, California.\n\n\n___________________________________\nBRENDAN NGEHSI NEWANFORBI"),
]
 
 
# ==========================================================
# MAIN
# ==========================================================
 
def main():
    out = "/home/claude/Complaint_Newanforbi_v_Randstad_US_LLC_et_al_v3.pdf"
    d = PleadingPaper(out)
 
    # === TOP HEADER (condensed) ===
    # Draw attorney block with tight 15pt spacing to save pleading lines
    c = d.c
    atty_y = d._line_y(0)  # Start at line 1 position
    atty_lh = 15  # Tight line height
    atty_lines = [
        ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
        ("Plaintiff, In Pro Per", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12),
        ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12),
        ("E-mail: bnn.cdla@gmail.com", "Times-Roman", 12),
    ]
    for i, (txt, fn, sz) in enumerate(atty_lines):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4  # Resume at line 5
    d.blank_line()
 
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
 
    # === CAPTION BLOCK ===
    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("RANDSTAD US, LLC, a Delaware limited", True, False),
        ("liability company; THE RK LOGISTICS", True, False),
        ("GROUP, INC., a California corporation;", True, False),
        ("and DOES 1 through 20, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
 
    right = [
        ("Case No. __________________", False, False),
        ("", False, False),
        ("COMPLAINT FOR DAMAGES", True, False),
        ("", False, False),
        ("(1) Violation of Penal Code", False, False),
        ("      \u00a7 290.46(j)(2)(E);", False, False),
        ("(2) Wrongful Termination in", False, False),
        ("      Violation of Public Policy;", False, False),
        ("(3) Violation of ICRAA", False, False),
        ("      (Civ. Code \u00a7 1786 et seq.);", False, False),
        ("(4) Invasion of Privacy", False, False),
        ("      (Cal. Const. Art. I, \u00a7 1);", False, False),
        ("(5) Negligence Per Se", False, False),
        ("      (Evid. Code \u00a7 669);", False, False),
        ("(6) Unfair Business Practices", False, False),
        ("      (Bus. & Prof. Code \u00a7 17200)", False, False),
        ("", False, False),
        ("[Unlimited Civil]", False, True),
        ("[Jury Trial Demanded]", False, True),
    ]
 
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
 
    d.blank_line()
 
    # RENDER BODY
    for c_type, text in CONTENT:
        if c_type == "HEADER":
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type == "SUBHEAD":
            for line in text.split("\n"):
                d.write_line(line, bold=True, center=False)
            d.blank_line()
        elif c_type == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif c_type == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=36)
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
