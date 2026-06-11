# Validation Errors

`Schema.parse()` raises `ValidationError`. Its `issues` tuple retains deterministic traversal order and each `ValidationIssue` includes `path`, `code`, `message`, `expected`, and `received_type` fields.

```python
from typewall import ValidationError, w

schema = w.object({"count": w.int(), "enabled": w.bool()})
try:
    schema.parse({"count": "1", "enabled": 1})
except ValidationError as error:
    assert [issue.path for issue in error.issues] == [("count",), ("enabled",)]
```

Error messages report types and paths without embedding complete rejected values.
