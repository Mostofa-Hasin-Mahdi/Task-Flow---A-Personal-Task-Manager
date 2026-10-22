import React, { useState } from 'react';
import ErrorMessage from './ErrorMessage';

/**
 * Task creation form with title, description, priority, and due_date.
 */
export default function TaskForm({ onAddTask }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('medium');
  const [dueDate, setDueDate] = useState('');
  const [fieldError, setFieldError] = useState('');
  const [serverError, setServerError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

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

    setIsSubmitting(true);
    try {
      await onAddTask({
        title: trimmedTitle,
        description: description.trim() || null,
        priority,
        due_date: dueDate || null,
      });
      setTitle('');
      setDescription('');
      setPriority('medium');
      setDueDate('');
    } catch (err) {
      setServerError({
        message: err.message || 'Failed to create task',
        details: err.details,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit} noValidate>
      <h2 className="form-heading">New Task</h2>

      {serverError && (
        <ErrorMessage
          message={serverError.message}
          details={serverError.details}
        />
      )}

      <div className="form-group">
        <label htmlFor="task-title" className="form-label">
          Task Title <span className="required-star">*</span>
        </label>
        <input
          id="task-title"
          type="text"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (fieldError) setFieldError('');
          }}
          disabled={isSubmitting}
          aria-invalid={!!fieldError}
          aria-describedby={fieldError ? 'task-title-error' : undefined}
        />
        {fieldError && (
          <div id="task-title-error" className="field-error" role="alert">
            {fieldError}
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="task-description" className="form-label">
          Description <span className="optional-tag">(optional)</span>
        </label>
        <textarea
          id="task-description"
          rows={3}
          placeholder="Add details, notes, or subtasks..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-row-dual">
        <div className="form-group flex-1">
          <label htmlFor="task-priority" className="form-label">
            Priority
          </label>
          <select
            id="task-priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            disabled={isSubmitting}
          >
            <option value="low">Low Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="high">High Priority</option>
          </select>
        </div>

        <div className="form-group flex-1">
          <label htmlFor="task-due-date" className="form-label">
            Due Date <span className="optional-tag">(optional)</span>
          </label>
          <input
            id="task-due-date"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={isSubmitting}
          />
        </div>
      </div>

      <div className="form-actions">
        <button
          type="submit"
          className="btn-primary"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Adding Task...' : 'Add Task'}
        </button>
      </div>
    </form>
  );
}
