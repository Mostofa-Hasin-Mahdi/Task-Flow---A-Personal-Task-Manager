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
