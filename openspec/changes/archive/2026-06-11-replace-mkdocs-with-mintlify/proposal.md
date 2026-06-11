## Why

The documentation stack (MkDocs Material + mkdocstrings + `mike`) requires
self-managed strict builds, Python autodoc tooling that the packaging guards must
explicitly forbid from base dependencies, and a GitHub Pages release workflow.
Moving to Mintlify gives a hosted, MDX-authored site with platform-native
versioning and a lighter CI gate, removing three Python documentation
dependencies from the project. This is a project-hardening tooling change with no
impact on the TypeWall runtime or any deferred runtime capability.

## What Changes

- Add a Mintlify `docs.json` configuration and convert the 15 existing
  documentation pages from Markdown to MDX (callouts, code fences, links).
- Hand-write the API reference (`reference/api.md`) as static MDX, replacing the
  mkdocstrings `:::` autodoc directives.
- Replace the CI `documentation` gate (`mkdocs build --strict`) with a Node-based
  Mintlify CLI check (`mint broken-links` plus config validation); keep the
  example conformance test.
- **BREAKING (docs delivery):** Replace the `mike` GitHub Pages deploy in
  `docs-release.yml` with Mintlify platform deployment and Mintlify-native
  versioning. The published documentation URL and versioning mechanism change.
- Remove the `mike`, `mkdocs-material`, and `mkdocstrings[python]` dependencies,
  delete `mkdocs.yml`, and update packaging metadata (`pyproject.toml` sdist
  include), release verification (`scripts/verify_release.py`), base-dependency
  guard (`scripts/check_base_dependencies.py`), `README.md`, and the contributing
  guide accordingly.

## Capabilities

### New Capabilities

- *(none)* — this change re-tools an existing capability rather than introducing
  a new one.

### Modified Capabilities

- `project-documentation`: Documentation tooling requirements change from a
  versioned MkDocs site to a Mintlify (MDX + `docs.json`) site with native
  versioning; the API reference becomes a maintained hand-written reference
  instead of mkdocstrings-generated output; and the strict-build gate becomes a
  Mintlify CLI link/config check.

## Impact

- **Removed:** `mkdocs.yml`; `mike`, `mkdocs-material`, `mkdocstrings[python]`
  dependencies (`pyproject.toml` `docs` group).
- **Added:** `docs.json` (Mintlify config); MDX documentation sources.
- **Modified:** `docs/**` (Markdown → MDX); `pyproject.toml` (sdist include);
  `.github/workflows/ci.yml` (`documentation` job); `.github/workflows/docs-release.yml`
  (Mintlify deploy); `scripts/verify_release.py` (required-file set);
  `scripts/check_base_dependencies.py` (forbidden base requirements);
  `README.md` and `docs/development/contributing.md` (build/release instructions).
- **Unaffected:** TypeWall runtime/package, and `tests/conformance/test_examples.py`,
  which continues to validate the runnable examples.
- **Operational:** Connecting the repository to the Mintlify platform (GitHub
  app) is a one-time manual setup performed outside this change.
