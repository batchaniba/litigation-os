import re, sys, textwrap, types
from pathlib import Path
REPO = Path("/workspace/m20-merge/repo")
sys.path.insert(0, str(REPO/"internal/scripts/lib"))
src = Path("ref/r.py").read_text().replace('REPO = HERE.parents[4]', 'REPO = Path("/workspace/m20-merge/repo")')
r = types.ModuleType("r"); r.__file__="/workspace/m20-pleading/ref/r.py"; exec(compile(src, "r.py", "exec"), r.__dict__)
FC = r.FOOTER_CASE
DRAFT_H = [("Hon. Jenna M. Whitman, Dept. 25",False,False),("Hearing: Jan. 8, 2027, 9:00 a.m.",False,False),
           ("(reservation; verify entered order)",False,False),("Reservation No. 958052306492",False,False),
           ("Action filed May 29, 2026",False,False),("Trial: Not set",False,False)]
PKT_H = [("Hon. Jenna M. Whitman, Dept. 25",False,False),("Hearing: January 8, 2027, 9:00 a.m.,",False,False),
         ("Department 25; Reservation No. 958052306492",False,False),
         ("Action filed May 29, 2026",False,False),("Trial: Not set",False,False)]
HEAR = ["Hon. Jenna M. Whitman, Dept. 25","Hearing: January 8, 2027, 9:00 a.m., Department",
        "25; Reservation No. 958052306492","Action filed May 29, 2026","Trial: Not set"]
def right(title, hearing):
    rows=[("Case No. 26CV191136",False),("",False)]
    rows += [(l,True) for l in textwrap.wrap(title.replace("\u2019","'").upper(), 36)]
    rows.append(("",False)); rows += [(h,False) for h in HEAR]; return rows
from pleading_paper import (CONTENT_LEFT, CONTENT_WIDTH, CONTENT_RIGHT, VERT_LINE_RIGHT)
def header(d, meta):
    c=d.c; y0=d._line_y(0)
    for i,(t,b) in enumerate([("BRENDAN NGEHSI NEWANFORBI",1),("1455 Cat Tail Drive",0),("Stockton, CA 95204",0),
        ("Telephone: (209) 801-4442",0),("Email: bnn.cdl@gmail.com",0),("Petitioner, in propria persona",0)]):
        c.setFont("Times-Bold" if b else "Times-Roman",12); c.drawString(CONTENT_LEFT, y0-i*13.5, t)
    d.current_line=5
    d.write_line("SUPERIOR COURT OF THE STATE OF CALIFORNIA", bold=True, center=True)
    d.write_line("COUNTY OF ALAMEDA", bold=True, center=True)
    L=lambda n: d._line_y(n-1)
    bx=CONTENT_LEFT+CONTENT_WIDTH*0.55; x=CONTENT_LEFT+8
    c.setFont("Times-Bold",12); c.drawString(x,L(9),"BRENDAN NGEHSI NEWANFORBI,")
    c.setFont("Times-Roman",12); c.drawRightString(bx-90,L(10)-6,"Petitioner,")
    c.drawString(x+30,L(12),"v.")
    c.setFont("Times-Bold",12)
    for i,t in enumerate(["CALIFORNIA HIGHWAY PATROL;","G. SERRATO, in his official capacity","as Captain and","Commander of CHP Dublin Area,"]):
        c.drawString(x,L(13)-i*16,t)
    c.setFont("Times-Roman",12); c.drawRightString(bx-80,L(16)-4,"Respondents.")
    c.setLineWidth(0.75); top=L(9)+14; bot=L(16)-12
    c.line(VERT_LINE_RIGHT,top,bx,top); c.line(VERT_LINE_RIGHT,bot,bx,bot); c.line(bx,top,bx,bot)
    rx=bx+12; y=L(9)
    for t,b in meta["right"]:
        fn="Times-Bold" if b else "Times-Roman"; sz=9
        while sz>7 and c.stringWidth(t,fn,sz)>CONTENT_RIGHT-rx-6: sz-=0.25
        c.setFont(fn,sz); c.drawString(rx,y,t); y-=15
    d.current_line=18
def render(md_path, out_path):
    from pleading_paper import PleadingPaper
    docs=r.split_docs(md_path.read_text()); stats={"papers":[],"mpa_substance_pages":None}
    d=None
    for title,body in docs:
        meta=r.PAPERS[title]
        if d is None: d=PleadingPaper(str(out_path), doc_title_footer=meta["footer"])
        else: d.doc_title_footer=meta["footer"]; d.start_new_page()
        header(d, meta); r.render_body(d, body, meta, stats)
    d.save()
JOBS = [  # src, out name, {title: short footer}, hearing, draft
 ("01","Declaration of Brendan Ngehsi Newanforbi - Pleading",{None:"DECLARATION OF B.N. NEWANFORBI"},DRAFT_H,True),
 ("02","Alternative A Proposed Judgment Directing Certification - Pleading",{None:"[ALT. A PROPOSED] JUDGMENT"},DRAFT_H,True),
 ("03","Alternative Proposed Order Setting Limited Evidentiary Proceedings - Pleading",{None:"[ALT. PROPOSED] EVIDENTIARY ORDER"},DRAFT_H,True),
 ("04","Alternative A Proposed Peremptory Writ Directing Certification - Pleading",{None:"[ALT. A PROPOSED] WRIT"},DRAFT_H,True),
 ("05","Proof of Service of Motion Papers (Blank Form) - Pleading",{None:"PROOF OF SERVICE"},DRAFT_H,True),
 ("06","Motion Packet - Notice, MPA, Declaration, Proposed Writ, Alt Order, Proposed Judgment, Proof of Service - Pleading",{
   "PETITIONER'S NOTICE OF MOTION AND MOTION FOR ISSUANCE OF PEREMPTORY WRIT OF MANDATE":"NOTICE OF MOTION",
   "MEMORANDUM OF POINTS AND AUTHORITIES":"MEMORANDUM OF POINTS AND AUTHORITIES",
   "DECLARATION OF BRENDAN NGEHSI NEWANFORBI IN SUPPORT OF MOTION FOR PEREMPTORY WRIT OF MANDATE":"DECLARATION OF B.N. NEWANFORBI",
   "[PROPOSED] PEREMPTORY WRIT OF MANDATE":"[PROPOSED] PEREMPTORY WRIT",
   "[ALTERNATIVE PROPOSED] ORDER SETTING LIMITED EVIDENTIARY PROCEEDINGS ON FIRST CAUSE OF ACTION":"[ALT. PROPOSED] EVIDENTIARY ORDER",
   "[PROPOSED] JUDGMENT GRANTING RELIEF ON FIRST CAUSE OF ACTION AND DIRECTING LAWFUL RECONSIDERATION":"[PROPOSED] JUDGMENT",
   "PROOF OF SERVICE OF MOTION PAPERS":"PROOF OF SERVICE"},PKT_H,False),
 ("07","Memorandum of Points and Authorities - Pleading",{None:"MEMORANDUM OF POINTS AND AUTHORITIES"},DRAFT_H,True),
 ("08","Alternative B Proposed Peremptory Writ Directing Reconsideration - Pleading",{None:"[ALT. B PROPOSED] WRIT"},DRAFT_H,True),
 ("09","Alternative B Proposed Judgment Directing Reconsideration - Pleading",{None:"[ALT. B PROPOSED] JUDGMENT"},DRAFT_H,True),
 ("10","Notice of Motion and Motion for Judgment on First Cause of Action - Pleading",{None:"NOTICE OF MOTION"},DRAFT_H,True),
]
FOOTMAP = {"PETITIONER'S NOTICE OF MOTION AND MOTION FOR ISSUANCE OF PEREMPTORY WRIT OF MANDATE":"NOTICE OF MOTION FOR PEREMPTORY WRIT OF MANDATE", "PETITIONER'S NOTICE OF MOTION AND MOTION FOR JUDGMENT ON FIRST CAUSE OF ACTION AND FOR ISSUANCE OF PEREMPTORY WRIT OF MANDATE":"NOTICE OF MOTION FOR JUDGMENT AND PEREMPTORY WRIT OF MANDATE"}
SIG_START = re.compile(r"^(DATED|Dated|Date:|Executed|IT IS SO|Issued:|_{5,}|\[ACTUAL SIGNATURE)")
orig_write_para = r._write_para
sig=[False]; SIGPNG='/workspace/m20-pleading/assets/sig.png'
from pleading_paper import CONTENT_RIGHT
def write_para(d, raw):
    lines=[l.strip() for l in raw.splitlines() if l.strip()]
    if lines and SIG_START.match(lines[0]) and (len(lines)>1 or lines[0].startswith("_")):
        d.ensure_space(len(lines)+2)
        for i,l in enumerate(lines):
            if i==0 and not l.startswith("_") and not l.startswith("[ACTUAL"):
                d.write_wrapped(r.md_inline(l), first_indent=0)
            elif l.startswith("/s/"):
                d.blank_line(); sig[0]=True
            elif l.startswith("_") and sig[0]:
                sig[0]=False; d._ensure_line(); y=d._line_y(d.current_line)
                lw=d.c.stringWidth(l,"Times-Roman",12); cx=CONTENT_RIGHT-20-lw/2
                from PIL import Image as _I; iw,ih=_I.open(SIGPNG).size; h=30; w=h*iw/ih
                if w>lw+10: w=lw+10; h=w*ih/iw
                d.c.drawImage(SIGPNG,cx-w/2,y+2,width=w,height=h,mask='auto')
                d.write_line(r.md_inline(l), right=True, right_margin_offset=20)
            elif len(l) > 44:
                d.write_wrapped(r.md_inline(l), first_indent=0, indent=0)
            else:
                d.write_line(r.md_inline(l), right=True, right_margin_offset=20)
        d.blank_line(); return
    orig_write_para(d, raw)
r._write_para = write_para
r.split_docs = lambda md: [(m.group(1).strip(), m.group(2).strip()) for m in re.finditer(r"^# ([^\n]+)\n(.*?)(?=^# |\Z)", md, re.S|re.M)]
out = Path("out"); out.mkdir(exist_ok=True)
import pymupdf
ONLY=set(sys.argv[1:])
for sid, name, footers, hearing, draft in JOBS:
    if ONLY and sid not in ONLY: continue
    md = Path(f"src/{sid}.md").read_text()
    r.PAPERS = {}
    for t,_ in r.split_docs(md):
        f = footers.get(t, footers.get(None))
        r.PAPERS[t] = {"footer": FOOTMAP.get(t, t.replace("\u2019","'").upper()) + " - 26CV191136", "right": right(t, hearing), "center_title": False}
    tmp = Path(f"src/{sid}.md")
    dest = out/f"{name}.pdf"
    render(tmp, dest); r._drop_empty_trailing_pages(dest)
    print(sid, len(pymupdf.open(dest)), dest.name)
