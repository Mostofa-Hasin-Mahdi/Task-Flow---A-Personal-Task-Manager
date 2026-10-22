import { useState, useEffect, useCallback } from 'react';
import { taskApi } from '../services/taskApi';

/**
 * Custom hook encapsulating task state and CRUD operations.
 */
export function useTasks() {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all' | 'pending' | 'completed'

  const loadTasks = useCallback(async (statusFilter) => {
    setIsLoading(true);
    setError(null);
    try {
      const activeFilter = statusFilter !== undefined ? statusFilter : filter;
      const data = await taskApi.getTasks(activeFilter);
      setTasks(data);
    } catch (err) {
      setError(err.message || 'Failed to load tasks');
    } finally {
      setIsLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    loadTasks(filter);
  }, [filter, loadTasks]);

  const addTask = async (taskData) => {
    setError(null);
    try {
      const newTask = await taskApi.createTask(taskData);
      // Reload tasks or re-fetch to maintain priority ordering correctly
      await loadTasks();
      return newTask;
    } catch (err) {
      setError(err.message || 'Failed to create task');
      throw err;
    }
  };

  const editTask = async (id, payload) => {
    setError(null);
    try {
      const updatedTask = await taskApi.updateTask(id, payload);
      setTasks((prev) =>
        prev.map((t) => (t.id === id ? updatedTask : t))
      );
      return updatedTask;
    } catch (err) {
      setError(err.message || 'Failed to update task');
      throw err;
    }
  };

  const toggleTask = async (id) => {
    setError(null);
    try {
      const updatedTask = await taskApi.toggleTask(id);
      if (filter === 'all') {
        setTasks((prev) =>
          prev.map((t) => (t.id === id ? updatedTask : t))
        );
      } else {
        // If viewing 'pending' or 'completed', the toggled task is removed from this filtered view
        setTasks((prev) => prev.filter((t) => t.id !== id));
      }
      return updatedTask;
    } catch (err) {
      setError(err.message || 'Failed to toggle task');
      throw err;
    }
  };

  const removeTask = async (id) => {
    setError(null);
    try {
      await taskApi.deleteTask(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
    } catch (err) {
      setError(err.message || 'Failed to delete task');
      throw err;
    }
  };

  return {
    tasks,
    isLoading,
    error,
    filter,
    setFilter,
    loadTasks,
    addTask,
    editTask,
    toggleTask,
    removeTask,
  };
}
