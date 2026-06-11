# TypeWall

TypeWall validates Python values with immutable, reusable schemas. Parsing is strict, errors are structured and deterministic, and framework integrations remain optional.

```python
from typewall import w

Config = w.object({
    "host": w.str(),
    "port": w.int().min(1).max(65535),
    "debug": w.bool().default(False),
})

config = Config.parse({"host": "localhost", "port": 8000})
```

Start with [Getting Started](getting-started.md), then use the focused guides or [API Reference](reference/api.md).
