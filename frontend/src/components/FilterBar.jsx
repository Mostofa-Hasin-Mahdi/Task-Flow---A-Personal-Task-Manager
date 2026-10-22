import React from 'react';

/**
 * FilterBar component for switching between All, Pending, and Completed tasks.
 * Uses strict square design, aria-pressed attributes, and counts summary.
 */
export default function FilterBar({ currentFilter, onFilterChange, counts }) {
  const filters = [
    { key: 'all', label: 'All' },
    { key: 'pending', label: 'Pending' },
    { key: 'completed', label: 'Completed' },
  ];

  return (
    <div className="filter-bar-container">
      <div className="filter-buttons" role="group" aria-label="Filter tasks">
        {filters.map(({ key, label }) => {
          const isActive = currentFilter === key;
          return (
            <button
              key={key}
              type="button"
              className={`filter-btn ${isActive ? 'active' : ''}`}
              onClick={() => onFilterChange(key)}
              aria-pressed={isActive}
            >
              {label}
            </button>
          );
        })}
      </div>

      {currentFilter === 'all' && counts && (
        <div className="task-counts-summary" aria-live="polite">
          <span className="count-item pending">
            <strong>{counts.pending}</strong> pending
          </span>
          <span className="count-separator">•</span>
          <span className="count-item completed">
            <strong>{counts.completed}</strong> completed
          </span>
        </div>
      )}
    </div>
  );
}
