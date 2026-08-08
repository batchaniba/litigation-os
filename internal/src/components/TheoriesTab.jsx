import { theories } from "../data/theories";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { formatMatterRefs } from "../utils/matterRefs.js";

export const TheoriesTab = () => {
  const theme = useTheme();
  return (
    <div>
      <h2 style={{ fontSize: 24, fontWeight: 700, color: theme.heading, marginBottom: 24 }}>Thematic Legal Theories</h2>
      <div className="grid-cards">
        {theories.map(t => (
          <div key={t.id} style={{ background: theme.cardBg, borderRadius: 10, padding: 24, border: `1px solid ${theme.cardBorder}`, display: "flex", flexDirection: "column", gap: 12, transition: "border-color 0.3s" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ fontSize: 28 }}>{t.icon}</span>
              <div>
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, color: theme.heading, lineHeight: 1.3 }}>{t.title}</div>
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: GOLD, marginTop: 2 }}>Matters {formatMatterRefs(t.matters)}</div>
              </div>
            </div>
            <p style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.mutedText, lineHeight: 1.7, margin: 0 }}>{t.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
