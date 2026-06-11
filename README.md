# TypeWall

TypeWall is a lightweight, schema-first runtime validation library for Python 3.9 through 3.14. It provides strict parsing, deterministic structured errors, immutable schemas, composition, custom processing, type-derived schemas, boundary adapters, and optional FastAPI integration.

## Installation

```shell
pip install typewall
pip install "typewall[fastapi]"  # optional FastAPI integration
```

## Quick Start

```python
from typewall import w

User = w.object({
    "name": w.str().min(2),
    "age": w.int().min(0).optional(),
    "tags": w.list(w.str()).default([]),
})

user = User.parse({"name": "Ada"})
assert user == {"name": "Ada", "tags": []}
```

TypeWall is strict: it does not coerce `"42"` into `42`. Use explicit boundary adapters such as `parse_env()` when text conversion is required.

## Error Inspection

```python
result = User.safe_parse({"name": 42})
if not result.ok:
    for issue in result.errors:
        print(issue.path, issue.code, issue.message)
```

`parse()` raises one `ValidationError` containing every independently reachable issue. `safe_parse()` returns the same ordered issues without raising.

## Integrations

- JSON Schema 2020-12: `to_json_schema(schema)`
- OpenAPI 3.1 schema objects: `to_openapi_schema(schema)`
- Environment mappings: `ObjectSchema.parse_env()`
- CLI: `typewall validate module:attribute [path|-]`
- FastAPI: `typewall.integrations.fastapi.request_body()`

See the [documentation](docs/index.md), [guides](docs/guides/), and [runnable examples](examples/). Development and benchmark commands are documented in [CONTRIBUTING](docs/development/contributing.md).

## Development

```shell
uv sync --all-groups --all-extras --python 3.14
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pyright
uv run mkdocs build --strict
uv run pytest benchmarks --benchmark-only
```

TypeWall is distributed under the MIT license.
