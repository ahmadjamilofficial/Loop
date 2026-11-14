from fastapi import APIRouter
from app.schemas import HealthResponse
from app import config

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns API status and version. No authentication required.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=config.API_VERSION)
