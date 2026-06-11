## 1. Mintlify configuration

- [x] 1.1 Add `docs.json` with site name, theme, and navigation groups (Home, Guides, API Reference, Development) mirroring the current MkDocs nav
- [x] 1.2 Configure Mintlify-native `versions` in `docs.json` to replace `mike` versioning

## 2. Documentation content (Markdown → MDX)

- [x] 2.1 Convert `docs/index.md`, `docs/getting-started.md`, and `docs/errors.md` to MDX (callouts, code fences, links)
- [x] 2.2 Convert the 8 `docs/guides/*.md` pages to MDX
- [x] 2.3 Convert the 3 `docs/development/*.md` pages to MDX
- [x] 2.4 Replace `docs/reference/api.md` mkdocstrings `:::` directives with a hand-written MDX API reference covering public builders, schemas, results, issues, exceptions, export functions, adapters, and integrations
- [x] 2.5 Update `docs/development/contributing.md` build/release instructions (remove `mkdocs build`/`mike`, document `mint dev`/`mint broken-links` and Mintlify deploy)

## 3. Remove MkDocs toolchain

- [x] 3.1 Delete `mkdocs.yml`
- [x] 3.2 Remove the `docs` dependency group (`mike`, `mkdocs-material`, `mkdocstrings[python]`) from `pyproject.toml`
- [x] 3.3 Remove `/mkdocs.yml` from the `pyproject.toml` sdist include
- [x] 3.4 Remove the mkdocs* entries from `FORBIDDEN_BASE_REQUIREMENTS` in `scripts/check_base_dependencies.py`
- [x] 3.5 Replace `mkdocs.yml` with `docs.json` in the required-file set in `scripts/verify_release.py`
- [x] 3.6 Update `README.md` documentation build/serve instructions

## 4. CI and release workflows

- [x] 4.1 Update the `documentation` job in `.github/workflows/ci.yml` to set up Node, install the Mintlify CLI, and run `mint broken-links` (plus config validation) instead of `mkdocs build --strict`
- [x] 4.2 Keep `pytest tests/conformance/test_examples.py` in the `documentation` job
- [x] 4.3 Delete the obsolete `mike` GitHub Pages workflow `.github/workflows/docs-release.yml` (Mintlify platform setup and its deploy flow are configured later on the Mintlify platform, not in this change)

## 5. Verification

- [x] 5.1 Run `mint broken-links` (and `mint dev` preview) locally with no broken links or config errors
- [x] 5.2 Run `uv run --frozen pytest tests/conformance/test_examples.py` and confirm it passes
- [x] 5.3 Grep the repo to confirm no remaining references to `mkdocs`, `mkdocstrings`, or `mike` outside `openspec/changes/archive`

## 6. Self-contained `docs/` Mintlify project

- [x] 6.1 Move `docs.json` to `docs/docs.json` and re-path nav entries relative to the new location (drop the `docs/` prefix); fix internal `/docs/...` links
- [x] 6.2 Add `docs/package.json` declaring the pinned `mint` dev dependency with `dev`/`broken-links` scripts
- [x] 6.3 Generate and commit `docs/package-lock.json`; ignore `docs/node_modules/` in `.gitignore`
- [x] 6.4 Update the CI `documentation` job to `npm ci` + `npm run broken-links` in `docs/` (drop global `mint` install)
- [x] 6.5 Update packaging metadata: drop `/docs.json` from the sdist include and require `docs/docs.json` in `scripts/verify_release.py`
- [x] 6.6 Update `README.md` and `docs/development/contributing.md` to run the docs toolchain from `docs/`

## 7. Branding and contribution guide

- [x] 7.1 Add brick-wall + wordmark logo SVGs (`docs/logo/light.svg`, `docs/logo/dark.svg`) and `docs/favicon.svg`
- [x] 7.2 Wire `logo` and `favicon` into `docs/docs.json`
- [x] 7.3 Add a branded README header (logo `<picture>`) and shields.io badges (stars, PyPI, Python versions, license, CI) pointing at `MyGenX/TypeWall`
- [x] 7.4 Surface the GitHub repo + star badge on the docs landing page (`docs/index.md`)
- [x] 7.5 Document the fork → work → open PR → get merged workflow in `docs/development/contributing.md` (`<Steps>`) and a root `CONTRIBUTING.md`
