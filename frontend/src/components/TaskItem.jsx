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
  });
}

/**
 * Checks if a task is overdue (pending and due_date < start of today).
 */
function isTaskOverdue(task) {
  if (!task.due_date || task.status === 'completed') return false;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Parse YYYY-MM-DD cleanly in local timezone
  const parts = task.due_date.split('-');
  if (parts.length === 3) {
    const dueDate = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    return dueDate < today;
  }
  return new Date(task.due_date) < today;
}

/**
 * TaskItem component rendering task content, priority badge, due date, overdue highlight,
 * square checkbox, edit, and delete confirmation.
 */
export default function TaskItem({ task, onToggle, onEdit, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const isCompleted = task.status === 'completed';
  const overdue = isTaskOverdue(task);

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
      <li className={`task-item ${isCompleted ? 'completed' : 'pending'} ${overdue ? 'overdue' : ''}`}>
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
              <div className="badge-group">
                {/* Priority label */}
                <span className={`priority-badge priority-${task.priority || 'medium'}`}>
                  {task.priority || 'medium'}
                </span>
                {/* Overdue badge if pending & past due date */}
                {overdue && (
                  <span className="overdue-badge">
                    Overdue
                  </span>
                )}
                {/* Status label */}
                <span className={`status-badge ${isCompleted ? 'completed' : 'pending'}`}>
                  {isCompleted ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>

            {task.description && (
              <p className="task-description">{task.description}</p>
            )}

            <div className="task-meta">
              {task.due_date && (
                <span className={`task-due-date ${overdue ? 'text-overdue' : ''}`}>
                  Due: {formatDate(task.due_date)}
                </span>
              )}
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
