import type { IntelligenceCatalog } from "../../intelligence/types";
import issues from "./issues.json";
import authorities from "./authorities.json";
import actors from "./actors.json";
import matrices from "./matrices.json";
import facts from "./facts.json";
import argumentSnapshots from "./arguments.json";
import dependencies from "./dependencies.json";
import fingerprints from "./fingerprints.json";
import judges from "./judges.json";
import recap from "./recap.json";
import motions from "./motions.json";
import citeproof from "./citeproof.json";

export const intelligenceCatalog = {
  issues,
  authorities,
  matrices,
  facts,
  arguments: argumentSnapshots,
  dependencies,
  fingerprints,
  judges,
  attorneys: actors.attorneys,
  firms: actors.firms,
  recap,
  motions,
  citeproof,
} as IntelligenceCatalog;

export function issueById(id: string) {
  return intelligenceCatalog.issues.find((issue) => issue.id === id);
}

export function authorityById(id: string) {
  return intelligenceCatalog.authorities.find((authority) => authority.id === id);
}
