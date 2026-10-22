# Task-Flow

A focused, accessible personal task manager with a dark-mode square design system, built with **React (Vite)**, **FastAPI**, and **PostgreSQL (Neon)**. Designed following strict **SOLID** principles, layered clean architecture, and unified HTTP response envelopes.

---

## Live Demos

- **Frontend (Vercel):** [https://task-flow-a-personal-task-manager.vercel.app](https://task-flow-a-personal-task-manager.vercel.app) *(or your deployed Vercel domain)*
- **Backend API (Render):** [https://task-flow-api.onrender.com](https://task-flow-api.onrender.com)
- **Interactive API Docs (Swagger):** [https://task-flow-api.onrender.com/docs](https://task-flow-api.onrender.com/docs)
- **API Health Check:** [https://task-flow-api.onrender.com/health](https://task-flow-api.onrender.com/health)

> **Note on Free Hosting:** Render's free tier spins down web services after periods of inactivity. If the app has been idle, the initial request might take 30–50 seconds to wake up. Subsequent requests respond instantly.

---

## Features

### Required Core Features
- [x] **Task Creation:** Add tasks with title (1–255 characters) and optional description.
- [x] **Client & Server Validation:** Whitespace trimming, empty title prevention, title length enforcement, with field-level error messages (returns HTTP 400, overriding FastAPI default 422).
- [x] **Status Toggling:** Switch task state between `pending` and `completed` with persistent timestamp updates.
- [x] **Inline Editing:** Edit title and description directly within the task item.
- [x] **Safe Deletion:** Accessible custom modal confirmation (Escape key handling, tab trap) before irreversible deletion.
- [x] **Network Resilience:** Friendly error notices when the backend service is offline.
- [x] **Strict Square Design:** Zero border-radius (`border-radius: 0 !important`) across all elements, inputs, buttons, checkboxes, and dialogs.

### Bonus Features Implemented
- [x] **Priority Levels:** Assign `Low`, `Medium`, or `High` priority to tasks.
- [x] **Server-Side Priority Ordering:** High priority tasks are displayed at the top, ordered via an SQL `CASE` expression in the repository layer.
- [x] **Due Dates & Overdue Highlighting:** Set due dates. Pending tasks past their due date display a danger-highlighted **"Overdue"** badge and red border indicator.
- [x] **Server-Side Filter Bar:** Filter tasks by `All`, `Pending`, or `Completed` via query parameter (`?status=`), accompanied by live task count badges (`X pending • Y completed`).
- [x] **Automated Test Suite:** 17 unit and integration tests using an in-memory `FakeTaskRepository` executing in under 0.15s.

---

## Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | React 19, Vite | Custom Vanilla CSS (no CSS frameworks), Design Tokens, mobile-first |
| **Backend** | FastAPI, Python 3.12 | Layered architecture, Pydantic v2, Pydantic-Settings |
| **Database** | PostgreSQL 16+ (Neon) | SQLAlchemy 2.0 ORM, psycopg v3 driver, connection pooling |
| **Migrations** | Alembic | Version-controlled schema migrations with SQL CHECK constraints |
| **Testing** | Pytest, TestClient | In-memory protocol fakes (DIP/LSP), unit and API route coverage |
| **Deployment** | Vercel & Render | Vercel for SPA frontend, Render for FastAPI backend, Neon for Serverless Postgres |

---

## Architecture & SOLID Principles

```
frontend/src/
  ├── services/       # taskApi.js (Only place making HTTP fetch requests)
  ├── hooks/          # useTasks.js (State management, loading/error flags)
  ├── components/     # UI render-only components
  └── styles/         # tokens.css & base.css & components.css

backend/app/
  ├── api/
  │    ├── routes/    # HTTP translation only. No ORM or business logic.
  │    └── deps.py    # FastAPI Depends injection wiring.
  ├── services/       # Domain business logic; depends strictly on TaskRepository Protocol.
  ├── repositories/   # Only place accessing SQLAlchemy DB Session.
  ├── models/         # SQLAlchemy 2.0 Declarative ORM models.
  ├── schemas/        # Pydantic v2 validation and envelope serialization.
  └── core/           # Configuration, custom errors, global exception handlers.
```

### SOLID in this Project
1. **Single Responsibility (SRP):** Routers handle HTTP status codes; Services handle business rules; Repositories handle database queries; Components only render UI.
2. **Open/Closed (OCP):** Added Priority and Due Date bonus features via a new Alembic migration and extended schemas without modifying the existing error-handling middleware or router lifecycle.
3. **Liskov Substitution (LSP):** `SqlTaskRepository` and `FakeTaskRepository` both satisfy the `TaskRepository` Protocol. The service behaves identically with either.
4. **Interface Segregation (ISP):** Repositories expose only the 5 specific methods required (`list`, `get`, `create`, `update`, `delete`).
5. **Dependency Inversion (DIP):** `TaskService` depends on the `TaskRepository` interface rather than a concrete SQLAlchemy session. Dependency injection via FastAPI `Depends(get_task_service)`.

---

## Prerequisites

- **Python:** 3.12+
- **Node.js:** 20+
- **Database:** PostgreSQL (local instance or cloud Neon connection string)

---

## Local Setup (Run in under 5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/Mostofa-Hasin-Mahdi/Task-Flow---A-Personal-Task-Manager.git
cd Task-Flow---A-Personal-Task-Manager
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
# (Edit .env with your Neon or local PostgreSQL connection string)

# Run migrations
alembic upgrade head

# (Optional) Seed 5 sample tasks
python -m scripts.seed

# Run backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Frontend Setup
In a new terminal:
```bash
cd frontend

# Install dependencies
npm install

# Create .env from template
cp .env.example .env

# Run Vite development server
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) in your browser.

---

## Environment Variables

### Backend (`backend/.env`)
| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string with psycopg v3 | `postgresql+psycopg://user:pass@host/db?sslmode=require` |
| `TEST_DATABASE_URL` | Optional database connection for integration tests | `postgresql+psycopg://user:pass@localhost:5432/taskflow_test` |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins | `http://localhost:5173,https://my-app.vercel.app` |
| `APP_ENV` | Environment name | `development` or `production` |

### Frontend (`frontend/.env`)
| Variable | Description | Example |
|---|---|---|
| `VITE_API_URL` | Base API endpoint for the backend | `http://localhost:8000/api` |

---

## API Reference

All successful responses return `{ "data": ... }`. All failures return `{ "error": { "message": "...", "details": ... } }`.

| Method | Endpoint | Description | Success Code | Error Codes |
|---|---|---|---|---|
| `GET` | `/health` | Health check probe | `200 OK` | `500` |
| `GET` | `/api/tasks` | List tasks (supports `?status=pending\|completed`) | `200 OK` | `400, 500` |
| `POST` | `/api/tasks` | Create a new task | `201 Created` | `400, 500` |
| `PUT` | `/api/tasks/{id}` | Update title, description, priority, due date, status | `200 OK` | `400, 404, 500` |
| `PATCH` | `/api/tasks/{id}/toggle` | Flip status between `pending` and `completed` | `200 OK` | `400, 404, 500` |
| `DELETE` | `/api/tasks/{id}` | Delete task | `200 OK` | `400, 404, 500` |

### Example Success Response:
```json
{
  "data": {
    "id": 1,
    "title": "Master Antigravity",
    "description": "Build high-quality software with clean architecture",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-11-01",
    "created_at": "2026-10-22T09:36:49.832300Z",
    "updated_at": "2026-10-22T09:36:49.832300Z"
  }
}
```

### Example 400 Validation Error Response:
```json
{
  "error": {
    "message": "Validation error",
    "details": [
      {
        "field": "title",
        "issue": "Value error, Title cannot be empty or only whitespace"
      }
    ]
  }
}
```

---

## Running Automated Tests

Run the backend test suite:
```bash
cd backend
pytest -v
```

**Coverage:**
- Request body and query parameter validation (empty strings, length limits, invalid formats).
- Status code adherence (200, 201, 400, 404).
- In-memory service logic unit tests (state toggle rules, not-found exceptions).
- Priority ordering verification.

---

## Database Schema

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    due_date DATE NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    CONSTRAINT check_task_status CHECK (status IN ('pending', 'completed')),
    CONSTRAINT check_task_priority CHECK (priority IN ('low', 'medium', 'high'))
);
```

---

## Design Decisions

1. **Overriding 422 to 400:** FastAPI returns HTTP 422 Unprocessable Entity by default for Pydantic validation failures. Modern HTTP standards designate 400 Bad Request for malformed payloads or invalid inputs. We implemented a custom exception handler in `app/core/handlers.py` to intercept `RequestValidationError` and return 400 with a clean list of `{field, issue}` objects.
2. **Zero Border-Radius Everywhere:** To achieve a brutalist, clean aesthetic, a global CSS reset (`*, *::before, *::after { border-radius: 0 !important; }`) guarantees zero rounded corners across native browser form controls, custom modals, buttons, and custom checkboxes.
3. **Repository Protocol:** Python's `typing.Protocol` allows structural subtyping. This allows testing all service logic with an in-memory `FakeTaskRepository` without spinning up a live test database or mocking SQLAlchemy internals.

---

## AI Assistance Disclosure

Google Antigravity was used as an agentic pair programmer to assist with scaffolding, typing, and implementation of this project following human-curated specifications and architecture design constraints. All code, design patterns, and database migrations were reviewed and verified.

---

## License

MIT
