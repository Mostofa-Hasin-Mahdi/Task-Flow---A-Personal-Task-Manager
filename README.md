# Task-Flow

A focused, accessible personal task manager with a dark-mode square design system, built with **React (Vite)**, **FastAPI**, and **PostgreSQL (Neon)**. Designed following strict **SOLID** principles, layered clean architecture, and unified HTTP response envelopes.

---

## Live Demos

- **Frontend (Vercel):** [https://task-flow-a-personal-task-manager.vercel.app](https://task-flow-a-personal-task-manager.vercel.app)
- **Backend API (Render):** [https://taskflow-api-cyld.onrender.com](https://taskflow-api-cyld.onrender.com)
- **Interactive API Docs (Swagger):** [https://taskflow-api-cyld.onrender.com/docs](https://taskflow-api-cyld.onrender.com/docs)
- **API Health Check:** [https://taskflow-api-cyld.onrender.com/health](https://taskflow-api-cyld.onrender.com/health)

> **Note on Free Hosting:** Render's free tier spins down web services after periods of inactivity. If the app has been idle, the initial request might take 30–50 seconds to wake up. Subsequent requests respond instantly.

---

## Features

### Required Core Features
- [x] **Task Creation:** Add tasks with title (1–255 characters) and optional description.
- [x] **Client & Server Validation:** Whitespace trimming, empty title prevention, title length enforcement, with field-level error messages (returns HTTP 400, overriding FastAPI's default 422).
- [x] **Status Toggling:** Switch task state between `pending` and `completed` with persistent timestamp updates.
- [x] **Inline Editing:** Edit title, description, priority, and due date directly within the task item.
- [x] **Safe Deletion:** Accessible custom modal confirmation with Escape key handling and focus management before irreversible deletion.
- [x] **Network Resilience:** Friendly error notices when the backend service is offline.
- [x] **Strict Square Design:** Zero border-radius (`border-radius: 0 !important`) across all elements, inputs, buttons, checkboxes, and dialogs.

### Bonus Features Implemented
- [x] **Priority Levels:** Assign `Low`, `Medium`, or `High` priority to tasks.
- [x] **Server-Side Priority Ordering:** High priority tasks appear at the top, ordered via an SQL `CASE` expression in the repository layer.
- [x] **Due Dates & Overdue Highlighting:** Set due dates. Pending tasks past their due date display a danger-highlighted **"Overdue"** badge and red border indicator.
- [x] **Server-Side Filter Bar:** Filter tasks by `All`, `Pending`, or `Completed` via query parameter (`?status=`), accompanied by live task count badges (`X pending • Y completed`).
- [x] **Automated Test Suite & CI:** 21 offline unit/API tests (running in < 0.35s) plus 4 database integration tests with a GitHub Actions CI pipeline running on every push.

---

## Tech Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | React 19, Vite | Custom Vanilla CSS (no CSS frameworks), Design Tokens, mobile-first |
| **Backend** | FastAPI, Python 3.12 | Layered architecture, Pydantic v2, Pydantic-Settings |
| **Database** | PostgreSQL 16+ (Neon) | SQLAlchemy 2.0 ORM, psycopg v3 driver, connection pooling |
| **Migrations** | Alembic | Version-controlled schema migrations with SQL CHECK constraints |
| **Testing** | Pytest, TestClient | 21 unit + 4 integration tests; in-memory repository fakes (DIP/LSP) |
| **CI / CD** | GitHub Actions | Automated workflow running pytest suite and frontend Vite build on push |
| **Deployment** | Vercel & Render | Vercel for SPA frontend, Render for FastAPI backend, Neon for Serverless Postgres |

---

## Architecture & Project Structure

```
task-flow/
├── backend/
│   ├── alembic/              # Database migration environments and version scripts
│   ├── app/
│   │   ├── api/              # HTTP routers (tasks.py, health.py) and deps.py wiring
│   │   ├── core/             # Settings (pydantic-settings), errors, and exception handlers
│   │   ├── db/               # DeclarativeBase and get_db session generator
│   │   ├── models/           # SQLAlchemy 2.0 ORM Task model with CHECK constraints
│   │   ├── repositories/     # TaskRepository Protocol and SqlTaskRepository
│   │   ├── schemas/          # Pydantic v2 request schemas and data envelopes
│   │   ├── services/         # TaskService business domain logic
│   │   └── main.py           # Application factory (create_app), CORS, and router assembly
│   ├── scripts/              # Idempotent seed script (seed.py)
│   ├── tests/                # Unit, service, API route, and integration tests
│   ├── Dockerfile            # Container definition for containerized deployments
│   ├── requirements.txt      # Pinned backend dependencies
│   └── pytest.ini            # Pytest configuration and test marker registration
├── frontend/
│   ├── src/
│   │   ├── components/       # Presentational UI components (TaskForm, TaskList, TaskItem, etc.)
│   │   ├── hooks/            # useTasks.js state management hook
│   │   ├── services/         # taskApi.js HTTP client service (sole place with fetch)
│   │   ├── styles/           # tokens.css (CSS variables), base.css, components.css
│   │   ├── App.jsx           # Main container layout
│   │   └── main.jsx          # React 19 bootstrap entrypoint
│   └── package.json          # Vite and React dependencies
├── docker-compose.yml        # Local PostgreSQL 16 service definition
├── render.yaml               # Render Blueprint deployment definition
└── .github/workflows/ci.yml  # GitHub Actions CI pipeline
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
- **Docker** (optional, for local PostgreSQL) or a cloud PostgreSQL database (e.g. Neon)

---

## Local Setup (Run in under 10 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/Mostofa-Hasin-Mahdi/Task-Flow---A-Personal-Task-Manager.git
cd Task-Flow---A-Personal-Task-Manager
```

### 2. Start Database
**Option A: Using Docker Compose (Recommended for local dev)**
```bash
docker compose up -d
```
*This starts a local PostgreSQL 16 instance on port 5432 and initializes both `taskflow` and `taskflow_test` databases.*

**Option B: Using Neon (Cloud PostgreSQL)**
Use your Neon connection string in `backend/.env` with `postgresql+psycopg://` and `?sslmode=require`.

### 3. Backend Setup
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
# If using Docker Compose: DATABASE_URL=postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow
# If using Neon: use your Neon connection string

# Run migrations to apply database tables and constraints
alembic upgrade head

# Seed initial sample tasks (Idempotent: skips if rows already exist)
python -m scripts.seed

# Run backend development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Frontend Setup
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
    "title": "Master Clean Architecture",
    "description": "Adhere to SOLID principles and clean layering",
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

The test suite is divided into fast unit/API tests (offline, in-memory) and PostgreSQL integration tests:

### 1. Fast Unit & API Route Tests (Default - Offline)
```bash
cd backend
pytest -v
```
- **Execution:** Runs **21 tests in under 0.35 seconds** without needing a database connection.
- **Coverage:** Input validations (empty strings, whitespace-only, 255+ char bounds), route status codes (200, 201, 400, 404), PUT/PATCH edge cases (missing IDs, invalid status values, empty bodies), service toggle rules, and priority ordering logic using an in-memory `FakeTaskRepository`.

### 2. Database Integration Tests (Against Live PostgreSQL)
```bash
cd backend
pytest -m integration -v
```
*(Requires `TEST_DATABASE_URL` in environment or `.env`)*
- **Coverage:** Tests `SqlTaskRepository` directly, executes Alembic migrations programmatically on the test database, verifies the SQL `CASE` priority ordering directly in PostgreSQL, and verifies that PostgreSQL engine `CHECK` constraints (`check_task_status`, `check_task_priority`) reject invalid data with `IntegrityError`.

---

## Deployment Setup

The live application is hosted across three specialized cloud tiers:

1. **Database (Neon Serverless PostgreSQL):**
   - Cloud PostgreSQL 16 instance with SSL enforcement (`?sslmode=require`).
   - Tables and constraints managed via Alembic migrations.
2. **Backend (Render Web Service):**
   - **Runtime:** Python 3.12
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** `DATABASE_URL`, `CORS_ORIGINS` (including the Vercel production URL), `APP_ENV=production`.
3. **Frontend (Vercel):**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `vite build`
   - **Environment Variable:** `VITE_API_URL=https://taskflow-api-cyld.onrender.com/api`

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

## Known Limitations & Future Roadmap

1. **Single-User Scope (No Auth):** The current system is designed as a single-user task manager. A natural next step is adding multi-tenancy with JWT authentication (`OAuth2PasswordBearer` + refresh tokens) and a `user_id` foreign key on tasks.
2. **Optimistic UI Updates:** State toggling is currently pessimistic (the UI waits for the cloud database round-trip before updating the checkbox). Implementing optimistic updates with rollback would make toggling feel instantaneous on high-latency networks.
3. **Pagination & Search:** `GET /api/tasks` currently fetches all tasks matching the filter. Adding `limit`/`offset` query parameters and full-text search will support scaling to thousands of tasks.
4. **End-to-End Browser Tests:** While backend unit, API, and DB integration tests are automated with CI, adding Playwright tests would verify browser clicks and modal interactions end-to-end.

---

## AI Assistance Disclosure

Google Antigravity was used as an agentic pair programmer to assist with scaffolding, typing, and implementation of this project following human-curated specifications and architecture design constraints. All code, design patterns, and database migrations were reviewed and verified.

---

## License

[MIT](LICENSE)
