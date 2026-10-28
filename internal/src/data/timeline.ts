import type { TimelineEvent } from "../types/portfolio";
import publicTimeline from "./timeline.public.json";

/** Public timeline projection — the SPA never bundles the internal full log. */
export const timeline = publicTimeline as TimelineEvent[];
