import type { Matter, TimelineEvent } from "../types/portfolio";
import { clusterForMatter, exposuresForMatter, linkKindLabel, relatedMatters } from "./crossMatter";

export function crossMatterSection(matter: Matter): string {
  const cluster = clusterForMatter(matter.number);
  if (!cluster) return "";
  const peers = relatedMatters(matter.number);
  const exposures = exposuresForMatter(matter.number);
  return `
## Cross-matter significance

**Cluster:** ${cluster.label}

${peers
    .map(
      (peer) =>
        `### Matter ${peer.number} — ${peer.relationship}\n\n- **Relationship:** ${peer.kinds
          .map(linkKindLabel)
          .join("; ")}\n- **Severity:** ${peer.severity}\n\n${peer.significance}\n\nSources:\n${peer.sources
          .map((source) => `- ${source}`)
          .join("\n")}`,
    )
    .join("\n\n")}

### Open cross-matter exposure

${
    exposures.length
      ? exposures
          .map(
            (exposure) =>
              `- **${exposure.label}** (${exposure.severity}, ${exposure.status}) — ${exposure.detail}\n  - Remedy: ${exposure.remedy}`,
          )
          .join("\n")
      : "None recorded."
  }
`;
}

export function matterMarkdown(matter: Matter, next?: TimelineEvent, recent?: TimelineEvent) {
  return `# Matter ${matter.number}: ${matter.caption}

**Case number:** ${matter.case_no}  
**Court:** ${matter.court}  
**Status:** ${matter.status}  
**Judge:** ${matter.judge}  
**Filed:** ${matter.filed}

## At a glance

- **Next action:** ${next?.event ?? "No upcoming action recorded"}
- **Next deadline:** ${next?.date ?? "None recorded"}
- **Recent development:** ${recent ? `${recent.date} — ${recent.event}` : "None recorded"}

## Claims

${matter.claims}

## Causes of action

${matter.causes.map((cause) => `- ${cause}`).join("\n")}

## Key facts

${matter.key_facts}

## Procedural status

${matter.procedural_status}

## Damages and risk

**Estimated damages:** ${matter.damages}

${matter.risk}

## Documents

${(matter.documents ?? []).map((document) => `- ${document.label}`).join("\n") || "No documents linked."}
${crossMatterSection(matter)}`;
}

export function downloadMatterSummary(matter: Matter, content: string) {
  const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `matter-${String(matter.number).padStart(2, "0")}-summary.md`;
  anchor.click();
  URL.revokeObjectURL(url);
}
