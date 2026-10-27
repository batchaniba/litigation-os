import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';

const repo='/home/user/workspace/portfolio';
const room=path.join(repo,'internal/private/research/matter-32');
const main=execFileSync('git',['rev-parse','HEAD'],{cwd:repo,encoding:'utf8'}).trim();
const ref='origin/research/matter-20-2026-10-24';
const m20=execFileSync('git',['rev-parse',ref],{cwd:repo,encoding:'utf8'}).trim();
const backup=execFileSync('git',['rev-parse','origin/documents'],{cwd:repo,encoding:'utf8'}).trim();
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const records=[], gaps=[], byHash=new Map();
function store(bytes,dest,source,expected=null) {
  const sha=hash(bytes);
  if(expected && sha!==expected) throw new Error(`HASH MISMATCH ${source.path}`);
  const prior=byHash.get(sha);
  if(prior){prior.sources.push(source);return prior;}
  fs.mkdirSync(path.dirname(path.join(room,dest)),{recursive:true});
  fs.writeFileSync(path.join(room,dest),bytes);
  const r={id:`R${String(records.length+1).padStart(3,'0')}`,path:dest,sha256:sha,size:bytes.length,sources:[source]};
  if(dest.endsWith('.pdf')){
    try {
      r.pages=Number(execFileSync('pdfinfo',[path.join(room,dest)],{encoding:'utf8'}).match(/^Pages:\s+(\d+)/m)?.[1])||null;
      const text=`07-source-text/${sha}.txt`;
      fs.mkdirSync(path.join(room,'07-source-text'),{recursive:true});
      execFileSync('pdftotext',['-layout',path.join(room,dest),path.join(room,text)]);
      r.text_path=text;
    }catch(e){r.extraction_error=String(e.message);}
  }
  records.push(r);byHash.set(sha,r);return r;
}
fs.mkdirSync(room,{recursive:true});
for(const [name,content] of [
  ['ND-Cal-MTD-Operative.pdf','ECF 22 motion to dismiss FAC and strike, filed 2026-10-26, 19 pages'],
  ['ND-Cal-MTD-Meza-Gonzalez.pdf','ECF 23 defendants DECLINE magistrate jurisdiction, filed 2026-10-26, 1 page; NOT a second MTD']
]){
  store(fs.readFileSync(`/home/user/.perplexity/attachments/c5a9f59a293d453fb34f8c1b3619435e/${name}`),`00-user-inputs/${name}`,{type:'user_attachment',path:name,content,filing_status:'ECF stamp on supplied PDF; no live docket verification'});
}
for(const n of ['01','02','20','24','32','33']){
  for(const file of fs.readdirSync(`${repo}/internal/src/data/matters/${n}`)){
    const p=`internal/src/data/matters/${n}/${file}`;
    store(fs.readFileSync(path.join(repo,p)),`06-source-snapshots/matters/${n}/${file}`,{type:'graph_snapshot',commit:main,path:p,warning:'historical snapshot, not a live docket check'});
  }
}
const manifest=JSON.parse(fs.readFileSync(`${repo}/internal/src/data/documents/manifest.json`));
const files=manifest.files.filter(x=>x.path.endsWith('.pdf') && (
  /^\/documents\/matter-32\/(ndcal|from-01|from-02)\//.test(x.path) ||
  /^\/documents\/matter-33\/incident\//.test(x.path) ||
  (/matter-24/.test(x.path)&&/screen|sufficien|Dkt.?0?5|IFP|dismiss|opposition-critique/i.test(x.path))
));
for(const x of files){
  const dest=`01-portfolio-records/${x.path.slice('/documents/'.length)}`;
  const source={type:'portfolio_manifest',commit:main,path:x.path,expected_sha256:x.sha256,filing_status:'inventory label only; inspect ECF stamp and docket'};
  let bytes=null;
  const local=path.join(repo,'internal/public',x.path);
  if(fs.existsSync(local)){const b=fs.readFileSync(local);if(hash(b)===x.sha256){bytes=b;source.retrieval='main working tree';}}
  if(!bytes){
    try {
      const response=await fetch(`https://litigation-doc-api.ss8sxswwkt.workers.dev/doc/${x.sha256}`);
      if(response.ok){
        const b=Buffer.from(await response.arrayBuffer());
        if(hash(b)===x.sha256){bytes=b;source.retrieval='Cloudflare R2-backed Worker';source.url=`https://litigation-doc-api.ss8sxswwkt.workers.dev/doc/${x.sha256}`;source.r2_key=`sha256/${x.sha256.slice(0,2)}/${x.sha256.slice(2)}.pdf`;}
        else source.worker_error='hash mismatch rejected';
      }else source.worker_error=`HTTP ${response.status}`;
    }catch(e){source.worker_error=e.message;}
  }
  if(!bytes){
    for(const prefix of ['documents/','internal/public/documents/','public/documents/']){
      const p=prefix+x.path.slice('/documents/'.length);
      try{const b=execFileSync('git',['show',`${backup}:${p}`],{cwd:repo,maxBuffer:120*1024*1024,stdio:['ignore','pipe','ignore']});if(hash(b)===x.sha256){bytes=b;source.retrieval='documents cold backup';source.backup_commit=backup;source.backup_path=p;break;}}catch{}
    }
  }
  if(bytes){store(bytes,dest,source,x.sha256);console.log(`OK ${x.path}`);}
  else {gaps.push(source);console.log(`GAP ${x.path}`);}
}
const tree=execFileSync('git',['ls-tree','-r','--name-only',m20],{cwd:repo,encoding:'utf8'}).split('\n');
for(const p of tree.filter(p=>p.startsWith('internal/private/research/matter-20/')&&(
  /\/02-incident-evidence\/|\/03-discovery-production\/|\/00-user-inputs\/Newanforbi-v-Serrato/.test(p)||
  /\/08-audit\/(manifest.json|inventory.md)$/.test(p)
))){
  const rel=p.slice('internal/private/research/matter-20/'.length);
  const dest=/\/08-audit\//.test(p)?`05-prior-analysis/matter-20-audit/${path.basename(p)}`:`02-incident-and-production/matter-20-branch/${rel}`;
  try{store(execFileSync('git',['show',`${m20}:${p}`],{cwd:repo,maxBuffer:120*1024*1024}),dest,{type:'prior_research_source',branch:ref,commit:m20,path:p,warning:'source records preserved; prior analysis and filing labels are not adopted'});}catch(e){gaps.push({path:p,error:e.message});}
}
for(const dir of ['internal/docs/matter-20-production-set-one','internal/docs/judges']){
  if(!fs.existsSync(path.join(repo,dir)))continue;
  for(const file of fs.readdirSync(path.join(repo,dir))){
    const p=`${dir}/${file}`;
    if(!fs.statSync(path.join(repo,p)).isFile() || !/\.(md|pdf|json|txt)$/.test(p))continue;
    if(dir.includes('judges')&&!/krishnan/i.test(file))continue;
    store(fs.readFileSync(path.join(repo,p)),`05-prior-analysis/main/${p}`,{type:'repo_supporting_material',commit:main,path:p,warning:'not independently adopted legal analysis'});
  }
}
fs.mkdirSync(path.join(room,'08-audit'),{recursive:true});
fs.writeFileSync(path.join(room,'08-audit/manifest.json'),JSON.stringify({created:'2026-10-26',main_commit:main,matter20_commit:m20,documents_commit:backup,records,gaps},null,2)+'\n');
fs.writeFileSync(path.join(room,'08-audit/SHA256SUMS'),records.map(r=>`${r.sha256}  ${r.path}`).join('\n')+'\n');
fs.writeFileSync(path.join(room,'08-audit/inventory.md'),'# Source inventory\n\nGenerated from the preservation manifest. Original bytes control; no inventory label proves filing, truth or operative status.\n\n| ID | File | Pages | Bytes | Source occurrences |\n|---|---|---:|---:|---:|\n'+records.map(r=>`| ${r.id} | ${r.path.replaceAll('|','\\|')} | ${r.pages??''} | ${r.size} | ${r.sources.length} |`).join('\n')+`\n\n## Retrieval gaps\n\n${gaps.map(g=>`- ${g.path}: ${g.worker_error||g.error||'not recovered'}`).join('\n')||'No selected-manifest PDF retrieval gaps.'}\n`);
console.log(JSON.stringify({assets:records.length,pdfs:records.filter(x=>x.path.endsWith('.pdf')).length,gaps:gaps.length,worker:records.filter(x=>x.sources.some(s=>s.retrieval==='Cloudflare R2-backed Worker')).length},null,2));
