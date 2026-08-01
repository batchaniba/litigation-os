import { useState } from "react";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { cases } from "../data/matters";
import { outcomes } from "../data/outcomes";

const fmt = (n) => "$" + n.toLocaleString();

const GREEN  = "#16a34a";
const AMBER  = "#d97706";
const BLUE   = "#0284c7";

const realized   = outcomes.realized.reduce((s, r) => s + r.amount, 0);
const anticipated = outcomes.anticipated.reduce((s, r) => s + r.amount, 0);
const combined   = realized + anticipated;
const moderate   = outcomes.portfolio_exposure.moderate;
const demandTotal = outcomes.active_demands.reduce((s, d) => s + d.demand_amount, 0);
const demandSentDates = outcomes.active_demands.map(d => new Date(d.sent_date));
const demandDeadlines = outcomes.active_demands.map(d => new Date(d.deadline));
const earliestSent = new Date(Math.min(...demandSentDates));
const latestSent = new Date(Math.max(...demandSentDates));
const earliestDeadline = new Date(Math.min(...demandDeadlines));
const latestDeadline = new Date(Math.max(...demandDeadlines));
const fmtDate = (d) => d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
const demandSentRange = earliestSent.getTime() === latestSent.getTime()
  ? fmtDate(earliestSent)
  : `${fmtDate(earliestSent)} – ${fmtDate(latestSent)}`;
const demandDeadlineRange = earliestDeadline.getTime() === latestDeadline.getTime()
  ? fmtDate(earliestDeadline)
  : `${fmtDate(earliestDeadline)} – ${fmtDate(latestDeadline)}`;
const totalMatterCount = cases.length;
const activeMatterCount = cases.filter(c => !c.archived).length;

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
          <div style={{
            display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, paddingTop: 18,
          }}>
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
          {totalMatterCount} matters filed across six jurisdictions. {activeMatterCount} active. The first recoveries are in — one settled,
          one heading to default judgment, {outcomes.active_demands.length} demands outstanding. All pro se.
        </p>
      </div>

      {/* Stat tiles */}
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 28 }}>
        <StatTile
          label="Confirmed — Settled"
          amount={realized}
          color={GREEN}
          sub="Matter 22 · Pilot Travel Centers · July 11, 2026"
          confidential={outcomes.realized.some(r => r.confidential)}
          theme={theme}
        />
        <StatTile
          label="Anticipated — Default Judgment"
          amount={anticipated}
          prefix="~"
          color={AMBER}
          sub="Matter 12 · Diamond / Alpine · Prove-up Aug. 12, 2026"
          theme={theme}
          href="https://claude.ai/code/artifact/41e12d5f-30c9-439d-9f58-2aaf9317a9ac"
          linkLabel="The Last Mile: judgment → cash walkthrough"
        />
        <StatTile
          label="Combined Near-Term"
          amount={combined}
          prefix="~"
          color={BLUE}
          sub={`vs. ${fmt(moderate)} portfolio exposure (moderate)`}
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
          }}>Recovery vs. Portfolio Exposure (Moderate)</div>
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.mutedText,
          }}>{fmt(combined)} of {fmt(moderate)}</div>
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
          {pct.toFixed(1)}% captured · {fmt(moderate - combined)} remaining at moderate estimate across {activeMatterCount} active matters
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
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
        {outcomes.anticipated.map(item => (
          <OutcomeCard key={item.matter} item={item} color={AMBER} statusLabel="Default Pending" theme={theme} />
        ))}
      </div>

      {/* Active Demands */}
      <SectionHeading label="Active Demands" color="#ea580c" count={outcomes.active_demands.length} theme={theme} />
      <div style={{
        background: theme.cardBg,
        border: "1px solid #ea580c30",
        borderRadius: 10, padding: "14px 20px", marginBottom: 14,
        display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12,
      }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.mutedText, lineHeight: 1.6,
        }}>
          Pre-filing demands transmitted <strong style={{ color: theme.heading }}>{demandSentRange}</strong> · Response deadlines <strong style={{ color: "#ea580c" }}>{demandDeadlineRange}</strong>
        </div>
        <div>
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700,
            letterSpacing: 2, textTransform: "uppercase", color: "#ea580c", marginBottom: 4, textAlign: "right",
          }}>Combined Demand</div>
          <div style={{
            fontFamily: "'Cormorant Garamond', Georgia, serif",
            fontSize: 28, fontWeight: 700, color: "#ea580c",
          }}>{fmt(demandTotal)}</div>
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
        {outcomes.active_demands.map(item => (
          <DemandCard key={item.matter} item={item} theme={theme} />
        ))}
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
          because the defendant's own adverse-action notice named the registry as the only reason for termination.
          There was nothing to litigate. Matter 12 reaches a default posture because both defendants chose not
          to respond. Matters 25 and 26 are already filed and assigned; pre-filing demands of $85,000 each went
          out citing the Pilot settlement as a resolved precedent. Matter 27 followed the same $85,000 pattern
          against both Randstad and RK Logistics after a termination that came before the FCRA waiting period
          even ran; the complaint is already on file (No. 26CV199902, Alameda Sup. Ct.), both defendants were
          SERVED July 30, 2026, and RK Logistics has since denied the demand through counsel — a response that
          reaches only the Tameny claim against RK Logistics and leaves Randstad's own exposure untouched. These outcomes are not anomalies; they reflect the quality of the underlying record
          across all {totalMatterCount} matters. The remaining {fmt(moderate - combined)} at moderate estimate represents
          {activeMatterCount} active matters where that same record is still at work.
        </p>
      </div>
    </div>
  );
}

function DemandCard({ item, theme }) {
  const [open, setOpen] = useState(false);
  const ORANGE = "#ea580c";
  const RED = "#ef4444";
  const denied = item.response_status === "denied";
  const statusColor = denied ? RED : ORANGE;
  const statusLabel = denied ? "Denied" : "Demand Pending";
  return (
    <div style={{
      background: theme.cardBg,
      borderRadius: 10,
      border: `1px solid ${open ? statusColor + "60" : theme.cardBorder}`,
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
        <div style={{
          width: 40, height: 40, borderRadius: 8,
          background: ORANGE + "18",
          border: `1px solid ${ORANGE}44`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700,
          color: ORANGE, flexShrink: 0,
        }}>{item.matter}</div>

        <div style={{ flex: 1, minWidth: 200 }}>
          <div style={{ fontSize: 16, fontWeight: 700, color: theme.heading, marginBottom: 3 }}>
            {item.caption}
          </div>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText }}>
            {item.case_no} · {item.court}
          </div>
        </div>

        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase",
          background: statusColor + "18", color: statusColor, border: `1px solid ${statusColor}44`,
          borderRadius: 20, padding: "4px 14px", whiteSpace: "nowrap",
        }}>{statusLabel}</div>

        <div style={{
          fontFamily: "'Cormorant Garamond', Georgia, serif",
          fontSize: 26, fontWeight: 700, color: statusColor, whiteSpace: "nowrap",
        }}>{fmt(item.demand_amount)}</div>

        <div aria-hidden style={{
          color: theme.subtleText, fontSize: 18,
          transition: "transform 0.3s", transform: open ? "rotate(180deg)" : "rotate(0)",
        }}>▾</div>
      </button>

      {open && (
        <div style={{ padding: "0 24px 24px", borderTop: `1px solid ${theme.cardBorder}` }}>
          <div style={{
            display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, paddingTop: 18,
          }}>
            <div>
              <Label>Demand Sent</Label>
              <p style={bodyText(theme)}>{item.sent_date}</p>
              <Label>Response Deadline</Label>
              <p style={bodyText(theme)}>{item.deadline} · {item.deadline_time}</p>
              {denied && (
                <>
                  <Label>Response Received</Label>
                  <p style={{ ...bodyText(theme), color: RED }}>{item.response_date} — Denied</p>
                </>
              )}
            </div>
            <div>
              <Label>Respondent's Counsel</Label>
              <p style={bodyText(theme)}>{item.counsel}<br />{item.counsel_email}</p>
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

function SectionHeading({ label, color, count, theme }) {
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
