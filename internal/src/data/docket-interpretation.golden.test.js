// Golden tests for the Family 3 extraction ("strategy as data").
// These fixtures capture the pre-extraction behavior of the docket
// interpretation functions byte-for-byte. The functions keep the same
// names and signatures after the refactor — they just read their
// thresholds, weights, and patterns from
// internal/src/data/rules/docket-interpretation.json instead of
// hardcoding them. If any fixture fails, the refactor changed behavior.
//
// Fixture inputs live in ./courtlistener/fixtures/docket-interpretation.json;
// expected outputs were captured from the pre-extraction code on
// 2026-09-17 and must not be hand-edited.
import { describe, expect, it } from "vitest";
import {
  detectDeadlineCandidate,
  factPrefix,
  inferFactActor,
  inferFactType,
} from "../../scripts/courtlistener/entries.mjs";
import {
  descriptionSimilarity,
  findMatchingTimelineEvent,
  reconcileEntries,
  scoreTimelineMatch,
} from "../../scripts/courtlistener/reconcile.mjs";
import { BOOTSTRAP_MATTERS } from "../../scripts/courtlistener/sync-dockets.mjs";
import {
  guessDocType,
  guessFiler,
  packetFlag,
  toDocketRow,
} from "../../scripts/split-matter.mjs";
import fixture from "./courtlistener/fixtures/docket-interpretation.json";

const FNS = {
  inferFactType,
  inferFactActor,
  detectDeadlineCandidate,
  factPrefix,
  scoreTimelineMatch,
  descriptionSimilarity,
  findMatchingTimelineEvent,
  reconcileEntries,
  guessFiler,
  guessDocType,
  packetFlag,
  toDocketRow,
};
const VALUES = { BOOTSTRAP_MATTERS };

describe("docket-interpretation golden fixtures", () => {
  for (const c of fixture.cases) {
    it(c.id, () => {
      if ("value" in c) {
        expect(VALUES[c.value]).toEqual(c.expected);
      } else {
        expect(FNS[c.fn](...c.args)).toEqual(c.expected);
      }
    });
  }
});
