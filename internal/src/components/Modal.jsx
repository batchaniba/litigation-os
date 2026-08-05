import { useEffect, useId, useRef } from "react";

export const Modal = ({ isOpen, onClose, title, children }) => {
  const dialogRef = useRef(null);
  const titleId = useId();

  useEffect(() => {
    if (!isOpen) return;
    const previouslyFocused = document.activeElement;
    const dialog = dialogRef.current;
    const focusable = () => dialog?.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])') ?? [];
    dialog?.querySelector("button")?.focus();
    const onKeyDown = (e) => {
      if (e.key === "Escape") onClose();
      if (e.key !== "Tab") return;
      const items = Array.from(focusable());
      if (!items.length) { e.preventDefault(); dialog?.focus(); return; }
      const first = items[0];
      const last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
    document.addEventListener("keydown", onKeyDown);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = prevOverflow;
      if (previouslyFocused instanceof HTMLElement) previouslyFocused.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      onClick={onClose}
      className="modal-backdrop"
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={title ? titleId : undefined}
        aria-label={title ? undefined : "Dialog"}
        tabIndex={-1}
        onClick={(e) => e.stopPropagation()}
        className="modal-dialog"
      >
        <button
          onClick={onClose}
          aria-label="Close"
          className="modal-close"
        >
          ×
        </button>
        {title && (
          <h2 id={titleId} className="modal-title">
            {title}
          </h2>
        )}
        {children}
      </div>
    </div>
  );
};
