# Contributing

Synchronize all development groups and extras with `uv sync --all-groups --all-extras`. Required local checks are:

```shell
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pyright
uv run python tests/typing/check_negative.py
uv run pytest --cov=typewall --cov-branch
uv run mkdocs build --strict
uv run python -m build
```

Focused tests use `-m unit`, `-m property`, `-m integration`, `-m conformance`, or `-m distribution`. The unfiltered suite remains the authoritative collection gate.

Published releases deploy immutable documentation versions with `mike` and update the `latest` alias through the documentation release workflow.
