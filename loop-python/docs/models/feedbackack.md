# FeedbackAck


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `id`                                                       | *str*                                                      | :heavy_check_mark:                                         | Generated feedback ID.                                     |
| `interaction_id`                                           | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `rating`                                                   | [models.FeedbackAckRating](../models/feedbackackrating.md) | :heavy_check_mark:                                         | N/A                                                        |
| `has_correction`                                           | *bool*                                                     | :heavy_check_mark:                                         | True if a correction was provided.                         |
| `stored`                                                   | *Literal[False]*                                           | :heavy_check_mark:                                         | N/A                                                        |