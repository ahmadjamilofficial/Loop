# Feedback

## Overview

Submit user reactions (like/dislike + optional correction). The server validates and acks. The SDK writes locally.

### Available Operations

* [submit_feedback](#submit_feedback) - Submit feedback

## submit_feedback

Records a user's reaction to a model response.

`rating` must be `up` (the response was good) or `down` (the response was bad).

If the model was wrong, pass the correct answer in `correction`. It becomes the target response for fine-tuning: the `chosen` side of a DPO pair, or the gold label in supervised fine-tuning.

The server validates and acks. The SDK writes the record to ~/.loop/feedback.jsonl.

### Example Usage: thumbs_down_with_correction

<!-- UsageSnippet language="python" operationID="submit_feedback" method="post" path="/v1/feedback" example="thumbs_down_with_correction" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.feedback.submit_feedback(interaction_id="int_a1b2c3d4", rating="down", correction="The capital of Pakistan is Islamabad.", comment="Response was missing context.")

    # Handle response
    print(res)

```
### Example Usage: thumbs_up

<!-- UsageSnippet language="python" operationID="submit_feedback" method="post" path="/v1/feedback" example="thumbs_up" -->
```python
from loop import Loop


with Loop() as l_client:

    res = l_client.feedback.submit_feedback(interaction_id="int_a1b2c3d4", rating="up")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                    | Type                                                                                                         | Required                                                                                                     | Description                                                                                                  |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `interaction_id`                                                                                             | *str*                                                                                                        | :heavy_check_mark:                                                                                           | ID returned by log_interaction or log_interactions_batch.                                                    |
| `rating`                                                                                                     | [models.FeedbackCreateRating](../../models/feedbackcreaterating.md)                                          | :heavy_check_mark:                                                                                           | 'up' means the response was good. 'down' means the response was bad.                                         |
| `correction`                                                                                                 | *OptionalNullable[str]*                                                                                      | :heavy_minus_sign:                                                                                           | The correct answer. Used as the training target. For DPO: becomes 'chosen'. For SFT: becomes the gold label. |
| `comment`                                                                                                    | *OptionalNullable[str]*                                                                                      | :heavy_minus_sign:                                                                                           | Free-text comment from the user.                                                                             |
| `user_id`                                                                                                    | *OptionalNullable[str]*                                                                                      | :heavy_minus_sign:                                                                                           | Anonymised user identifier. Never use real PII here.                                                         |
| `retries`                                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                             | :heavy_minus_sign:                                                                                           | Configuration to override the default retry behavior of the client.                                          |

### Response

**[models.SubmitFeedbackResponse](../../models/submitfeedbackresponse.md)**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ErrorResponse    | 422                     | application/json        |
| errors.LoopDefaultError | 4XX, 5XX                | \*/\*                   |