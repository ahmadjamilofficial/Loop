"""
Feedback endpoints — stateless.

Validates the feedback payload and returns an ack with a generated ID.
The SDK writes the feedback record to ~/.loop/feedback.jsonl locally.

This is where the user's like/dislike and optional correction are
accepted and confirmed. The SDK captures this — typically by showing
the user a prompt in the terminal or a widget in the app.
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Request, status
from app.schemas import FeedbackAck, FeedbackCreate

router = APIRouter(tags=["Feedback"])


@router.post(
    "/feedback",
    response_model=FeedbackAck,
    status_code=status.HTTP_201_CREATED,
    summary="Submit feedback",
    description=(
        "Records a user's reaction to a model response. "
        "rating must be 'up' (good) or 'down' (bad). "
        "If the model was wrong, pass the correct answer in correction — "
        "it becomes the target response in fine-tuning. "
        "The server validates and acks; the SDK writes to ~/.loop/feedback.jsonl."
    ),
)
def submit_feedback(body: FeedbackCreate, request: Request) -> FeedbackAck:
    return FeedbackAck(
        id=str(uuid.uuid4()),
        interaction_id=body.interaction_id,
        rating=body.rating,
        has_correction=body.correction is not None,
        stored=False,
    )
