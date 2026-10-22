from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint returning standardized response envelope."""
    return {"data": {"status": "ok"}}
