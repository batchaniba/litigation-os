import { useEffect, useState } from "react";
import { loadMatter } from "../data/matters/loadMatter";
import type { Matter } from "../types/portfolio";

export type MatterLoadStatus = "idle" | "loading" | "ready" | "error";

type MatterState = {
  matter: Matter | null;
  status: MatterLoadStatus;
  error: string | null;
  /** Matter number this state was last keyed to; null when idle/cleared. */
  requestKey: number | null;
};

const IDLE: MatterState = { matter: null, status: "idle", error: null, requestKey: null };

export function useMatter(number: number | null | undefined) {
  const requestKey =
    number == null || Number.isNaN(Number(number)) ? null : Number(number);
  const [state, setState] = useState<MatterState>(IDLE);

  // Reset / mark loading during render when the requested matter changes
  // (eslint-plugin-react-hooks@7 set-state-in-effect).
  if (requestKey == null && state.requestKey !== null) {
    setState(IDLE);
  } else if (requestKey != null && state.requestKey !== requestKey) {
    setState({ matter: null, status: "loading", error: null, requestKey });
  }

  useEffect(() => {
    if (requestKey == null) return;

    let cancelled = false;
    loadMatter(requestKey)
      .then((record) => {
        if (cancelled) return;
        setState({ matter: record, status: "ready", error: null, requestKey });
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setState({
          matter: null,
          status: "error",
          error: err instanceof Error ? err.message : "Failed to load matter",
          requestKey,
        });
      });

    return () => {
      cancelled = true;
    };
  }, [requestKey]);

  return { matter: state.matter, status: state.status, error: state.error };
}
