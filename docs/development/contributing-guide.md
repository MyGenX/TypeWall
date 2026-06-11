---
title: "Contributing"
description: "Local checks and documentation workflow"
---

Synchronize all development groups and extras with `uv sync --all-groups --all-extras`. Required local checks are:

```shell
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pyright
uv run python tests/typing/check_negative.py
uv run pytest --cov=typewall --cov-branch
uv run python -m build
```

Focused tests use `-m unit`, `-m property`, `-m integration`, `-m conformance`, or `-m distribution`. The unfiltered suite remains the authoritative collection gate.

## How to contribute

TypeWall uses a fork-based pull request workflow against [`MyGenX/TypeWall`](https://github.com/MyGenX/TypeWall).

<Steps>
<Step title="Fork the repository">
Fork [`MyGenX/TypeWall`](https://github.com/MyGenX/TypeWall) to your own account and clone your fork (replace `YOUR-USERNAME`):

```shell
git clone https://github.com/YOUR-USERNAME/TypeWall.git
cd TypeWall
git remote add upstream https://github.com/MyGenX/TypeWall.git
```
</Step>
<Step title="Work on a branch">
Create a focused feature branch, make your changes, and run the local checks above until they pass:

```shell
git checkout -b feat/my-change
```
</Step>
<Step title="Open a pull request">
Push the branch to your fork and open a PR against `MyGenX/TypeWall:main`:

```shell
git push origin feat/my-change
```
</Step>
<Step title="Get it merged">
Address review feedback and keep the branch up to date with `upstream/main`. A maintainer merges the PR once checks pass and the review is approved.
</Step>
</Steps>

## Documentation

Documentation is a self-contained [Mintlify](https://mintlify.com) project under `docs/`. Install its toolchain once, then preview the site and check for broken links:

```shell
cd docs
npm install
npm run dev
npm run broken-links
```

<Note>
Published documentation is deployed through the Mintlify platform via its GitHub integration, which manages versioning automatically. There is no manual deploy step in this repository.
</Note>
