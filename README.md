<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo/dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo/light.svg">
    <img alt="TypeWall" src="docs/logo/light.svg" width="280">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/MyGenX/TypeWall"><img alt="GitHub stars" src="https://img.shields.io/github/stars/MyGenX/TypeWall?style=flat&logo=github&color=2563EB"></a>
  <a href="https://pypi.org/project/typewall/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/typewall?color=2563EB"></a>
  <a href="https://pypi.org/project/typewall/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/typewall?color=2563EB"></a>
  <a href="https://github.com/MyGenX/TypeWall/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/MyGenX/TypeWall?color=2563EB"></a>
  <a href="https://github.com/MyGenX/TypeWall/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/MyGenX/TypeWall/ci.yml?branch=main&label=CI"></a>
</p>

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

See the [documentation](docs/index.md), [guides](docs/guides/), and [runnable examples](examples/). The documentation site is a self-contained [Mintlify](https://mintlify.com) project under `docs/`; preview it locally with `cd docs && npm install && npm run dev`. Development and benchmark commands are documented in the [contributing guide](docs/development/contributing-guide.md).

## Development

```shell
uv sync --all-groups --all-extras --python 3.14
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pyright
uv run pytest benchmarks --benchmark-only
```

## Contributing

Contributions go through a fork-based pull request workflow:

1. **Fork** [`MyGenX/TypeWall`](https://github.com/MyGenX/TypeWall) to your account.
2. **Work** on a feature branch in your fork, running the local checks above.
3. **Open a PR** from your branch against `MyGenX/TypeWall:main`.
4. Address review feedback and **get it merged**.

See [CONTRIBUTING.md](CONTRIBUTING.md) and the [contributing guide](docs/development/contributing-guide.md) for the full workflow and required checks.

TypeWall is distributed under the MIT license.
