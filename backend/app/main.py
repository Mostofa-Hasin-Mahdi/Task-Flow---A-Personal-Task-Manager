from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.handlers import register_exception_handlers


def create_app() -> FastAPI:
    """Application factory that configures CORS, exception handlers, and API routes."""
    settings = get_settings()

    app = FastAPI(
        title="Task-Flow API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url=None,
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register custom and global error handlers
    register_exception_handlers(app)

    # Register routers
    app.include_router(health_router)

    return app


app = create_app()
