import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";

export const ServiceTracker = ({ serviceTracking }) => {
  const theme = useTheme();

  if (!serviceTracking || serviceTracking.length === 0) return null;

  const servedCount = serviceTracking.filter(s => s.served).length;
  const totalCount = serviceTracking.length;

  return (
    <div style={{ marginTop: 18 }}>
      <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: GOLD, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 8 }}>
        Service Tracker ({servedCount}/{totalCount})
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {serviceTracking.map((defendant, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "10px 12px",
              borderRadius: 6,
              background: theme.navySubtleBg,
              border: `1px solid ${theme.cardBorder}`,
            }}
          >
            <div
              style={{
                width: 20,
                height: 20,
                borderRadius: 4,
                border: `2px solid ${defendant.served ? "#10B981" : theme.cardBorder}`,
                background: defendant.served ? "#10B98118" : "transparent",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                flexShrink: 0,
              }}
            >
              {defendant.served && (
                <span style={{ color: "#10B981", fontSize: 14, fontWeight: 700 }}>✓</span>
              )}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 600, color: theme.heading, marginBottom: 2 }}>
                {defendant.name}
              </div>
              <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText }}>
                {defendant.title} · {defendant.location}
              </div>
              {defendant.dateServed && (
                <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 10, color: "#10B981", marginTop: 2 }}>
                  Served: {defendant.dateServed}
                </div>
              )}
            </div>
            <div
              style={{
                fontFamily: "'DM Sans', sans-serif",
                fontSize: 11,
                fontWeight: 600,
                color: defendant.served ? "#10B981" : "#9CA3AF",
                padding: "4px 8px",
                borderRadius: 4,
                background: defendant.served ? "#10B98115" : theme.cardBorder,
              }}
            >
              {defendant.served ? "Served" : "Pending"}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
