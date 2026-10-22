# Task-Flow: Antigravity Implementation Guide

**Stack:** React (Vite) + FastAPI + PostgreSQL (local first, then Neon)
**Deploy:** Backend on Hugging Face Spaces (Docker), frontend on Vercel, database on Neon
**Design:** Dark mode, muted professional palette, zero border-radius
**Architecture:** SOLID, layered (routers, services, repositories, models)

---

## How to use this guide

1. Work through the phases **in order**. Each phase ends with a verification checklist and a commit.
2. Paste the prompt for the phase into Antigravity. Use **Planning mode**, read the plan and artifacts, and only then approve.
3. Give each agent **one phase only**. Do not ask it to build everything at once.
4. After each phase, **run and read the code yourself**. You must be able to explain every line in the follow-up interview.
5. Commit after each phase with a clear message. A readable git history is a quiet quality signal.
6. If an agent drifts from the rules (rounded corners, SQL in routers, 422 instead of 400), paste the relevant rule back and ask it to fix it.

### Phase overview

| Phase | Goal | Output |
|---|---|---|
| 0 | Repo and workspace rules | Skeleton, rules file, .gitignore |
| 1 | Local PostgreSQL | docker-compose, env files |
| 2 | Backend foundation | Config, DB session, errors, handlers |
| 3 | Backend task feature | Model, schemas, repo, service, routes, migration |
| 4 | Backend seed and tests | Seed script, pytest suite |
| 5 | Frontend foundation | Vite app, design tokens, API service |
| 6 | Frontend features | Hook and all components |
| 7 | Frontend polish | Responsive, states, accessibility, filter |
| 8 | Bonus features | Priority, due date, overdue highlight |
| 9 | Local end-to-end verification | Manual and curl test pass |
| 10 | Deployment | Neon, Hugging Face, Vercel |
| 11 | README and final audit | README, checklist, interview prep |
| 12 | Project overview document | `docs/PROJECT_OVERVIEW.md` explaining every module for your own understanding |

Do phase 8 only after phase 9's required-feature checks pass. The assignment states bonuses are only scored if required features are fully functional. If short on time, do the filter bar (phase 7) and skip the rest of phase 8.

---

## Phase 0: Repo and workspace rules

**Goal:** a clean skeleton and rules that every agent follows.

### Manual steps

1. Create the repo `task-flow` (or `taskflow-yourname`) and open it as the Antigravity workspace.
2. Create the folders `backend/`, `frontend/`.
3. Add the workspace rules file. The location depends on your Antigravity version (commonly `.agent/rules/`); check the Rules/Customizations panel if unsure. Use the content below.

### Workspace rules (paste into the rules file)

```
PROJECT: Task-Flow, a single-user task manager (React + FastAPI + PostgreSQL).

BACKEND
- FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, psycopg v3, pytest.
- Layers: routers -> services -> repositories -> models. Dependencies flow one way.
- Routers: HTTP only. No business logic, no ORM or SQL calls.
- Services: business rules. They depend on a repository Protocol, not on SQLAlchemy.
- Repositories: the only place that touches the database session.
- Inject dependencies with FastAPI Depends.
- Validation errors MUST return HTTP 400 (not FastAPI's default 422).
- Missing resources return 404. Unexpected errors return a generic 500 with no stack trace.
- Consistent JSON: success -> {"data": ...}; failure -> {"error": {"message": "...", "details": ...}}.
- Secrets and config only via environment variables (pydantic-settings). Never hardcode credentials.
- Use parameterized queries / ORM only. No string-built SQL.

FRONTEND
- React + Vite, plain JavaScript (or TypeScript if I say so), custom CSS only. No CSS frameworks.
- Structure: services/ (HTTP only), hooks/ (state and actions), components/ (render only).
- Every API call goes through services/taskApi.js.
- border-radius is ALWAYS 0 everywhere, including inputs, buttons, checkboxes and dialogs.
- Colors come only from CSS variables in styles/tokens.css. Dark mode, muted, professional palette.
- Mobile-first. Layout must work at 360px width. Touch targets are at least 44px.

GENERAL
- Apply SOLID. One responsibility per file. Prefer small focused modules.
- No dead code, no commented-out blocks, no console.log or print debugging left behind.
- Consistent naming and formatting. Meaningful names. Short docstrings/comments only where intent is not obvious.
- Never commit .env files. Keep .env.example files current.
- Before finishing a task, list the files you changed and how to verify the change.
```

### Antigravity prompt

```
Read the workspace rules. Create the project skeleton for "Task-Flow":

task-flow/
  backend/
  frontend/
  README.md  (placeholder with just the project title for now)
  .gitignore (Python, Node, .env, venv, __pycache__, node_modules, dist, .pytest_cache)

Do not write any application code yet. Output a short plan listing the folders you created, then stop.
```

### Verify and commit

- [ ] Rules file is in place and visible in Antigravity
- [ ] `.gitignore` includes `.env`
- [ ] Commit: `chore: initialize repo skeleton and workspace rules`

---

## Phase 1: Local PostgreSQL and environment files

**Goal:** a local database you can connect to, and documented env variables.

### Antigravity prompt

```
Set up local PostgreSQL for development.

1. Create docker-compose.yml at the repo root with a postgres:16-alpine service named "db":
   - POSTGRES_USER=taskflow, POSTGRES_PASSWORD=taskflow, POSTGRES_DB=taskflow
   - port 5432:5432, a named volume for data
   - a healthcheck using pg_isready
2. Add an init script (mounted into /docker-entrypoint-initdb.d) that also creates a second database "taskflow_test" for tests.
3. Create backend/.env.example with:
   DATABASE_URL=postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow
   TEST_DATABASE_URL=postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow_test
   CORS_ORIGINS=http://localhost:5173
   APP_ENV=development
4. Create frontend/.env.example with:
   VITE_API_URL=http://localhost:8000/api
5. Do not create real .env files. Tell me the exact commands to start the database and to confirm both databases exist.
```

### Manual steps

```
docker compose up -d
docker compose ps
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

If you use a native Postgres install instead of Docker, create the `taskflow` and `taskflow_test` databases by hand and adjust the connection strings.

### Verify and commit

- [ ] `docker compose ps` shows the db healthy
- [ ] Can connect: `docker compose exec db psql -U taskflow -d taskflow -c "\l"` lists both databases
- [ ] Commit: `chore: add local postgres via docker compose and env examples`

---

## Phase 2: Backend foundation

**Goal:** the app boots, reads config, connects to the DB, and has a consistent error system, with no task logic yet.

### Antigravity prompt

```
Build the backend foundation in backend/ following the workspace rules. No task feature yet.

Structure:
backend/
  app/
    main.py
    core/config.py
    core/errors.py
    core/handlers.py
    db/base.py
    db/session.py
    api/deps.py
    api/routes/health.py
  requirements.txt

Requirements:
- requirements.txt: fastapi, uvicorn[standard], sqlalchemy>=2, alembic, psycopg[binary], pydantic>=2, pydantic-settings, pytest, httpx. Pin sensible versions.
- core/config.py: a pydantic-settings Settings class reading DATABASE_URL, TEST_DATABASE_URL, CORS_ORIGINS (comma-separated, parsed into a list), APP_ENV from environment/.env. Expose a cached get_settings().
- db/base.py: SQLAlchemy 2.0 DeclarativeBase.
- db/session.py: engine and sessionmaker built from settings, and a get_db generator dependency that always closes the session and rolls back on error.
- core/errors.py: AppError base class (status_code, message, details), plus NotFoundError (404) and ValidationError (400).
- core/handlers.py: register exception handlers that return {"error": {"message": ..., "details": ...}}:
  * AppError -> its status code
  * fastapi RequestValidationError -> 400 (NOT 422), with readable details listing field and message
  * StarletteHTTPException -> its status code in the same JSON shape (so unknown routes return a JSON 404)
  * generic Exception -> 500 with message "Internal server error", log the real error server-side, never leak a stack trace
- main.py: an app factory create_app() that adds CORS middleware using CORS_ORIGINS, registers handlers, and includes the health router under no prefix. app = create_app().
- api/routes/health.py: GET /health returns {"data": {"status": "ok"}}.

Explain how each file maps to a SOLID principle in 1-2 lines each. Tell me how to run it: create venv, install, uvicorn command.
```

### Verify and commit

- [ ] `uvicorn app.main:app --reload` starts without errors
- [ ] `GET http://localhost:8000/health` returns `{"data":{"status":"ok"}}`
- [ ] `GET /nope` returns JSON 404 in the standard error shape
- [ ] `http://localhost:8000/docs` loads
- [ ] Commit: `feat(backend): app factory, config, db session, error handling`

---

## Phase 3: Backend task feature

**Goal:** all five required endpoints, layered with SOLID, backed by an Alembic migration.

### Antigravity prompt

```
Implement the tasks feature in the backend following the workspace rules and the existing foundation.

Add:
app/models/task.py
app/schemas/task.py
app/repositories/task_repository.py
app/services/task_service.py
app/api/routes/tasks.py
(update api/deps.py and main.py to wire everything)
alembic setup with a first migration

MODEL (table "tasks"):
- id: integer primary key, autoincrement
- title: String(255), not null
- description: Text, nullable
- status: String(20), not null, default 'pending', with a CHECK constraint (status IN ('pending','completed'))
- created_at: timezone-aware DateTime, server_default now(), not null
- updated_at: timezone-aware DateTime, server_default now(), onupdate now(), not null

SCHEMAS (Pydantic v2):
- TaskCreate: title (strip whitespace, min_length 1, max_length 255, whitespace-only must fail), description optional (strip; empty string becomes None)
- TaskUpdate: all fields optional (title, description, status: Literal['pending','completed']). If title is provided it follows the same rules as create. An update body with no fields should be rejected with a validation error.
- TaskRead: id, title, description, status, created_at, updated_at (from_attributes=True)
- Response envelopes: {"data": TaskRead} and {"data": [TaskRead]}

REPOSITORY:
- Define a TaskRepository Protocol with: list(status: str | None), get(task_id), create(data), update(task, data), delete(task).
- Implement SqlTaskRepository using a SQLAlchemy Session (SQLAlchemy 2.0 select() style). This is the only file that touches the session. Commit inside the repository methods.
- Order list results by created_at descending.

SERVICE:
- TaskService receives a TaskRepository via its constructor (dependency inversion).
- Methods: list_tasks(status), get_task(id) (raises NotFoundError), create_task, update_task (raises NotFoundError), toggle_task (flips pending <-> completed, raises NotFoundError), delete_task (raises NotFoundError).
- Invalid status filter value in list_tasks raises ValidationError (400).

ROUTES (prefix /api/tasks, HTTP only, no logic):
- GET /api/tasks?status=pending|completed -> 200
- POST /api/tasks -> 201
- PUT /api/tasks/{task_id} -> 200
- PATCH /api/tasks/{task_id}/toggle -> 200
- DELETE /api/tasks/{task_id} -> 200 with {"data": {"id": <id>}} (or 204, pick one and be consistent)
- task_id is an int path param; a non-integer must return 400 through the global handler.
- Use correct status codes: 200, 201, 400, 404, 500.

WIRING:
- api/deps.py: get_task_service(db = Depends(get_db)) builds TaskService(SqlTaskRepository(db)).

ALEMBIC:
- Initialize Alembic in backend/alembic, configure env.py to read DATABASE_URL from settings and use Base.metadata (import the models so autogenerate sees them).
- Generate the first migration "create tasks table" and make sure the CHECK constraint and server defaults are in it.

Finally give me: the commands to run the migration, and 6 curl commands that exercise happy paths and error paths (empty title, whitespace title, bad id format, missing id).
```

### Manual steps

```
cd backend
alembic upgrade head
uvicorn app.main:app --reload
```

### Verify and commit

- [ ] `alembic upgrade head` creates the `tasks` table (check with `psql`)
- [ ] POST valid task returns **201** with the `{ "data": ... }` shape
- [ ] POST empty title returns **400**, whitespace-only title returns **400**, 256-char title returns **400**
- [ ] `PUT /api/tasks/999` returns **404**, `PUT /api/tasks/abc` returns **400**
- [ ] PATCH toggle flips status and updates `updated_at`
- [ ] DELETE removes the row, second DELETE returns **404**
- [ ] Open the router file and confirm there is no business logic or ORM in it
- [ ] Commit: `feat(backend): task CRUD with layered architecture and migration`

---

## Phase 4: Seed script and backend tests

**Goal:** a reproducible seed and a test suite (counts as the unit-test bonus).

### Antigravity prompt

```
Add a seed script and tests to the backend.

SEED:
- scripts/seed.py (runnable as: python -m scripts.seed from backend/). It uses the existing session and repository layer to insert 4-5 realistic sample tasks (mix of pending and completed). It must be idempotent: skip seeding if the tasks table already has rows. Print a short summary.
- Note: sample data lives only in the seed script, never in application code.

TESTS (pytest, in backend/tests/):
- conftest.py:
  * A FakeTaskRepository (in-memory, implements the same Protocol) for fast unit tests.
  * A client fixture using fastapi TestClient with app.dependency_overrides[get_task_service] pointing to TaskService(FakeTaskRepository()).
- test_tasks_api.py covering:
  * POST valid -> 201 and envelope shape
  * POST empty title -> 400
  * POST whitespace-only title -> 400
  * POST title longer than 255 -> 400
  * GET list returns created tasks; ?status filter works; invalid ?status -> 400
  * PUT updates title; PUT unknown id -> 404; PUT with invalid status -> 400
  * PATCH toggle flips status twice; unknown id -> 404
  * DELETE -> success then 404 on repeat
  * non-integer id -> 400
- test_task_service.py: unit tests for toggle logic and NotFoundError using the fake repository directly (no HTTP).
- One optional integration test marked @pytest.mark.integration that runs the repository against TEST_DATABASE_URL (create tables, run a create/get/delete round trip, clean up).

Add a pytest.ini with the integration marker registered. Explain how this demonstrates the Liskov and Dependency Inversion principles.
```

### Manual steps

```
cd backend
python -m scripts.seed
pytest -q
```

### Verify and commit

- [ ] Seed runs twice without duplicating data
- [ ] `pytest -q` passes
- [ ] Commit: `test(backend): seed script, unit and service tests`

---

## Phase 5: Frontend foundation

**Goal:** Vite + React app with design tokens, base styles and a clean API service. No UI features yet.

### Antigravity prompt

```
Create the frontend in frontend/ with Vite + React (JavaScript). Follow the workspace rules. Foundation only: no task UI yet.

Structure:
frontend/src/
  services/taskApi.js
  hooks/            (empty for now)
  components/       (empty for now)
  styles/tokens.css
  styles/base.css
  App.jsx
  main.jsx

DESIGN TOKENS (styles/tokens.css) - dark, muted, professional, square:
:root {
  --bg: #121418;
  --surface: #1a1d23;
  --surface-2: #21252c;
  --border: #2e333c;
  --text: #d5d9e0;
  --text-muted: #8a909b;
  --accent: #5f7f9c;
  --accent-hover: #6f90ae;
  --success: #6b8f71;
  --warning: #b39363;
  --danger: #a65f5f;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-6: 24px; --space-8: 32px;
  --font: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
Also add a global rule: *, *::before, *::after { border-radius: 0 !important; box-sizing: border-box; }
Set color-scheme: dark.

BASE STYLES (styles/base.css): reset, body background/text from tokens, readable line-height, visible focus outlines using --accent, base styles for buttons, inputs and textareas (1px solid --border, background --surface-2, min-height 44px, no shadows, no gradients), a centered max-width container (720px) with padding that works from 360px up.

API SERVICE (services/taskApi.js):
- Base URL from import.meta.env.VITE_API_URL.
- Functions: getTasks(status), createTask({title, description}), updateTask(id, payload), toggleTask(id), deleteTask(id).
- A single private request() helper that: calls fetch with JSON headers, parses JSON safely, returns the unwrapped "data" on success, and on failure throws an ApiError carrying the server's error.message and details. Handle network failures with a friendly message ("Cannot reach the server").
- Components must never call fetch directly.

App.jsx: just render the app title "Task-Flow" in the container to prove styles load. Remove all Vite template boilerplate and unused assets. Add the .env.example entry if missing.
```

### Verify and commit

- [ ] `npm install && npm run dev` serves on port 5173
- [ ] Dark background, muted palette, no Vite template leftovers
- [ ] Inspect element: nothing has rounded corners
- [ ] Commit: `feat(frontend): vite scaffold, design tokens, api service`

---

## Phase 6: Frontend features

**Goal:** every required feature works in the UI.

### Antigravity prompt

```
Implement the task UI in frontend/src following the workspace rules. Components render only; state lives in a hook; HTTP lives in services/taskApi.js.

HOOK hooks/useTasks.js:
- State: tasks, isLoading, error (page-level), filter ('all' | 'pending' | 'completed').
- Actions: loadTasks, addTask, editTask, toggleTask, removeTask, setFilter.
- Each action calls the service, updates state, and sets a friendly error on failure. Rethrow errors from addTask and editTask so forms can show field-level messages.
- Load tasks on mount and when the filter changes (filtering is done server-side via ?status).

COMPONENTS (components/):
- TaskForm.jsx: title input (required) + optional description textarea + "Add task" button. Client-side validation: trim the title; if empty, show a visible error message under the field ("Title is required") and do not call the API. Also display server 400 messages. Clear the form after success. Disable the button while submitting.
- TaskList.jsx: renders a list of TaskItem, plus the empty state ("No tasks yet") and loading state.
- TaskItem.jsx: shows title, optional description, status label, and created date formatted for humans. Contains a square custom checkbox/toggle, an Edit button, and a Delete button. Visual distinction: pending = accent left border; completed = strikethrough title, muted text, success left border and a "Completed" label.
- TaskEditForm.jsx: inline edit mode inside the TaskItem (title + description, Save and Cancel). Same empty-title validation and error display.
- ConfirmDialog.jsx: a custom modal (not window.confirm) with title, message, Cancel and Delete buttons. Closes on Escape, traps focus reasonably, square corners, uses the danger color for the confirm action. Delete only happens after confirmation.
- ErrorMessage.jsx: a reusable inline error block using --danger with role="alert".

App.jsx composes: header, TaskForm, (FilterBar placeholder for phase 7), TaskList, and the page-level ErrorMessage.

Styles: put component styles in styles/components.css using only tokens. No rounded corners, no shadows, 1px borders.

When done, list the user flows I should click through to verify.
```

### Verify and commit

- [ ] Create a task with and without description
- [ ] Submit an empty title and see the error message, with no network call made (check the Network tab)
- [ ] Toggle a task, refresh the page, and the state persists
- [ ] Edit a task, then edit with an empty title and see the error
- [ ] Delete shows the confirmation dialog, Cancel keeps the task, Delete removes it
- [ ] Stop the backend and see the friendly "cannot reach server" message instead of a blank screen
- [ ] Commit: `feat(frontend): task list, form, edit, toggle, delete with confirmation`

---

## Phase 7: Frontend polish (responsive, states, filter)

**Goal:** professional finish and the filter bonus.

### Antigravity prompt

```
Polish the frontend.

1. FilterBar.jsx: three square buttons "All", "Pending", "Completed" showing the active one (use --accent background or a bottom border, not rounded pills). Wire it to useTasks.setFilter. Use aria-pressed. Show a filter-specific empty state ("No pending tasks").
2. Responsive: verify and fix the layout at 360px, 768px and 1280px. On mobile, task action buttons must stay reachable (stack or wrap) with at least 44px touch targets. No horizontal scrolling at 360px.
3. Accessibility: labels associated with inputs, visible focus states, aria-live for error messages, buttons have accessible names, the dialog has role="dialog" and aria-modal.
4. Custom square checkbox: hide the native checkbox visually but keep it accessible, and draw a square box with a checkmark using --success.
5. Task counts: show a small muted summary like "3 pending, 2 completed" derived from the current data (only when filter is 'all').
6. Clean up: remove unused CSS, unused imports, console statements and any commented-out code. Ensure formatting is consistent.

Do a final scan of all CSS for any border-radius other than 0 or any hard-coded hex colors outside tokens.css and report what you found and fixed.
```

### Verify and commit

- [ ] Browser devtools responsive mode at 360px looks clean
- [ ] Filter switches between All, Pending and Completed
- [ ] Tab key navigation works through the whole UI
- [ ] Commit: `feat(frontend): filter bar, responsive layout, accessibility polish`

---

## Phase 8: Bonus features (optional)

**Do this only after required features are rock solid.** Pick based on remaining time. Priority and due date require a backend migration.

### Antigravity prompt

```
Add two bonus features across backend and frontend. Keep the layering intact and do not break existing endpoints or tests.

BACKEND:
- Add columns to tasks via a NEW Alembic migration (do not edit the first one):
  * priority: String(10), not null, default 'medium', CHECK IN ('low','medium','high')
  * due_date: Date, nullable
- Update schemas: TaskCreate and TaskUpdate accept optional priority (Literal) and due_date (date); TaskRead returns both. Reject invalid priority with 400. 
- Repository list ordering: sort by priority (high first), then created_at descending. Implement this with a CASE expression in the repository, not in the router.
- Update tests for the new fields (valid, invalid priority, invalid date) and keep all existing tests passing.

FRONTEND:
- TaskForm and TaskEditForm: add a priority select (Low/Medium/High) and a due date input.
- TaskItem: show a priority label using muted colors (low = text-muted, medium = accent, high = warning) and the due date. If the task is pending and the due date is before today, mark it overdue with the --danger color and an "Overdue" label.
- Keep square corners and tokens-only colors.

Explain how the Open/Closed principle made this change small.
```

### Verify and commit

- [ ] Migration applies on top of existing data without errors
- [ ] Tasks sort high priority first
- [ ] Overdue pending tasks are highlighted; completed overdue tasks are not
- [ ] `pytest -q` still passes
- [ ] Commit: `feat: priority and due date with overdue highlighting`

---

## Phase 9: Local end-to-end verification

**Goal:** prove the whole app works before touching deployment.

### Antigravity prompt (audit agent)

```
Act as a strict reviewer grading this repo against this rubric (20 points each): Functionality, Code Quality & Organisation, API Design & HTTP Standards, Database Integration, README & Setup.

Do NOT change code yet. Review the backend and frontend and produce a report with:
1. Any place the layering is violated (logic in routers, ORM outside repositories, fetch outside services).
2. Any endpoint whose status codes or response shape are inconsistent with the rules.
3. Any validation gap (frontend or backend) for title: empty, whitespace, too long.
4. Any SQL injection risk, hardcoded credential, or committed secret.
5. Any dead code, commented-out code, unused imports, console/print debugging.
6. Any rounded corners or hard-coded colors in the CSS.
7. Any accessibility or responsive issue at 360px.
Rank findings by severity and propose fixes. Wait for my approval before editing.
```

Then approve and fix. Next, run the manual checklist.

### Manual curl checks

```
# create
curl -i -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -d '{"title":"Test","description":"hello"}'
# empty title -> 400
curl -i -X POST http://localhost:8000/api/tasks -H "Content-Type: application/json" -d '{"title":"   "}'
# bad id format -> 400
curl -i -X PATCH http://localhost:8000/api/tasks/abc/toggle
# missing id -> 404
curl -i -X DELETE http://localhost:8000/api/tasks/99999
# invalid filter -> 400
curl -i "http://localhost:8000/api/tasks?status=foo"
```

### Fresh-clone test

Clone the repo into a **new folder**, follow only your README (once written in phase 11), and confirm it runs. Repeat this after phase 11.

### Verify and commit

- [ ] All five endpoints return the correct codes and consistent JSON
- [ ] Every UI flow works end to end with the local database
- [ ] No console errors in the browser
- [ ] Commit: `fix: address audit findings`

---

## Phase 10: Deployment

**Order matters:** Neon, then Hugging Face, then Vercel, then update CORS.

### 10.1 Neon (database)

1. Create a Neon project and copy the connection string.
2. Convert it for SQLAlchemy and psycopg: replace the prefix with `postgresql+psycopg://` and make sure it ends with `?sslmode=require`.
3. Run the migration against Neon from your machine (do not save this URL in any file):

```
cd backend
DATABASE_URL="postgresql+psycopg://USER:PASS@HOST/DB?sslmode=require" alembic upgrade head
DATABASE_URL="postgresql+psycopg://USER:PASS@HOST/DB?sslmode=require" python -m scripts.seed
```

On Windows PowerShell, set the variable first with `$env:DATABASE_URL="..."` and then run the commands.

### 10.2 Hugging Face Spaces (backend)

**Antigravity prompt:**

```
Prepare the backend for deployment on a Hugging Face Docker Space.

1. Create backend/Dockerfile: python:3.12-slim, WORKDIR /app, copy requirements.txt and pip install --no-cache-dir, copy the rest, run as a non-root user, EXPOSE 7860, CMD uvicorn app.main:app --host 0.0.0.0 --port 7860.
2. Create backend/.dockerignore (venv, __pycache__, .env, tests caches, .git).
3. Create backend/SPACE_README.md containing the Hugging Face front matter:
   ---
   title: taskflow-api
   emoji: 📝
   sdk: docker
   app_port: 7860
   ---
   plus a one-line description. I will copy it as README.md into the Space repo.
4. Make sure the app reads DATABASE_URL and CORS_ORIGINS only from environment variables and that startup does not crash if CORS_ORIGINS contains multiple comma-separated origins.
5. Give me the exact steps to create the Space and push only the backend/ contents to it, keeping my main GitHub repo separate.
```

**Manual steps:**

1. Create a new Space at huggingface.co, SDK **Docker**, blank template.
2. In Space **Settings, Variables and secrets**, add secrets: `DATABASE_URL` (the Neon URL) and `CORS_ORIGINS` (set to your Vercel URL once known; use `http://localhost:5173` temporarily).
3. Push the backend to the Space repo. Options: add the Space as a git remote and `git subtree push --prefix backend hf main`, or copy the `backend/` contents plus the Space README into a separate folder and push that.
4. Wait for the build, then open `https://<user>-<space-name>.hf.space/health`.

Note: free Spaces sleep when idle, so the first request can take a while. Mention it in the README.

### 10.3 Vercel (frontend)

1. Import the GitHub repo in Vercel.
2. Set **Root Directory** to `frontend`. Framework preset: Vite.
3. Add environment variable `VITE_API_URL=https://<user>-<space-name>.hf.space/api`.
4. Deploy.
5. Copy the final Vercel URL, go back to the Space secrets, and set `CORS_ORIGINS` to it (comma-separated if you also want localhost). Restart the Space.

### Verify and commit

- [ ] `/health` works on the live HF URL
- [ ] Live frontend loads tasks from the live backend (no CORS errors in the console)
- [ ] Create, edit, toggle and delete work on the live site and persist after refresh
- [ ] No secrets in the repo (search the repo for `neon.tech` and `postgresql+psycopg://`)
- [ ] Commit: `chore: add dockerfile and deployment config`

---

## Phase 11: README and final audit

**Goal:** the README is worth 20 points. A reviewer should be running the app in under 10 minutes.

### Antigravity prompt

```
Write the root README.md for Task-Flow. A reviewer must be able to clone and run the app in under 10 minutes using only this file. Keep it accurate to the actual repo; verify every command and path against the files.

Sections:
1. Title, one-paragraph description, and Live Demo links (frontend on Vercel, backend API on Hugging Face Spaces, with a note that the free Space may take ~30-60s to wake up).
2. Features (required and bonus, marked clearly).
3. Tech stack: React + Vite, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, PostgreSQL (Neon in production), pytest, Docker; Vercel / Hugging Face Spaces / Neon for deployment.
4. Architecture: folder tree for backend and frontend, and a short "SOLID in this project" section mapping each principle to a concrete file or pattern.
5. Prerequisites: Python 3.12, Node 20+, Docker (or local PostgreSQL 16).
6. Local setup, step by step: clone, start database (docker compose up -d), backend venv + install + copy .env + alembic upgrade head + seed + run, frontend install + copy .env + run. Include Windows and macOS/Linux activation commands.
7. Environment variables: a table for backend and frontend (name, description, example).
8. API reference: table of the five endpoints (method, path, body, success code, error codes) plus /health, with one example request and response in the standard envelope, and the error shape.
9. Database schema table.
10. Running tests: commands and what is covered.
11. Deployment notes: Neon, Hugging Face Docker Space (port 7860, secrets), Vercel (root directory, VITE_API_URL), CORS.
12. Design decisions: dark muted theme, zero border-radius, validation returns 400 instead of FastAPI's default 422 (and why), repository Protocol for testability.
13. AI assistance disclosure: honest statement that Google Antigravity was used for scaffolding and implementation, and that I reviewed and can explain the code.
14. Known limitations and what I would do with more time (e.g. auth, pagination, optimistic UI updates, E2E tests with Playwright, CI pipeline).

Tone: clear and professional, no fluff. Use fenced code blocks for all commands.
```

### Final audit checklist

**Functionality**
- [ ] View, add, edit, toggle, delete all work, including after refresh
- [ ] Empty-title error is visible; server errors are surfaced
- [ ] Delete requires confirmation
- [ ] Filter works (bonus)

**API and HTTP**
- [ ] 200, 201, 400, 404, 500 all used correctly
- [ ] Validation errors return 400, not 422
- [ ] Every response follows `{ data }` or `{ error }`

**Database**
- [ ] Real PostgreSQL, migrations included, seed documented
- [ ] No string-built SQL, no hardcoded credentials

**Code quality**
- [ ] No dead code, commented-out blocks or debug logging
- [ ] Layering respected on both sides
- [ ] Consistent naming and formatting

**UI**
- [ ] Dark, muted palette via tokens only
- [ ] No rounded corners anywhere
- [ ] Usable at 360px with 44px touch targets
- [ ] Own custom CSS written (no CSS framework)

**Submission**
- [ ] Public GitHub repo with a clear name
- [ ] README at root, `.env.example` in backend and frontend, no `.env` committed
- [ ] Fresh-clone test passed from the README alone
- [ ] Live URLs added to the README
- [ ] Repo link sent to your contact before the deadline
- [ ] (Optional) 2 to 5 minute screen recording explaining one technical decision

### Interview preparation

Be ready to explain these without looking at the code:

1. Why the router, service, repository and model are separate, and what each one knows about.
2. How the dependency flows: `Depends` builds the service, which receives the repository, and how tests swap in a fake.
3. Why validation errors return 400 and how you overrode FastAPI's default.
4. How the toggle works and why it lives in the service.
5. How SQLAlchemy parameterization prevents SQL injection.
6. Why the frontend uses a hook plus a service layer instead of calling fetch in components.
7. How CORS is configured and why it differs between local and production.
8. What happens when the HF Space is asleep, and how the UI handles a slow or failed request.
9. One thing you would change with more time, and why.

---

## Phase 12: Project overview document (for your own understanding)

**Goal:** a single document, written by Antigravity from the **actual code**, that explains how the whole system works: backend, frontend and the "middleware" layer in between. This is your study guide for the follow-up technical interview, and it also shows reviewers you understand your own project.

Run this phase **last**, after the code, deployment and README are final, so the document describes what really exists rather than what was planned.

"Middleware" here means everything that sits between layers or wraps requests: CORS, exception handlers, validation handling, dependency injection (`Depends`, `get_db`), and on the frontend the API service and `request()` helper that sit between the UI and the server.

### Antigravity prompt

```
Read the entire repository carefully (backend, frontend, migrations, tests, Dockerfile, docker-compose, env examples, README). Then write docs/PROJECT_OVERVIEW.md, a learning-oriented walkthrough of how this project works, written for a junior developer who needs to deeply understand it and explain it in a technical interview.

STRICT ACCURACY RULES:
- Describe only what actually exists in the code. Do not invent files, functions or behavior. Before writing about a file, open it.
- Use real file paths and real function/class names. Quote short real code snippets (under 15 lines each) where they clarify the explanation.
- If something is a trade-off, shortcut or limitation, say so honestly.

TONE: clear, plain English, beginner-friendly, no fluff. Explain the "why" behind each decision, not only the "what". Define each technical term the first time it appears.

REQUIRED STRUCTURE:

1. Project at a glance
   - What Task-Flow does, the tech stack, and a Mermaid architecture diagram: Browser (React on Vercel) -> FastAPI (Hugging Face) -> PostgreSQL (Neon), plus the local-development equivalent.
   - A table of top-level folders and what each one is for.

2. The life of a request (end to end)
   - Walk through, step by step, what happens when a user clicks "Add task": the component event, the hook action, the service call, the HTTP request, CORS, routing, validation, dependency injection, service logic, repository, SQL, database, response envelope, and how the UI updates.
   - Provide a Mermaid sequence diagram for this flow.
   - Then repeat briefly for one failure path: submitting an empty title (show both the frontend check and what the backend would return as 400 if the frontend were bypassed).
   - Then repeat briefly for another: toggling or deleting a task that no longer exists (404 path).

3. Backend, module by module
   For EVERY file in backend/app and related folders, write a subsection with: Purpose; What it contains; What it depends on; What depends on it; How it connects to the next layer; Which SOLID principle it demonstrates (only if genuinely relevant).
   Cover at minimum: main.py (app factory), core/config.py, core/errors.py, core/handlers.py, db/base.py, db/session.py, models, schemas, the repository Protocol and its SQL implementation, the service, api/deps.py, routes, Alembic (env.py and the migrations), scripts/seed.py, and the tests (including the fake repository and dependency_overrides).
   Include a layered diagram showing which layer may call which (and which calls are forbidden).

4. The middleware and cross-cutting layer
   Explain how each of these works and where it is configured:
   - CORS middleware (and why local and production origins differ)
   - Exception handlers: AppError, RequestValidationError -> 400 (and why FastAPI defaults to 422), HTTP exceptions, the generic 500 handler
   - Dependency injection: Depends, get_db (open/commit/rollback/close lifecycle), get_task_service
   - The consistent response envelope ({ data } / { error }) and where it is enforced
   - Environment configuration via pydantic-settings
   - Frontend counterparts: the request() helper, ApiError, unwrapping of { data }, and the network-failure message
   Include a table: Concern | Where implemented | What it protects against.

5. Frontend, module by module
   For EVERY file in frontend/src, write a subsection with: Purpose; Props/inputs and outputs (for components); State it owns; Who calls it; What it calls.
   Cover: main.jsx, App.jsx, services/taskApi.js, hooks/useTasks.js, every component, and the CSS files (tokens.css, base.css, components.css), explaining the design-token approach and the zero-border-radius rule.
   Include a component tree diagram and a state-flow explanation (where state lives, how updates propagate, how loading/error/empty states are decided, how server-side filtering works).

6. Database
   - The tasks table column by column, with the reason for each type and constraint (CHECK constraint, timestamps with timezone, defaults, onupdate).
   - How migrations work, how to create a new one, and how the same migration runs against local Postgres and Neon.
   - Why parameterized queries / ORM prevent SQL injection, with a concrete example from this codebase.

7. Testing strategy
   - What is unit-tested vs integration-tested, how the fake repository replaces the real one, and what each test file proves. List what is NOT tested.

8. Deployment topology
   - Neon, Hugging Face Docker Space (port 7860, secrets), Vercel (root directory, build-time VITE_API_URL), CORS wiring between them, cold-start behavior of the free Space, and a table of every environment variable: where it is set (local / HF / Vercel) and what breaks if it is wrong.

9. SOLID in this project
   - One subsection per principle (S, O, L, I, D) pointing to concrete files and showing a short before/after or "what would change if we added X" example. Be honest where a principle is only partially applied.

10. How to extend it (worked examples)
   - Step-by-step, naming the exact files to touch and in which order, for: (a) adding a "tags" field, (b) adding pagination to GET /api/tasks, (c) adding user authentication at a high level.

11. Debugging guide
   - A table of symptoms -> likely layer -> where to look (e.g. 400 vs 422, CORS errors, 404 vs 500, stale UI after a mutation, "cannot reach server").

12. Interview Q&A
   - 15 likely technical interview questions about this project with concise model answers grounded in this codebase, plus 5 "what would you improve" answers.

13. Glossary
   - Short definitions of every technical term used (e.g. ORM, migration, dependency injection, CORS, envelope, Protocol, idempotent, cold start).

FORMAT: valid GitHub-flavored Markdown, a table of contents at the top with anchor links, Mermaid diagrams in fenced mermaid blocks, consistent heading levels. Aim for thorough but scannable: use tables and diagrams where they help.

After writing, do a verification pass: list every file path mentioned in the document and confirm it exists in the repo; fix any that do not. Report the result.
```

### Manual steps

1. Read the document top to bottom once, with the code open beside it. Wherever the explanation does not match your understanding, ask Antigravity a follow-up question about that section until it makes sense.
2. Test yourself: close the document and, for each backend and frontend file, say out loud what it does and what it calls.
3. Optionally link it from the README under a "Documentation" heading, so reviewers see you documented the architecture.
4. Mermaid diagrams render on GitHub. If you preview locally, use an editor with Mermaid support.

### Verify and commit

- [ ] `docs/PROJECT_OVERVIEW.md` exists and has a working table of contents
- [ ] Every file path mentioned actually exists (the agent's verification pass reported clean)
- [ ] The request-lifecycle section matches what you see in the browser's Network tab
- [ ] You can explain each module without reading the document
- [ ] Commit: `docs: add project overview and architecture walkthrough`

---

## Troubleshooting quick reference

| Symptom | Likely cause | Fix |
|---|---|---|
| Validation returns 422 | Default FastAPI handler still active | Check `core/handlers.py` registers `RequestValidationError` and is called in `create_app()` |
| `alembic` cannot connect | Wrong `DATABASE_URL` or db not running | `docker compose ps`; check `.env` |
| Neon connection error | Missing SSL | Append `?sslmode=require` |
| CORS error in browser | Origin not in `CORS_ORIGINS` | Add exact origin (no trailing slash), restart the service |
| Vercel app calls localhost | `VITE_API_URL` missing at build time | Set it in Vercel env vars and redeploy (Vite bakes it in at build) |
| HF Space stuck on building or unhealthy | Wrong port | Dockerfile and front matter must both use 7860 |
| First live request is slow or times out | Free Space was asleep | Wait and retry; document in README |
| Round corners appear | Default browser control styling | Use `appearance: none` and rely on the global `border-radius: 0 !important` rule |