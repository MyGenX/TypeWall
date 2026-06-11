---
title: "TypeWall"
description: "Strict schema-first runtime validation for Python"
---

<p><a href="https://github.com/MyGenX/TypeWall" target="_blank"><img src="https://img.shields.io/github/stars/MyGenX/TypeWall?style=flat&logo=github&color=2563EB" alt="GitHub stars" /></a> <a href="https://pypi.org/project/typewall/" target="_blank"><img src="https://img.shields.io/pypi/v/typewall?color=2563EB" alt="PyPI version" /></a> <a href="https://pypi.org/project/typewall/" target="_blank"><img src="https://img.shields.io/pypi/pyversions/typewall?color=2563EB" alt="Python versions" /></a> <a href="https://github.com/MyGenX/TypeWall/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/github/license/MyGenX/TypeWall?color=2563EB" alt="License" /></a></p>

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

Start with [Getting Started](/getting-started), then use the focused guides or [API Reference](/reference/api).

<Card title="MyGenX/TypeWall on GitHub" icon="github" href="https://github.com/MyGenX/TypeWall">
  Star the repository, browse the source, and open issues or pull requests.
</Card>

