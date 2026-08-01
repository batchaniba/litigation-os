import { useSearchParams } from "react-router-dom";
import { MattersTab } from "../components/MattersTab";
import { useCaseFilters } from "../hooks/useCaseFilters";

export default function MattersRoute() {
  const [params] = useSearchParams();
  const cluster = Number(params.get("cluster"));
  const filters = useCaseFilters(cluster >= 1 && cluster <= 5 ? cluster : null);
  return <MattersTab {...filters} />;
}
