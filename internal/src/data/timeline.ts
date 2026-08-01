import type { TimelineEvent } from "../types/portfolio";
import full from "./timeline.json";

/** Full timeline event log — import only from route/search chunks, not the shell. */
export const timeline = full as TimelineEvent[];
