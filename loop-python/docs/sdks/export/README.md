# Export

## Overview

Describes the fine-tuning export formats. The SDK exports from local storage — no data passes through the server.

### Available Operations

* [export_formats](#export_formats) - List export formats

## export_formats

Returns the schemas for each supported fine-tuning export format.

The SDK uses these schemas when it exports from local storage. No data is sent to or from the server — this endpoint just describes the wire format so the SDK can write correct files.

### Example Usage

<!-- UsageSnippet language="python" operationID="export_formats" method="get" path="/v1/export/formats" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.export.export_formats()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ExportFormatsResponseResponse](../../models/exportformatsresponseresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.LoopDefaultError | 4XX, 5XX                | \*/\*                   |