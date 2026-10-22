import logging
from typing import Any
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.errors import AppError

logger = logging.getLogger("taskflow")


def error_response(status_code: int, message: str, details: Any = None) -> JSONResponse:
    """Standardized JSON error envelope: {"error": {"message": ..., "details": ...}}"""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "details": details,
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Registers global exception handlers to enforce uniform JSON error shapes and status codes."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        # Override FastAPI's default 422 to return HTTP 400 as required by project specification
        formatted_details = []
        for err in exc.errors():
            loc = " -> ".join(str(item) for item in err.get("loc", []) if item != "body")
            msg = err.get("msg", "Invalid input")
            formatted_details.append({"field": loc or "body", "issue": msg})

        return error_response(
            status_code=400,
            message="Validation error",
            details=formatted_details,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return error_response(
            status_code=exc.status_code,
            message=str(exc.detail),
            details=None,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        # Log the actual stack trace server-side without leaking implementation details to client
        logger.exception("Unhandled server exception: %s", exc)
        return error_response(
            status_code=500,
            message="Internal server error",
            details=None,
        )
