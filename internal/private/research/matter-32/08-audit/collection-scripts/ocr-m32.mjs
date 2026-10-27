import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
const room='/home/user/workspace/portfolio/internal/private/research/matter-32';
const m=JSON.parse(fs.readFileSync(room+'/08-audit/manifest.json'));
const ids=new Set(['R071','R082','R087','R180','R184','R192','R193','R194','R195','R196','R197','R199']);
const queue=m.records.filter(r=>r.pages && (ids.has(r.id)||r.sources.some(s=>s.type==='git_history_recovery')) && fs.readFileSync(room+'/'+r.text_path,'utf8').replace(/Case[^\n]+/g,'').trim().length<r.pages*100);
fs.mkdirSync(room+'/07-source-text/ocr',{recursive:true});
for(const r of queue){
  const tmp=`/home/user/workspace/ocr-${r.id}`;fs.mkdirSync(tmp,{recursive:true});
  execFileSync('pdftoppm',['-r','125','-png',room+'/'+r.path,tmp+'/p'],{maxBuffer:2*1024*1024});
  let text='';
  for(const file of fs.readdirSync(tmp).sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}))){
    text+=`PDF PAGE ${Number(file.match(/-(\d+)\.png$/)?.[1])}\n\n`+execFileSync('tesseract',[tmp+'/'+file,'stdout'],{encoding:'utf8',maxBuffer:10*1024*1024,stdio:['ignore','pipe','ignore']})+'\n\f';
  }
  r.ocr_text_path=`07-source-text/ocr/${r.sha256}.txt`;
  r.ocr_warning='Machine OCR at 125 dpi. Read source page before quoting; original PDF hash unchanged.';
  fs.writeFileSync(room+'/'+r.ocr_text_path,text);
  fs.rmSync(tmp,{recursive:true});console.log('OCR',r.id,r.pages,r.path);
}
fs.writeFileSync(room+'/08-audit/manifest.json',JSON.stringify(m,null,2)+'\n');
