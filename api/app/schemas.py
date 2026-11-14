"""
Pydantic v2 request/response schemas.

The server is stateless — it validates these shapes and returns
structured responses with generated IDs. The SDK writes the
actual data to ~/.loop/ on the user's machine.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field
import uuid


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    type: str
    message: str
    request_id: str

class ErrorResponse(BaseModel):
    error: ErrorDetail


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str = "ok"
    version: str


# ---------------------------------------------------------------------------
# Interactions
# ---------------------------------------------------------------------------

ChatMessage = Dict[str, str]  # {"role": "user", "content": "..."}

class InteractionCreate(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="Client-generated ID. If omitted the server generates a UUID."
    )
    prompt: Union[str, List[ChatMessage]] = Field(
        ...,
        description="Plain string or list of {role, content} chat messages."
    )
    response: str
    model: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class InteractionAck(BaseModel):
    id: str = Field(..., description="Use this ID in subsequent feedback() calls.")
    timestamp: datetime
    stored: bool = Field(
        False,
        description=(
            "Always false — the server is stateless. "
            "The SDK stores this interaction locally."
        )
    )

class InteractionBatchCreate(BaseModel):
    interactions: List[InteractionCreate] = Field(..., min_length=1, max_length=100)

class InteractionBatchAck(BaseModel):
    ids: List[str]
    count: int
    stored: bool = False


# ---------------------------------------------------------------------------
# Feedback
# ---------------------------------------------------------------------------

class FeedbackCreate(BaseModel):
    interaction_id: str = Field(..., description="ID returned by log().")
    rating: Literal["up", "down"] = Field(
        ...,
        description="'up' = good response, 'down' = bad response."
    )
    correction: Optional[str] = Field(
        None,
        description="The correct answer, if the model was wrong. Used as the 'chosen' response in DPO training."
    )
    comment: Optional[str] = None
    user_id: Optional[str] = None

class FeedbackAck(BaseModel):
    id: str
    interaction_id: str
    rating: str
    has_correction: bool
    stored: bool = Field(
        False,
        description="Always false — the SDK stores feedback locally."
    )


# ---------------------------------------------------------------------------
# Export (SDK reads local storage, but can also request a schema)
# ---------------------------------------------------------------------------

class ExportFormat(BaseModel):
    format: Literal["chat_jsonl", "alpaca_jsonl", "dpo_jsonl"]
    description: str
    schema_example: Dict[str, Any]

class ExportFormatsResponse(BaseModel):
    formats: List[ExportFormat]


# ---------------------------------------------------------------------------
# Stats (SDK computes from local storage and can POST a summary)
# ---------------------------------------------------------------------------

class StatsSummary(BaseModel):
    total_interactions: int
    total_feedback: int
    thumbs_up: int
    thumbs_down: int
    with_correction: int
    without_correction: int
    models: List[str] = []
