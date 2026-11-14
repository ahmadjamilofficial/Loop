"""
Stats endpoint — stateless echo.

The SDK computes stats from local storage and can POST them here
to get a validated summary back. Useful for the `loop stats` CLI command.
"""
from __future__ import annotations

from fastapi import APIRouter
from app.schemas import StatsSummary

router = APIRouter(tags=["Stats"])


@router.post(
    "/stats",
    response_model=StatsSummary,
    summary="Validate and echo a stats summary",
    description=(
        "The SDK computes this from local storage and POSTs it here for validation. "
        "The server echoes it back. Nothing is stored."
    ),
)
def echo_stats(body: StatsSummary) -> StatsSummary:
    return body
