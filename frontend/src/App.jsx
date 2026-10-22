import React, { useMemo } from 'react';
import { useTasks } from './hooks/useTasks';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import FilterBar from './components/FilterBar';
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
    setFilter,
    addTask,
    editTask,
    toggleTask,
    removeTask,
  } = useTasks();

  // Compute live task counts when viewing all tasks
  const counts = useMemo(() => {
    let pending = 0;
    let completed = 0;
    for (const t of tasks) {
      if (t.status === 'completed') {
        completed += 1;
      } else {
        pending += 1;
      }
    }
    return { pending, completed };
  }, [tasks]);

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
        <FilterBar
          currentFilter={filter}
          onFilterChange={setFilter}
          counts={counts}
        />

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
