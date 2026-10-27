import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const room = path.resolve(here, '..');
const controls = JSON.parse(fs.readFileSync(path.join(here, 'research-controls.json'), 'utf8'));
const original = JSON.parse(fs.readFileSync(path.join(room, '08-audit/manifest.json'), 'utf8'));
const supplemental = JSON.parse(fs.readFileSync(path.join(here, 'supplemental-source-manifest.json'), 'utf8'));
const errors = [];
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const ids = new Set(original.records.map(record => record.id));
const knownUrls = new Set(supplemental.records.map(record => record.url));
let wordCount = 0;

if (original.records.length !== 224) errors.push('Unexpected original manifest count');
if (original.records.find(record => record.id === 'R125')?.sha256 !== controls.authoritative_fac.sha256) {
  errors.push('Wrong authoritative FAC');
}
const expectedRanges = [[38, 42], [43, 47], [48, 53], [54, 58], [59, 63], [64, 70]];
for (const [index, claim] of controls.claims.entries()) {
  if (claim.count !== index + 1 || JSON.stringify(claim.paragraphs) !== JSON.stringify(expectedRanges[index])) {
    errors.push(`Wrong claim map at ${index + 1}`);
  }
}
if (controls.claims[3].defendants.includes('Meza')) errors.push('Count IV heading incorrectly expanded');
if (!controls.claims[5].defendants.includes('Melano')) errors.push('Count VI incorrectly narrowed to Meza');
for (const file of controls.required_outputs) {
  const target = path.join(here, file);
  if (!fs.existsSync(target)) {
    errors.push(`Missing deliverable ${file}`);
    continue;
  }
  const text = fs.readFileSync(target, 'utf8');
  wordCount += text.split(/\s+/).length;
  if (text.includes('\u2014')) errors.push(`Em dash in authored text: ${file}`);
  for (const id of text.match(/\bR\d{3}\b/g) || []) {
    if (!ids.has(id)) errors.push(`Unknown record ${id} in ${file}`);
  }
  for (const match of text.matchAll(/\]\(([^)\s]+)\)/g)) {
    const url = match[1];
    if (/^https?:\/\//.test(url)) {
      if (!knownUrls.has(url)) errors.push(`Unregistered authority URL ${url}`);
      if (/github|workers\.dev|fx\.doj|drive\.google/.test(url)) {
        errors.push(`Private-document/repo URL in substantive analysis ${file}`);
      }
    } else if (!url.startsWith('#') && !fs.existsSync(path.resolve(here, url.split('#')[0]))) {
      errors.push(`Broken relative link ${url} in ${file}`);
    }
  }
}
for (const source of supplemental.records.filter(record => record.status === 'captured_pdf')) {
  const file = path.join(here, source.path);
  if (!fs.existsSync(file)) {
    errors.push(`Missing authority original ${source.path}`);
    continue;
  }
  const data = fs.readFileSync(file);
  if (sha(data) !== source.sha256 || data.length !== source.size) errors.push(`Authority integrity: ${source.path}`);
  if (data.subarray(0, 5).toString() !== '%PDF-') errors.push(`Invalid PDF: ${source.path}`);
}
const core = fs.readFileSync(path.join(here, 'opposition-decision-memorandum.md'), 'utf8');
for (const required of ['0.073', '01:07:29', 'Lingo', 'Costanich', 'Moore', 'other deprivation of liberty', '21718(a)(1)']) {
  if (!core.includes(required)) errors.push(`Missing critical analysis marker: ${required}`);
}
if (core.split(/\s+/).length < 4500) errors.push('Decision memorandum below intended substantive scope');
for (const file of fs.readdirSync(path.join(room, '04-workshop')).filter(name => name.endsWith('.md'))) {
  const preserved = [controls.parallel_upstream_synthesis, controls.parallel_upstream_timing_audit]
    .find(entry => entry.path === `04-workshop/${file}`);
  if (preserved) {
    if (sha(fs.readFileSync(path.join(room, '04-workshop', file))) !== preserved.sha256) {
      errors.push('Preserved parallel synthesis changed');
    }
    continue;
  }
  if (!fs.readFileSync(path.join(room, '04-workshop', file), 'utf8').includes('Superseded') &&
      !fs.readFileSync(path.join(room, '04-workshop', file), 'utf8').includes('Historical scaffold')) {
    errors.push(`Old scaffold not marked superseded: ${file}`);
  }
}
const auditText = fs.readFileSync(path.join(here, 'adversarial-leakage-audit.md'), 'utf8');
const index = JSON.parse(fs.readFileSync(path.join(here, 'adversarial-leakage-index.json'), 'utf8'));
if (sha(auditText) !== index.audit_sha256) errors.push('Audit index content hash is stale');
if (index.findings.length !== 22 || new Set(index.findings.map(f => f.id)).size !== 22) {
  errors.push('Audit must contain 22 uniquely indexed findings');
}
for (const finding of index.findings) {
  if (!auditText.includes(`### ${finding.id}: ${finding.title}`) ||
      !auditText.includes(`“${finding.verbatim_excerpt}”`)) errors.push(`Audit/index mismatch: ${finding.id}`);
  if (!finding.anchors.length) errors.push(`No source anchor: ${finding.id}`);
  for (const anchor of finding.anchors) {
    if (!/^(04-workshop|09-deep-analysis)\/[^/]+\.md$/.test(anchor.path)) {
      errors.push(`Unsafe audit source: ${anchor.path}`);
      continue;
    }
    const source = fs.readFileSync(path.join(room, anchor.path), 'utf8');
    const offset = source.indexOf(finding.verbatim_excerpt);
    if (sha(source) !== anchor.sha256 || offset < 0 ||
        source.slice(0, offset).split('\n').length !== anchor.line_start ||
        source.slice(0, offset + finding.verbatim_excerpt.length).split('\n').length !== anchor.line_end) {
      errors.push(`Stale or incorrect source excerpt: ${finding.id}`);
    }
  }
}
const combined = fs.readFileSync(path.join(here, 'deliverables/Matter-32-Opposition-Research-Engine.md'), 'utf8');
if (!combined.includes(auditText.replace(/^(#{1,5}) /gm, '$1# '))) errors.push('Combined export missing current audit');
const result = {
  ok: errors.length === 0,
  claim_modules: controls.claims.length,
  authored_markdown_outputs: controls.required_outputs.length,
  verified_adversarial_leakage_findings: index.findings.length,
  approximate_words: wordCount,
  original_source_records: original.records.length,
  registered_authority_urls: supplemental.records.length,
  supplemental_pdf_captures: supplemental.records.filter(record => record.status === 'captured_pdf').length,
  capture_failures: supplemental.records.filter(record => record.status === 'capture_failed').length,
  open_or_partial_filing_gates: controls.filing_gates.filter(gate => gate.status !== 'complete').length,
  errors
};
console.log(JSON.stringify(result, null, 2));
if (errors.length) process.exitCode = 1;
