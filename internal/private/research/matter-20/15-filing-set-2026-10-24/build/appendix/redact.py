"""True raster redaction of App pages in body.pdf (stamped). Values are not logged."""
import pymupdf, io
from PIL import Image, ImageDraw, ImageFont
import json as _j, pathlib as _p
_L=_p.Path(__file__).with_name("redact_ids.local.json")
if not _L.exists(): raise SystemExit("redact_ids.local.json missing; see 00-README-HANDOFF.md")
_D=_j.loads(_L.read_text()); IDS=_D["IDS"]
OFF=_D["OFF"]
MANUAL={19:[(173,234,298,255),(213,449,298,472)], 23:[(173,330,298,352)],
 39:[(290,66.5,366,78),(76,101,132,119),(175,153,232,167)],
 40:[(298,64,366,76.5),(79,98,140,116)], 41:[(300,89.5,368,99.5),(82,120,140,139)],
 44:[(202,281.5,252,295),(208,312.5,266,324),(408,280.5,474,293)], 49:[(48,90.5,101,99.5)]}
PAGES=sorted({19,23,28,31,32,39,40,41,43,44,45,47,48,49,51,54,55,70,82})
DPI=200
BOXES=[]
import os; FAST=os.environ.get('FAST')=='1'
def rects(pg,k):
    out=[]
    for v in IDS: out+= [(r,False) for r in pg.search_for(v)]
    for v in OFF: out+= [(r,True) for r in pg.search_for(v)]
    if k==32:  # label token following the offense-code token (prefix in local json)
        ws=pg.get_text("words")
        for i,w in enumerate(ws):
            if w[4].startswith(_D["P32_PREFIX"]) and i+1<len(ws) and ws[i+1][4].upper().startswith("PC"):
                out.append((pymupdf.Rect(ws[i+1][:4]),True))
    out+=[(pymupdf.Rect(r),False) for r in MANUAL.get(k,[])]
    return out
def vtrim(gray,x0,x1,y0,y1,L,ctr=None):
    """best L-px window of ink (rules excluded) within y0..y1, trimmed to ink"""
    import numpy as _n
    W,H=gray.size; y0,y1=max(0,int(y0)),min(H,int(y1))
    a=_n.asarray(gray.crop((max(0,int(x0)),y0,min(W,int(x1)),y1)))<140
    if a.size==0: return None
    c=a.sum(1).astype(float); w=a.shape[1]; c[c>=0.4*w]=0; c[c<2]=0
    n=len(c); L=max(1,min(int(L),n))
    cs=_n.concatenate([[0],_n.cumsum(c)]); cc=(ctr-y0) if ctr is not None else n/2
    m=[(cs[k+L]-cs[k])*max(0.05,1-0.8*abs(k+L/2-cc)/L) for k in range(n-L+1)]
    k=int(_n.argmax(m))
    if m[k]==0: return None
    seg=_n.nonzero(c[k:k+L])[0]
    return y0+k+seg[0],y0+k+seg[-1]+1
def vband(gray,x0,x1,y0,y1,yc,s):
    """rows (px) of the dark ink band of the line through yc, within x0..x1, clamped to y0..y1"""
    W,H=gray.size; x0,x1=max(0,int(x0)),min(W-1,int(x1)); y0,y1=max(0,int(y0)),min(H-1,int(y1))
    px=gray.load()
    def dark(y): return sum(1 for x in range(x0,x1+1,1) if px[x,y]<140)>=2
    yc=int(min(max(yc,y0),y1))
    if not dark(yc):
        for d in range(1,int(3*s)):
            if yc-d>=y0 and dark(yc-d): yc-=d; break
            if yc+d<=y1 and dark(yc+d): yc+=d; break
        else: return None
    a=b=yc
    while a-1>=y0 and dark(a-1): a-=1
    while b+1<=y1 and dark(b+1): b+=1
    return a,b
def apply(path):
    src=pymupdf.open(path); log={}
    out=pymupdf.open()
    for i in range(len(src)):
        k=i+1
        if k not in PAGES: out.insert_pdf(src,from_page=i,to_page=i); continue
        pg=src[i]; R=rects(pg,k); log[k]=len(R)
        pix=pg.get_pixmap(dpi=DPI); im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
        dr=ImageDraw.Draw(im); s=DPI/72; gray=im.convert("L")
        try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",int(7*s))
        except Exception: f=ImageFont.load_default()
        native=any(t['type']==0 and not t['font'].startswith('Times') for t in pg.get_texttrace())
        MAN=[pymupdf.Rect(m) for m in MANUAL.get(k,[])]
        for r,lab in R:
            if r in MAN: pl=pr=0.5
            elif native: pl=pr=1.5
            else: pl,pr=3+0.1*r.width,5+0.45*r.width
            bx0,bx1=(r.x0-pl)*s,(r.x1+pr)*s
            if r in MAN: ylo,yhi,yc=r.y0*s,r.y1*s,None
            else:
                h=r.height; yc=0.9*h*s
                ylo,yhi=(r.y0-0.45*h)*s,(r.y1+0.2*h)*s
            band=None if (yc is None or native) else vtrim(gray,bx0,bx1,ylo,yhi,yc,(r.y0+r.y1)/2*s)
            if native and r not in MAN: band=((r.y0+0.12*r.height)*s,(r.y1-0.08*r.height)*s); 
            if native and r not in MAN: p0=0.5
            else: p0=None
            if band: a,b=band
            else: a,b=ylo,yhi
            p=(0.5 if r in MAN else (p0 or 1.5))*s; box=[bx0,a-p,bx1,b+p]
            dr.rectangle(box,fill="black"); BOXES.append((k,box))
            if lab:
                fs=int(7*s)
                while fs>8 and (fs>(box[3]-box[1])*0.8 or dr.textlength("[REDACTED]",font=f.font_variant(size=fs))>box[2]-box[0]-2): fs-=1
                f2=f.font_variant(size=fs); tw=dr.textlength("[REDACTED]",font=f2)
                if True: dr.text((box[0]+(box[2]-box[0]-tw)/2,box[1]+((box[3]-box[1])-fs)/2-1),"[REDACTED]",fill="white",font=f2)
        if FAST: im.save(f"/tmp/rp/{k:03d}.png"); continue
        b=io.BytesIO(); im.save(b,"JPEG",quality=82)
        np=out.new_page(width=pg.rect.width,height=pg.rect.height); np.insert_image(np.rect,stream=b.getvalue())
        tp=np.get_textpage_ocr(dpi=300,full=True)
        for x0,y0,x1,y1,wd,*_ in np.get_text("words",textpage=tp):
            fs=max(4,(y1-y0)*0.85); fw=pymupdf.get_text_length(wd,fontname="helv",fontsize=fs)
            if fw>0 and fw>(x1-x0): fs=fs*(x1-x0)/fw
            np.insert_text((x0,y1-(y1-y0)*0.18),wd,fontsize=fs,fontname="helv",render_mode=3)
    if FAST: return
    out.save(str(path)+".tmp",garbage=3,deflate=True); out.close(); src.close()
    import os; os.replace(str(path)+".tmp",path)
    print("redacted pages / rect counts:",log)
