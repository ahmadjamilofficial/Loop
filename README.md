# Loop

<p align="center">
  <strong>Close the feedback loop. Build better AI.</strong>
</p>

<p align="center">
  A developer-friendly, type-safe Python SDK for collecting human feedback on AI interactions and turning it into fine-tuning datasets.
</p>

<p align="center">
  <a href="https://github.com/ahmadjamilofficial/Loop">GitHub</a> ·
  <a href="https://loop-systematic-architecture-api-index.vercel.app/docs">API Documentation</a> ·
  <a href="https://pypi.org/project/loop/">PyPI</a>
</p>

<p align="center">
  ![Python](https://img.shields.io/badge/Python-3.10+-blue)
  ![License](https://img.shields.io/badge/License-MIT-green)
  ![Status](https://img.shields.io/badge/Status-Beta-orange)
  ![SDK](https://img.shields.io/badge/SDK-Speakeasy-purple)
</p>

---

## What is Loop?

**Loop is an open-source, local-first RLHF toolkit for AI developers.**

It gives developers a simple way to capture model interactions, collect human feedback, and transform that feedback into datasets for model training.

Instead of building your own feedback infrastructure, you can integrate Loop into your Python application and start collecting useful training signals.

### The idea

Your AI application generates a response. A user evaluates it. Loop captures that feedback and helps turn it into structured training data.

```text
AI Application
      |
      v
 Model Interaction
      |
      v
  Loop SDK
      |
      +------> Local Interaction Storage
      |         ~/.loop/interactions.jsonl
      |
      v
  Human Feedback
      |
      +------> Local Feedback Storage
      |         ~/.loop/feedback.jsonl
      |
      v
 Dataset Generation
      |
      +------> Chat JSONL
      +------> Alpaca JSONL
      +------> DPO JSONL
```

### Why Loop?

- **Local-first:** Interaction and feedback records are stored on the developer's machine.
- **Developer-friendly:** A straightforward Python SDK with typed interfaces.
- **Privacy-conscious:** The hosted validation API is designed to be stateless and does not persist interaction or feedback records.
- **Training-ready:** Organize feedback into formats used by modern fine-tuning workflows.
- **Open source:** MIT-licensed and designed to be extended by the community.

## How it works

Loop has two main components:

### 1. Python SDK

The SDK integrates with your AI application. It handles interaction logging, feedback submission, local storage, and dataset workflows.

Local records are stored under:

```text
~/.loop/
├── interactions.jsonl
└── feedback.jsonl
```

### 2. Loop API

The hosted API provides validation and acknowledgement services.

**Production API:**

```text
https://loop-systematic-architecture-api-index.vercel.app
```

The API validates incoming requests, generates or confirms interaction identifiers, and returns responses. According to the current architecture, it does not persist interaction or feedback records.

### Request lifecycle

1. Your application sends an interaction through the SDK.
2. The API validates the request and returns an identifier.
3. The SDK writes the interaction to local storage.
4. Your application collects user feedback.
5. The API validates and acknowledges the feedback.
6. The SDK writes the feedback locally.
7. The local dataset workflow transforms eligible records into training examples.

**Your interaction and feedback data stays local rather than being stored in Loop's hosted API.**

---

## Installation

Loop requires **Python 3.10 or later**.

The SDK can be installed using `uv`, `pip`, or Poetry.

> **Current installation:** The commands below install directly from the GitHub repository's `loop-python` directory. Use these until the package is published and a stable PyPI installation is available.

### Using uv

```bash
uv add git+https://github.com/ahmadjamilofficial/Loop.git#subdirectory=loop-python
```

### Using pip

```bash
pip install git+https://github.com/ahmadjamilofficial/Loop.git#subdirectory=loop-python
```

### Using Poetry

```bash
poetry add git+https://github.com/ahmadjamilofficial/Loop.git#subdirectory=loop-python
```

### Verify installation

```python
from loop import Loop

client = Loop()

response = client.health.health()
print(response)
```

---

## Quickstart

Get started by logging an interaction and submitting feedback.

```python
from loop import Loop

with Loop() as client:

    # 1. Log an AI interaction
    interaction = client.interactions.log_interaction(
        prompt="What is the capital of Pakistan?",
        response="Islamabad",
        model="my-model-v1",
        metadata={
            "application": "my-ai-app",
            "environment": "development",
        },
    )

    interaction_id = interaction.result.id

    print("Interaction ID:", interaction_id)

    # 2. Submit positive feedback
    client.feedback.submit_feedback(
        interaction_id=interaction_id,
        rating="up",
    )

    # 3. Submit negative feedback with a correction
    client.feedback.submit_feedback(
        interaction_id=interaction_id,
        rating="down",
        correction="The capital of Pakistan is Islamabad.",
        comment="The answer needs a more complete explanation.",
    )
```

The SDK handles the API requests and, according to the local-first design, writes the corresponding records to your local Loop storage.

---

## SDK usage

### Log an interaction

Use `log_interaction()` whenever your AI application generates a response.

```python
from loop import Loop

with Loop() as client:

    result = client.interactions.log_interaction(
        prompt="Explain machine learning in simple terms.",
        response="Machine learning is a field of AI...",
        model="my-model-v1",
        session_id="session_001",
        metadata={
            "application": "chatbot",
            "version": "1.0",
        },
    )

    print(result.result.id)
    print(result.result.timestamp)
    print(result.result.stored)
```

The response contains:

| Property | Description |
|---|---|
| `result.id` | Interaction identifier |
| `result.timestamp` | Interaction timestamp |
| `result.stored` | API storage indicator; currently `False` |

The API acknowledges the interaction, while the SDK is responsible for local persistence.

### Log multiple interactions

For applications that generate multiple responses, use batch logging.

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

    print(result)
```

The batch operation supports up to 100 interactions per request.

### Submit feedback

Loop supports positive and negative feedback.

```python
client.feedback.submit_feedback(
    interaction_id="YOUR_INTERACTION_ID",
    rating="up",
)
```

For negative feedback, you can include a correction and a comment:

```python
client.feedback.submit_feedback(
    interaction_id="YOUR_INTERACTION_ID",
    rating="down",
    correction="A better response goes here.",
    comment="The original response was inaccurate.",
)
```

Supported feedback fields:

| Field | Required | Description |
|---|---|---|
| `interaction_id` | Yes | ID of the interaction |
| `rating` | Yes | `up` or `down` |
| `correction` | No | Improved response |
| `comment` | No | Additional feedback |
| `user_id` | No | An anonymized user identifier |

Avoid sending real names, email addresses, or other unnecessary personal information.

---

## Dataset generation

One of Loop's main goals is to turn feedback into useful training data.

The project supports three dataset formats.

### Chat JSONL

Compatible with OpenAI-style chat fine-tuning workflows and modern training frameworks.

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

### Alpaca JSONL

Instruction, input, and output format.

```json
{
  "instruction": "What is the capital of Pakistan?",
  "input": "",
  "output": "Islamabad"
}
```

### DPO JSONL

Direct Preference Optimization format, containing a prompt, a preferred response, and a rejected response.

```json
{
  "prompt": "What is the capital of Pakistan?",
  "chosen": "Islamabad",
  "rejected": "Karachi"
}
```

### How feedback maps to training data

| Feedback | Dataset behavior |
|---|---|
| `up` without correction | Positive supervised fine-tuning example |
| `down` with correction | DPO preference pair and corrected SFT example |
| `down` without correction | Recorded for feedback statistics; not used as a training example |

A correction is treated as the preferred response in the current DPO mapping. Developers should review generated preference pairs before using them for training.

### Supported formats and ecosystem

| Format | Typical ecosystem |
|---|---|
| Chat JSONL | OpenAI fine-tuning, LLaMA-Factory, Axolotl |
| Alpaca JSONL | Alpaca-compatible trainers, LLaMA-Factory |
| DPO JSONL | Hugging Face TRL, Axolotl, Unsloth |

The API exposes `export_formats()` to retrieve the supported format schemas. Dataset generation is part of the local-data workflow; consult the SDK implementation for the exact exporter interface and command available in your installed version.

---

## Available resources and operations

The Python SDK exposes the following resources:

| Resource | Method | Purpose |
|---|---|---|
| Health | `health()` | Check API availability |
| Interactions | `log_interaction()` | Log one interaction |
| Interactions | `log_interactions_batch()` | Log multiple interactions |
| Feedback | `submit_feedback()` | Submit human feedback |
| Export | `export_formats()` | Retrieve supported dataset schemas |
| Stats | `echo_stats()` | Submit and receive a statistics summary |

### Health check

```python
from loop import Loop

with Loop() as client:
    result = client.health.health()
    print(result)
```

### Retrieve export formats

```python
from loop import Loop

with Loop() as client:
    formats = client.export.export_formats()
    print(formats)
```

---

## Asynchronous usage

Loop also supports asynchronous requests.

```python
import asyncio

from loop import Loop


async def main():

    async with Loop() as client:

        result = await client.health.health_async()

        print(result)


asyncio.run(main())
```

Use the asynchronous client in applications built around `asyncio`, such as asynchronous web servers and AI applications.

---

## Configuration

The SDK can be configured when initializing the client.

### Server selection

Loop provides two server configurations:

| Index | Server | Description |
|---|---|---|
| `0` | `https://loop-systematic-architecture-api-index.vercel.app` | Production |
| `1` | `http://localhost:8000` | Local development |

Select a server by index:

```python
from loop import Loop

with Loop(server_idx=0) as client:
    result = client.health.health()
    print(result)
```

Alternatively, provide a custom server URL:

```python
from loop import Loop

with Loop(
    server_url="http://localhost:8000",
) as client:

    result = client.health.health()
    print(result)
```

### Timeout configuration

The SDK supports a configurable request timeout.

```python
from loop import Loop

with Loop(timeout_ms=30000) as client:
    result = client.health.health()
    print(result)
```

The default timeout is 30 seconds.

---

## Retries

The SDK supports configurable retry behavior for operations that support retries.

You can override the retry strategy for a single request:

```python
from loop import Loop
from loop.utils import BackoffStrategy, RetryConfig

with Loop() as client:

    result = client.health.health(
        retry_config=RetryConfig(
            "backoff",
            BackoffStrategy(1, 50, 1.1, 100),
            False,
        )
    )

    print(result)
```

You can also configure retries when initializing the client:

```python
from loop import Loop
from loop.utils import BackoffStrategy, RetryConfig

retry = RetryConfig(
    "backoff",
    BackoffStrategy(1, 50, 1.1, 100),
    False,
)

with Loop(retry_config=retry) as client:

    result = client.health.health()
    print(result)
```

Check the individual operation documentation for retry support and applicable configuration.

---

## Error handling

Loop provides a common base exception called `LoopError` for HTTP error responses.

It exposes useful information about the failed request.

| Property | Type | Description |
|---|---|---|
| `message` | `str` | Error message |
| `status_code` | `int` | HTTP status code |
| `headers` | `httpx.Headers` | Response headers |
| `body` | `str` | Raw response body |
| `raw_response` | `httpx.Response` | Underlying HTTP response |
| `data` | Optional | Structured error information, when available |

### Example

```python
from loop import Loop, errors

with Loop() as client:

    try:

        result = client.interactions.log_interaction(
            prompt="What is the capital of Pakistan?",
            response="Islamabad",
            model="my-model-v1",
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

### Primary exception

- `LoopError`: Base class for HTTP error responses.

For operation-specific errors, refer to the method documentation.

---

## Custom HTTP clients

The Loop SDK uses `httpx` for HTTP communication.

You can provide your own HTTP client to customize request behavior, including headers, proxies, timeouts, and other HTTP configuration.

### Custom synchronous client

```python
import httpx

from loop import Loop

http_client = httpx.Client(
    headers={
        "x-custom-header": "someValue",
    }
)

with Loop(client=http_client) as client:
    result = client.health.health()
    print(result)
```

### Custom asynchronous client

The SDK also supports custom asynchronous HTTP clients through its async client interface.

This can be useful when integrating Loop into applications that already manage their own HTTP connections.

---

## Resource management

The `Loop` client supports context managers.

Use a context manager to ensure HTTP connections are properly closed when your application finishes using the SDK.

### Synchronous

```python
from loop import Loop

def main():

    with Loop() as client:

        result = client.health.health()
        print(result)


if __name__ == "__main__":
    main()
```

### Asynchronous

```python
import asyncio

from loop import Loop


async def main():

    async with Loop() as client:

        result = await client.health.health_async()
        print(result)


asyncio.run(main())
```

For long-running applications, create and reuse an appropriate client instance rather than repeatedly creating new clients for every request.

---

## Debugging

Loop supports debug logging for SDK requests and responses.

### Enable debug logging in Python

```python
import logging

from loop import Loop

logging.basicConfig(level=logging.DEBUG)

with Loop(
    debug_logger=logging.getLogger("loop"),
) as client:

    result = client.health.health()
    print(result)
```

### Enable debug mode using an environment variable

Set:

```bash
LOOP_DEBUG=true
```

Supported truthy values include:

- `true`
- `1`
- `yes`
- `on`

Any other value leaves debug logging disabled.

Be careful when enabling request logging in production. Logs may contain prompts, responses, or other application data.

---

## API reference

The Loop API is built with FastAPI and provides the following endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/health` | Health check |
| `POST` | `/v1/interactions` | Validate an interaction |
| `POST` | `/v1/interactions/batch` | Validate multiple interactions |
| `POST` | `/v1/feedback` | Validate feedback |
| `GET` | `/v1/export/formats` | Retrieve supported export schemas |
| `POST` | `/v1/stats` | Validate and echo statistics |

**Interactive API documentation:**

https://loop-systematic-architecture-api-index.vercel.app/docs

### Response identifiers

API responses include an `X-Request-Id` header.

Error responses use a structured format:

```json
{
  "error": {
    "type": "validation_error",
    "message": "Invalid request",
    "request_id": "uuid"
  }
}
```

---

## Development

### Requirements

- Python 3.10+
- pip
- Git

### Run the API locally

Clone the repository:

```bash
git clone https://github.com/ahmadjamilofficial/Loop.git

cd Loop
```

Install the API dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn api.app.main:app --reload --port 8000
```

The local API will be available at:

```text
http://localhost:8000
```

Interactive documentation:

```text
http://localhost:8000/docs
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
│   └── src/
│       └── loop/
│           ├── sdk.py
│           ├── interactions.py
│           ├── feedback.py
│           ├── health.py
│           ├── export.py
│           └── stats.py
│
├── openapi/
│   └── openapi.json
│
├── .speakeasy/
│   └── workflow.yaml
│
├── .github/
│   └── workflows/
│       ├── sdk_generation.yaml
│       └── sdk_publish.yaml
│
├── requirements.txt
├── vercel.json
└── README.md
```

### Environment variables

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `LOOP_DEBUG` | No | `false` | Enable SDK debug logging |
| `DATABASE_URL` | No | `sqlite:///./loop.db` | Optional database configuration |

The current stateless API does not require a database for its standard validation and acknowledgement workflow. Database configuration is optional and should not be interpreted as evidence that interaction data is persisted by the hosted service.

---

## SDK generation

Loop's Python SDK is generated using **Speakeasy**.

The OpenAPI specification acts as the source of truth for SDK generation.

Key components:

- `openapi/openapi.json` — API specification.
- `.speakeasy/workflow.yaml` — SDK generation configuration.
- `loop-python/` — Generated Python SDK.
- GitHub Actions — Automated SDK generation and publishing workflows.

Because the SDK is generated programmatically, manual modifications to generated files may be overwritten during regeneration.

---

## Maturity

<sub>Beta software</sub>

Loop is currently in beta. APIs and SDK interfaces may change between releases, including potentially breaking changes.

For applications that depend on Loop, pin your installation to a specific version or Git commit when appropriate.

The project is evolving, and production users should test their integration carefully before relying on it for critical workflows.

---

## Privacy and data handling

Loop is designed around a local-first data model.

- Interaction records are written to the user's local machine.
- Feedback records are written to the user's local machine.
- The hosted API validates requests and returns acknowledgements.
- The standard API workflow does not require user accounts.
- Developers control their local JSONL data.

Local storage location:

```text
~/.loop/
```

Developers remain responsible for protecting local files, managing backups, and avoiding unnecessary personal or sensitive information in prompts, metadata, and feedback.

---

## Contributing

Contributions, bug reports, ideas, and improvements are welcome.

If you find a problem or have an idea for Loop:

1. Open an issue describing the problem or proposal.
2. Include a reproducible example when possible.
3. Submit a pull request with your changes.

Since the Python SDK is generated programmatically, changes to generated files should be made through the appropriate source specification or generation workflow whenever possible.

---

## License

Loop is released under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Loop</strong>
  <br/>
  Close the feedback loop. Build better AI.
  <br/><br/>
  <a href="https://github.com/ahmadjamilofficial/Loop">GitHub Repository</a>
</p>
