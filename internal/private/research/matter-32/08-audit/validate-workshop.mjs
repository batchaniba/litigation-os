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
  const preservedUpstreamHashes={
    'opposition-deep-research-analysis.md':'619c1bc644f45ae6f09e92e88e7c62fe929fa2b7c3289c13fa8c0a3ae814e23e',
    'chp-video-transcript-timing-audit.md':'9a4d2bd5fcc598e718d3aabbcf1a7b1119fd795812d9553c7c86074f8378423a'
  };
  const unchangedParallelSynthesis=preservedUpstreamHashes[file]&&
    sha(fs.readFileSync(path.join(workshop,file)))===preservedUpstreamHashes[file];
  if(/[—]/.test(text)&&!text.includes('Preserved upstream document from commit `5b306800`')&&!unchangedParallelSynthesis)errors.push(`Style: em dash in ${file}`);
}
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}
else console.log(JSON.stringify({ok:true,preserved_assets:manifest.records.length,pdf_assets:manifest.records.filter(r=>r.pages).length,unresolved_retrieval_gaps:manifest.gaps.length,workshop_files:fs.readdirSync(workshop).length},null,2));
