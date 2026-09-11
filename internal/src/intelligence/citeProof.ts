import type { AuthorityCatalogEntry, CiteProofAudit, IntelligenceCatalog } from "./types";

export function auditCitation(authority: AuthorityCatalogEntry, catalog: IntelligenceCatalog): CiteProofAudit {
  const seeded = catalog.citeproof[authority.id] ?? {};
  const binding = authority.bindingIn.includes("CA9") || authority.bindingIn.includes("SCOTUS") || seeded.binding === true;
  return {
    authorityId: authority.id,
    exists: seeded.exists ?? true,
    propositionFound: seeded.propositionFound ?? (authority.proposition ? true : null),
    reversed: seeded.reversed ?? authority.reversed,
    criticized: seeded.criticized ?? authority.criticized,
    binding: seeded.binding ?? binding,
    court: seeded.court ?? authority.court,
    posture: seeded.posture ?? authority.posture,
    parentheticalOverstates: seeded.parentheticalOverstates ?? null,
    notes: seeded.notes ?? (authority.proposition ? [authority.proposition] : []),
  };
}

export function auditCatalog(catalog: IntelligenceCatalog): CiteProofAudit[] {
  return catalog.authorities.map((authority) => auditCitation(authority, catalog));
}
