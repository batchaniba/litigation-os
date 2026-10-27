import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const room='/home/user/workspace/portfolio/internal/private/research/matter-32';
const m=JSON.parse(fs.readFileSync(room+'/08-audit/manifest.json','utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const sources=[
['Khoja-899-F3d-988.pdf','https://cdn.ca9.uscourts.gov/datastore/opinions/2018/08/13/16-56069.pdf'],
['Grier-21-16702.pdf','https://cdn.ca9.uscourts.gov/datastore/opinions/2023/01/20/21-16702.pdf'],
['Ngumezi-980-F3d-1285.pdf','https://cdn.ca9.uscourts.gov/datastore/opinions/2020/11/20/19-10243.pdf'],
['Chism-661-F3d-380.pdf','https://cdn.ca9.uscourts.gov/datastore/opinions/2011/08/25/10-35085.pdf'],
['Whittlestone-618-F3d-970.pdf','https://cdn.ca9.uscourts.gov/datastore/opinions/2010/08/17/09-16353.pdf'],
['Gonzalez-v-Trevino-2024.pdf','https://www.supremecourt.gov/opinions/23pdf/22-1025_1a72.pdf'],
['Wesby-583-US-48.pdf','https://www.supremecourt.gov/opinions/17pdf/15-1485_1qm2.pdf'],
];
function add(bytes,dest,source){
  const existing=m.records.find(x=>x.path===dest);if(existing)return;
  fs.mkdirSync(path.dirname(room+'/'+dest),{recursive:true});fs.writeFileSync(room+'/'+dest,bytes);
  const hash=sha(bytes),r={id:`R${String(m.records.length+1).padStart(3,'0')}`,path:dest,sha256:hash,size:bytes.length,sources:[source]};
  if(dest.endsWith('.pdf')){
    r.pages=Number(execFileSync('pdfinfo',[room+'/'+dest],{encoding:'utf8'}).match(/^Pages:\s+(\d+)/m)?.[1]);
    r.text_path=`07-source-text/${hash}.txt`;execFileSync('pdftotext',['-layout',room+'/'+dest,room+'/'+r.text_path]);
  }
  m.records.push(r);console.log('PRESERVED',r.id,dest);
}
for(const [name,url] of sources){
  const response=await fetch(url);if(!response.ok)throw new Error(`${response.status} ${url}`);
  const bytes=Buffer.from(await response.arrayBuffer());
  if(bytes.subarray(0,5).toString()!=='%PDF-')throw new Error(`Non-PDF response ${url}`);
  add(bytes,`03-authorities/${name}`,{type:'primary_legal_authority',url,retrieved:'2026-10-26',warning:'Downloaded original opinion; no comprehensive subsequent-history certification'});
}
const saved='/home/user/.perplexity/sessions/fa775ecf-4a8e-42d5-8dca-575c038194d1/tool_calls';
add(fs.readFileSync(saved+'/fetch_url/output_32b42cc17b5a469496754e045930c10f.txt'),'03-authorities/Kim-2026-04-20-public-text-reproduction.txt',{type:'external_public_text_reproduction',url:'https://www.courtlistener.com/opinion/10913465/brendan-ngehsi-newanforbi-v-state-of-california-et-al/',retrieved:'2026-10-26',warning:'Raw fetch-tool output containing public text reproduction, not stamped original PDF; later HTML request encountered 403'});
add(fs.readFileSync(saved+'/exec/output_b4768a8323c54d8f93edd1c5fb9b3633.txt'),'08-audit/cloudflare-r2-index-inspection.json',{type:'cloudflare_connector_read_result',bucket:'litigation-documents',key:'index/path-to-sha256.json',retrieved:'2026-10-26',warning:'Read-only audit. R2 index has 1726 entries; 200 matter-32 entries. Specific old FAC object is present in bucket listing despite public Worker 404; binary API response is not used as a substitute PDF'});
for(const file of ['collect-m32.mjs','recover-m32.mjs','ocr-m32.mjs','finish-m32.mjs']){
  add(fs.readFileSync('/home/user/workspace/'+file),`08-audit/collection-scripts/${file}`,{type:'collection_script',warning:'Provenance implementation record; original execution used workspace-specific paths. Do not rerun blindly on finalized room.'});
}
m.collection_summary={
  date:'2026-10-26',
  room_pattern:'origin/research/matter-20-2026-10-24',
  branch:'research/matter-32-mtd-opposition-2026-10-26',
  original_audiovisual_recovered:false,
  original_kim_recommendation_pdf_recovered:false,
  live_docket_verified:false,
  cloudflare_write_operations:0,
  public_deployments:0,
  duplicate_policy:'Exact-byte SHA-256 deduplication; multiple source occurrences retained; variant scans kept separately',
  text_policy:'pdftotext derivatives; selected 125-dpi Tesseract OCR labeled and original PDF pages visually checked for central form/warrant claims'
};
fs.writeFileSync(room+'/08-audit/manifest.json',JSON.stringify(m,null,2)+'\n');
fs.writeFileSync(room+'/08-audit/SHA256SUMS',m.records.map(r=>`${r.sha256}  ${r.path}`).join('\n')+'\n');
fs.writeFileSync(room+'/08-audit/inventory.md','# Source inventory\n\nGenerated from manifest.json. Original bytes control. Exact duplicates retain all source occurrences; different scans remain separate. Inventory labels and graph snapshots do not certify filing, truth, operative pleading, current docket, or deadlines.\n\n| ID | File | Pages | Bytes | Source occurrences |\n|---|---|---:|---:|---:|\n'+m.records.map(r=>`| ${r.id} | ${r.path.replaceAll('|','\\|')} | ${r.pages??''} | ${r.size} | ${r.sources.length} |`).join('\n')+'\n\n## Remaining selected-manifest retrieval gaps\n\n'+m.gaps.map(g=>`- ${g.path}: ${g.worker_error||g.error||'unavailable'}`).join('\n')+'\n\n## Coverage limits\n\nNo original video or stamped original Kim recommendation PDF was recovered. The R2 index and object listing confirm that the old FAC PDF exists in storage even though the public Worker returned 404; its original bytes were not recovered. This is a retrieval/access gap, not a representation that the object is missing. Public text reproduction and plaintiff-created transcript remain distinctly labeled.\n');
console.log(JSON.stringify({assets:m.records.length,pdfs:m.records.filter(x=>x.pages).length,gaps:m.gaps.length},null,2));
