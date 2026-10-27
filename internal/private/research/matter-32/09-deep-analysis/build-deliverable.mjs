import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Mechanical assembly: authoring and corrections remain in the source modules.
const here = path.dirname(fileURLToPath(import.meta.url));
const controls = JSON.parse(fs.readFileSync(path.join(here, 'research-controls.json'), 'utf8'));
const exportLinks = text => text.replace(/\[([^\]]+)\]\(adversarial-leakage-audit\.md\)/g, '$1 (included in this export)');
const files = [
  'opposition-decision-memorandum.md',
  'evidence-to-claim-matrix.md',
  'authority-treatment-ledger.md',
  'amendment-and-proof-proffer.md',
  'red-team-and-brief-blueprint.md',
  'adversarial-leakage-audit.md'
];
const sections = [
  '# Matter 32 Opposition Research Engine',
  'Decision-grade analysis for the opposition to ECF 22, with the Matter 20 production and historical Chi Soo Kim record integrated. Private research as of October 26, 2026; this is not a filing-ready brief or a certification of live deadlines, complete original media, or citator clearance.',
  '## Reading map\n\nRead the adversarial-leakage audit before selecting any court-facing language. The decision memorandum comes first in this combined internal export, followed by the evidence matrix, authority treatment ledger, amendment/proof proffer, red-team brief blueprint, and leakage audit appendix. This export deliberately preserves private red-team analysis and is not suitable for filing as a whole. Record IDs refer to the preserved branch source manifest; public authorities retain clickable original URLs throughout.',
  exportLinks(fs.readFileSync(path.join(here, files[0]), 'utf8').replace(/^# .+\n/, ''))
];
for (const file of files.slice(1)) {
  const body = exportLinks(fs.readFileSync(path.join(here, file), 'utf8')
    .replace(/^(#{1,5}) /gm, '$1# '));
  sections.push(`\n---\n\n${body}`);
}
sections.push('## Remaining filing gates\n\nThese unresolved items do not prevent research use, but they limit filing-stage factual and procedural representations.\n\n' +
  controls.filing_gates.map(gate => `- **${gate.gate.replaceAll('_', ' ')}:** ${gate.status}; blocks ${gate.blocks}.`).join('\n'));
const directory = path.join(here, 'deliverables');
fs.mkdirSync(directory, { recursive: true });
const output = path.join(directory, 'Matter-32-Opposition-Research-Engine.md');
fs.writeFileSync(output, sections.join('\n\n') + '\n');
console.log(JSON.stringify({ output, approximate_words: sections.join(' ').split(/\s+/).length }, null, 2));
