````markdown
# TypeWall

## Project Idea

**TypeWall** is a Python runtime validation library inspired by TypeScript tools like **Zod**, **Joi**, and similar schema validators.

The goal is not to copy TypeScript APIs directly, but to bring the same developer experience into Python in a way that feels natural, readable, and Pythonic.

```python
from typewall import w

UserSchema = w.object({
    "name": w.str().min(2),
    "email": w.str().email(),
    "age": w.int().min(18),
})

user = UserSchema.parse(payload)
````

---

## Where the Idea Comes From

Modern TypeScript validation libraries are popular because they provide:

* Simple schema declaration
* Runtime validation
* Type-safe parsing
* Clear validation errors
* Composable validators
* Good developer experience

Python already has strong tools like **Pydantic**, **Marshmallow**, and **Cerberus**, but TypeWall can target a slightly different style:

> Lightweight, chainable, schema-first validation without requiring model classes.

---

## Core Concept

TypeWall validates data at the boundary of the application.

Common use cases:

* API request validation
* Config validation
* Environment variable validation
* CLI input validation
* Webhook payload validation
* Data pipeline validation
* LLM/tool input validation

Example:

```python
from typewall import w

Config = w.object({
    "DATABASE_URL": w.str().url(),
    "DEBUG": w.bool().default(False),
    "PORT": w.int().min(1).max(65535),
})

config = Config.parse_env()
```

---

## Pythonic Design Direction

### 1. Use `w` as the Main Builder

Inspired by Zod’s `z`, but adapted to the TypeWall brand.

```python
from typewall import w

schema = w.str().min(3).max(50)
```

Also support a clearer alias:

```python
from typewall import tw
```

But documentation should prefer:

```python
from typewall import w
```

---

### 2. Use Python Naming Conventions

Avoid TypeScript-style names where Python has better conventions.

Prefer:

```python
w.str()
w.int()
w.bool()
w.list()
w.dict()
```

Instead of:

```python
w.string()
w.number()
w.boolean()
w.array()
```

Optional aliases can exist, but the default API should feel Python-native.

---

### 3. Support Both Dict-Based and TypedDict-Like Validation

Simple schema-first style:

```python
User = w.object({
    "id": w.uuid(),
    "name": w.str(),
    "email": w.str().email(),
})
```

Later, support Python typing integration:

```python
from typing import TypedDict
from typewall import schema_from_type

class UserInput(TypedDict):
    name: str
    email: str
    age: int

User = schema_from_type(UserInput)
```

---

### 4. Prefer `parse()` and `safe_parse()`

```python
user = User.parse(data)
```

Raises validation error.

```python
result = User.safe_parse(data)

if result.ok:
    user = result.data
else:
    print(result.errors)
```

This keeps the API familiar but still clean in Python.

---

### 5. Rich Pythonic Errors

Validation errors should be structured and easy to inspect.

```python
try:
    User.parse(data)
except ValidationError as error:
    print(error.to_dict())
```

Example error format:

```python
{
    "email": ["Invalid email address"],
    "age": ["Expected int, got str"]
}
```

For nested objects:

```python
{
    "profile.address.city": ["Required field missing"]
}
```

---

## Example API

```python
from typewall import w

User = w.object({
    "id": w.uuid(),
    "name": w.str().min(2),
    "email": w.str().email(),
    "age": w.int().min(18),
    "tags": w.list(w.str()).default([]),
    "is_active": w.bool().default(True),
})

data = User.parse({
    "id": "8d74b7d1-0f36-42da-a5fc-f24e5827d1c3",
    "name": "John",
    "email": "john@example.com",
    "age": 24,
})
```

---

## Possible Validators

### Primitive Validators

```python
w.str()
w.int()
w.float()
w.bool()
w.none()
w.any()
```

### String Validators

```python
w.str().min(2)
w.str().max(100)
w.str().email()
w.str().url()
w.str().regex(...)
w.str().uuid()
```

### Number Validators

```python
w.int().min(1)
w.int().max(100)
w.float().positive()
w.float().negative()
```

### Collection Validators

```python
w.list(w.str())
w.dict(w.str(), w.int())
w.tuple([w.str(), w.int()])
```

### Object Validators

```python
w.object({
    "name": w.str(),
    "age": w.int().optional(),
})
```

### Utility Validators

```python
w.literal("admin")
w.enum(["admin", "user", "guest"])
w.union([w.str(), w.int()])
w.optional(w.str())
w.nullable(w.str())
```

---

## Implementation Ideas

### 1. Base Schema Class

Every validator can inherit from a base `Schema` class.

```python
class Schema:
    def parse(self, value):
        ...

    def safe_parse(self, value):
        ...

    def optional(self):
        ...

    def default(self, value):
        ...
```

---

### 2. Chainable Rule System

Each schema keeps a list of validation rules.

```python
w.str().min(2).max(20).email()
```

Internally:

```python
StringSchema(
    rules=[
        MinLengthRule(2),
        MaxLengthRule(20),
        EmailRule(),
    ]
)
```

---

### 3. Result Object for Safe Parsing

```python
result = schema.safe_parse(data)

if result.ok:
    result.data
else:
    result.errors
```

Possible implementation:

```python
@dataclass
class ParseResult:
    ok: bool
    data: Any = None
    errors: list[ValidationIssue] = field(default_factory=list)
```

---

### 4. Error Path Tracking

Each validation error should know where it happened.

```python
ValidationIssue(
    path=["user", "email"],
    message="Invalid email address",
    expected="email",
    received="not-an-email",
)
```

This allows clean output:

```python
"user.email": "Invalid email address"
```

---

## Implementation Phases

## Phase 1 — Core MVP

Goal: Basic usable validation library.

Features:

* `w.str()`
* `w.int()`
* `w.float()`
* `w.bool()`
* `w.object()`
* `w.list()`
* `parse()`
* `safe_parse()`
* Basic error handling
* Required/optional fields
* Default values

Example target:

```python
User = w.object({
    "name": w.str(),
    "age": w.int().optional(),
})
```

---

## Phase 2 — Common Validation Rules

Goal: Make it useful for real API/config validation.

Add:

* String min/max
* Number min/max
* Email validation
* URL validation
* UUID validation
* Regex validation
* Enum/literal validation
* Better nested error messages

---

## Phase 3 — Advanced Composition

Goal: Support complex schemas.

Add:

* `w.union()`
* `w.intersection()`
* `w.tuple()`
* `w.dict()`
* `w.nullable()`
* `w.any()`
* Custom validators
* Transform hooks

Example:

```python
UserId = w.union([
    w.int(),
    w.str().uuid(),
])
```

---

## Phase 4 — Python Typing Integration

Goal: Make TypeWall work better with Python’s type system.

Add:

* Type hints for schema output
* `schema_from_type()`
* TypedDict support
* Dataclass support
* Better IDE/autocomplete experience
* MyPy/Pyright-friendly typing where possible

---

## Phase 5 — Developer Experience

Goal: Make the library pleasant to use.

Add:

* Beautiful error formatting
* JSON schema export
* OpenAPI-compatible schema export
* CLI validator
* Environment variable parser
* FastAPI helper integration

Example:

```python
from typewall.integrations.fastapi import validate_body
```

---

## Phase 6 — Packaging and Release

Goal: Prepare for public usage.

Tasks:

* Create PyPI package `typewall`
* Add README with examples
* Add documentation site
* Add GitHub Actions CI
* Add unit tests
* Add benchmark tests
* Publish `0.1.0`

---

## Suggested Package Identity

```text
Package name: typewall
Import API: from typewall import w
Tagline: Runtime type validation for Python
```

Alternative tagline:

```text
A Pythonic schema validation toolkit inspired by Zod and Joi.
```

---

## MVP Scope

For the first version, keep it small:

```python
from typewall import w

User = w.object({
    "name": w.str().min(2),
    "email": w.str().email(),
    "age": w.int().min(18),
})

result = User.safe_parse(payload)
```

The MVP should focus on being:

* Small
* Fast
* Easy to read
* Easy to test
* Pythonic
* Useful without framework dependency

```
```
