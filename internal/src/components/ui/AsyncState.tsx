import type { ReactNode } from "react";

export function RouteLoading({ label = "Loading" }: { label?: string }) {
  return <div className="route-loading" role="status" aria-label={label} />;
}

export function EmptyState({ title, detail, action }: { title: string; detail?: string; action?: ReactNode }) {
  return (
    <div className="empty-state">
      <div>
        <h2>{title}</h2>
        {detail && <p>{detail}</p>}
        {action}
      </div>
    </div>
  );
}
