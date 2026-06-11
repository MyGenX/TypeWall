# Custom Processing

Refinements run after built-in validation. Transforms run only after all validation and refinements succeed.

```python
from typewall import w

Name = w.str().refine(lambda value: bool(value.strip()), "Name is empty").transform(str.strip)
assert Name.parse("  Ada  ") == "Ada"
```

Arbitrary callbacks cannot be represented faithfully in JSON Schema unless explicit export metadata is supplied.
