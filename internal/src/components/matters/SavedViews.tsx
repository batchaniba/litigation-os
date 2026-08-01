import { useState } from "react";
import { useSavedMatterViews, type SavedMatterView } from "../../hooks/useSavedMatterViews";
import type { MatterFilterState } from "../../hooks/useCaseFilters";
import { useTheme } from "../../ThemeContext";

export function SavedViews({ current, onApply }: { current: MatterFilterState; onApply: (view: SavedMatterView) => void }) {
  const [name, setName] = useState("");
  const { views, save, remove } = useSavedMatterViews();
  const theme = useTheme();
  const saveCurrent = () => { const trimmed = name.trim(); if (!trimmed) return; save(trimmed, current); setName(""); };
  return (
    <details className="saved-views" style={{ background: theme.cardBg, borderColor: theme.cardBorder }}>
      <summary>Saved views <span>{views.length}</span></summary>
      <div className="saved-view-grid">
        {views.map((view) => <div key={view.id} className="saved-view-row"><button onClick={() => onApply(view)}>{view.name}</button>{!view.builtIn && <button className="saved-view-delete" onClick={() => remove(view.id)} aria-label={`Delete saved view ${view.name}`}>×</button>}</div>)}
      </div>
      <div className="save-view-form"><input value={name} onChange={(event) => setName(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") saveCurrent(); }} placeholder="Name this view" aria-label="Saved view name" style={{ background: theme.inputBg, borderColor: theme.cardBorder, color: theme.inputColor }} /><button onClick={saveCurrent} disabled={!name.trim()}>Save current</button></div>
    </details>
  );
}
