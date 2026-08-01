import { useRef } from "react";
import { useNavigate } from "react-router-dom";
import { CensusTab } from "../components/CensusTab";
import { usePortfolioUI } from "../context/PortfolioUIContext";
import { ROUTES, routeForTab } from "../routes";

export default function CensusRoute() {
  const navigate = useNavigate();
  const ui = usePortfolioUI();
  const pending = useRef({ status: "all", cluster: null as number | null, search: "" });

  const navigateToTab = (tab: string) => {
    if (tab === "Matters") {
      const params = new URLSearchParams();
      if (pending.current.status) params.set("status", pending.current.status);
      if (pending.current.cluster) params.set("cluster", String(pending.current.cluster));
      if (pending.current.search) params.set("q", pending.current.search);
      navigate(`${ROUTES.matters}?${params}`);
      return;
    }
    navigate(routeForTab(tab));
  };

  return (
    <CensusTab
      setActiveTab={navigateToTab}
      setClusterFilter={(cluster: number | null) => { pending.current.cluster = cluster; }}
      setStatusFilter={(status: string) => { pending.current.status = status; }}
      setSearchQuery={(search: string) => { pending.current.search = search; }}
      damagesView={ui.damagesView}
      setDamagesView={ui.setDamagesView}
      setShowPastEvents={ui.setShowPastEvents}
    />
  );
}
