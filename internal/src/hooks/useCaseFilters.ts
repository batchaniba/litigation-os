import { useMemo, useState } from "react";
import { cases } from "../data/matters";
import type { Matter } from "../types/portfolio";

export const useCaseFilters = (initialCluster: number | null = null) => {
  const [statusFilter, setStatusFilter] = useState("active");
  const [clusterFilter, setClusterFilter] = useState<number | null>(initialCluster);
  const [typeFilter, setTypeFilter] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredCases = useMemo(() => (cases as Matter[]).filter((matter) => {
    if (statusFilter === "active" && matter.archived) return false;
    if (clusterFilter && matter.cluster !== clusterFilter) return false;
    if (typeFilter && matter.type !== typeFilter) return false;
    if (!searchQuery) return true;

    const query = searchQuery.toLowerCase();
    return [matter.caption, matter.case_no, matter.claims, matter.defendants, matter.key_facts]
      .some((value) => value.toLowerCase().includes(query));
  }), [statusFilter, clusterFilter, typeFilter, searchQuery]);

  return {
    statusFilter, setStatusFilter, clusterFilter, setClusterFilter,
    typeFilter, setTypeFilter, searchQuery, setSearchQuery, filteredCases,
  };
};
