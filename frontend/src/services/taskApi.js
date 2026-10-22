/**
 * Custom Error class carrying server message and validation details.
 */
export class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Internal request helper:
 * - sends JSON headers
 * - parses responses safely
 * - unwraps `data` property on success
 * - handles network errors and server error envelopes
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  };

  let response;
  try {
    response = await fetch(url, config);
  } catch {
    throw new ApiError('Cannot reach the server. Please check your connection.', 0);
  }

  let json;
  try {
    json = await response.json();
  } catch {
    throw new ApiError(
      `Unexpected server response (${response.status} ${response.statusText})`,
      response.status
    );
  }

  if (!response.ok) {
    const errorPayload = json?.error || {};
    const message = errorPayload.message || 'An unexpected error occurred.';
    const details = errorPayload.details || null;
    throw new ApiError(message, response.status, details);
  }

  return json.data;
}

export const taskApi = {
  /**
   * Fetch all tasks, optionally filtered by status ('pending' | 'completed').
   */
  getTasks(status) {
    const query = status && status !== 'all' ? `?status=${encodeURIComponent(status)}` : '';
    return request(`/tasks${query}`, { method: 'GET' });
  },

  /**
   * Create a new task.
   */
  createTask({ title, description }) {
    return request('/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
  },

  /**
   * Update an existing task.
   */
  updateTask(id, payload) {
    return request(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    });
  },

  /**
   * Toggle task status between pending and completed.
   */
  toggleTask(id) {
    return request(`/tasks/${id}/toggle`, {
      method: 'PATCH',
    });
  },

  /**
   * Delete a task by ID.
   */
  deleteTask(id) {
    return request(`/tasks/${id}`, {
      method: 'DELETE',
    });
  },
};
