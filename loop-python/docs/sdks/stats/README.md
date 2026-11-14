# Stats

## Overview

SDK-computed stats echoed back for validation.

### Available Operations

* [echo_stats](#echo_stats) - Echo stats summary

## echo_stats

The SDK computes stats from local storage and POSTs them here for validation. The server echoes the summary back. Nothing is stored.

Used by the `loop stats` CLI command to display a validated summary.

### Example Usage

<!-- UsageSnippet language="python" operationID="echo_stats" method="post" path="/v1/stats" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.stats.echo_stats(total_interactions=142, total_feedback=98, thumbs_up=71, thumbs_down=27, with_correction=19, without_correction=8, models=[
        "my-model-v1",
        "my-model-v2",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `total_interactions`                                                | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `total_feedback`                                                    | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `thumbs_up`                                                         | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `thumbs_down`                                                       | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `with_correction`                                                   | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `without_correction`                                                | *int*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `models`                                                            | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.EchoStatsResponse](../../models/echostatsresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 422                     | application/json        |
| errors.LoopDefaultError | 4XX, 5XX                | \*/\*                   |