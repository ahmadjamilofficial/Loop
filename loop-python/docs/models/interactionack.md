# InteractionAck


## Fields

| Field                                                                     | Type                                                                      | Required                                                                  | Description                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `id`                                                                      | *str*                                                                     | :heavy_check_mark:                                                        | The confirmed interaction ID. Pass this to feedback().                    |
| `timestamp`                                                               | [date](https://docs.python.org/3/library/datetime.html#date-objects)      | :heavy_check_mark:                                                        | N/A                                                                       |
| `stored`                                                                  | *Literal[False]*                                                          | :heavy_check_mark:                                                        | Always false. The server stores nothing. The SDK writes to local storage. |