# Format

## Example Usage

```python
from loop.models import Format

# Open enum: unrecognized values are captured as UnrecognizedStr
value: Format = "chat_jsonl"
```


## Values

This is an open enum. Unrecognized values will not fail type checks.

- `"chat_jsonl"`
- `"alpaca_jsonl"`
- `"dpo_jsonl"`
