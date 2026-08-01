import { useEffect, useState } from "react";
import type { MatterFilterState } from "./useCaseFilters";

export interface SavedMatterView extends MatterFilterState { id: string; name: string; builtIn?: boolean }

const STORAGE_KEY = "newanforbi.saved-matter-views.v1";
const BUILT_INS: SavedMatterView[] = [
  { id: "active-federal", name: "Active federal", builtIn: true, status: "active", cluster: null, type: "Federal", query: "", sort: "deadline" },
  { id: "active-state", name: "Active state", builtIn: true, status: "active", cluster: null, type: "State", query: "", sort: "deadline" },
  { id: "upcoming", name: "Upcoming deadlines", builtIn: true, status: "upcoming", cluster: null, type: null, query: "", sort: "deadline" },
  { id: "exposure", name: "Highest exposure", builtIn: true, status: "active", cluster: null, type: null, query: "", sort: "exposure" },
];

export function useSavedMatterViews() {
  const [custom, setCustom] = useState<SavedMatterView[]>(() => {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]"); } catch { return []; }
  });
  useEffect(() => { localStorage.setItem(STORAGE_KEY, JSON.stringify(custom)); }, [custom]);
  const save = (name: string, state: MatterFilterState) => setCustom((views) => [...views, { ...state, id: crypto.randomUUID(), name }]);
  const remove = (id: string) => setCustom((views) => views.filter((view) => view.id !== id));
  return { views: [...BUILT_INS, ...custom], save, remove };
}
