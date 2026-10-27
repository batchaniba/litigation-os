import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const room = path.resolve(here, '..');
const audit = fs.readFileSync(path.join(here, 'adversarial-leakage-audit.md'), 'utf8');
const sourcePaths = [
  ...['opposition-decision-memorandum.md', 'evidence-to-claim-matrix.md',
    'amendment-and-proof-proffer.md', 'red-team-and-brief-blueprint.md']
    .map(file => `09-deep-analysis/${file}`),
  '04-workshop/opposition-deep-research-analysis.md'
];
const sources = sourcePaths.map(file => ({
  path: file,
  text: fs.readFileSync(path.join(room, file), 'utf8')
}));
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const findings = [];
const errors = [];
for (const match of audit.matchAll(/^### (A\d{2}): ([^\n]+)\n([\s\S]*?)(?=^### |^## |$(?![\s\S]))/gm)) {
  const [, id, title, body] = match;
  const quote = body.match(/\*\*Verbatim(?: heading)?:\*\* “([^”]+)”/)?.[1];
  if (!quote) { errors.push(`${id}: missing verbatim excerpt`); continue; }
  const anchors = [];
  for (const source of sources) {
    const offset = source.text.indexOf(quote);
    if (offset >= 0) anchors.push({
      path: source.path,
      line_start: source.text.slice(0, offset).split('\n').length,
      line_end: source.text.slice(0, offset + quote.length).split('\n').length,
      sha256: sha(source.text)
    });
  }
  if (!anchors.length) errors.push(`${id}: excerpt not found: ${quote}`);
  findings.push({ id, title, verbatim_excerpt: quote, anchors });
}
if (findings.length !== 22) errors.push(`Expected 22 findings; got ${findings.length}`);
if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else {
  const result = {
    title: 'Matter 32 Adversarial-Leakage Audit Index',
    audit_path: '09-deep-analysis/adversarial-leakage-audit.md',
    audit_sha256: sha(audit),
    note: 'Exact excerpts and immutable-content locators; findings are internal drafting controls, not adjudications.',
    findings
  };
  fs.writeFileSync(path.join(here, 'adversarial-leakage-index.json'), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ ok: true, verified_findings: findings.length }, null, 2));
}
