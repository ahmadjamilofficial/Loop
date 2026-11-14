# Loop

Loop is a free RLHF (Reinforcement Learning from Human Feedback) tool for AI builders. Install the SDK, log your model's interactions, collect user feedback (thumbs up, thumbs down, corrections), and export clean fine-tuning datasets. Everything stays on your machine — no cloud storage, no accounts, no cost.

Production API: `https://loop-systematic-architecture-api-index.vercel.app`

---

## Table of contents

- [How it works](#how-it-works)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [SDK reference](#sdk-reference)
- [Local storage](#local-storage)
- [Export formats](#export-formats)
- [API reference](#api-reference)
- [Deploying the API](#deploying-the-api)
- [Repository layout](#repository-layout)
- [Environment variables](#environment-variables)

---

## How it works

```
Your app
  |
  v
loopsdk                          (runs on your machine)
  |-- logs interaction           writes to ~/.loop/interactions.jsonl
  |-- collects feedback          writes to ~/.loop/feedback.jsonl
  |-- exports training data      reads local files, writes train.jsonl
  |
  v
Loop API                         (stateless, hosted on Vercel)
  |-- validates request shape
  |-- returns confirmed ID
  |-- stores nothing
```

The API is a stateless validator. It confirms that your requests are well-formed and returns structured IDs. All data is written locally by the SDK.

---

## Installation

```bash
pip install loopsdk
```

Requires Python 3.10 or later.

---

## Quickstart

```python
from loop import Loop

client = Loop()

# 1. Log an interaction — your model's prompt and response
res = client.interactions.log_interaction(
    prompt="What is the capital of Pakistan?",
    response="Islamabad",
    model="my-model-v1",
)

interaction_id = res.result.id
print(f"Logged: {interaction_id}")

# 2. Submit feedback — thumbs up
client.feedback.submit_feedback(
    interaction_id=interaction_id,
    rating="up",
)

# 3. Submit feedback — thumbs down with a correction
client.feedback.submit_feedback(
    interaction_id=interaction_id,
    rating="down",
    correction="The capital of Pakistan is Islamabad.",
    comment="Response was missing context.",
)
```

---

## SDK reference

### `Loop()`

Instantiates the client. No arguments required — the base URL defaults to the production API.

```python
from loop import Loop

client = Loop()
```

Optional parameters:

| Parameter | Type | Description |
|---|---|---|
| `server_url` | string | Override the base URL. Use `http://localhost:8000` for local development. |
| `timeout_ms` | integer | Request timeout in milliseconds. Default: 30000. |

---

### `client.interactions.log_interaction()`

Logs a single prompt/response pair. The server validates and returns a confirmed ID. The SDK writes the record locally.

```python
res = client.interactions.log_interaction(
    prompt="What is the capital of Pakistan?",   # str or list of chat messages
    response="Islamabad",
    model="my-model-v1",                          # optional
    metadata={"user_tier": "free"},               # optional
    session_id="sess_abc123",                     # optional
)

interaction_id = res.result.id
```

**prompt** accepts either a plain string or a list of chat messages:

```python
# Plain string
prompt="What is the capital of Pakistan?"

# Chat messages
prompt=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of Pakistan?"},
]
```

Returns a `LogInteractionResponse` with:
- `result.id` — the interaction ID, use this in `submit_feedback()`
- `result.timestamp` — confirmed timestamp
- `result.stored` — always `False` (server stores nothing)

---

### `client.interactions.log_interactions_batch()`

Logs up to 100 interactions in one call.

```python
res = client.interactions.log_interactions_batch(
    interactions=[
        {"prompt": "Q1", "response": "A1", "model": "v1"},
        {"prompt": "Q2", "response": "A2", "model": "v1"},
    ]
)

ids = res.result.ids   # list of confirmed IDs in order
```

---

### `client.feedback.submit_feedback()`

Submits a user reaction to a logged interaction.

```python
# Thumbs up — the response was good
client.feedback.submit_feedback(
    interaction_id="int_abc123",
    rating="up",
)

# Thumbs down with correction — the model was wrong
client.feedback.submit_feedback(
    interaction_id="int_abc123",
    rating="down",
    correction="The correct answer is X.",
    comment="Optional free-text note.",
    user_id="user_456",   # anonymised, optional
)
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `interaction_id` | string | Yes | ID from `log_interaction()`. |
| `rating` | `"up"` or `"down"` | Yes | `"up"` = good response. `"down"` = bad response. |
| `correction` | string | No | The correct answer. Used as the training target. |
| `comment` | string | No | Free-text note. Stored locally, not used in training. |
| `user_id` | string | No | Anonymised user ID. Do not use real names or emails. |

How corrections map to training formats:

| Scenario | Training use |
|---|---|
| `rating="up"`, no correction | Positive SFT example |
| `rating="down"` + correction | DPO pair: `chosen=correction`, `rejected=original_response`. Also a gold SFT example. |
| `rating="down"`, no correction | Counted in stats, not used for training |

---

### `client.health.health()`

Checks connectivity to the API.

```python
res = client.health.health()
print(res.result.status)   # "ok"
print(res.result.version)  # "0.1.0"
```

---

### `client.export.export_formats()`

Returns the schemas for the three supported fine-tuning export formats.

```python
res = client.export.export_formats()
for fmt in res.result.formats:
    print(fmt.format, fmt.description)
```

---

### `client.stats.echo_stats()`

Submits a stats summary computed from local storage. The server validates and echoes it back.

```python
from loop.models import StatsSummary

res = client.stats.echo_stats(
    total_interactions=142,
    total_feedback=98,
    thumbs_up=71,
    thumbs_down=27,
    with_correction=19,
    without_correction=8,
    models=["my-model-v1"],
)
```

---

## Local storage

The SDK writes all data to `~/.loop/` on your machine:

```
~/.loop/
  interactions.jsonl    one JSON object per line, one per interaction
  feedback.jsonl        one JSON object per line, one per feedback record
```

These files are plain JSONL — you can open them in any text editor or process them with `jq`, pandas, or any other tool.

---

## Export formats

The SDK reads from `~/.loop/feedback.jsonl` and writes a training file. Three formats are supported:

### chat_jsonl

OpenAI chat format. Compatible with OpenAI fine-tuning, LLaMA-Factory, Axolotl, and most modern trainers.

```json
{"messages": [{"role": "user", "content": "What is the capital of Pakistan?"}, {"role": "assistant", "content": "Islamabad"}]}
```

### alpaca_jsonl

Alpaca instruction format. Compatible with Alpaca, LLaMA-Factory, and similar frameworks.

```json
{"instruction": "What is the capital of Pakistan?", "input": "", "output": "Islamabad"}
```

### dpo_jsonl

DPO preference format. Only feedback records with a correction are included. Compatible with TRL, Axolotl, and Unsloth DPO trainers.

```json
{"prompt": "What is the capital of Pakistan?", "chosen": "The capital is Islamabad.", "rejected": "Islamabad"}
```

---

## API reference

The API is stateless and stores nothing. It validates requests and returns structured acks.

Base URL: `https://loop-systematic-architecture-api-index.vercel.app`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/v1/health` | Health check |
| POST | `/v1/interactions` | Validate and confirm a single interaction |
| POST | `/v1/interactions/batch` | Validate and confirm up to 100 interactions |
| POST | `/v1/feedback` | Validate and ack a feedback record |
| GET | `/v1/export/formats` | Return export format schemas |
| POST | `/v1/stats` | Echo a stats summary |

All responses include an `X-Request-Id` header. Errors use the format:

```json
{
  "error": {
    "type": "validation_error",
    "message": "...",
    "request_id": "uuid"
  }
}
```

Interactive docs: `https://loop-systematic-architecture-api-index.vercel.app/docs`

---

## Deploying the API

The API is already deployed at the production URL above. If you want to self-host:

**Prerequisites:** Python 3.10+, pip

```bash
# Clone the repo
git clone https://github.com/ahmadjamilofficial/Loop.git
cd Loop

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api.app.main:app --reload --port 8000
```

**Deploy to Vercel:**

1. Push the repo to GitHub.
2. Import on [vercel.com](https://vercel.com) — no settings needed.
3. Click Deploy.

`vercel.json` routes all requests to `api/app/main.py` automatically.

---

## Repository layout

```
loop/
  api/
    app/
      main.py              FastAPI app — Vercel entry point
      config.py            Version constants
      middleware.py        X-Request-Id header
      schemas.py           Pydantic request/response shapes
      routers/
        health.py
        interactions.py
        feedback.py
        export.py
        stats.py
  loop-python/             Generated Python SDK (by Speakeasy)
    src/loop/
      sdk.py               Main Loop client class
      interactions.py      Interactions sub-SDK
      feedback.py          Feedback sub-SDK
      health.py            Health sub-SDK
      export.py            Export sub-SDK
      stats.py             Stats sub-SDK
      models/              Pydantic models
      errors/              Exception classes
  openapi/
    openapi.json           OpenAPI 3.1 spec — source of truth
  .speakeasy/
    workflow.yaml          Speakeasy generation + publish config
  .github/workflows/
    sdk_generation.yaml    Generates SDK on schedule / manual trigger
    sdk_publish.yaml       Publishes to PyPI on merge to main
  requirements.txt         API dependencies
  vercel.json              Vercel routing config
  README.md
```

---

## Environment variables

The API has no required environment variables for local use. Optional:

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./loop.db` | Only needed if you want persistent storage on Vercel. Set to a Postgres URL. |
| `LOOP_DEBUG` | `false` | Set to `true` to enable verbose logging. |

For the SDK, no environment variables are required.
