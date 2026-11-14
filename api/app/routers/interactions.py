"""
Interaction endpoints — stateless.

The server validates the request shape and returns a confirmed ID.
The SDK is responsible for writing the interaction to local storage
at ~/.loop/interactions.jsonl before or after calling this endpoint.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Request, status
from app.schemas import (
    InteractionAck,
    InteractionBatchAck,
    InteractionBatchCreate,
    InteractionCreate,
)

router = APIRouter(tags=["Interactions"])


@router.post(
    "/interactions",
    response_model=InteractionAck,
    status_code=status.HTTP_201_CREATED,
    summary="Log an interaction",
    description=(
        "Validates a prompt/response pair and returns a confirmed ID. "
        "The server stores nothing — the SDK writes this to ~/.loop/interactions.jsonl."
    ),
)
def log_interaction(body: InteractionCreate, request: Request) -> InteractionAck:
    interaction_id = body.id or str(uuid.uuid4())
    ts = body.timestamp or datetime.now(timezone.utc)
    return InteractionAck(id=interaction_id, timestamp=ts, stored=False)


@router.post(
    "/interactions/batch",
    response_model=InteractionBatchAck,
    status_code=status.HTTP_201_CREATED,
    summary="Log a batch of interactions",
    description="Validates up to 100 interactions and returns their confirmed IDs.",
)
def log_interactions_batch(body: InteractionBatchCreate, request: Request) -> InteractionBatchAck:
    ids = [item.id or str(uuid.uuid4()) for item in body.interactions]
    return InteractionBatchAck(ids=ids, count=len(ids), stored=False)
