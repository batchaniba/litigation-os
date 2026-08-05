import { useEffect } from "react";

export const Modal = ({ isOpen, onClose, title, children }) => {
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
      className="modal-backdrop"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
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
          <h3 className="modal-title">
            {title}
          </h3>
        )}
        {children}
      </div>
    </div>
  );
};
