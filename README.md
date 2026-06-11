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

TypeWall supports strict string, integer, float, boolean, object, and list schemas;
required, optional, and defaulted fields; constraints, composition, transforms,
type-derived schemas, and structured validation errors. It does not coerce values.
Schema export, environment parsing, CLI tools, and framework integrations are
intentionally deferred to later phases.

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

## Constraints

```python
Account = w.object({
    "name": w.str().min(2).max(80),
    "email": w.str().email(),
    "homepage": w.str().url().optional(),
    "age": w.int().min(18),
})
```

String constraints include length, email, URL, UUID, and regex validation. Integer
and float schemas support inclusive ranges plus positive and negative checks.
Constraint declarations are available as immutable `schema.rules`; each rule exposes
stable `metadata` for the later schema-export phase.

## Composition

```python
Identifier = w.union((w.int(), w.str().uuid()))
Coordinates = w.tuple((w.float(), w.float()))
Labels = w.dict(w.str(), w.int())
Role = w.enum(["admin", "user"])
```

TypeWall also provides literals, intersections, nullable schemas, `w.any()`, and
`w.none()`. Union failures retain per-branch issues, and transformed dictionary keys
cannot silently overwrite an existing parsed key.

## Custom Processing

```python
NormalizedName = (
    w.str()
    .refine(str.strip, "Name must not be empty", code="empty_name")
    .transform(str.strip)
)
```

Refinements run after built-in validation. Transforms run only after every validation
and refinement succeeds. These callbacks are runtime behavior and cannot be exported
accurately as JSON Schema without explicit metadata in a future integration phase.

## Python Types

```python
from dataclasses import dataclass
from typing import TypedDict

from typewall import schema_from_type


class UserInput(TypedDict):
    name: str
    age: int


@dataclass
class User:
    name: str
    age: int = 18


InputSchema = schema_from_type(UserInput)
UserSchema = schema_from_type(User)
```

`schema_from_type()` supports primitives, `Any`, `None`, lists, dictionaries, fixed
tuples, unions, optionals, literals, TypedDict declarations, dataclasses, and supported
recursive declarations. Unsupported annotations fail during schema construction with
the annotation path.

## Typing Contract

MyPy and Pyright verify the same conservative output-type contract. Primitive,
collection, literal, tuple, union, nullable, transformed, and dataclass-derived schemas
preserve their parsed output types. Manually declared `w.object()` schemas currently
return `dict[str, Any]`; exact dictionary-shape inference is deferred.

## Export Metadata

Constraint rules expose serializable metadata. Composition schemas expose their
declared literals, enum values, item schemas, members, or wrapped schema. Custom
refinements and transforms contain arbitrary Python callbacks and must be treated as
non-representable by schema exporters unless a later API supplies explicit metadata.

## Development

TypeWall uses `uv` and supports CPython 3.9 through 3.14.

```shell
UV_CACHE_DIR=.uv-cache uv sync --python 3.14
UV_CACHE_DIR=.uv-cache uv run pytest
UV_CACHE_DIR=.uv-cache uv run ruff check .
UV_CACHE_DIR=.uv-cache uv run mypy
UV_CACHE_DIR=.uv-cache uv run pyright
UV_CACHE_DIR=.uv-cache uv run python tests/typing/check_negative.py
```
