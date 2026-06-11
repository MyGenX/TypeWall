# Environment Parsing

Object schemas can parse a supplied mapping or `os.environ`. Strings remain strings; integers, floats, booleans, and structured JSON use documented canonical conversions.

```python
from typewall import w

Settings = w.object({"PORT": w.int(), "DEBUG": w.bool().default(False)})
assert Settings.parse_env({"PORT": "8000", "DEBUG": "true"}) == {
    "PORT": 8000,
    "DEBUG": True,
}
```

Conversion errors identify the variable path without echoing its complete raw value.
