# InteractionBatchAck


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `ids`                                                      | List[*str*]                                                | :heavy_check_mark:                                         | Confirmed IDs in the same order as the input interactions. |
| `count`                                                    | *int*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `stored`                                                   | *Literal[False]*                                           | :heavy_check_mark:                                         | N/A                                                        |