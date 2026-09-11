import type { MatterSummary } from "../types/portfolio";
import type { GraphEdge, GraphNode, IntelligenceCatalog, KnowledgeGraph } from "./types";
import { clustersForMatter, linksForMatter } from "../utils/crossMatter";

function node(partial: GraphNode): GraphNode {
  return partial;
}

export function buildKnowledgeGraph(summaries: MatterSummary[], catalog: IntelligenceCatalog): KnowledgeGraph {
  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];
  const seen = new Set<string>();

  const addNode = (item: GraphNode) => {
    if (seen.has(item.id)) return;
    seen.add(item.id);
    nodes.push(item);
  };
  const addEdge = (item: GraphEdge) => {
    if (seen.has(item.id)) return;
    seen.add(item.id);
    edges.push(item);
  };

  for (const issue of catalog.issues) {
    addNode(node({ id: `issue:${issue.id}`, kind: "Issue", label: issue.label, issues: [issue.id] }));
  }
  for (const authority of catalog.authorities) {
    addNode(
      node({
        id: `authority:${authority.id}`,
        kind: "Authority",
        label: authority.label,
        issues: authority.issues,
        attrs: { citation: authority.citation, court: authority.court },
      }),
    );
    for (const other of authority.cites) {
      addEdge({
        id: `cites:${authority.id}:${other}`,
        kind: "cites",
        from: `authority:${authority.id}`,
        to: `authority:${other}`,
      });
    }
    for (const other of authority.citedBy) {
      addEdge({
        id: `cited_by:${other}:${authority.id}`,
        kind: "cited_by",
        from: `authority:${other}`,
        to: `authority:${authority.id}`,
      });
    }
  }
  for (const firm of catalog.firms) {
    addNode(node({ id: `firm:${firm.id}`, kind: "Firm", label: firm.name }));
  }
  for (const attorney of catalog.attorneys) {
    addNode(node({ id: `attorney:${attorney.id}`, kind: "Attorney", label: attorney.name, issues: attorney.issues }));
    addEdge({
      id: `employed:${attorney.id}`,
      kind: "employed_by",
      from: `attorney:${attorney.id}`,
      to: `firm:${attorney.firm}`,
    });
  }
  for (const judge of catalog.judges) {
    addNode(node({ id: `judge:${judge.id}`, kind: "Judge", label: judge.judge, attrs: { court: judge.court } }));
  }

  for (const summary of summaries) {
    const matterId = `matter:${summary.number}`;
    addNode(
      node({
        id: matterId,
        kind: "Matter",
        label: summary.caption,
        matter: summary.number,
        attrs: { phase: summary.phase, court: summary.court, lifecycle: summary.lifecycle },
      }),
    );
    addNode(node({ id: `defendant:${summary.number}`, kind: "Defendant", label: summary.defendants, matter: summary.number }));
    addEdge({
      id: `party:${summary.number}`,
      kind: "party_to",
      from: `defendant:${summary.number}`,
      to: matterId,
      matter: summary.number,
    });

    const haystack = summary.judge.toLowerCase();
    const judgeHit = catalog.judges.find((row) => haystack.includes(row.id) || haystack.includes(row.judge.toLowerCase()));
    if (judgeHit) {
      addEdge({
        id: `assigned:${summary.number}:${judgeHit.id}`,
        kind: "assigned_to",
        from: matterId,
        to: `judge:${judgeHit.id}`,
        matter: summary.number,
      });
    }

    for (const cause of summary.causes) {
      const claimId = `claim:${summary.number}:${cause.slice(0, 48)}`;
      addNode(node({ id: claimId, kind: "Claim", label: cause, matter: summary.number }));
      addEdge({ id: `contains:${claimId}`, kind: "contains", from: matterId, to: claimId, matter: summary.number });
    }
  }

  for (const attorney of catalog.attorneys) {
    for (const matter of attorney.matters) {
      addEdge({
        id: `represents:${attorney.id}:${matter}`,
        kind: "represents",
        from: `attorney:${attorney.id}`,
        to: `matter:${matter}`,
        matter,
      });
      for (const issue of attorney.issues) {
        addEdge({
          id: `raises:${attorney.id}:${matter}:${issue}`,
          kind: "raises",
          from: `attorney:${attorney.id}`,
          to: `issue:${issue}`,
          matter,
        });
      }
    }
  }

  for (const matrix of catalog.matrices) {
    for (const element of matrix.elements) {
      const elementId = `element:${element.id}`;
      addNode(
        node({
          id: elementId,
          kind: "Element",
          label: element.label,
          matter: matrix.matter,
          issues: element.issue ? [element.issue] : [],
        }),
      );
      addEdge({
        id: `contains:${elementId}`,
        kind: "contains",
        from: `claim:${matrix.matter}:${matrix.claim_id}`,
        to: elementId,
        matter: matrix.matter,
      });
      addNode(node({ id: `claim:${matrix.matter}:${matrix.claim_id}`, kind: "Claim", label: matrix.claim, matter: matrix.matter }));
      addEdge({
        id: `claim-in:${matrix.claim_id}`,
        kind: "contains",
        from: `matter:${matrix.matter}`,
        to: `claim:${matrix.matter}:${matrix.claim_id}`,
        matter: matrix.matter,
      });
      if (element.issue) {
        addEdge({
          id: `same_issue:${matrix.matter}:${element.issue}`,
          kind: "same_issue",
          from: `matter:${matrix.matter}`,
          to: `issue:${element.issue}`,
          matter: matrix.matter,
        });
      }
      for (const authority of element.authority) {
        addEdge({
          id: `cites:${element.id}:${authority}`,
          kind: "cites",
          from: elementId,
          to: `authority:${authority}`,
          matter: matrix.matter,
        });
      }
    }
  }

  for (const fact of catalog.facts) {
    addNode(node({ id: `fact:${fact.id}`, kind: "Fact", label: fact.fact, issues: fact.issues }));
    for (const matter of fact.supports) {
      addEdge({ id: `supports:${fact.id}:${matter}`, kind: "supports", from: `fact:${fact.id}`, to: `matter:${matter}`, matter });
    }
    for (const contradiction of fact.contradicted_by) {
      addNode(node({ id: `admission:${fact.id}:${contradiction.slice(0, 24)}`, kind: "Admission", label: contradiction }));
      addEdge({
        id: `contradicts:${fact.id}:${contradiction.slice(0, 24)}`,
        kind: "contradicts",
        from: `admission:${fact.id}:${contradiction.slice(0, 24)}`,
        to: `fact:${fact.id}`,
      });
    }
  }

  for (const motion of catalog.motions) {
    addNode(
      node({
        id: `docket:${motion.id}`,
        kind: motion.status === "decided" ? "CourtOrder" : "DocketEntry",
        label: motion.label,
        matter: motion.matter,
        issues: motion.issues,
      }),
    );
    addEdge({
      id: `filed:${motion.id}`,
      kind: "filed_in",
      from: `docket:${motion.id}`,
      to: `matter:${motion.matter}`,
      matter: motion.matter,
    });
    for (const issue of motion.issues) {
      addEdge({
        id: `raises:${motion.id}:${issue}`,
        kind: "raises",
        from: `docket:${motion.id}`,
        to: `issue:${issue}`,
        matter: motion.matter,
      });
    }
  }

  for (const summary of summaries) {
    for (const cluster of clustersForMatter(summary.number)) {
      for (const link of linksForMatter(summary.number)) {
        const kind = link.kinds.includes("authority_dependency")
          ? "authority_dependency"
          : link.kinds.includes("same_statute") || link.kinds.includes("shared_predicate")
            ? "same_issue"
            : "depends_on";
        addEdge({
          id: `xm:${link.id}:${summary.number}`,
          kind,
          from: `matter:${link.from}`,
          to: `matter:${link.to}`,
          matter: summary.number,
          label: cluster.id,
        });
      }
    }
  }

  const byId: Record<string, GraphNode> = {};
  for (const item of nodes) byId[item.id] = item;
  return { nodes, edges, byId };
}
