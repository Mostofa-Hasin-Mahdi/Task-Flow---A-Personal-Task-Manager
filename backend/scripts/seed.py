"""Database seed script for Task-Flow.

Can be run via: python -m scripts.seed (from backend/ directory).
Inserts realistic sample tasks idempotently using the repository layer.
"""

from app.db.session import SessionLocal
from app.repositories.task_repository import SqlTaskRepository
from app.schemas.task import TaskCreate

SAMPLE_TASKS = [
    {
        "title": "Set up project architecture and workspace rules",
        "description": "Establish SOLID layered architecture and enforce zero border-radius constraint.",
        "status": "completed",
    },
    {
        "title": "Configure PostgreSQL database and migrations",
        "description": "Initialize Alembic and configure connection pooling for Neon PostgreSQL.",
        "status": "completed",
    },
    {
        "title": "Build frontend task management UI with custom CSS",
        "description": "Implement responsive dark-mode interface with accessible square controls.",
        "status": "pending",
    },
    {
        "title": "Integrate client API service and error toast alerts",
        "description": "Connect Vite frontend to FastAPI backend using consistent JSON envelopes.",
        "status": "pending",
    },
    {
        "title": "Deploy to Hugging Face Spaces and Vercel",
        "description": "Containerize backend with Dockerfile and configure production CORS policies.",
        "status": "pending",
    },
]


def seed_database() -> None:
    """Idempotently seed the tasks table if no tasks currently exist."""
    db = SessionLocal()
    try:
        repo = SqlTaskRepository(db=db)
        existing_tasks = repo.list()
        if existing_tasks:
            print(f"Database already contains {len(existing_tasks)} tasks. Skipping seed.")
            return

        print("Seeding database with initial sample tasks...")
        for item in SAMPLE_TASKS:
            task = repo.create(
                data=TaskCreate(
                    title=item["title"],
                    description=item["description"],
                )
            )
            # If the sample item specifies completed, toggle/set status
            if item["status"] == "completed":
                task.status = "completed"
                db.commit()
            print(f"  + Added: [{task.status.upper()}] {task.title}")

        print(f"Successfully seeded {len(SAMPLE_TASKS)} tasks into the database.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
