import React from 'react';
import TaskItem from './TaskItem';

/**
 * TaskList component handling loading states, empty states, and task rendering.
 */
export default function TaskList({ tasks, isLoading, onToggle, onEdit, onDelete, filter }) {
  if (isLoading) {
    return (
      <div className="task-list-loading" aria-live="polite">
        <p className="loading-text">Loading tasks...</p>
      </div>
    );
  }

  if (!tasks || tasks.length === 0) {
    const emptyMessage =
      filter === 'completed'
        ? 'No completed tasks yet.'
        : filter === 'pending'
        ? 'No pending tasks. You are all caught up!'
        : 'No tasks yet. Create your first task above!';

    return (
      <div className="task-list-empty" aria-live="polite">
        <p className="empty-title">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <ul className="task-list" aria-label="Task list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
