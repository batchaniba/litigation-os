import pymupdf,sys,subprocess
from PIL import Image
d=pymupdf.open('/workspace/m20-pleading/appendix/body_unredacted.pdf')
k=int(sys.argv[1]);x0,y0,x1,y1=map(float,sys.argv[2:6]);s=200/72
p=d[k-1].get_pixmap(dpi=200,clip=pymupdf.Rect(x0,y0,x1,y1));a=Image.frombytes('RGB',(p.width,p.height),p.samples)
b=Image.open(f'/tmp/rp/{k:03d}.png').crop((int(x0*s),int(y0*s),int(x0*s)+a.width,int(y0*s)+a.height))
c=Image.new('RGB',(a.width,a.height*2+6),'red');c.paste(a,(0,0));c.paste(b,(0,a.height+6));c.save(sys.argv[6])
