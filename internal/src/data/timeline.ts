import type { TimelineEvent } from "../types/portfolio";
// Public projection: settlement / demand figures are withheld by
// internal/scripts/sync-public-timeline.mjs. The full log stays in timeline.json.
import full from "./timeline.public.json";

/** Public timeline event log — import only from route/search chunks, not the shell. */
export const timeline = full as TimelineEvent[];
