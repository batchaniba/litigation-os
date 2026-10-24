import sys; sys.path.insert(0,'/workspace/m20-pleading/appendix')
import redact
from PIL import Image
redact.apply('/workspace/m20-pleading/appendix/body_unredacted.pdf')
from collections import defaultdict
G=defaultdict(list)
for k,b in redact.BOXES: G[k].append(b)
for k,bs in G.items():
    im=Image.open(f'/tmp/rp/{k:03d}.png'); cs=[]
    for b in bs:
        c=im.crop((max(0,b[0]-150),max(0,b[1]-70),min(im.width,b[2]+150),min(im.height,b[3]+70))); cs.append(c)
    W=max(c.width for c in cs); H=sum(c.height+8 for c in cs)
    M=Image.new('RGB',(W,H),(255,0,0)); y=0
    for c in cs: M.paste(c,(0,y)); y+=c.height+8
    M.save(f'/tmp/rp/c{k:03d}.png')
