import sys, textwrap, pymupdf
from pathlib import Path
sys.path.insert(0,"/workspace/m20-merge/repo/internal/scripts/lib")
sys.path.insert(0,"/workspace/m20-pleading")
from pleading_paper import PleadingPaper, CONTENT_LEFT, CONTENT_RIGHT, VERT_LINE_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
R=Path("/workspace/m20-merge/iw/internal/private/research/matter-20")
PET=R/"01-portfolio-records/matter-32/from-20/0.Newanforbi v. CHP - Writ of Mandate.pdf"
SU=R/"03-discovery-production/session-uploads"
COV=R/"03-discovery-production/branch-snapshots/agent__matter-20-production-map/internal/docs/matter-20-production-set-one/Dashcam Videos Coversheet.pdf"
W=Path("/workspace/m20-pleading/appendix"); OUT=Path("/workspace/m20-pleading/out")
EX=[
("A","Signed April 20, 2026 denial letter of Capt. G. Serrato, Commander, CHP Dublin Area",[(PET,[45])],"Filed petition (May 29, 2026) PDF p. 45 (Pet. Ex. 1)",[]),
("B","April 9, 2026 Form I-918 Supplement B certification submission, with April 9 transmittal e-mail and April 10, 2026 CHP acknowledgment e-mail",[(PET,range(47,67)),(PET,[145,146])],"Filed petition PDF pp. 47-66 (Pet. Exs. 2-4, incl. petition cover sheets at pp. 52, 61) and pp. 145-146 (Pet. Ex. 13)",
 ["WORKING COPY reconstructed from the filed petition (PDF pp. 47-66, 145-146).","Pending verification against the as-sent April 9, 2026 e-mail and attachments.","Petition exhibit cover sheets (Exhibits 3 and 4) are reproduced as filed."]),
("C","CHP production Exhibit 5 (complete): CHP 202 arrest report, laboratory reports, DS 367 forms, chemical test admonition, probable cause declaration, notice to appear, consolidated arrest report, CHP 180, search warrant and affidavit, blood test request, property receipt, arrest screen prints",[("BATES",None),(SU/"Exhibit-5-CHP-202-DS-367-Warrant-Affidavit.pdf",None)],"Respondents' production of Oct. 23, 2026, AGO 000029-000053 (25 pp.), preceded by a one-page Bates index",[]),
("D","CHP Incident Detail Report (CAD log), Incident No. 241101GG0064 (complete)",[(SU/"Exhibit-3-Incident-Log-241101GG0064.pdf",None)],"Respondents' production of Oct. 23, 2026, AGO 000022-000024 (3 pp.)",[]),
("E","CHP 415 daily activity records, Oct. 31, 2024: Officer S. Meza-Gonzales (ID 023295) and Officer J. Melano (ID 023054)",[(SU/"Exhibit-8-CHP-415-Meza-Gonzales-10-31-2024.pdf",None),(SU/"Exhibit-11-CHP-415-Melano-10-31-2024.pdf",None)],"Respondents' production of Oct. 23, 2026, production Exhibits 8 and 11 (1 p. each)",[]),
("F","Petitioner-prepared transcript of CHP dashcam recording, Nov. 1, 2024 - the 15-page edition submitted with the April 9, 2026 request",[(PET,range(68,83))],"Filed petition PDF pp. 68-82 (Pet. Ex. 5)",
 ["CONDITIONAL STATUS: prepared by Petitioner; speaker labels and bracketed","descriptions are Petitioner's own. Not CHP-certified and not a substitute for","the original recording, which controls. Offered as the edition submitted to CHP","with the April 9 request. Not the separate 19-page Matter 33 edition."]),
("G","Penal Code section 851.6 detention certificate, CHP Dublin",[(PET,[90])],"Filed petition PDF p. 90 (Pet. Ex. 7)",[]),
("H","CHP/POST correspondence: CHP complaint assignment letter (Mar. 26, 2026) and POST acknowledgment letter (Mar. 23, 2026)",[(PET,[141]),(PET,[143])],"Filed petition PDF pp. 141 (Pet. Ex. 11) and 143 (Pet. Ex. 12)",
 ["Correspondence only. The underlying complaints submitted to CHP and POST","have not yet been located and are not included."]),
("I","CHP Dublin Area beat assignment sheet, Oct. 31, 2024 (graveyard shift)",[(SU/"Exhibit-4-Beat-sheet-10-31-2024.pdf",None)],"Respondents' production of Oct. 23, 2026, AGO 000025 (1 p.)",[]),
]
BATES=[(29,33,"CHP 202 Driving Under the Influence arrest-investigation report (pp. 1-5)"),(34,39,"Laboratory reports, Ascertain Forensics No. 2024-004531 (ethanol; drug panels)"),
(40,41,"DS 367 Age 21 and Older Officer's Statement (pp. 1-2)"),(42,42,"DS 367 Administrative Per Se Suspension/Revocation Order and Temporary Driver License"),
(43,43,"Chemical Test Admonition (CVC 23154, 23612)"),(44,44,"Declaration and Determination of Probable Cause for Warrantless Arrest (Alameda County)"),
(45,45,"CHP 215 Notice to Appear No. RJ68845"),(46,46,"Alameda County Consolidated Arrest Report"),(47,47,"CHP 180 Vehicle Report"),
(48,49,"Search Warrant (DUI Blood Draw, Pen. Code 1524(a)(13)) and Statement of Probable Cause/Affidavit"),(50,50,"Bay Area PLS Blood Test Request Form"),
(51,51,"Alameda County Sheriff's Department Prisoner Property Receipt"),(52,53,"CHP Area Information System Arrest Screen Print (2 pp.)")]
def bates_index(path,first_app):
    c=canvas.Canvas(str(path),pagesize=letter); w,h=letter
    c.setFont("Times-Bold",14); c.drawCentredString(w/2,h-80,"EXHIBIT C - BATES INDEX")
    c.setFont("Times-Roman",10.5); c.drawCentredString(w/2,h-98,"CHP production Exhibit 5, AGO 000029-000053 (25 pages, reproduced complete and in produced order)")
    y=h-130; c.setFont("Times-Bold",10.5); c.drawString(60,y,"Bates range"); c.drawString(170,y,"App. pages"); c.drawString(250,y,"Document (description supplied by Petitioner for convenience)"); y-=6; c.line(60,y,w-60,y); y-=16
    c.setFont("Times-Roman",10.5)
    for a,b,dsc in BATES:
        c.drawString(60,y,f"AGO {a:06d}"+(f"-{b:06d}" if b!=a else ""))
        aa,bb=first_app+a-29,first_app+b-29; c.drawString(170,y,f"App. {aa:03d}"+(f"-{bb:03d}" if bb!=aa else ""))
        for k,ln in enumerate(textwrap.wrap(dsc,62)): c.drawString(250,y-k*13,ln)
        y-=13*len(textwrap.wrap(dsc,62))+7
    c.save()
def cover(path,L,desc,note):
    c=canvas.Canvas(str(path),pagesize=letter); w,h=letter
    c.setFont("Times-Bold",54); c.drawCentredString(w/2,h/2+60,f"EXHIBIT {L}")
    c.setFont("Times-Roman",13); y=h/2+10
    for ln in textwrap.wrap(desc,62): c.drawCentredString(w/2,y,ln); y-=17
    if note:
        y-=22; c.setFont("Times-Bold",10.5)
        for ln in note: c.drawCentredString(w/2,y,ln); y-=14
    c.save()
import os
MODE=os.environ.get('MODE','decl')
if MODE=='packet':
    A=pymupdf.open(OUT/'Exhibits A-I to Declaration - Appendix.pdf'); ni=2
    toc=[(t[1].split()[-1],t[2]-ni) for t in A.get_toc() if t[1].startswith('Exhibit')]
if MODE!='packet':
    app=pymupdf.open(); rows=[]; toc=[]
    for L,desc,parts,src,note in EX:
        import slip as SL
        n=sum(1 if f=="BATES" else (len(list(pg)) if pg else len(pymupdf.open(f))) for f,pg in parts)
        cp=W/f"cover_{L}.pdf"; SL.slip(cp,L,len(app)+1,len(app)+1+n)
        start=len(app)+1; app.insert_pdf(pymupdf.open(cp)); toc.append((L,start))
        for f,pgs in parts:
            if f=="BATES":
                bates_index(W/"bates_C.pdf",len(app)+2); app.insert_pdf(pymupdf.open(W/"bates_C.pdf")); continue
            s=pymupdf.open(f); pgs=list(pgs) if pgs else list(range(1,len(s)+1))
            for p in pgs: app.insert_pdf(s,from_page=p-1,to_page=p-1)
        rows.append((L,desc,src,start,len(app)))
    ocred=[]; COVERS={s for _,s in toc}
    for i,pg in enumerate(app):
        if len(pg.get_text().strip())>=200 or i+1 in COVERS: continue
        tp=pg.get_textpage_ocr(dpi=300,full=True)
        for x0,y0,x1,y1,wd,*_ in pg.get_text("words",textpage=tp):
            if pg.get_text("text",clip=pymupdf.Rect(x0,y0,x1,y1)).strip(): continue
            fs=max(4,(y1-y0)*0.85); fw=pymupdf.get_text_length(wd,fontname="helv",fontsize=fs)
            if fw>0 and fw>(x1-x0): fs=fs*(x1-x0)/fw
            pg.insert_text((x0,y1-(y1-y0)*0.18),wd,fontsize=fs,fontname="helv",render_mode=3)
        ocred.append(i+1)
    # stamp, scaling page down if content would be covered
    final=pymupdf.open(); scaled=[]
    for i,pg in enumerate(app):
        r=pg.rect; stamp=pymupdf.Rect(r.x1-90,r.y1-26,r.x1-14,r.y1-8)
        hit=any(pymupdf.Rect(b[:4]).intersects(stamp) for b in pg.get_text("blocks")) or \
            any(pymupdf.Rect(x["bbox"]).intersects(stamp) for x in pg.get_image_info()) or \
            any(d["rect"].intersects(stamp) for d in pg.get_drawings())
        np=final.new_page(width=612,height=792)
        if i+1 in COVERS: np.show_pdf_page(np.rect,app,i); continue
        if hit or abs(r.width-612)>1 or abs(r.height-792)>1:
            np.show_pdf_page(pymupdf.Rect(18,0,594,792-36),app,i,keep_proportion=True); scaled.append(i+1)
        else: np.show_pdf_page(np.rect,app,i)
        np.insert_textbox(pymupdf.Rect(612-104,792-28,612-18,792-10),f"App. {i+1:03d}",fontname="tibo",fontsize=10,align=2)
    final.save(W/"body.pdf")
    import shutil; shutil.copy(W/"body.pdf",W/"body_unredacted.pdf"); import redact; redact.apply(W/"body.pdf")
    # index on pleading paper
    import build_hdr as H
    d=PleadingPaper(str(W/"index.pdf"),doc_title_footer="INDEX OF EXHIBITS - 26CV191136")
    T="INDEX OF EXHIBITS TO DECLARATION OF BRENDAN NGEHSI NEWANFORBI IN SUPPORT OF MOTION FOR PEREMPTORY WRIT OF MANDATE"
    H.header(d,{"right":H.right(T,None)})
    d.write_line("INDEX OF EXHIBITS",bold=True,center=True)
    d.write_wrapped("Exhibits to the Declaration of Brendan Ngehsi Newanforbi in Support of Motion for Peremptory Writ of Mandate (Cal. Rules of Court, rule 3.1110(f)). \"App.\" numbers are stamped at the bottom right of each appendix page; each source document retains its own Bates or printed page numbers.")
    c=d.c; xs=[CONTENT_LEFT,CONTENT_LEFT+30,CONTENT_LEFT+250,CONTENT_RIGHT-70,CONTENT_RIGHT]
    def rowlines(cells,fs=9):
        ws=[int((xs[k+1]-xs[k]-6)/(fs*0.47)) for k in range(4)]
        return [textwrap.wrap(t,ws[k]) or [""] for k,t in enumerate(cells)]
    y=[d._line_y(d.current_line)+6]
    def draw(cells,bold=False):
        fs=9; wl=rowlines(cells); n=max(len(x) for x in wl); hgt=n*11+6
        if y[0]-hgt<d._line_y(27):
            d.start_new_page(); y[0]=d._line_y(0)+6
        c.setLineWidth(0.5)
        for k in range(4):
            c.setFont("Times-Bold" if bold else "Times-Roman",fs)
            for j,t in enumerate(wl[k]): c.drawString(xs[k]+3,y[0]-11-j*11,t)
        c.rect(xs[0],y[0]-hgt,xs[4]-xs[0],hgt)
        for x in xs[1:4]: c.line(x,y[0],x,y[0]-hgt)
        y[0]-=hgt
    draw(["Exh.","Description","Source / Bates","App. pages"],True)
    for L,desc,src,a,b in rows: draw([L,desc,src,f"App. {a:03d}-{b:03d}"])
    d.save()
    idx=pymupdf.open(W/"index.pdf"); ni=len(idx)
    A=pymupdf.open(); A.insert_pdf(idx); A.insert_pdf(pymupdf.open(W/"body.pdf"))
    A.set_toc([[1,"Index of Exhibits",1]]+[[1,f"Exhibit {L}",s+ni] for L,s in toc])
    an=OUT/"Exhibits A-I to Declaration - Appendix.pdf"; A.save(an,garbage=3,deflate=True)
    # declaration + appendix
    D=pymupdf.open(OUT/"Declaration of Brendan Ngehsi Newanforbi - Pleading.pdf"); nd=len(D)
    dt=D.get_toc() or []
    D.insert_pdf(A); D.set_toc(dt+[[1,"Declaration",1]]*(not dt)+[[1,"Index of Exhibits",nd+1]]+[[2,f"Exhibit {L}",nd+ni+s] for L,s in toc])
    D.save(OUT/"Declaration of Brendan Ngehsi Newanforbi with Exhibits A-I.pdf",garbage=3,deflate=True)
if MODE in ('packet','all'):
    # packet
    pk=list(OUT.glob("Motion Packet - *Pleading.pdf"))[0]; P=pymupdf.open(pk)
    foot=lambda p: P[p].get_text()
    dec=[i for i in range(len(P)) if "DECLARATION OF BRENDAN NGEHSI NEWANFORBI IN SUPPORT OF MOTION FOR PEREMPTORY WRIT OF MANDATE - 26CV191136" in foot(i)]
    end=max(dec)
    N=pymupdf.open(); N.insert_pdf(P,to_page=end); N.insert_pdf(A); N.insert_pdf(P,from_page=end+1)
    FT=[("NOTICE OF MOTION FOR PEREMPTORY WRIT OF MANDATE - 26CV191136","Notice of Motion"),("MEMORANDUM OF POINTS AND AUTHORITIES - 26CV191136","Memorandum of Points and Authorities"),
        ("DECLARATION OF BRENDAN NGEHSI NEWANFORBI IN SUPPORT OF MOTION FOR PEREMPTORY WRIT OF MANDATE - 26CV191136","Declaration of Brendan Ngehsi Newanforbi"),
        ("[PROPOSED] PEREMPTORY WRIT OF MANDATE - 26CV191136","[Proposed] Peremptory Writ of Mandate"),("[ALTERNATIVE PROPOSED] ORDER SETTING LIMITED EVIDENTIARY PROCEEDINGS","[Alternative Proposed] Order Setting Limited Evidentiary Proceedings"),
        ("[PROPOSED] JUDGMENT GRANTING RELIEF","[Proposed] Judgment"),("PROOF OF SERVICE OF MOTION PAPERS - 26CV191136","Proof of Service")]
    def newp(i): return i+1 if i<=end else i+1+len(A)
    T=[]; last=None
    for i in range(len(P)):
        txt=P[i].get_text().replace("\n"," ")
        lab=next((l for f,l in FT if f in txt),None)
        if lab and lab!=last: T.append([1,lab,newp(i)]); last=lab
        if i==end: T+= [[2,"Appendix of Exhibits - Index",end+2]]+[[3,f"Exhibit {L}",end+1+ni+s] for L,s in toc]
    N.set_toc(T)
    N.save(OUT/(pk.stem+" - with Exhibits A-I.pdf"),garbage=3,deflate=True)
    print(T)
