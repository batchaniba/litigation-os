import type { Matter, MatterDocumentRef, MatterSummary } from "../../types/portfolio";
import { resolveDocuments } from "../documents";
import summaries from "./summaries.json";
import { assembleSplitMatter } from "./assembleMatter.js";

// Light records for list/search/dashboard — keep the shell bundle small.
export const cases = summaries as MatterSummary[];

// Split NN/matter.json plus sibling tables. Legacy glob remains so a new NN.json still loads.
const legacyLoaders = import.meta.glob(["./*.json", "!./summaries.json", "!./document-index.json"]) as Record<
  string,
  () => Promise<{ default: Matter & { documents?: MatterDocumentRef[] } }>
>;

const splitIdentityLoaders = import.meta.glob("./*/matter.json") as Record<
  string,
  () => Promise<{ default: Record<string, unknown> }>
>;

const splitPartLoaders = import.meta.glob(
  "./*/{docket,clocks,parties,counsel,claims,damages,evidence,documents}.json",
) as Record<string, () => Promise<{ default: unknown }>>;

function padded(number: number): string {
  return String(number).padStart(2, "0");
}

export function matterFileKey(number: number): string {
  return `./${padded(number)}.json`;
}

function splitIdentityKey(number: number): string {
  return `./${padded(number)}/matter.json`;
}

async function loadSplitParts(number: number) {
  const prefix = `./${padded(number)}/`;
  const names = ["docket", "clocks", "parties", "counsel", "claims", "damages", "evidence", "documents"] as const;
  const parts: Record<string, unknown> = {};
  await Promise.all(
    names.map(async (name) => {
      const loader = splitPartLoaders[`${prefix}${name}.json`];
      if (!loader) return;
      parts[name] = (await loader()).default;
    }),
  );
  return parts;
}

function finishMatter(raw: Matter & { documents?: MatterDocumentRef[] }): Matter {
  const documents = resolveDocuments(raw.documents);
  return {
    ...raw,
    documents,
    evidenceCount: raw.evidenceCount ?? (Array.isArray(raw.evidence) ? raw.evidence.length : 0),
    documentCount: raw.documentCount ?? documents.length,
  };
}

export function loadMatter(number: number): Promise<Matter> {
  const splitLoader = splitIdentityLoaders[splitIdentityKey(number)];
  if (splitLoader) {
    return Promise.all([splitLoader(), loadSplitParts(number)]).then(([mod, parts]) => {
      const assembled = assembleSplitMatter({
        matter: mod.default,
        docket: parts.docket as object[] | undefined,
        clocks: parts.clocks as object[] | undefined,
        parties: parts.parties as object | undefined,
        counsel: parts.counsel as object | undefined,
        claims: parts.claims as object | undefined,
        damages: parts.damages as object | string | undefined,
        evidence: parts.evidence as object[] | string[] | undefined,
        documents: parts.documents as object[] | undefined,
      }) as unknown as Matter & { documents?: MatterDocumentRef[] };
      return finishMatter(assembled);
    });
  }

  const loader = legacyLoaders[matterFileKey(number)];
  if (!loader) {
    return Promise.reject(new Error(`No matter JSON for number ${number}`));
  }
  return loader().then((mod) => finishMatter(mod.default));
}

export function getMatterSummary(number: number): MatterSummary | undefined {
  return cases.find((matter) => matter.number === number);
}
