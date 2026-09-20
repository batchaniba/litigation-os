// Numbered cluster buckets vs named cross-matter graph.
//
// Numbered truth: internal/src/data/clusters.js + matter.json `cluster`.
// Named graph:    internal/src/data/index/clusters.json (from crossMatter.json).
// The two systems must not be used interchangeably.
import {
  CLUSTERS,
  CLUSTER_LABELS,
  NUMBERED_CLUSTER_IDS,
  formatMatterRanges,
  isNumberedClusterId,
  numberedClusterById,
} from "../../src/data/clusters.js";

export {
  CLUSTERS,
  CLUSTER_LABELS,
  NUMBERED_CLUSTER_IDS,
  formatMatterRanges,
  isNumberedClusterId,
  numberedClusterById,
};

export function mattersByNumberedCluster(matters) {
  const byCluster = new Map(CLUSTERS.map((c) => [c.n, []]));
  const unknown = [];
  for (const matter of matters ?? []) {
    const id = Number(matter.cluster);
    if (!isNumberedClusterId(id)) {
      unknown.push(matter);
      continue;
    }
    byCluster.get(id).push(matter.number);
  }
  for (const list of byCluster.values()) list.sort((a, b) => a - b);
  return { byCluster, unknown };
}

export function clusterMatterPhrase(nums) {
  if (!nums.length) return "";
  const ranges = formatMatterRanges(nums);
  return nums.length === 1 ? `Matter ${ranges}` : `Matters ${ranges}`;
}

export function clusterHeadingLine(n, matterNumbers) {
  const def = numberedClusterById(n);
  if (!def) throw new Error(`unknown numbered cluster ${n}`);
  const phrase = clusterMatterPhrase(matterNumbers);
  return phrase
    ? `### Cluster ${n} — ${def.label} (${phrase})`
    : `### Cluster ${n} — ${def.label}`;
}

export function clusterHeadingBlock(n, matterNumbers) {
  return `<a id="cluster-${n}"></a>\n${clusterHeadingLine(n, matterNumbers)}`;
}

export function clusterTocLine(n) {
  const def = numberedClusterById(n);
  if (!def) throw new Error(`unknown numbered cluster ${n}`);
  return `- [${n} — ${def.label}](#cluster-${n})`;
}

export function buildClusterToc(matters) {
  const { byCluster } = mattersByNumberedCluster(matters);
  return CLUSTERS.filter((c) => (byCluster.get(c.n) ?? []).length > 0)
    .map((c) => `  ${clusterTocLine(c.n)}`)
    .join("\n");
}

/** Expand "22, 25–27, 31" / "36-40" into integer matter numbers. */
export function parseMatterRangeList(text) {
  const nums = [];
  for (const part of String(text ?? "").split(",")) {
    const token = part.trim();
    if (!token) continue;
    const range = token.match(/^(\d+)\s*[–-]\s*(\d+)$/);
    if (range) {
      const start = Number(range[1]);
      const end = Number(range[2]);
      if (end < start) continue;
      for (let n = start; n <= end; n++) nums.push(n);
      continue;
    }
    if (/^\d+$/.test(token)) nums.push(Number(token));
  }
  return [...new Set(nums)].sort((a, b) => a - b);
}

function sameNumbers(a, b) {
  if (a.length !== b.length) return false;
  return a.every((n, i) => n === b[i]);
}

function looksLikeNumberedId(id) {
  return typeof id === "number" || (typeof id === "string" && /^\d+$/.test(id.trim()));
}

/**
 * Fail closed when README / matter.cluster / named-graph ids drift from
 * clusters.js. The historical README inversion (3 = Consumer Fraud, 5 =
 * Employment) is the fixture this is built to catch.
 */
export function collectNumberedClusterIssues({
  matters = [],
  readme = "",
  namedClusters = [],
} = {}) {
  const errors = [];
  const known = [...NUMBERED_CLUSTER_IDS].sort((a, b) => a - b);
  const knownLabel = known.join(", ");
  const { byCluster, unknown } = mattersByNumberedCluster(matters);

  for (const matter of unknown) {
    errors.push(
      `Matter ${matter.number} has unknown numbered cluster id ${JSON.stringify(matter.cluster)} ` +
        `(canonical map is ${knownLabel} in internal/src/data/clusters.js).`,
    );
  }

  const seenNamed = new Set();
  for (const cluster of namedClusters ?? []) {
    const id = cluster?.id;
    const key = String(id);
    if (seenNamed.has(key)) continue;
    seenNamed.add(key);
    if (id == null || id === "") {
      errors.push("named cluster is missing an id (index/clusters.json / crossMatter.json).");
      continue;
    }
    if (looksLikeNumberedId(id) || isNumberedClusterId(id)) {
      errors.push(
        `named cluster id ${JSON.stringify(id)} looks like a numbered bucket — ` +
          `named graph ids must be slugs (e.g. chp-nov2024), not matter.cluster integers.`,
      );
    }
  }

  const headingRe = /^### Cluster (\d+)\s+[—–-]\s+(.+?)\s*$/gm;
  const found = new Map();
  for (const match of readme.matchAll(headingRe)) {
    const n = Number(match[1]);
    const rest = match[2].trim();
    const label = rest.replace(/\s+\((?:Matter|Matters)\s+[^)]+\)\s*$/, "").trim();
    const listedMatch = rest.match(/\((?:Matter|Matters)\s+([^)]+)\)\s*$/);
    found.set(n, {
      label,
      listed: listedMatch ? parseMatterRangeList(listedMatch[1]) : null,
      raw: rest,
    });
  }

  for (const cl of CLUSTERS) {
    const heading = found.get(cl.n);
    if (!heading) {
      errors.push(`README is missing a "### Cluster ${cl.n} — ${cl.label}" heading.`);
      continue;
    }
    if (heading.label !== cl.label) {
      errors.push(
        `README Cluster ${cl.n} heading is "${heading.label}" but the numbered map ` +
          `(clusters.js) says "${cl.label}".`,
      );
    }
    if (heading.listed) {
      const expected = byCluster.get(cl.n) ?? [];
      if (!sameNumbers(heading.listed, expected)) {
        errors.push(
          `README Cluster ${cl.n} lists matters ${heading.listed.join(", ") || "(none)"} ` +
            `but matter.cluster data has ${expected.join(", ") || "(none)"}.`,
        );
      }
    }
  }

  for (const [n, heading] of found) {
    if (!NUMBERED_CLUSTER_IDS.has(n)) {
      errors.push(`README has Cluster ${n} ("${heading.label}") which is not in the numbered map.`);
    }
  }

  const tocRe = /^\s*-\s+\[(\d+)\s+[—–-]\s+([^\]]+)\]\(#cluster-\1\)\s*$/gm;
  const tocFound = new Map();
  for (const match of readme.matchAll(tocRe)) {
    tocFound.set(Number(match[1]), match[2].trim());
  }
  // Also accept the older auto-slug TOC form so an inverted label still fails
  // even when the href is the GitHub heading slug instead of #cluster-N.
  const tocLooseRe = /^\s*-\s+\[(\d+)\s+[—–-]\s+([^\]]+)\]\(#[^)]+\)\s*$/gm;
  for (const match of readme.matchAll(tocLooseRe)) {
    const n = Number(match[1]);
    if (!tocFound.has(n)) tocFound.set(n, match[2].trim());
  }

  if (tocFound.size) {
    for (const cl of CLUSTERS) {
      const label = tocFound.get(cl.n);
      if (!label) {
        errors.push(`README contents is missing a Cluster ${cl.n} TOC entry for "${cl.label}".`);
        continue;
      }
      if (label !== cl.label) {
        errors.push(
          `README contents lists Cluster ${cl.n} as "${label}" but the numbered map ` +
            `(clusters.js) says "${cl.label}".`,
        );
      }
    }
  }

  return errors;
}
