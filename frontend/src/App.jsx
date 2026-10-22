import React from 'react';
import { useTasks } from './hooks/useTasks';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import ErrorMessage from './components/ErrorMessage';
import './styles/tokens.css';
import './styles/base.css';
import './styles/components.css';

export default function App() {
  const {
    tasks,
    isLoading,
    error,
    filter,
    addTask,
    editTask,
    toggleTask,
    removeTask,
  } = useTasks();

  return (
    <main className="container">
      <header className="app-header">
        <h1 className="app-title">Task-Flow</h1>
        <p className="app-subtitle">
          Personal task manager built with React and FastAPI.
        </p>
      </header>

      {error && (
        <ErrorMessage
          message={error}
        />
      )}

      <TaskForm onAddTask={addTask} />

      <section aria-label="Tasks Section">
        <TaskList
          tasks={tasks}
          isLoading={isLoading}
          onToggle={toggleTask}
          onEdit={editTask}
          onDelete={removeTask}
          filter={filter}
        />
      </section>
    </main>
  );
}
