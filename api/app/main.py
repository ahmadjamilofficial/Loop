"""
Loop API — stateless Vercel entry point.

This server validates requests and returns structured acks with generated IDs.
It stores absolutely nothing. All interaction and feedback data is written to
the user's local machine by the Loop SDK (~/.loop/).

Vercel reads this file via vercel.json and serves it as a serverless function.
"""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import config
from app.middleware import RequestIdMiddleware
from app.routers import export, feedback, health, interactions, stats


app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.API_VERSION,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-Id"],
)

# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    rid = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=422,
        content={"error": {"type": "validation_error", "message": str(exc.errors()), "request_id": rid}},
        headers={"X-Request-Id": rid},
    )

@app.exception_handler(Exception)
async def server_error(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=500,
        content={"error": {"type": "server_error", "message": "An unexpected error occurred.", "request_id": rid}},
        headers={"X-Request-Id": rid},
    )

# ---------------------------------------------------------------------------
# Routes — all under /v1
# ---------------------------------------------------------------------------

V1 = "/v1"
app.include_router(health.router,       prefix=V1)
app.include_router(interactions.router, prefix=V1)
app.include_router(feedback.router,     prefix=V1)
app.include_router(export.router,       prefix=V1)
app.include_router(stats.router,        prefix=V1)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "api": "Loop",
        "version": config.API_VERSION,
        "docs": "/docs",
        "note": "This server is stateless. All data is stored locally by the SDK.",
    }
