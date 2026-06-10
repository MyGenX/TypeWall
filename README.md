# TypeWall

Runtime type validation for Python with a small, schema-first API.

```python
from typewall import w

User = w.object({
    "name": w.str(),
    "age": w.int().optional(),
    "tags": w.list(w.str()).default([]),
})

user = User.parse({"name": "Ada"})
assert user == {"name": "Ada", "tags": []}
```

Use `safe_parse()` when validation failures should be returned instead of raised:

```python
result = User.safe_parse({"name": 42})

if not result.ok:
    print(result.to_dict())
```

The MVP supports strict string, integer, float, boolean, object, and list schemas;
required, optional, and defaulted fields; and structured validation errors. It does
not coerce values. Constraints, advanced composition, transforms, type-derived
schemas, schema export, environment parsing, CLI tools, and framework integrations
are intentionally deferred to later phases.

## MVP Public API

- Builders: `w`, `tw`, and `SchemaBuilder`
- Schemas: `Schema`, `StringSchema`, `IntegerSchema`, `FloatSchema`,
  `BooleanSchema`, `ObjectSchema`, and `ListSchema`
- Parsing: `Schema.parse()` and `Schema.safe_parse()`
- Field configuration: `Schema.optional()` and `Schema.default()`
- Results and errors: `ParseResult`, `ValidationIssue`, and `ValidationError`

MVP object schemas reject unknown keys, omit absent optional fields, defensively
copy defaults, and aggregate independently reachable issues in deterministic order.
The error dictionary uses `$` for root failures and dot-delimited paths for nested
fields and list indexes.

## Development

TypeWall uses `uv` and supports CPython 3.9 through 3.14.

```shell
UV_CACHE_DIR=.uv-cache uv sync --python 3.14
UV_CACHE_DIR=.uv-cache uv run pytest
UV_CACHE_DIR=.uv-cache uv run ruff check .
UV_CACHE_DIR=.uv-cache uv run mypy
```
