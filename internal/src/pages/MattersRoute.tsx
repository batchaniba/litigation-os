import { useSearchParams } from "react-router";
import { MattersTab } from "../components/MattersTab";
import { useCaseFilters, type MatterSortKey } from "../hooks/useCaseFilters";

const SORT_KEYS: MatterSortKey[] = ["number", "filed", "deadline", "exposure", "court", "status"];

export default function MattersRoute() {
  const [params] = useSearchParams();
  const cluster = Number(params.get("cluster"));
  const sort = params.get("sort");
  const sortKey = SORT_KEYS.find((key) => key === sort) ?? "number";
  const filters = useCaseFilters({
    cluster: cluster >= 1 && cluster <= 5 ? cluster : null,
    status: params.get("status") ?? "active",
    type: params.get("type"),
    query: params.get("q") ?? "",
    sort: sortKey,
  });
  return <MattersTab {...filters} />;
}
