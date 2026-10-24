import re, sys, textwrap, types
from pathlib import Path
REPO = Path("/workspace/m20-merge/repo")
sys.path.insert(0, str(REPO/"internal/scripts/lib"))
src = Path("/workspace/m20-pleading/ref/r.py").read_text().replace('REPO = HERE.parents[4]', 'REPO = Path("/workspace/m20-merge/repo")')
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
