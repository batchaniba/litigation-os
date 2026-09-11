import type { RecapAdvice, RecapWatchEntry } from "./types";

export function recapAdvice(entry: RecapWatchEntry): RecapAdvice {
  if (entry.inRecap) {
    return {
      documentId: entry.id,
      action: "retrieve",
      reason: "Already in RECAP. Retrieve; do not repurchase on PACER.",
      strategicValue: entry.strategicValue,
      inRecap: true,
      prayerPending: entry.prayerPending,
    };
  }
  if (entry.prayerPending) {
    return {
      documentId: entry.id,
      action: "wait",
      reason: "A RECAP prayer is pending. Watch rather than buy unless the clock expires first.",
      strategicValue: entry.strategicValue,
      inRecap: false,
      prayerPending: true,
    };
  }
  if (entry.strategicValue === "LOW") {
    return {
      documentId: entry.id,
      action: "skip",
      reason: `${entry.why} Estimated usefulness: LOW. Do not purchase.`,
      strategicValue: "LOW",
      inRecap: false,
      prayerPending: false,
    };
  }
  return {
    documentId: entry.id,
    action: "retrieve",
    reason: `${entry.why} Retrieval recommended.`,
    strategicValue: entry.strategicValue,
    inRecap: false,
    prayerPending: false,
  };
}
