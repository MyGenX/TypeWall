# Contributing to TypeWall

Thanks for your interest in improving TypeWall! Contributions go through a
fork-based pull request workflow against
[`MyGenX/TypeWall`](https://github.com/MyGenX/TypeWall).

## Workflow: fork → work → open PR → get merged

1. **Fork** [`MyGenX/TypeWall`](https://github.com/MyGenX/TypeWall) to your account
   and clone your fork:

   ```shell
   git clone https://github.com/<your-username>/TypeWall.git
   cd TypeWall
   git remote add upstream https://github.com/MyGenX/TypeWall.git
   ```

2. **Work** on a focused feature branch in your fork:

   ```shell
   git checkout -b feat/my-change
   ```

   Make your changes and run the local checks below until they pass.

3. **Open a pull request** by pushing your branch to your fork and opening a PR
   against `MyGenX/TypeWall:main`:

   ```shell
   git push origin feat/my-change
   ```

4. **Get it merged** — address review feedback and keep your branch up to date
   with `upstream/main`. A maintainer merges the PR once checks pass and the
   review is approved.

## Local checks

Synchronize all development groups and extras, then run the required checks:

```shell
uv sync --all-groups --all-extras
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pyright
uv run python tests/typing/check_negative.py
uv run pytest --cov=typewall --cov-branch
uv run python -m build
```

Documentation is a self-contained [Mintlify](https://mintlify.com) project under
`docs/`; preview it with `cd docs && npm install && npm run dev` and check links
with `npm run broken-links`.

See the [contributing guide](docs/development/contributing-guide.md) for the full
details.
