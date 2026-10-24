from pleading_paper import *
from reportlab.lib.colors import black, white, Color
G1=Color(.45,.45,.45); G2=Color(.78,.78,.78); G3=Color(.93,.93,.93)
CX=(VERT_LINE_LEFT+CONTENT_RIGHT)/2
SLIP={
"A":("Denial of Form I-918 Supplement B Certification",
 ["Letter dated April 20, 2026  \u00b7  Capt. G. Serrato, Commander, CHP Dublin Area","To Brendan N. Newanforbi  \u00b7  File No. 390.18437.17620.26-050","Filed petition PDF p. 45 (Pet. Ex. 1)  \u00b7  App. {r}"]),
"B":("Form I-918 Supplement B Certification Request",
 ["Submitted April 9, 2026  \u00b7  Brendan Ngehsi Newanforbi to CHP Dublin Area","With April 9 transmittal e-mail and April 10, 2026 CHP acknowledgment","Filed petition PDF pp. 47\u201366, 145\u2013146 (Pet. Exs. 2\u20134, 13)  \u00b7  App. {r}"]),
"C":("CHP Arrest Records \u2014 Production Exhibit 5",
 ["Arrest of November 1, 2024  \u00b7  CHP 202, DS 367, warrant and affidavit, screen prints","Produced October 23, 2026 by Respondents (Cal. Dept. of Justice)","AGO 000029\u2013000053  \u00b7  App. {r}"]),
"D":("CHP Incident Detail Report (CAD Log)",
 ["Incident No. 241101GG0064  \u00b7  November 1, 2024","Produced October 23, 2026 by Respondents (Cal. Dept. of Justice)","AGO 000022\u2013000024  \u00b7  App. {r}"]),
"E":("CHP 415 Daily Activity Records",
 ["October 31, 2024  \u00b7  Officers S. Meza-Gonzales (ID 023295) and J. Melano (ID 023054)","Produced October 23, 2026 by Respondents (Cal. Dept. of Justice)","Production Exhibits 8 and 11  \u00b7  App. {r}"]),
"F":("Transcript of CHP Dashcam Recording",
 ["Recording of November 1, 2024  \u00b7  Prepared by Petitioner","15-page edition submitted to CHP with the April 9, 2026 request","Filed petition PDF pp. 68\u201382 (Pet. Ex. 5)  \u00b7  App. {r}"]),
"G":("Penal Code \u00a7 851.6 Detention Certificate",
 ["CHP Dublin Area (01991)  \u00b7  Arrest of November 1, 2024","Certifies a detention only, not an arrest","Filed petition PDF p. 90 (Pet. Ex. 7)  \u00b7  App. {r}"]),
"H":("CHP and POST Complaint Correspondence",
 ["CHP complaint assignment letter, March 26, 2026  \u00b7  Capt. G. Serrato","POST acknowledgment letter, March 23, 2026","Filed petition PDF pp. 141, 143 (Pet. Exs. 11, 12)  \u00b7  App. {r}"]),
"I":("CHP Dublin Area Beat Assignment Sheet",
 ["October 31, 2024  \u00b7  Graveyard shift","Produced October 23, 2026 by Respondents (Cal. Dept. of Justice)","AGO 000025  \u00b7  App. {r}"]),
}
NOTE={"B":["Working copy reconstructed from the filed petition; pending verification","against the as-sent April 9, 2026 e-mail and attachments."],
"F":["Conditional status: prepared by Petitioner; speaker labels and bracketed descriptions are Petitioner\u2019s own.","Not CHP-certified and not a substitute for the original recording, which controls.","Not the separate 19-page Matter 33 edition."],
"H":["Correspondence only; the underlying complaints to CHP and POST are not included."]}
FOOT="Declaration of Brendan Ngehsi Newanforbi ISO Motion for Judgment on First Cause of Action"
def slip(path,L,a,b):
    d=PleadingPaper(str(path),doc_title_footer=f"EXHIBIT {L} - 26CV191136"); c=d.c
    r=f"{a:03d}\u2013{b:03d}"; x0,x1=VERT_LINE_RIGHT,CONTENT_RIGHT; y0,y1=FOOTER_RULE_Y+10,PAGE_H-34
        # banner
    bh=62; c.setFillColor(black); c.rect(x0,y1-bh,x1-x0,bh,fill=1,stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold",12.5); c.drawCentredString((x0+x1)/2,y1-21,"ALAMEDA COUNTY SUPERIOR COURT")
    cap="NEWANFORBI v. CALIFORNIA HIGHWAY PATROL, ET AL."; c.setFont("Helvetica",9)
    c.drawCentredString((x0+x1)/2,y1-37,cap); c.setFont("Helvetica",9); c.drawCentredString((x0+x1)/2,y1-52,"Case No. 26CV191136")
    # progress marker
    L9="ABCDEFGHI"; sp=17; sx=(x0+x1)/2-sp*4
    for k,ch in enumerate(L9):
        cx=sx+k*sp
        if ch==L:
            c.setFillColor(black); c.circle(cx,y1-bh-26,7.2,fill=1,stroke=0); c.setFillColor(white); c.setFont("Helvetica-Bold",8.5)
        else: c.setFillColor(G2 if L9.index(ch)>L9.index(L) else G1); c.setFont("Helvetica",8.5)
        c.drawCentredString(cx,y1-bh-29,ch)
    c.setFillColor(G1); c.setFont("Helvetica",7); c.drawCentredString((x0+x1)/2,y1-bh-46,f"EXHIBIT {L} OF I")
    m=(x0+x1)/2
    c.setFillColor(black); c.setFont("Helvetica",26); c.drawCentredString(m,505,"E X H I B I T")
    c.setFont("Helvetica-Bold",210); c.drawCentredString(m,335,L)
    c.setLineWidth(0.9); c.line(m-170,312,m+170,312)
    t,lines=SLIP[L]; c.setFont("Helvetica-Bold",14.5); c.drawCentredString(m,288,t)
    c.setFont("Helvetica",10); y=267
    for ln in lines:
        ln=ln.format(r=r); fs=10
        while c.stringWidth(ln,"Helvetica",fs)>x1-x0-24: fs-=.25
        c.setFont("Helvetica",fs); c.drawCentredString(m,y,ln); y-=15
    if L in NOTE:
        y-=10; c.setStrokeColor(G2); c.setLineWidth(0.5); c.line(m-40,y+6,m+40,y+6); y-=8
        c.setFillColor(G1)
        for ln in NOTE[L]:
            fs=8
            while c.stringWidth(ln,"Helvetica-Oblique",fs)>x1-x0-30: fs-=.25
            c.setFont("Helvetica-Oblique",fs); c.drawCentredString(m,y,ln); y-=11
    c.setFillColor(G1); c.setFont("Helvetica",7.5); c.drawCentredString(CX,9,FOOT)
    # right-edge App. tab (in margin, clear of rule)
    tx,tw,th=CONTENT_RIGHT+6,24,150; ty=420
    c.setFillColor(G3); c.setStrokeColor(G2); c.setLineWidth(.5); c.roundRect(tx,ty,tw,th,4,fill=1,stroke=1)
    c.setFillColor(black); c.rect(tx,ty+th-24,tw,24,fill=1,stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold",13); c.drawCentredString(tx+tw/2,ty+th-17,L)
    c.saveState(); c.translate(tx+tw/2+3.5,ty+(th-24)/2); c.rotate(90); c.setFillColor(G1); c.setFont("Helvetica",8.5); c.drawCentredString(0,0,f"APP. {r}"); c.restoreState()
    # App. page stamp on the footer row, right
    c.setFillColor(black); c.setFont("Times-Bold",10); c.drawRightString(CONTENT_RIGHT-4,FOOTER_PAGE_Y,f"App. {a:03d}")
    d.save()
