// Classify npm outdated JSON the way the old Dependabot groups did.
// In-range rows (`current` → `wanted`) are `npm update`. Out-of-range
// (`wanted` → `latest`) are a human major bump. TypeScript majors stay ignored
// until typescript-eslint peers TS 7+.

export const IGNORE_MAJOR = new Set(["typescript"]);

export const GROUPS = [
  {
    name: "dev-tooling",
    kinds: ["minor", "patch"],
    match: /^(eslint|@eslint\/|typescript-eslint$|@testing-library\/|jsdom$|globals$)/,
  },
  {
    name: "build-tooling",
    kinds: ["minor", "patch"],
    match: /^(vite$|@vitejs\/|typescript$)/,
  },
  {
    name: "react-ecosystem",
    kinds: ["minor", "patch"],
    match: /^(react$|react-dom$|react-router|@types\/react$|@types\/react-dom$)/,
  },
  {
    name: "vitest-stack",
    kinds: ["major", "minor", "patch"],
    match: /^(vitest$|@vitest\/)/,
  },
  {
    name: "react-stack",
    kinds: ["major"],
    match: /^(react$|react-dom$|react-router|@types\/react$|@types\/react-dom$)/,
  },
];

export function parseRequirementsTxt(text) {
  const rows = [];
  for (const raw of text.split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, "").trim();
    if (!line) continue;
    const m = line.match(/^([A-Za-z0-9_.-]+)\s*>=\s*([0-9][^\s;]*)/);
    if (!m) continue;
    rows.push({ name: m[1], floor: m[2] });
  }
  return rows;
}

export function cmpSemver(a, b) {
  const parse = (v) =>
    String(v)
      .replace(/^v/, "")
      .split(/[-+]/)[0]
      .split(".")
      .map((n) => parseInt(n, 10) || 0);
  const aa = parse(a);
  const bb = parse(b);
  const len = Math.max(aa.length, bb.length);
  for (let i = 0; i < len; i += 1) {
    const d = (aa[i] || 0) - (bb[i] || 0);
    if (d) return d > 0 ? 1 : -1;
  }
  return 0;
}

export function classifyNpm(outdated) {
  const inRange = [];
  const major = [];
  const ignoredMajor = [];
  for (const [name, info] of Object.entries(outdated || {})) {
    const current = info.current ?? "?";
    const wanted = info.wanted ?? current;
    const latest = info.latest ?? wanted;
    const type = info.type ?? "dependencies";
    if (current !== wanted) {
      inRange.push({
        name,
        current,
        wanted,
        latest,
        type,
        group: groupFor(name, "patch"),
      });
    }
    // npm's "latest" dist-tag can lag a newer current line (jsdom 30, react-router 8).
    if (cmpSemver(latest, wanted) > 0) {
      const row = {
        name,
        current,
        wanted,
        latest,
        type,
        group: groupFor(name, "major"),
      };
      if (IGNORE_MAJOR.has(name)) ignoredMajor.push(row);
      else major.push(row);
    }
  }
  const byName = (a, b) => a.name.localeCompare(b.name);
  inRange.sort(byName);
  major.sort(byName);
  ignoredMajor.sort(byName);
  return { inRange, major, ignoredMajor };
}

export function groupFor(name, kind) {
  const kinds = kind === "major" ? ["major"] : ["minor", "patch"];
  for (const g of GROUPS) {
    if (g.kinds.some((k) => kinds.includes(k)) && g.match.test(name)) return g.name;
  }
  return "other";
}

export function formatReport({ npm, pip }) {
  const lines = [];
  const { inRange, major, ignoredMajor } = npm;
  lines.push("## npm");
  if (!inRange.length && !major.length) {
    lines.push("Current — lockfile matches the registry within declared ranges.");
  } else {
    if (inRange.length) {
      lines.push(`In-range (${inRange.length}) — \`npm run deps:update\`:`);
      for (const row of inRange) {
        lines.push(`  ${row.name}  ${row.current} → ${row.wanted}  [${row.group}]`);
      }
    }
    if (major.length) {
      lines.push(`Major / out-of-range (${major.length}) — bump package.json by hand, keep peer groups together:`);
      for (const row of major) {
        lines.push(`  ${row.name}  ${row.wanted} → ${row.latest}  [${row.group}]`);
      }
    }
  }
  if (ignoredMajor.length) {
    lines.push("Ignored majors (typescript-eslint still peers typescript <6.1):");
    for (const row of ignoredMajor) {
      lines.push(`  ${row.name}  ${row.wanted} → ${row.latest}`);
    }
  }
  if (pip) {
    lines.push("", "## pip (requirements.txt floors vs PyPI)");
    if (pip.error) {
      lines.push(`Skipped: ${pip.error}`);
    } else if (!pip.stale.length) {
      lines.push("Current — every floor is already the latest on PyPI.");
    } else {
      lines.push(`Stale floors (${pip.stale.length}) — edit requirements.txt, then pip install:`);
      for (const row of pip.stale) {
        lines.push(`  ${row.name}  ${row.floor} → ${row.latest}`);
      }
    }
  }
  return `${lines.join("\n")}\n`;
}

export function pipStale(rows, latestByName) {
  return rows
    .filter((row) => {
      const latest = latestByName.get(row.name);
      return latest && latest !== row.floor;
    })
    .map((row) => ({ name: row.name, floor: row.floor, latest: latestByName.get(row.name) }));
}
