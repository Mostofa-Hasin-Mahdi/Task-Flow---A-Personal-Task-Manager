import React from 'react';

/**
 * Reusable inline error alert component.
 */
export default function ErrorMessage({ message, details }) {
  if (!message) return null;

  return (
    <div className="error-alert" role="alert">
      <div className="error-alert-title">{message}</div>
      {details && Array.isArray(details) && details.length > 0 && (
        <ul className="error-alert-list">
          {details.map((item, idx) => (
            <li key={idx}>
              <strong>{item.field || 'Error'}:</strong> {item.issue || item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
