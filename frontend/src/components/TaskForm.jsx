import React, { useState } from 'react';
import ErrorMessage from './ErrorMessage';

/**
 * Task creation form with client-side trimming validation and server error display.
 */
export default function TaskForm({ onAddTask }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
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
      });
      setTitle('');
      setDescription('');
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
