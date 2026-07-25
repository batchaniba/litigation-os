import { useState, useMemo } from "react";
import { PORTFOLIO } from "../data";

export const useCaseFilters = () => {
  const [statusFilter, setStatusFilter] = useState("active"); // "active" | "all"
  const [clusterFilter, setClusterFilter] = useState(null);
  const [typeFilter, setTypeFilter] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredCases = useMemo(() => {
    return PORTFOLIO.cases.filter(c => {
      if (statusFilter === "active" && c.archived) return false;
      if (clusterFilter && c.cluster !== clusterFilter) return false;
      if (typeFilter && c.type !== typeFilter) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        return c.caption.toLowerCase().includes(q) || c.claims.toLowerCase().includes(q) || c.defendants.toLowerCase().includes(q) || c.key_facts.toLowerCase().includes(q);
      }
      return true;
    });
  }, [statusFilter, clusterFilter, typeFilter, searchQuery]);

  return { statusFilter, setStatusFilter, clusterFilter, setClusterFilter, typeFilter, setTypeFilter, searchQuery, setSearchQuery, filteredCases };
};
