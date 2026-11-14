"""
Export schema endpoint — stateless.

The server does not store data, so it cannot stream files.
Instead it describes the export formats so the SDK knows exactly
what schema to write when it exports from local storage.

The SDK's `loop export` command reads ~/.loop/feedback.jsonl and
writes the requested format to the current directory.
"""
from __future__ import annotations

from fastapi import APIRouter
from app.schemas import ExportFormat, ExportFormatsResponse

router = APIRouter(tags=["Export"])


@router.get(
    "/export/formats",
    response_model=ExportFormatsResponse,
    summary="List export formats",
    description=(
        "Returns the schemas for each supported fine-tuning export format. "
        "The SDK uses these to write local JSONL files — no data is sent to the server."
    ),
)
def export_formats() -> ExportFormatsResponse:
    return ExportFormatsResponse(
        formats=[
            ExportFormat(
                format="chat_jsonl",
                description=(
                    "OpenAI chat format. Compatible with OpenAI fine-tuning, "
                    "LLaMA-Factory, Axolotl, and most modern trainers."
                ),
                schema_example={
                    "messages": [
                        {"role": "user", "content": "<prompt>"},
                        {"role": "assistant", "content": "<response>"},
                    ]
                },
            ),
            ExportFormat(
                format="alpaca_jsonl",
                description=(
                    "Alpaca instruction format. Compatible with Alpaca, "
                    "LLaMA-Factory, and similar fine-tuning frameworks."
                ),
                schema_example={
                    "instruction": "<prompt>",
                    "input": "",
                    "output": "<response>",
                },
            ),
            ExportFormat(
                format="dpo_jsonl",
                description=(
                    "DPO preference format. Only feedback records that have a correction are included. "
                    "chosen = correction, rejected = original model response. "
                    "Compatible with TRL, Axolotl, and Unsloth DPO trainers."
                ),
                schema_example={
                    "prompt": "<prompt>",
                    "chosen": "<correction>",
                    "rejected": "<original_response>",
                },
            ),
        ]
    )
