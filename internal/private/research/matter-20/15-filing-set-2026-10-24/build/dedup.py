import sys,hashlib,pikepdf
p=pikepdf.open(sys.argv[1],allow_overwriting_input=True)
seen={};d=0
for o in list(p.objects):
  if isinstance(o,pikepdf.Dictionary) and o.get('/Type')=='/FontDescriptor':
    for k in('/FontFile','/FontFile2','/FontFile3'):
      if k in o:
        s=o[k]; h=hashlib.sha1(s.read_raw_bytes()+repr(s.stream_dict).encode()).hexdigest()
        if h in seen and seen[h].objgen!=s.objgen: o[k]=seen[h]; d+=1
        else: seen.setdefault(h,s)
p.save(sys.argv[1],object_stream_mode=pikepdf.ObjectStreamMode.generate,compress_streams=True)
print('dedup',d)
