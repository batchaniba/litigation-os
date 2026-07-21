import { useEffect } from "react";
import { useTheme } from "../ThemeContext";
import { GOLD } from "../constants";

export const Modal = ({ isOpen, onClose, title, children }) => {
  const theme = useTheme();

  useEffect(() => {
    if (!isOpen) return;
    const onKeyDown = (e) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", onKeyDown);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = prevOverflow;
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed", inset: 0, background: "rgba(0,0,0,0.6)",
        display: "flex", alignItems: "center", justifyContent: "center",
        padding: 24, zIndex: 1000,
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        onClick={(e) => e.stopPropagation()}
        style={{
          background: `${theme.cardBg}80`, border: `1px solid ${theme.cardBorder}`,
          backdropFilter: "blur(10px)", WebkitBackdropFilter: "blur(10px)",
          borderRadius: 10, padding: 28, width: "100%", maxWidth: 560,
          maxHeight: "85vh", overflowY: "auto", position: "relative",
          boxShadow: "0 20px 60px rgba(0,0,0,0.4)",
        }}
      >
        <button
          onClick={onClose}
          aria-label="Close"
          style={{
            position: "absolute", top: 12, right: 12, width: 28, height: 28,
            borderRadius: 6, border: `1px solid ${theme.cardBorder}`,
            background: "transparent", color: theme.secondaryText,
            fontSize: 16, cursor: "pointer", display: "flex",
            alignItems: "center", justifyContent: "center", lineHeight: 1,
          }}
        >
          ×
        </button>
        {title && (
          <h3 style={{
            fontSize: 15, fontWeight: 700, color: GOLD,
            margin: "0 28px 12px 0", fontFamily: "'DM Sans', sans-serif",
          }}>
            {title}
          </h3>
        )}
        {children}
      </div>
    </div>
  );
};
