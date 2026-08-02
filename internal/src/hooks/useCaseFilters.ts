import { useMemo, useState } from "react";
import { cases } from "../data/matters";
import { matter_damages } from "../data/damages";
import upcoming from "../data/upcoming.json";
import type { MatterSummary, TimelineEvent } from "../types/portfolio";
import { parseEventDatePDT } from "../utils/dateUtils";
import { isArchivedMatter } from "../utils/matterLifecycle";

export type MatterSortKey = "number" | "filed" | "deadline" | "exposure" | "court" | "status";
export interface MatterFilterState { status: string; cluster: number | null; type: string | null; query: string; sort: MatterSortKey }

const nextDeadlineByMatter = new Map<number, number>();
for (const event of upcoming as TimelineEvent[]) {
  const timestamp = +parseEventDatePDT(event.date);
  for (const raw of event.matters.split(",")) {
    const matter = Number(raw.trim());
    if (matter && (!nextDeadlineByMatter.has(matter) || timestamp < nextDeadlineByMatter.get(matter)!)) nextDeadlineByMatter.set(matter, timestamp);
  }
}
const exposureByMatter = new Map(matter_damages.map((item) => [item.number, item.moderate]));
const filedTimestamp = (value: string) => {
  const match = value.match(/[A-Z][a-z]{2,8}\.?\s+\d{1,2},\s+\d{4}/);
  return match ? Date.parse(match[0].replace(".", "")) || 0 : 0;
};

export const useCaseFilters = (initial: Partial<MatterFilterState> = {}) => {
  const [statusFilter, setStatusFilter] = useState(initial.status ?? "active");
  const [clusterFilter, setClusterFilter] = useState<number | null>(initial.cluster ?? null);
  const [typeFilter, setTypeFilter] = useState<string | null>(initial.type ?? null);
  const [searchQuery, setSearchQuery] = useState(initial.query ?? "");
  const [sortKey, setSortKey] = useState<MatterSortKey>(initial.sort ?? "number");

  const filteredCases = useMemo(() => (cases as MatterSummary[]).filter((matter) => {
    if (statusFilter === "active" && isArchivedMatter(matter)) return false;
    if (statusFilter === "archived" && !isArchivedMatter(matter)) return false;
    if (statusFilter === "upcoming" && !nextDeadlineByMatter.has(matter.number)) return false;
    if (clusterFilter && matter.cluster !== clusterFilter) return false;
    if (typeFilter && matter.type !== typeFilter) return false;
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return [matter.caption, matter.case_no, matter.court, matter.claims, matter.defendants, matter.status, ...(matter.causes ?? [])]
      .some((value) => value?.toLowerCase().includes(query));
  }).sort((a, b) => {
    if (sortKey === "filed") return filedTimestamp(b.filed) - filedTimestamp(a.filed);
    if (sortKey === "deadline") return (nextDeadlineByMatter.get(a.number) ?? Infinity) - (nextDeadlineByMatter.get(b.number) ?? Infinity);
    if (sortKey === "exposure") return (exposureByMatter.get(b.number) ?? 0) - (exposureByMatter.get(a.number) ?? 0);
    if (sortKey === "court") return a.court.localeCompare(b.court);
    if (sortKey === "status") return a.status.localeCompare(b.status);
    return a.number - b.number;
  }), [statusFilter, clusterFilter, typeFilter, searchQuery, sortKey]);

  return {
    statusFilter, setStatusFilter, clusterFilter, setClusterFilter,
    typeFilter, setTypeFilter, searchQuery, setSearchQuery, sortKey, setSortKey, filteredCases,
  };
};
