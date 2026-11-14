# Loop

<p align="center">
  <strong>Close the feedback loop. Build better AI.</strong>
</p>

<p align="center">
  An open-source RLHF toolkit for AI developers.
  <br>
  Capture model interactions, collect human feedback, and build better training data.
</p>

<p align="center">
  <a href="https://github.com/ahmadjamilofficial/Loop">GitHub</a> ·
  <a href="https://github.com/Ahmadjamilofficial/Loop/Openapi/openapi.json">API Reference</a> ·
  <a href="https://github.com/ahmadjamilofficial/Loop/tree/main/loop-python/docs">SDK Documentation</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/Status-Beta-orange" alt="Beta Status">
  <img src="https://img.shields.io/badge/SDK-Speakeasy-purple" alt="Speakeasy SDK">
</p>

---

## What is Loop?

**Loop is a developer-focused Reinforcement Learning from Human Feedback (RLHF) toolkit.**

It provides a Python SDK and a lightweight validation API for capturing AI interactions, collecting human feedback, and organizing feedback into structured datasets for model improvement.

Every AI application produces valuable information:

- Which responses do users appreciate?
- Which answers are inaccurate or incomplete?
- What would a better answer look like?
- Which models consistently produce better results?
- Which interactions should become training examples?

Loop is designed to help developers capture these signals without building an entire feedback infrastructure from scratch.

Instead of treating user feedback as disposable application data, Loop treats it as a potential source of model improvement.

### The feedback loop

```text
              AI APPLICATION
                    |
                    v
             MODEL RESPONSE
                    |
                    v
              LOOP SDK
                    |
                    v
          INTERACTION CAPTURE
                    |
                    v
             HUMAN FEEDBACK
               /        \
              /          \
         POSITIVE       NEGATIVE
         FEEDBACK       FEEDBACK
                           |
                           v
                      CORRECTION
                           |
                           v
                  STRUCTURED DATA
                           |
                           v
                 TRAINING DATASETS
                    /    |    \
                   /     |     \
                CHAT  ALPACA   DPO
                    \    |    /
                     \   |   /
                      MODEL
                   IMPROVEMENT
```

## Why Loop?

Building an AI application is only one part of developing a useful AI system. Understanding how users interact with that system is equally important.

Loop focuses on that feedback layer.

| Capability | What it provides |
|---|---|
| Interaction logging | Capture prompts, model responses, and metadata |
| Human feedback | Record positive and negative reactions |
| Corrections | Capture improved answers for training workflows |
| Batch operations | Validate up to 100 interactions in one request |
| Typed Python SDK | Structured models and developer-friendly interfaces |
| Export schemas | Discover supported fine-tuning dataset formats |
| Stateless API | Validate requests without maintaining interaction databases |
| Local-first architecture | Designed around keeping interaction data under developer control |

### Design principles

**1. Developer-first**

A simple Python interface, typed request and response models, synchronous and asynchronous operations, and configurable HTTP clients.

**2. Privacy-conscious**

The hosted API is designed as a stateless validation service. It does not maintain a database of submitted interactions or feedback.

**3. Training-oriented**

Feedback is structured around the information that can help improve a model, rather than being limited to generic analytics.

**4. Open source**

Loop is designed to be inspectable, extensible, and community-driven.

---

## Architecture

Loop separates its API layer from its data-handling design.

### Python SDK

The Python SDK provides the client interface for:

- Logging individual interactions.
- Logging batches of interactions.
- Submitting human feedback.
- Retrieving export format definitions.
- Checking API health.
- Submitting statistics summaries.

The SDK is generated using Speakeasy from the project's OpenAPI specification.

### Loop API

The hosted API is built with FastAPI and Pydantic.

Production endpoint:

```text
https://loop-systematic-architecture-api-index.vercel.app
```

Interactive documentation:

https://loop-systematic-architecture-api-index.vercel.app/docs

The API:

- Validates incoming payloads.
- Generates or confirms interaction identifiers.
- Acknowledges feedback submissions.
- Provides export format schemas.
- Validates and echoes statistics summaries.
- Returns structured errors and request identifiers.

It does not persist interaction or feedback records.

### Intended local data model

The local-first architecture defines the following storage layout:

```text
~/.loop/
│
├── interactions.jsonl
│
└── feedback.jsonl
```

| File | Intended contents |
|---|---|
| `interactions.jsonl` | Prompts, responses, models, timestamps, metadata, and session identifiers |
| `feedback.jsonl` | Interaction references, ratings, corrections, comments, and feedback identifiers |

**Implementation status:** The API and generated SDK contracts describe this local-storage architecture. The currently committed generated SDK methods should not yet be assumed to implement local JSONL persistence or the `loop` CLI. Those capabilities need to be verified or completed in the SDK integration layer.

---

## Installation

Loop supports Python 3.10 and later.

### Install directly from GitHub

The Python SDK is located inside the `loop-python/` subdirectory.

**pip**

```bash
pip install git+https://github.com/ahmadjamilofficial/Loop.git#subdirectory=loop-python
```

**uv**

```bash
uv add git+https://github.com/ahmadjamilofficial/Loop.git#subdirectory=loop-python
```

**Poetry**

```bash
poetry add git+https://github.com/ahmadjamilofficial/Loop.git#subdirectory=loop-python
```

### Package information

| Property | Value |
|---|---|
| Distribution name | `loopsdk` |
| Python import | `loop` |
| Current SDK version in source | `0.0.2` |
| Minimum Python version | `3.10` |
| HTTP client | HTTPX |
| Data models | Pydantic |
| SDK generator | Speakeasy |

The package metadata currently identifies the distribution as `loopsdk`. Once the package is published to PyPI, the corresponding installation command should be:

```bash
pip install loopsdk
```

---

## Quickstart

### 1. Initialize Loop

```python
from loop import Loop

client = Loop()
```

### 2. Check API connectivity

```python
from loop import Loop

with Loop() as client:
    response = client.health.health()
    print(response)
```

The health endpoint returns the API status and version.

### 3. Log an interaction

```python
from loop import Loop

with Loop() as client:

    interaction = client.interactions.log_interaction(
        prompt="What is the capital of Pakistan?",
        response="Islamabad",
        model="my-model-v1",
        metadata={
            "application": "my-ai-app",
            "environment": "development",
        },
        session_id="session_001",
    )

    interaction_id = interaction.result.id

    print("Interaction ID:", interaction_id)
```

### 4. Submit feedback

Positive feedback:

```python
client.feedback.submit_feedback(
    interaction_id=interaction_id,
    rating="up",
)
```

Negative feedback with a correction:

```python
client.feedback.submit_feedback(
    interaction_id=interaction_id,
    rating="down",
    correction="The capital of Pakistan is Islamabad.",
    comment="The original response was incomplete.",
)
```

The feedback schema supports two ratings:

| Rating | Meaning |
|---|---|
| `up` | The response was good |
| `down` | The response was bad |

A correction is optional and represents an improved answer.

---

## Core SDK resources

The generated Python SDK exposes five primary resources.

| Resource | Operations | Purpose |
|---|---|---|
| Health | `health()` | API connectivity |
| Interactions | `log_interaction()` | Log an individual interaction |
| Interactions | `log_interactions_batch()` | Validate a batch of interactions |
| Feedback | `submit_feedback()` | Submit human feedback |
| Export | `export_formats()` | Retrieve supported export schemas |
| Stats | `echo_stats()` | Validate and echo a statistics summary |

### Interactions

Interactions represent the relationship between an input prompt and the response generated by an AI model.

An interaction can contain:

| Field | Required | Description |
|---|---|---|
| `prompt` | Yes | A string or list of chat messages |
| `response` | Yes | Model-generated response |
| `id` | No | Client-generated interaction identifier |
| `model` | No | Model name or version |
| `metadata` | No | Additional key-value information |
| `session_id` | No | Groups interactions into a conversation |
| `timestamp` | No | Defaults to current UTC time when omitted |

#### Plain-text prompts

```python
client.interactions.log_interaction(
    prompt="Explain artificial intelligence.",
    response="Artificial intelligence is...",
    model="model-v1",
)
```

#### Chat-message prompts

Loop also accepts a list of chat messages.

```python
client.interactions.log_interaction(
    prompt=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "Explain neural networks.",
        },
    ],
    response="Neural networks are computational models...",
    model="model-v1",
)
```

Supported chat roles:

- `system`
- `user`
- `assistant`

#### Client-generated IDs

Developers can supply their own interaction identifier.

```python
client.interactions.log_interaction(
    id="int_a1b2c3d4",
    prompt="What is machine learning?",
    response="Machine learning is a branch of AI.",
    model="model-v1",
)
```

A client-generated ID is useful when an application needs to associate feedback with an interaction before waiting for a server-generated identifier.

UUID-based identifiers are recommended.

### Batch interactions

Loop supports batch validation of up to 100 interactions in one request.

```python
from loop import Loop

with Loop() as client:

    result = client.interactions.log_interactions_batch(
        interactions=[
            {
                "prompt": "What is AI?",
                "response": "Artificial intelligence...",
                "model": "model-v1",
            },
            {
                "prompt": "What is ML?",
                "response": "Machine learning...",
                "model": "model-v1",
            },
        ]
    )

    print("IDs:", result.result.ids)
    print("Count:", result.result.count)
```

The API returns confirmed identifiers in the same order as the submitted interactions.

The batch endpoint requires at least one interaction and accepts a maximum of 100.

### Feedback

Feedback connects a user reaction to a previously logged interaction.

```python
client.feedback.submit_feedback(
    interaction_id="int_a1b2c3d4",
    rating="down",
    correction="A corrected response.",
    comment="The original answer contained an error.",
    user_id="anonymous-user-001",
)
```

| Field | Required | Description |
|---|---|---|
| `interaction_id` | Yes | Previously returned interaction ID |
| `rating` | Yes | `up` or `down` |
| `correction` | No | Corrected answer |
| `comment` | No | Additional feedback |
| `user_id` | No | An anonymized user identifier |

Avoid submitting real names, email addresses, or unnecessary personally identifiable information.

---

## Training data formats

Loop's API describes three fine-tuning formats.

The purpose is to organize interaction and feedback information into structures that can be consumed by model-training tools.

### 1. Chat JSONL

A conversational format based on messages and roles.

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is the capital of Pakistan?"
    },
    {
      "role": "assistant",
      "content": "Islamabad"
    }
  ]
}
```

Typical ecosystem:

- OpenAI-compatible chat fine-tuning workflows
- LLaMA-Factory
- Axolotl
- Other message-based training frameworks

### 2. Alpaca JSONL

An instruction-oriented format.

```json
{
  "instruction": "Explain machine learning.",
  "input": "",
  "output": "Machine learning is a field of artificial intelligence..."
}
```

Typical ecosystem:

- Alpaca-compatible workflows
- LLaMA-Factory
- Instruction fine-tuning pipelines

### 3. DPO JSONL

Direct Preference Optimization uses a preferred and rejected response for the same prompt.

```json
{
  "prompt": "What is the capital of Pakistan?",
  "chosen": "Islamabad",
  "rejected": "Karachi"
}
```

Typical ecosystem:

- Hugging Face TRL
- Axolotl
- Unsloth

### Feedback-to-training mapping

The current Loop design defines the following mapping:

| Feedback | Training interpretation |
|---|---|
| `up`, without correction | Positive supervised fine-tuning example |
| `down`, with correction | Corrected SFT target and DPO preference pair |
| `down`, without correction | Feedback signal; not a complete training example |

For a negative response with a correction:

```text
Prompt:
    What is the capital of Pakistan?

Original response:
    Karachi

User correction:
    Islamabad

DPO:
    chosen   = Islamabad
    rejected = Karachi
```

**Important:** A user correction is treated as the preferred response in this mapping. Corrections should be reviewed for factual accuracy and quality before being used as training labels.

### Retrieve available formats

The SDK provides an operation for retrieving export format definitions.

```python
from loop import Loop

with Loop() as client:

    formats = client.export.export_formats()

    print(formats.result.formats)
```

This endpoint returns format descriptions and schema examples. It does not upload or download training datasets.

The actual local dataset-generation workflow is part of the intended architecture and should be verified against the installed SDK implementation before being used as a production export command.

---

## Asynchronous support

Loop provides asynchronous versions of its SDK operations.

```python
import asyncio

from loop import Loop


async def main():

    async with Loop() as client:

        interaction = await client.interactions.log_interaction_async(
            prompt="Explain transformers.",
            response="Transformers are neural network architectures...",
            model="transformer-model-v1",
        )

        print(interaction.result.id)


asyncio.run(main())
```

Asynchronous feedback:

```python
async def submit_feedback():

    async with Loop() as client:

        result = await client.feedback.submit_feedback_async(
            interaction_id="int_a1b2c3d4",
            rating="up",
        )

        print(result)
```

Asynchronous operations are useful when integrating Loop into applications built around `asyncio`, asynchronous APIs, and other non-blocking workflows.

---

## API reference

The Loop API is built using FastAPI and exposes the following endpoints.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/v1/health` | API health and version |
| `POST` | `/v1/interactions` | Validate an interaction |
| `POST` | `/v1/interactions/batch` | Validate multiple interactions |
| `POST` | `/v1/feedback` | Validate and acknowledge feedback |
| `GET` | `/v1/export/formats` | Return dataset format definitions |
| `POST` | `/v1/stats` | Validate and echo statistics |

### API documentation

The interactive Swagger documentation is available at:

https://loop-systematic-architecture-api-index.vercel.app/docs

### Request IDs

API responses include an `X-Request-Id` header for request tracing.

### Error response structure

Validation errors use a structured JSON response.

```json
{
  "error": {
    "type": "validation_error",
    "message": "Invalid request",
    "request_id": "uuid"
  }
}
```

The API uses HTTP `422` for request validation failures.

---

## Configuration

The SDK can be configured at initialization.

### Server selection

Two servers are currently defined.

| Index | URL | Environment |
|---|---|---|
| `0` | `https://loop-systematic-architecture-api-index.vercel.app` | Production |
| `1` | `http://localhost:8000` | Local development |

#### Select a server by index

```python
from loop import Loop

with Loop(server_idx=0) as client:
    print(client.health.health())
```

#### Override the server URL

```python
from loop import Loop

with Loop(
    server_url="http://localhost:8000",
) as client:

    print(client.health.health())
```

### Timeout

The SDK accepts a request timeout in milliseconds.

```python
from loop import Loop

with Loop(timeout_ms=30000) as client:
    print(client.health.health())
```

The generated SDK uses HTTPX for network communication.

### Custom HTTP client

You can supply your own synchronous HTTPX client.

```python
import httpx

from loop import Loop

http_client = httpx.Client(
    headers={
        "x-custom-header": "some-value",
    }
)

with Loop(client=http_client) as client:
    print(client.health.health())
```

The SDK also accepts a custom asynchronous HTTP client through `async_client`.

---

## Retries

Loop supports configurable retry behavior for operations that support retries.

The retry configuration supports:

- Backoff strategy.
- Initial retry interval.
- Maximum retry interval.
- Exponential growth factor.
- Maximum elapsed time.
- Optional connection-error retries.
- Optional retryable status-code overrides.

### Configure retries globally

```python
from loop import Loop
from loop.utils import BackoffStrategy, RetryConfig

retry = RetryConfig(
    "backoff",
    BackoffStrategy(
        initial_interval=500,
        max_interval=60000,
        exponent=1.5,
        max_elapsed_time=300000,
    ),
    retry_connection_errors=True,
)

with Loop(retry_config=retry) as client:

    response = client.health.health()

    print(response)
```

### Configure retries per operation

```python
from loop import Loop
from loop.utils import BackoffStrategy, RetryConfig

retry = RetryConfig(
    "backoff",
    BackoffStrategy(500, 60000, 1.5, 300000),
    True,
)

with Loop() as client:

    response = client.health.health(
        retries=retry,
    )

    print(response)
```

Retry behavior is limited to operations that support it. Check the operation documentation for details.

---

## Error handling

The SDK exposes a base exception named `LoopError`.

It provides information about failed HTTP requests.

| Property | Type | Description |
|---|---|---|
| `message` | `str` | Error message |
| `status_code` | `int` | HTTP status code |
| `headers` | `httpx.Headers` | Response headers |
| `body` | `str` | Response body |
| `raw_response` | `httpx.Response` | Original HTTPX response |

### Example

```python
from loop import Loop, errors

with Loop() as client:

    try:

        result = client.interactions.log_interaction(
            prompt="What is the capital of Pakistan?",
            response="Islamabad",
            model="model-v1",
        )

        print(result)

    except errors.LoopError as error:

        print("Message:", error.message)
        print("Status:", error.status_code)
        print("Body:", error.body)
        print("Headers:", error.headers)

        if isinstance(error, errors.ErrorResponse):
            print(error.data.error)
```

### Error classes

| Error | Purpose |
|---|---|
| `LoopError` | Base class for HTTP errors |
| `ErrorResponse` | Structured API validation error |
| `LoopDefaultError` | Fallback HTTP error |
| `ResponseValidationError` | Unexpected response structure |
| `httpx.RequestError` | Network request failure |
| `httpx.ConnectError` | Connection failure |
| `httpx.TimeoutException` | Request timeout |

The SDK also exposes the underlying HTTPX response for further inspection.

---

## Resource management

Loop supports context managers for both synchronous and asynchronous clients.

### Synchronous

```python
from loop import Loop


def main():

    with Loop() as client:

        response = client.health.health()

        print(response)


if __name__ == "__main__":
    main()
```

### Asynchronous

```python
import asyncio

from loop import Loop


async def main():

    async with Loop() as client:

        response = await client.health.health_async()

        print(response)


asyncio.run(main())
```

Context managers close the SDK-managed HTTP connections when the client exits.

For long-running applications, reuse a client instance where appropriate rather than repeatedly creating clients for individual operations.

---

## Debugging

Loop supports SDK request and response logging.

### Enable debug logging

```python
import logging

from loop import Loop

logging.basicConfig(level=logging.DEBUG)

with Loop(
    debug_logger=logging.getLogger("loop"),
) as client:

    response = client.health.health()

    print(response)
```

### Environment variable

You can also enable the default logger with:

```bash
LOOP_DEBUG=true
```

Supported truthy values:

```text
true
1
yes
on
```

Debug logging should be used carefully because application requests may contain prompts, responses, metadata, or other sensitive content.

---

## IDE support

Loop uses Pydantic models and typed Python interfaces.

It should work with standard Python IDEs and editors.

For PyCharm, the Pydantic plugin can improve editor integration:

https://docs.pydantic.dev/latest/integrations/pycharm/

---

## Development

### Requirements

- Python 3.10+
- pip
- Git
- FastAPI
- Pydantic
- Uvicorn

### Clone the repository

```bash
git clone https://github.com/ahmadjamilofficial/Loop.git

cd Loop
```

### Install API dependencies

```bash
pip install -r requirements.txt
```

### Run the API locally

```bash
uvicorn api.app.main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### Python SDK development

The SDK source is located in:

```text
loop-python/
```

Install the SDK from the repository:

```bash
pip install -e ./loop-python
```

### Repository structure

```text
Loop/
│
├── api/
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── middleware.py
│       ├── schemas.py
│       │
│       └── routers/
│           ├── health.py
│           ├── interactions.py
│           ├── feedback.py
│           ├── export.py
│           └── stats.py
│
├── loop-python/
│   ├── src/
│   │   └── loop/
│   │       ├── sdk.py
│   │       ├── interactions.py
│   │       ├── feedback.py
│   │       ├── health.py
│   │       ├── export.py
│   │       ├── stats.py
│   │       ├── models/
│   │       ├── errors/
│   │       └── utils/
│   │
│   ├── docs/
│   │   ├── sdks/
│   │   │   ├── export/
│   │   │   ├── feedback/
│   │   │   ├── health/
│   │   │   ├── interactions/
│   │   │   └── stats/
│   │   │
│   │   └── models/
│   │
│   ├── .speakeasy/
│   │   └── workflow.yaml
│   │
│   ├── pyproject.toml
│   ├── README.md
│   └── README-PYPI.md
│
├── openapi/
│   └── openapi.json
│
├── .github/
│   └── workflows/
│
├── requirements.txt
├── vercel.json
└── README.md
```

---

## SDK generation

Loop's Python SDK is generated using [Speakeasy](https://www.speakeasy.com/).

The OpenAPI specification is the source of truth for the SDK.

### Generation workflow

```text
OpenAPI Specification
        |
        v
   Speakeasy Source
        |
        v
  Python SDK Generation
        |
        v
    loop-python/
        |
        v
 GitHub Actions Workflows
        |
        v
   SDK Distribution
```

Important project files:

| File | Purpose |
|---|---|
| `openapi/openapi.json` | OpenAPI 3.1 specification |
| `loop-python/.speakeasy/workflow.yaml` | SDK generation workflow |
| `loop-python/pyproject.toml` | Python package metadata |
| `loop-python/src/loop/` | Generated SDK implementation |
| `.github/workflows/` | Automation workflows |

Generated SDK files should not be modified manually unless the change is intended to be maintained through the generation process.

---

## Current maturity

<sub>Beta</sub>

Loop is actively evolving.

The current release should be treated as beta software. Interfaces, request models, and generated SDK methods may change between releases.

Before using Loop in production:

- Pin the SDK to a specific version.
- Test request and response handling.
- Validate generated training data.
- Review data-handling and privacy requirements.
- Verify local persistence and export functionality in the installed version.


## Contributing

Contributions are welcome.

You can contribute through:

- Bug reports.
- Feature requests.
- Documentation improvements.
- SDK improvements.
- API enhancements.
- Testing and reproducible examples.

For generated SDK changes, update the appropriate source specification or generation configuration where possible.

Open an issue or submit a pull request:

https://github.com/ahmadjamilofficial/Loop

---

## License

Loop's OpenAPI specification identifies the project as MIT-licensed.

The Python package metadata currently declares Apache-2.0, so the repository and package license metadata should be reconciled before release.

---

<p align="center">
  <strong>Loop</strong>
  <br>
  Close the feedback loop. Build better AI.
  <br><br>
  <a href="https://github.com/ahmadjamilofficial/Loop">Explore the repository</a>
</p>
