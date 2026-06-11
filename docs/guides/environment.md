---
title: "Environment Parsing"
description: "Parse mappings or os.environ with canonical conversions"
---

Object schemas can parse a supplied mapping or `os.environ`. Strings remain strings; integers, floats, booleans, and structured JSON use documented canonical conversions.

```python
from typewall import w

Settings = w.object({"PORT": w.int(), "DEBUG": w.bool().default(False)})
assert Settings.parse_env({"PORT": "8000", "DEBUG": "true"}) == {
    "PORT": 8000,
    "DEBUG": True,
}
```

<Warning>
Conversion errors identify the variable path without echoing its complete raw value.
</Warning>
