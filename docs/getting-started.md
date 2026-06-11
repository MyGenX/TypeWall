---
title: "Getting Started"
description: "Install TypeWall and build your first schema"
---

Install the core package with `pip install typewall`. Install `typewall[fastapi]` only when the FastAPI helper is needed.

Schemas are built from `w` (or its alias `tw`) and return parsed values:

```python
from typewall import w

User = w.object({"name": w.str(), "roles": w.list(w.str()).default([])})
assert User.parse({"name": "Ada"}) == {"name": "Ada", "roles": []}
```

<Note>
Use `safe_parse()` when validation failures are expected control flow. TypeWall does not coerce primitive input; adapters perform only their documented boundary conversions.
</Note>
