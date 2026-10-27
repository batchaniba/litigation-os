import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

// Mechanical archival of already researched public opinion URLs, not a search
// or an authentication workflow. Originals and retrieval errors stay distinct.
const here = path.dirname(fileURLToPath(import.meta.url));
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const files = fs.readdirSync(here).filter(name => name.endsWith('.md'));
const urls = new Set();
for (const file of files) {
  for (const match of fs.readFileSync(path.join(here, file), 'utf8').matchAll(/\]\((https?:\/\/[^)\s]+)\)/g)) {
    urls.add(match[1]);
  }
}
const directory = path.join(here, 'authority-originals');
fs.mkdirSync(directory, { recursive: true });
const records = [];
for (const url of [...urls].sort()) {
  const parsed = new URL(url);
  const record = { url, retrieved_at: new Date().toISOString(), status: 'linked_html_not_archived' };
  if (parsed.pathname.endsWith('.pdf')) {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(25000) });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = Buffer.from(await response.arrayBuffer());
      if (data.subarray(0, 5).toString() !== '%PDF-') throw new Error('Response is not a PDF');
      const name = `${hash(url).slice(0, 10)}-${path.basename(parsed.pathname)}`;
      const relative = `authority-originals/${name}`;
      fs.writeFileSync(path.join(here, relative), data);
      Object.assign(record, { status: 'captured_pdf', path: relative, size: data.length, sha256: hash(data) });
      console.log(`Captured ${parsed.pathname}: ${data.length} bytes`);
    } catch (error) {
      Object.assign(record, { status: 'capture_failed', error: String(error.message) });
      console.log(`Capture failed ${url}: ${error.message}`);
    }
  }
  records.push(record);
}
const manifest = {
  title: 'Supplemental authority-source manifest',
  generated_at: new Date().toISOString(),
  note: 'Separate from the original 224-record evidence manifest. A downloaded opinion is not a citator clearance.',
  records
};
fs.writeFileSync(path.join(here, 'supplemental-source-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(JSON.stringify({
  urls: records.length,
  captured_pdfs: records.filter(record => record.status === 'captured_pdf').length,
  failures: records.filter(record => record.status === 'capture_failed').length
}, null, 2));
