import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const repo='/home/user/workspace/portfolio', room=repo+'/internal/private/research/matter-32';
const m=JSON.parse(fs.readFileSync(room+'/08-audit/manifest.json'));
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const names=execFileSync('git',['log','--all','--name-only','--format='],{cwd:repo,encoding:'utf8',maxBuffer:200*1024*1024}).split('\n');
const historical=[...new Set(names)];
const remaining=[];
for(const g of m.gaps){
  let r=m.records.find(r=>r.sha256===g.expected_sha256);
  if(r){r.sources.push({...g,retrieval:'exact-byte duplicate recovered in prior Matter 20 workshop'});continue;}
  const candidates=historical.filter(p=>path.basename(p)===path.basename(g.path));
  let found=false;
  for(const p of candidates){
    const commits=execFileSync('git',['rev-list','--all','--',p],{cwd:repo,encoding:'utf8'}).trim().split('\n').filter(Boolean);
    for(const commit of commits){
      let b;try{b=execFileSync('git',['show',`${commit}:${p}`],{cwd:repo,maxBuffer:120*1024*1024,stdio:['ignore','pipe','ignore']});}catch{continue;}
      if(hash(b)!==g.expected_sha256)continue;
      const dest=`01-portfolio-records/${g.path.slice('/documents/'.length)}`;
      fs.mkdirSync(path.dirname(room+'/'+dest),{recursive:true});fs.writeFileSync(room+'/'+dest,b);
      const text=`07-source-text/${g.expected_sha256}.txt`;
      execFileSync('pdftotext',['-layout',room+'/'+dest,room+'/'+text]);
      const pages=Number(execFileSync('pdfinfo',[room+'/'+dest],{encoding:'utf8'}).match(/^Pages:\s+(\d+)/m)?.[1]);
      m.records.push({id:`R${String(m.records.length+1).padStart(3,'0')}`,path:dest,sha256:g.expected_sha256,size:b.length,pages,text_path:text,sources:[{...g,type:'git_history_recovery',retrieval:'exact-byte historical git object',recovery_commit:commit,recovery_path:p}]});
      console.log('RECOVERED',g.path,commit,p);found=true;break;
    }
    if(found)break;
  }
  if(!found)remaining.push(g);
}
m.gaps=remaining;
fs.writeFileSync(room+'/08-audit/manifest.json',JSON.stringify(m,null,2)+'\n');
fs.writeFileSync(room+'/08-audit/SHA256SUMS',m.records.map(r=>`${r.sha256}  ${r.path}`).join('\n')+'\n');
fs.writeFileSync(room+'/08-audit/inventory.md','# Source inventory\n\nGenerated from manifest.json. Originals control. Labels and sidecars do not prove truth, filing, operative status, or a current deadline.\n\n| ID | File | Pages | Bytes | Source occurrences |\n|---|---|---:|---:|---:|\n'+m.records.map(r=>`| ${r.id} | ${r.path.replaceAll('|','\\|')} | ${r.pages??''} | ${r.size} | ${r.sources.length} |`).join('\n')+'\n\n## Remaining selected-manifest retrieval gaps\n\n'+remaining.map(g=>`- ${g.path}: ${g.worker_error||g.error||'unavailable'}`).join('\n')+'\n');
console.log({records:m.records.length,pdfs:m.records.filter(r=>r.pages).length,gaps:remaining.length});
