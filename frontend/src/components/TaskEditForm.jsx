import React, { useState } from 'react';
import ErrorMessage from './ErrorMessage';

/**
 * Inline edit form for existing task item with priority and due_date.
 */
export default function TaskEditForm({ task, onSave, onCancel }) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [priority, setPriority] = useState(task.priority || 'medium');
  const [dueDate, setDueDate] = useState(task.due_date ? task.due_date.substring(0, 10) : '');
  const [fieldError, setFieldError] = useState('');
  const [serverError, setServerError] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFieldError('');
    setServerError(null);

    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      setFieldError('Title is required');
      return;
    }

    if (trimmedTitle.length > 255) {
      setFieldError('Title cannot exceed 255 characters');
      return;
    }

    setIsSaving(true);
    try {
      await onSave({
        title: trimmedTitle,
        description: description.trim() || null,
        priority,
        due_date: dueDate || null,
      });
    } catch (err) {
      setServerError({
        message: err.message || 'Failed to save changes',
        details: err.details,
      });
      setIsSaving(false);
    }
  };

  return (
    <form className="task-edit-form" onSubmit={handleSubmit} noValidate>
      {serverError && (
        <ErrorMessage
          message={serverError.message}
          details={serverError.details}
        />
      )}

      <div className="form-group">
        <label htmlFor={`edit-title-${task.id}`} className="form-label">
          Title
        </label>
        <input
          id={`edit-title-${task.id}`}
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (fieldError) setFieldError('');
          }}
          disabled={isSaving}
          aria-invalid={!!fieldError}
        />
        {fieldError && (
          <div className="field-error" role="alert">
            {fieldError}
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor={`edit-desc-${task.id}`} className="form-label">
          Description
        </label>
        <textarea
          id={`edit-desc-${task.id}`}
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isSaving}
        />
      </div>

      <div className="form-row-dual">
        <div className="form-group flex-1">
          <label htmlFor={`edit-priority-${task.id}`} className="form-label">
            Priority
          </label>
          <select
            id={`edit-priority-${task.id}`}
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            disabled={isSaving}
          >
            <option value="low">Low Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="high">High Priority</option>
          </select>
        </div>

        <div className="form-group flex-1">
          <label htmlFor={`edit-due-date-${task.id}`} className="form-label">
            Due Date
          </label>
          <input
            id={`edit-due-date-${task.id}`}
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={isSaving}
          />
        </div>
      </div>

      <div className="edit-actions">
        <button
          type="button"
          className="btn-secondary"
          onClick={onCancel}
          disabled={isSaving}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="btn-primary"
          disabled={isSaving}
        >
          {isSaving ? 'Saving...' : 'Save'}
        </button>
      </div>
    </form>
  );
}
