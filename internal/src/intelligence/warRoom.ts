import type { IntelligenceCatalog, LitigationEvent, WarRoom } from "./types";
import { relatedMatterNumbers } from "../utils/crossMatter";
import { detectContradictions } from "./contradictions";
import { diffArguments } from "./argumentDiff";

export function buildWarRoom(
  event: LitigationEvent,
  catalog: IntelligenceCatalog,
  options: { citeproofIds?: string[] } = {},
): WarRoom | null {
  if (event.type !== "MOTION_FILED" && event.type !== "ORDER_ENTERED" && event.type !== "ARGUMENT_CHANGED") {
    return null;
  }
  const matter = event.matter;
  if (!matter) return null;
  const motion = catalog.motions.find((row) => row.matter === matter && (event.docket == null || row.docket === event.docket));
  const issues = event.issues?.length ? event.issues : motion?.issues ?? [];
  const snapshot = [...catalog.arguments].reverse().find((row) => row.matter === matter);
  const prior = catalog.arguments.find((row) => row.matter === matter && row.id !== snapshot?.id);
  const diff = snapshot && prior ? diffArguments(prior, snapshot) : null;
  const facts = detectContradictions(catalog).filter((row) => row.supports.includes(matter));
  const newAuthorities = snapshot?.authorities ?? [];
  const citeproofIds = options.citeproofIds ?? Object.keys(catalog.citeproof);
  const inProof = newAuthorities.filter((id) => citeproofIds.includes(id));
  const weak = newAuthorities.filter((id) => catalog.citeproof[id]?.parentheticalOverstates || catalog.authorities.find((row) => row.id === id)?.supports === "mixed");

  const attacks = issues.map((issue) => ({
    issue,
    level: issue === "qualified_immunity" || issue === "standing" ? ("MEDIUM" as const) : ("HIGH" as const),
  }));

  return {
    matter,
    event: `${event.type.replaceAll("_", " ")} — ${event.summary.slice(0, 180)}`,
    docket: event.docket ?? motion?.docket,
    immediate:
      event.type === "MOTION_FILED"
        ? "Opposition clock activated. Do not treat a preview or email as a filed motion."
        : event.type === "ORDER_ENTERED"
          ? "Dependency clocks may have fired. Recalculate downstream CMC / JCMS / ADR dates."
          : "Defense position changed. Read the diff before drafting.",
    attacks,
    newAuthorities,
    authoritiesInCiteProof: inProof,
    weakOrMiscited: weak,
    newFacts: diff?.factualAdmissions ?? [],
    contradictions: facts.map((fact) => fact.fact),
    crossMatters: relatedMatterNumbers(matter),
    sequence: [
      "Read the attacking pages first",
      "Validate every new citation through CiteProof (existence, proposition, subsequent history)",
      "Run the argument diff against the prior defense position",
      "Check the contradiction engine against RFAs, manuals, and prior representations",
      "Draft the opposition skeleton from the weakest covered element",
    ],
  };
}

export function warRoomsFromEvents(events: LitigationEvent[], catalog: IntelligenceCatalog): WarRoom[] {
  return events.map((event) => buildWarRoom(event, catalog)).filter((room): room is WarRoom => Boolean(room));
}
