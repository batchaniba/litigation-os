import { useEffect, useState } from "react";
import { loadMatter } from "../data/matters";
import type { Matter } from "../types/portfolio";

export type MatterLoadStatus = "idle" | "loading" | "ready" | "error";

export function useMatter(number: number | null | undefined) {
  const [matter, setMatter] = useState<Matter | null>(null);
  const [status, setStatus] = useState<MatterLoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (number == null || Number.isNaN(Number(number))) {
      setMatter(null);
      setStatus("idle");
      setError(null);
      return;
    }

    let cancelled = false;
    setStatus("loading");
    setError(null);

    loadMatter(Number(number))
      .then((record) => {
        if (cancelled) return;
        setMatter(record);
        setStatus("ready");
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        setMatter(null);
        setStatus("error");
        setError(err instanceof Error ? err.message : "Failed to load matter");
      });

    return () => {
      cancelled = true;
    };
  }, [number]);

  return { matter, status, error };
}
