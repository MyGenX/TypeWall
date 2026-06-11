# Constraints

String schemas support length, email, URL, UUID, and regex constraints. Numeric schemas support inclusive ranges plus positive and negative checks.

```python
from typewall import w

Account = w.object({
    "email": w.str().email(),
    "age": w.int().min(18),
    "score": w.float().min(0.0).max(1.0),
})
```

Constraint builders return new schemas; the original schema remains unchanged.
