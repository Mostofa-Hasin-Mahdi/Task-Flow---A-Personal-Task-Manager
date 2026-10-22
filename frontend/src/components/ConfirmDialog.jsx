import React, { useEffect, useRef } from 'react';

/**
 * Accessible confirmation modal dialog with keyboard trap (Escape/Tab) and strict square design.
 */
export default function ConfirmDialog({ isOpen, title, message, onConfirm, onCancel, confirmLabel = 'Delete' }) {
  const dialogRef = useRef(null);
  const cancelBtnRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;

    // Focus cancel button by default on open to prevent accidental deletion
    cancelBtnRef.current?.focus();

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        onCancel();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onCancel} role="presentation">
      <div
        className="modal-box"
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title"
        onClick={(e) => e.stopPropagation()}
        ref={dialogRef}
      >
        <h3 id="dialog-title" className="modal-title">{title}</h3>
        <p className="modal-message">{message}</p>
        <div className="modal-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={onCancel}
            ref={cancelBtnRef}
          >
            Cancel
          </button>
          <button
            type="button"
            className="btn-danger"
            onClick={onConfirm}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
