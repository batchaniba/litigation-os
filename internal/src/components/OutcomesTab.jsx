import { useState } from "react";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { cases } from "../data/matters";
import { damages_table } from "../data/damages";
import { outcomes } from "../data/outcomes";
import { isActiveExposureRow, litigatingMatters, sumExposure } from "../utils/portfolioStats";

const fmt = (n) => "$" + n.toLocaleString();

const GREEN  = "#16a34a";
const AMBER  = "#d97706";
const BLUE   = "#0284c7";

const publicRealized = outcomes.realized.filter((r) => !r.confidential).reduce((s, r) => s + r.amount, 0);
const anticipated = outcomes.anticipated.reduce((s, r) => s + r.amount, 0);
const combinedIsConfidential = outcomes.realized.some((r) => r.confidential) && anticipated === 0;
const combined = publicRealized + anticipated;
const byNumber = new Map(cases.map((c) => [Number(c.number), c]));
const liveDamages = damages_table.filter((row) => isActiveExposureRow(row, byNumber));
const moderate = sumExposure(liveDamages, "moderate");
const totalMatterCount = cases.length;
const activeMatterCount = litigatingMatters(cases).length;

function StatTile({ label, amount, prefix = "", color, sub, confidential = false, theme, href, linkLabel }) {
  const Tag = href ? "a" : "div";
  const linkProps = href ? { href, target: "_blank", rel: "noopener noreferrer" } : {};
  return (
    <Tag
      {...linkProps}
      style={{
        flex: 1, minWidth: 180,
        background: theme.cardBg,
        border: `1px solid ${color}44`,
        borderRadius: 12,
        padding: "24px 28px",
        position: "relative",
        overflow: "hidden",
        display: "block",
        textDecoration: "none",
        color: "inherit",
        cursor: href ? "pointer" : "default",
      }}
    >
      <div style={{
        position: "absolute", top: 0, left: 0, right: 0, height: 3,
        background: color,
        borderRadius: "12px 12px 0 0",
      }} />
      <div style={{
        fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
        letterSpacing: 3, textTransform: "uppercase", color, marginBottom: 10,
      }}>{label}</div>
      {confidential ? (
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 15, fontWeight: 600,
          fontStyle: "italic", color: theme.mutedText, lineHeight: 1, paddingTop: 6,
        }}>Terms Confidential</div>
      ) : (
        <div style={{
          fontFamily: "'Cormorant Garamond', Georgia, serif",
          fontSize: 38, fontWeight: 700, color: theme.heading, lineHeight: 1,
        }}>
          {prefix}{fmt(amount)}
        </div>
      )}
      {sub && (
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 11,
          color: theme.mutedText, marginTop: 8, lineHeight: 1.4,
        }}>{sub}</div>
      )}
      {href && (
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 1, color, marginTop: 12,
          display: "flex", alignItems: "center", gap: 4,
        }}>
          {linkLabel || "Open"} <span aria-hidden="true">↗</span>
        </div>
      )}
    </Tag>
  );
}

function OutcomeCard({ item, color, statusLabel, theme }) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{
      background: theme.cardBg,
      borderRadius: 10,
      border: `1px solid ${open ? color + "60" : theme.cardBorder}`,
      overflow: "hidden",
      transition: "border-color 0.2s",
    }}>
      <button
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
        style={{
          width: "100%", padding: "18px 24px", cursor: "pointer",
          display: "flex", alignItems: "center", gap: 18, flexWrap: "wrap",
          background: "transparent", border: "none", textAlign: "left",
          color: "inherit", font: "inherit", lineHeight: "inherit",
        }}
      >
        {/* Matter number */}
        <div style={{
          width: 40, height: 40, borderRadius: 8,
          background: color + "18",
          border: `1px solid ${color}44`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700,
          color, flexShrink: 0,
        }}>{item.matter}</div>

        {/* Caption + meta */}
        <div style={{ flex: 1, minWidth: 200 }}>
          <div style={{ fontSize: 16, fontWeight: 700, color: theme.heading, marginBottom: 3 }}>
            {item.caption}
          </div>
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText,
          }}>
            {item.case_no} · {item.court}
          </div>
        </div>

        {/* Status pill */}
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase",
          background: color + "18", color, border: `1px solid ${color}44`,
          borderRadius: 20, padding: "4px 14px", whiteSpace: "nowrap",
        }}>{statusLabel}</div>

        {/* Amount */}
        <div style={{
          fontFamily: item.confidential ? "'DM Sans', sans-serif" : "'Cormorant Garamond', Georgia, serif",
          fontSize: item.confidential ? 12 : 26,
          fontWeight: item.confidential ? 600 : 700,
          fontStyle: item.confidential ? "italic" : "normal",
          color: item.confidential ? theme.mutedText : color,
          whiteSpace: "nowrap",
        }}>
          {item.confidential ? "Confidential" : `${item.type === "default_judgment" ? "~" : ""}${fmt(item.amount)}`}
        </div>

        <div aria-hidden style={{
          color: theme.subtleText, fontSize: 18,
          transition: "transform 0.3s", transform: open ? "rotate(180deg)" : "rotate(0)",
        }}>▾</div>
      </button>

      {open && (
        <div style={{
          padding: "0 24px 24px",
          borderTop: `1px solid ${theme.cardBorder}`,
        }}>
          <div className="grid-2" style={{ paddingTop: 18 }}>
            <div>
              <Label>Claims</Label>
              <p style={bodyText(theme)}>{item.claims}</p>
            </div>
            <div>
              <Label>{item.type === "settlement" ? "Resolution Date" : "Prove-Up Hearing"}</Label>
              <p style={bodyText(theme)}>{item.date}</p>
              {item.speed && <>
                <Label>Speed</Label>
                <p style={bodyText(theme)}>{item.speed}</p>
              </>}
              {item.served === false && <>
                <Label>Service Status</Label>
                <p style={bodyText(theme)}>Resolved before service completed</p>
              </>}
              {item.defendants && <>
                <Label>Defendants</Label>
                <p style={bodyText(theme)}>{item.defendants}</p>
              </>}
            </div>
          </div>
          <div style={{ marginTop: 14 }}>
            <Label>Notes</Label>
            <p style={{ ...bodyText(theme), lineHeight: 1.7 }}>{item.notes}</p>
          </div>
        </div>
      )}
    </div>
  );
}

const Label = ({ children }) => (
  <div style={{
    fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
    letterSpacing: 2, textTransform: "uppercase", color: GOLD, marginBottom: 6,
  }}>{children}</div>
);

const bodyText = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 13,
  color: theme.secondaryText, lineHeight: 1.6, margin: "0 0 14px",
});

export function OutcomesTab() {
  const theme = useTheme();
  const pct = Math.min((combined / moderate) * 100, 100);

  return (
    <div>
      {/* Page heading */}
      <div style={{ marginBottom: 32 }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 4, textTransform: "uppercase", color: GOLD, marginBottom: 8,
        }}>Portfolio Profit</div>
        <h2 style={{ fontSize: 28, fontWeight: 700, color: theme.heading, margin: "0 0 6px" }}>
          Results
        </h2>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13,
          color: theme.mutedText, margin: 0, maxWidth: 620,
        }}>
          {totalMatterCount} tracked matters (filed, closed, prefiling) across six jurisdictions.
          {" "}{activeMatterCount} currently litigating. Matter 22 settled and was dismissed; Matter 27
          has an executed settlement whose dismissal filing is not verified. No live public demands. All pro se.
        </p>
      </div>

      {/* Stat tiles */}
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 28 }}>
        <StatTile
          label="Confirmed — Settled"
          amount={realized}
          color={GREEN}
          sub="Matter 22 · Pilot Travel Centers · July 14, 2026 · dismissed Aug. 6"
          confidential={outcomes.realized.some(r => r.confidential)}
          theme={theme}
        />
        {outcomes.anticipated.length > 0 ? (
          <StatTile
            label="Anticipated — Default Judgment"
            amount={anticipated}
            prefix="~"
            color={AMBER}
            sub="Near-term recoveries booked below"
            theme={theme}
          />
        ) : (
          <StatTile
            label="Near-Term Booked"
            amount={0}
            color={AMBER}
            sub="Matter 12 default track closed — defense appeared Aug. 12"
            theme={theme}
          />
        )}
        <StatTile
          label="Combined Near-Term"
          amount={combined}
          prefix={outcomes.anticipated.length > 0 ? "~" : ""}
          color={BLUE}
          sub={combinedIsConfidential ? "Confidential recoveries omitted from this total" : `vs. ${fmt(moderate)} live exposure (moderate)`}
          confidential={combinedIsConfidential}
          theme={theme}
        />
      </div>

      {/* Progress bar */}
      <div style={{
        background: theme.cardBg,
        border: `1px solid ${theme.cardBorder}`,
        borderRadius: 10, padding: "20px 24px", marginBottom: 36,
      }}>
        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "baseline",
          marginBottom: 10, flexWrap: "wrap", gap: 8,
        }}>
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
            letterSpacing: 2, textTransform: "uppercase", color: GOLD,
          }}>Live exposure (moderate) — settled recoveries not totaled here</div>
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.mutedText,
          }}>{combinedIsConfidential ? "Confidential" : fmt(combined)} · {fmt(moderate)} live</div>
        </div>
        <div style={{
          height: 10, background: theme.barTrack, borderRadius: 6, overflow: "hidden",
        }}>
          <div style={{
            height: "100%", width: `${pct}%`,
            background: `linear-gradient(90deg, ${GREEN}, ${BLUE})`,
            borderRadius: 6, transition: "width 0.8s ease",
          }} />
        </div>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.mutedText,
          marginTop: 8,
        }}>
          {combinedIsConfidential
            ? `${fmt(moderate)} live moderate exposure across ${activeMatterCount} litigating matters. Settled/historical valuations (Matters 22, 27) are omitted so confidential amounts cannot be inferred.`
            : `${pct.toFixed(1)}% captured · ${fmt(moderate - combined)} remaining at moderate estimate across ${activeMatterCount} litigating matters`}
        </div>
      </div>

      {/* Confirmed */}
      <SectionHeading label="Confirmed" color={GREEN} count={outcomes.realized.length} theme={theme} />
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
        {outcomes.realized.map(item => (
          <OutcomeCard key={item.matter} item={item} color={GREEN} statusLabel="Settled" theme={theme} />
        ))}
      </div>

      {/* Anticipated */}
      <SectionHeading label="Near-Term" color={AMBER} count={outcomes.anticipated.length} theme={theme} />
      {outcomes.anticipated.length === 0 ? (
        <div style={{
          background: theme.cardBg,
          border: `1px solid ${theme.cardBorder}`,
          borderRadius: 10, padding: "18px 24px", marginBottom: 32,
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.mutedText, lineHeight: 1.6,
        }}>
          No near-term recovery is currently booked. Matter 12&apos;s default prove-up did not go forward on Aug. 12, 2026 —
          Diamond and Alpine appeared through counsel and disputed service. Further CMC Dec. 11, 2026.
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
          {outcomes.anticipated.map(item => (
            <OutcomeCard key={`${item.matter}-${item.type}`} item={item} color={AMBER} statusLabel="Default Pending" theme={theme} />
          ))}
        </div>
      )}

      <SectionHeading label="Active Demands" color="#ea580c" count={0} theme={theme} />
      <div style={{
        background: theme.cardBg,
        border: `1px solid ${theme.cardBorder}`,
        borderRadius: 10, padding: "18px 24px", marginBottom: 32,
        fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.mutedText, lineHeight: 1.6,
      }}>
        No live public demands. Matter 27 settlement is executed; dismissal filing is not verified.
        Passed-deadline letters are not counted as active, and defendants in one case are not counted as separate matters.
      </div>

      {/* Context note */}
      <div style={{
        background: theme.cardBg,
        border: `1px solid ${GOLD}30`,
        borderRadius: 10, padding: "20px 24px",
        borderLeft: `3px solid ${GOLD}`,
      }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase", color: GOLD, marginBottom: 10,
        }}>What the record shows</div>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText,
          lineHeight: 1.8, margin: 0,
        }}>
          Matter 22 settled in under seven weeks, pro se, before a single proof of service was filed —
          because the defendant&apos;s own adverse-action notice named the registry as the only reason for termination —
          and the action was dismissed with prejudice on August 6, 2026. Terms are confidential.
          Matter 12&apos;s default track closed when Diamond and Alpine appeared through counsel on August 12
          and disputed service; that case is back on an ordinary litigated path (CMC Dec. 11).
          FedEx (Matter 25) and UPS (Matter 26) are in federal court after removal. Matter 27 settlement
          is executed; dismissal filing is not verified. These outcomes reflect the quality of the
          underlying record across all {totalMatterCount} tracked matters. Live moderate exposure of{" "}
          {fmt(moderate)} covers {activeMatterCount} litigating matters; settled and historical
          valuations are kept separate.
        </p>
      </div>
    </div>
  );
}

function SectionHeading({ label, color, count }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 12, marginBottom: 14,
    }}>
      <div style={{
        fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 700,
        letterSpacing: 3, textTransform: "uppercase", color,
      }}>{label}</div>
      <div style={{
        fontFamily: "'DM Sans', sans-serif", fontSize: 11, fontWeight: 600,
        background: color + "18", color, border: `1px solid ${color}44`,
        borderRadius: 20, padding: "2px 10px",
      }}>{count} {count === 1 ? "matter" : "matters"}</div>
      <div style={{ flex: 1, height: 1, background: color + "30" }} />
    </div>
  );
}
