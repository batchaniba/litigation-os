import pymupdf,re,pikepdf,sys,glob
import json,pathlib
_D=json.load(open(pathlib.Path("/workspace/m20-pleading/appendix/redact_ids.local.json")))
_V=_D["IDS"]+_D["OFF"]+_D.get("VERIFY_EXTRA",[])
pat=re.compile("|".join(re.escape(x) for x in _V),re.I)
RAW=re.compile("|".join(re.escape(x) for x in _D["IDS"]).encode())
files=["Exhibits A-I to Declaration - Appendix.pdf","Declaration of Brendan Ngehsi Newanforbi with Exhibits A-I.pdf","Motion Packet - Notice, MPA, Declaration, Proposed Writ, Alt Order, Proposed Judgment, Proof of Service - Pleading - with Exhibits A-I.pdf"]
for f in files:
    d=pymupdf.open(f); hits=[]
    for i,p in enumerate(d):
        for m in pat.finditer(p.get_text()): hits.append((i+1,m.group()))
    # raw stream scan
    raw=0
    with pikepdf.open(f) as P:
        for o in P.objects:
            if isinstance(o,pikepdf.Stream):
                try: b=o.read_bytes()
                except Exception: continue
                if RAW.search(b): raw+=1
    print(f[:40],len(d),'pp',round(__import__('os').path.getsize(f)/1e6,2),'MB toc',len(d.get_toc()),'texthits',hits,'rawhits',raw)
