# Health

## Overview

API connectivity check.

### Available Operations

* [health](#health) - Health check

## health

Returns API status and version. Use this to verify connectivity.

### Example Usage

<!-- UsageSnippet language="python" operationID="health" method="get" path="/v1/health" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.health.health()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.HealthResponseResponse](../../models/healthresponseresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.LoopDefaultError | 4XX, 5XX                | \*/\*                   |