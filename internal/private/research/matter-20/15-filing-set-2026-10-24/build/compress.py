import sys,io,pikepdf,zlib
from pikepdf import PdfImage,Name
from PIL import Image, ImageChops
src,dst=sys.argv[1:3]
p=pikepdf.open(src); n=0
for o in list(p.objects):
  if not(isinstance(o,pikepdf.Stream) and o.get('/Subtype')=='/Image'): continue
  if int(o.get('/BitsPerComponent',8))==1 or o.get('/ImageMask'): continue
  if len(o.read_raw_bytes())<150000: continue
  try: im=PdfImage(o).as_pil_image()
  except Exception as e: print('skip',e); continue
  w,h=im.size
  if im.mode not in('L','RGB'): im=im.convert('RGB')
  if im.mode=='RGB':
    sm=im.resize((200,200)); r,g,b=sm.split()
    if max(ImageChops.difference(r,g).getextrema()[1],ImageChops.difference(g,b).getextrema()[1])<24: im=im.convert('L')
  s=min(1.0,1400/max(w,h)*1.0)  # ~170dpi on letter
  if s<1: im=im.resize((int(w*s),int(h*s)),Image.LANCZOS)
  b=io.BytesIO(); im.save(b,'JPEG',quality=75,optimize=True)
  if len(b.getvalue())>=len(o.read_raw_bytes()): continue
  o.write(b.getvalue(),filter=Name.DCTDecode)
  o.Width,o.Height=im.size; o.BitsPerComponent=8
  o.ColorSpace=Name.DeviceGray if im.mode=='L' else Name.DeviceRGB
  for k in('/DecodeParms','/Decode'):
    if k in o: del o[k]
  n+=1
p.remove_unreferenced_resources()
p.save(dst,object_stream_mode=pikepdf.ObjectStreamMode.generate,compress_streams=True,recompress_flate=True)
print('recompressed',n)
