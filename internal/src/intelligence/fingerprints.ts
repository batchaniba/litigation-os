import type { ArgumentSnapshot, FingerprintMatch, FingerprintProfile, IntelligenceCatalog } from "./types";

export function matchFingerprint(profile: FingerprintProfile, filing: ArgumentSnapshot): FingerprintMatch {
  const overlap = filing.arguments.filter((item) => profile.repeatedArguments.includes(item));
  const authOverlap = filing.authorities.filter((item) => profile.frequentAuthorities.includes(item));
  const denom = Math.max(1, profile.repeatedArguments.length + profile.frequentAuthorities.length);
  const score = Math.round(((overlap.length + authOverlap.length) / denom) * 100);
  return {
    attorneyId: profile.id,
    score,
    resembled: [...new Set([...overlap, ...authOverlap])],
    priorOutcomes: { granted: 0, denied: 0, mixed: 0 },
    vulnerableProposition: profile.leadDefense,
  };
}

export function fingerprintForMatter(catalog: IntelligenceCatalog, matter: number): FingerprintMatch[] {
  const filing = [...catalog.arguments].reverse().find((row) => row.matter === matter);
  if (!filing) return [];
  return catalog.fingerprints
    .filter((profile) => profile.matters.includes(matter))
    .map((profile) => matchFingerprint(profile, filing));
}
