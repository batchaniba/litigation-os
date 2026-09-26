import type { TimelineEvent } from "../types/portfolio";
import full from "./timeline.public.json";

/** Public timeline (timeline.public.json: settlement figures withheld; see
 *  internal/scripts/sync-public-timeline.mjs). Import only from route/search chunks, not the shell. */
export const timeline = full as TimelineEvent[];
