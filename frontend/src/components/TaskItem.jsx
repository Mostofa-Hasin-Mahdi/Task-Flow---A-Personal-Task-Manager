import React, { useState } from 'react';
import TaskEditForm from './TaskEditForm';
import ConfirmDialog from './ConfirmDialog';

/**
 * Human-friendly date formatter.
 */
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * TaskItem component rendering task content, square checkbox, edit, and delete confirmation.
 */
export default function TaskItem({ task, onToggle, onEdit, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const isCompleted = task.status === 'completed';

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggle(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  const handleSaveEdit = async (payload) => {
    await onEdit(task.id, payload);
    setIsEditing(false);
  };

  const handleConfirmDelete = async () => {
    setShowConfirm(false);
    await onDelete(task.id);
  };

  if (isEditing) {
    return (
      <li className={`task-item editing ${isCompleted ? 'completed' : 'pending'}`}>
        <TaskEditForm
          task={task}
          onSave={handleSaveEdit}
          onCancel={() => setIsEditing(false)}
        />
      </li>
    );
  }

  return (
    <>
      <li className={`task-item ${isCompleted ? 'completed' : 'pending'}`}>
        <div className="task-main">
          {/* Custom square accessible checkbox */}
          <label className="checkbox-container">
            <input
              type="checkbox"
              checked={isCompleted}
              onChange={handleToggle}
              disabled={isToggling}
              aria-label={`Mark "${task.title}" as ${isCompleted ? 'pending' : 'completed'}`}
            />
            <span className="checkbox-custom" aria-hidden="true" />
          </label>

          <div className="task-content">
            <div className="task-header-row">
              <h3 className={`task-title ${isCompleted ? 'strikethrough' : ''}`}>
                {task.title}
              </h3>
              <span className={`status-badge ${isCompleted ? 'completed' : 'pending'}`}>
                {isCompleted ? 'Completed' : 'Pending'}
              </span>
            </div>

            {task.description && (
              <p className="task-description">{task.description}</p>
            )}

            <div className="task-meta">
              <span className="task-date">Created {formatDate(task.created_at)}</span>
            </div>
          </div>
        </div>

        <div className="task-actions">
          <button
            type="button"
            className="btn-action edit"
            onClick={() => setIsEditing(true)}
            aria-label={`Edit task "${task.title}"`}
          >
            Edit
          </button>
          <button
            type="button"
            className="btn-action delete"
            onClick={() => setShowConfirm(true)}
            aria-label={`Delete task "${task.title}"`}
          >
            Delete
          </button>
        </div>
      </li>

      <ConfirmDialog
        isOpen={showConfirm}
        title="Delete Task"
        message={`Are you sure you want to delete "${task.title}"? This action cannot be undone.`}
        onConfirm={handleConfirmDelete}
        onCancel={() => setShowConfirm(false)}
      />
    </>
  );
}
