import graph from "../data/crossMatter.json";
import type {
  CrossMatterCluster,
  CrossMatterExposure,
  CrossMatterFoundation,
  CrossMatterGraph,
  CrossMatterLink,
  CrossMatterParty,
  RelatedMatter,
} from "../types/portfolio";

const crossMatterGraph = graph as unknown as CrossMatterGraph;

export const CROSS_MATTER_CLUSTERS: CrossMatterCluster[] = crossMatterGraph.clusters;

export const linkKindLabel = (kind: string): string =>
  crossMatterGraph.linkKinds[kind]?.label ?? kind;

export const linkKindDescription = (kind: string): string =>
  crossMatterGraph.linkKinds[kind]?.description ?? "";

export const allLinkKinds = (): string[] => Object.keys(crossMatterGraph.linkKinds);

export const clusterForMatter = (matter: number): CrossMatterCluster | undefined =>
  CROSS_MATTER_CLUSTERS.find((cluster) => cluster.matters.includes(matter));

export const clusterById = (id: string): CrossMatterCluster | undefined =>
  CROSS_MATTER_CLUSTERS.find((cluster) => cluster.id === id);

/**
 * Human-readable directional relationship for a link, read from `from`'s side.
 * Directionality matters: "stayed pending" is not the same claim as "controls".
 */
export function relationshipFor(link: CrossMatterLink, perspective: number): string {
  const peer = link.from === perspective ? link.to : link.from;
  if (link.direction === "mutual") {
    return `Reciprocal with Matter ${peer}`;
  }
  if (link.direction === "from_depends_on_to") {
    return link.from === perspective
      ? `This matter depends on Matter ${peer}`
      : `Matter ${peer} depends on this matter`;
  }
  // to_cites_from: the `to` matter cites the `from` matter's order.
  return link.to === perspective
    ? `This matter cites Matter ${peer}`
    : `Matter ${peer} cites this matter`;
}

export function linksForMatter(matter: number): CrossMatterLink[] {
  const cluster = clusterForMatter(matter);
  if (!cluster) return [];
  return cluster.links.filter((link) => link.from === matter || link.to === matter);
}

export function linksBetween(a: number, b: number): CrossMatterLink[] {
  const cluster = clusterForMatter(a);
  if (!cluster) return [];
  return cluster.links.filter(
    (link) => (link.from === a && link.to === b) || (link.from === b && link.to === a),
  );
}

export function kindsBetween(a: number, b: number): string[] {
  return Array.from(new Set(linksBetween(a, b).flatMap((link) => link.kinds)));
}

const SEVERITY_RANK: Record<string, number> = { high: 0, medium: 1, low: 2 };

/** Every peer matter of `matter`, collapsed to one entry per peer, worst severity first. */
export function relatedMatters(matter: number): RelatedMatter[] {
  const byPeer = new Map<number, RelatedMatter>();

  for (const link of linksForMatter(matter)) {
    const peer = link.from === matter ? link.to : link.from;
    const entry: RelatedMatter = {
      number: peer,
      link,
      kinds: link.kinds,
      relationship: relationshipFor(link, matter),
      significance: link.significance,
      severity: link.severity,
      sources: link.sources,
    };
    const existing = byPeer.get(peer);
    if (!existing) {
      byPeer.set(peer, entry);
      continue;
    }
    const merged: RelatedMatter = {
      ...existing,
      kinds: Array.from(new Set([...existing.kinds, ...link.kinds])),
      sources: Array.from(new Set([...existing.sources, ...link.sources])),
      significance: `${existing.significance}\n\n${link.significance}`,
      severity:
        SEVERITY_RANK[link.severity] < SEVERITY_RANK[existing.severity]
          ? link.severity
          : existing.severity,
      relationship:
        existing.relationship === relationshipFor(link, matter)
          ? existing.relationship
          : `${existing.relationship}; ${relationshipFor(link, matter)}`,
    };
    byPeer.set(peer, merged);
  }

  return Array.from(byPeer.values()).sort(
    (a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity] || a.number - b.number,
  );
}

export const relatedMatterNumbers = (matter: number): number[] =>
  relatedMatters(matter).map((entry) => entry.number);

export function exposuresForMatter(matter: number): CrossMatterExposure[] {
  const cluster = clusterForMatter(matter);
  if (!cluster) return [];
  return cluster.exposures
    .filter((exposure) => exposure.matters.includes(matter))
    .sort((a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity]);
}

export const openExposures = (cluster: CrossMatterCluster): CrossMatterExposure[] =>
  cluster.exposures
    .filter((exposure) => exposure.status !== "resolved")
    .sort((a, b) => SEVERITY_RANK[a.severity] - SEVERITY_RANK[b.severity]);

export function foundationForMatter(matter: number): CrossMatterFoundation[] {
  const cluster = clusterForMatter(matter);
  if (!cluster) return [];
  return cluster.foundation.filter((item) => item.matters.includes(matter));
}

export function partiesForMatter(matter: number): CrossMatterParty[] {
  const cluster = clusterForMatter(matter);
  if (!cluster) return [];
  return cluster.parties.filter(
    (party) => party.defendantIn.includes(matter) || party.factualIn.includes(matter),
  );
}

/** Ordered chain of authority-bearing links (who cites or leans on whom). */
export function authorityChain(cluster: CrossMatterCluster): CrossMatterLink[] {
  return cluster.links.filter((link) =>
    link.kinds.some(
      (kind) =>
        kind === "authority_dependency" ||
        kind === "persuasive_authority" ||
        kind === "stay_dependency",
    ),
  );
}

/** Number of distinct peer matters a matter is tied to. */
export const linkDegree = (matter: number): number => relatedMatterNumbers(matter).length;
