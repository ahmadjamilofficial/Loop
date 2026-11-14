# Interactions

## Overview

Log prompt/response pairs. The server validates and returns a confirmed ID. The SDK writes locally.

### Available Operations

* [log_interaction](#log_interaction) - Log an interaction
* [log_interactions_batch](#log_interactions_batch) - Log a batch of interactions

## log_interaction

Validates a prompt/response pair and returns a confirmed ID.

The server stores nothing. The SDK writes this record to ~/.loop/interactions.jsonl before or after calling this endpoint.

Supply your own `id` (any string, UUID recommended) so the SDK can reference it immediately in feedback() without waiting for the network.

### Example Usage

<!-- UsageSnippet language="python" operationID="log_interaction" method="post" path="/v1/interactions" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.interactions.log_interaction(prompt="What is the capital of Pakistan?", response="Islamabad", id="int_a1b2c3d4", model="my-model-v1", metadata={
        "user_tier": "free",
    }, session_id="sess_abc123")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                               | Type                                                                                                    | Required                                                                                                | Description                                                                                             |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `prompt`                                                                                                | [models.Prompt](../../models/prompt.md)                                                                 | :heavy_check_mark:                                                                                      | Plain string or list of chat messages.                                                                  |
| `response`                                                                                              | *str*                                                                                                   | :heavy_check_mark:                                                                                      | The model's response.                                                                                   |
| `id`                                                                                                    | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Client-generated ID. Recommended: use a UUID prefixed with 'int_'. If omitted the server generates one. |
| `model`                                                                                                 | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Model name or version identifier. Used to filter exports by model.                                      |
| `metadata`                                                                                              | Dict[str, *Any*]                                                                                        | :heavy_minus_sign:                                                                                      | Any extra key/value pairs you want to attach.                                                           |
| `session_id`                                                                                            | *OptionalNullable[str]*                                                                                 | :heavy_minus_sign:                                                                                      | Groups multiple interactions into a conversation.                                                       |
| `timestamp`                                                                                             | [date](https://docs.python.org/3/library/datetime.html#date-objects)                                    | :heavy_minus_sign:                                                                                      | Defaults to current UTC time if omitted.                                                                |
| `retries`                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                        | :heavy_minus_sign:                                                                                      | Configuration to override the default retry behavior of the client.                                     |

### Response

**[models.LogInteractionResponse](../../models/loginteractionresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 422                     | application/json        |
| errors.LoopDefaultError | 4XX, 5XX                | \*/\*                   |

## log_interactions_batch

Validates up to 100 interactions in one call and returns their confirmed IDs in order.

### Example Usage

<!-- UsageSnippet language="python" operationID="log_interactions_batch" method="post" path="/v1/interactions/batch" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.interactions.log_interactions_batch(interactions=[])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `interactions`                                                      | List[[models.InteractionCreate](../../models/interactioncreate.md)] | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.LogInteractionsBatchResponse](../../models/loginteractionsbatchresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 422                     | application/json        |
| errors.LoopDefaultError | 4XX, 5XX                | \*/\*                   |