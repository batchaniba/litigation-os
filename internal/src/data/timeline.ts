import type { TimelineEvent } from "../types/portfolio";
// Public projection: settlement / demand figures are withheld by
// internal/scripts/sync-public-timeline.mjs. The full log stays in timeline.json.
import publicTimeline from "./timeline.public.json";

/** Public timeline projection — the SPA never bundles the internal full log. */
export const timeline = publicTimeline as TimelineEvent[];
