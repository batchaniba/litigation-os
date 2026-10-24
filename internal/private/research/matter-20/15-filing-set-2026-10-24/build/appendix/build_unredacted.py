"""Make UNREDACTED variants of the 3 exhibit-bearing PDFs by swapping the redacted
appendix body pages for the stamped pages in body_unredacted.pdf (same build).
Output names add ' - UNREDACTED'. Keep outputs out of any public location."""
import pymupdf
from pathlib import Path
W=Path(__file__).parent; OUT=Path("/workspace/m20-pleading/out"); UO=OUT/"unredacted"; UO.mkdir(exist_ok=True)
STAMP="UNREDACTED \u2013 CONFIDENTIAL \u2013 NOT FOR PUBLIC FILING (CRC 1.201)"
B=pymupdf.open(W/"body_unredacted.pdf")
for p in B:
    F=pymupdf.Font("helv"); tw=pymupdf.TextWriter(p.rect,color=(0.8,0,0)); L=F.text_length(STAMP,8)
    tw.append(((612-L)/2,11),STAMP,font=F,fontsize=8); tw.write_text(p)
NAMES=["Exhibits A-I to Declaration - Appendix.pdf","Declaration of Brendan Ngehsi Newanforbi with Exhibits A-I.pdf",
 "Motion Packet - Notice, MPA, Declaration, Proposed Writ, Alt Order, Proposed Judgment, Proof of Service - Pleading - with Exhibits A-I.pdf"]
for n in NAMES:
    D=pymupdf.open(OUT/n); toc=D.get_toc(False)
    def app(p):
        w=[x for x in p.get_text('words') if x[1]>720]
        for a,b in zip(w,w[1:]):
            if a[4]=="App." and b[4].isdigit(): return "App. "+b[4]
    s=next(i for i in range(len(D)) if app(D[i])=="App. 001")
    for k in range(len(B)): assert app(D[s+k])==f"App. {k+1:03d}"==app(B[k]),(n,k)
    D.delete_pages(from_page=s,to_page=s+len(B)-1); D.insert_pdf(B,start_at=s); D.set_toc(toc)
    D.save(UO/(Path(n).stem+" - UNREDACTED.pdf"),garbage=3,deflate=True); print(n[:30],s,len(D))
