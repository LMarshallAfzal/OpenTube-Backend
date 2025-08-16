from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/ping")
def ping() -> dict:
    """Simple liveness probe"""
    return {"status": "ok"}
