import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const room=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const manifest=JSON.parse(fs.readFileSync(path.join(room,'08-audit/manifest.json'),'utf8'));
const ids=new Set(),paths=new Set(),errors=[];
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
for(const r of manifest.records){
  if(ids.has(r.id))errors.push(`Duplicate ID ${r.id}`);ids.add(r.id);
  if(paths.has(r.path))errors.push(`Duplicate path ${r.path}`);paths.add(r.path);
  if(r.path.startsWith('/')||r.path.split('/').includes('..'))errors.push(`Unsafe path ${r.path}`);
  const f=path.join(room,r.path);
  if(!fs.existsSync(f)){errors.push(`Missing ${r.path}`);continue;}
  const b=fs.readFileSync(f);
  if(sha(b)!==r.sha256)errors.push(`Hash mismatch ${r.id}`);
  if(b.length!==r.size)errors.push(`Size mismatch ${r.id}`);
  if(!r.sources?.length)errors.push(`Missing provenance ${r.id}`);
  if(r.pages&&b.subarray(0,5).toString()!=='%PDF-')errors.push(`Not PDF ${r.id}`);
  for(const key of ['text_path','ocr_text_path'])if(r[key]&&!fs.existsSync(path.join(room,r[key])))errors.push(`Missing ${key} ${r.id}`);
}
const workshop=path.join(room,'04-workshop');
for(const file of fs.readdirSync(workshop).filter(x=>x.endsWith('.md'))){
  const text=fs.readFileSync(path.join(workshop,file),'utf8');
  for(const id of text.match(/\bR\d{3}\b/g)||[])if(!ids.has(id))errors.push(`Unknown source ID ${id} in ${file}`);
  // Preserve the separately authored upstream memo without mechanical rewriting.
  // Its historical-status banner routes readers to the corrected analysis.
  const unchangedParallelSynthesis=file==='opposition-deep-research-analysis.md'&&
    sha(fs.readFileSync(path.join(workshop,file)))==='020d1c44ce234dc8464856de9d6bb4b836480bee3faba0b110ff97d94b2cea91';
  if(/[—]/.test(text)&&!text.includes('Preserved upstream document from commit `5b306800`')&&!unchangedParallelSynthesis)errors.push(`Style: em dash in ${file}`);
}
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}
else console.log(JSON.stringify({ok:true,preserved_assets:manifest.records.length,pdf_assets:manifest.records.filter(r=>r.pages).length,unresolved_retrieval_gaps:manifest.gaps.length,workshop_files:fs.readdirSync(workshop).length},null,2));
