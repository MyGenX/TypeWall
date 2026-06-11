## Context

TypeWall's documentation is currently a MkDocs Material site (`mkdocs.yml`) with
three Python documentation dependencies: `mkdocs-material` (theme/build),
`mkdocstrings[python]` (API autodoc from docstrings), and `mike` (versioned
GitHub Pages deploys). The content is 15 Markdown files under `docs/`, including
`docs/reference/api.md` which uses mkdocstrings `:::` directives to render the API
from the installed package. The toolchain is enforced across several places:
`ci.yml` (`mkdocs build --strict`), `docs-release.yml` (`mike` deploy),
`scripts/verify_release.py` (requires `mkdocs.yml` in the sdist),
`scripts/check_base_dependencies.py` (forbids mkdocs* in base deps), and
`pyproject.toml` (sdist include + `docs` dependency group).

Mintlify is a hosted documentation platform configured by `docs.json`, authored
in MDX, validated/previewed with the Node `mint` CLI, and deployed through a
GitHub-app connection with platform-native versioning. It has no Python autodoc
equivalent to mkdocstrings. This change re-tools documentation only; the TypeWall
runtime, package layout, and example conformance tests are untouched.

## Goals / Non-Goals

**Goals:**
- Replace the MkDocs/mkdocstrings/mike stack with a Mintlify `docs.json` + MDX
  site that covers the same topics and navigation structure.
- Remove all three Python documentation dependencies and every repo reference to
  `mkdocs.yml`, `mkdocs build`, and `mike`.
- Keep a meaningful documentation CI gate (Mintlify CLI link/config check) and
  preserve the existing runnable-example conformance coverage.
- Use Mintlify-native versioning in place of `mike`.

**Non-Goals:**
- No changes to TypeWall's public Python API, error contracts, dependencies, or
  Python 3.9–3.14 compatibility.
- No script-generated API autodoc; the API reference becomes hand-maintained MDX.
- No change to `tests/conformance/test_examples.py` or the examples themselves.
- Performing the one-time Mintlify platform/GitHub-app connection is operational
  setup, not part of this change's code edits.

## Decisions

**1. Hand-written MDX API reference (vs. script-generated autodoc).**
`docs/reference/api.md` mkdocstrings directives become hand-written MDX covering
the public builders, schemas, results, issues, exceptions, export functions,
adapters, and integrations. Rationale: Mintlify has no autodoc; a generation
script (griffe/pdoc → MDX) would add Node-and-Python build coupling for a small,
slow-changing public surface. Trade-off: the reference can drift from source; the
spec requires each documented object to resolve through a supported import path,
and review against the installed package guards this.

**2. Mintlify CLI link check as the CI docs gate (vs. config-only or no gate).**
The `documentation` job in `ci.yml` drops `mkdocs build --strict` and instead
sets up Node, installs the Mintlify CLI, and runs `mint broken-links` (plus
config validation) against the docs. The example conformance test
(`pytest tests/conformance/test_examples.py`) stays. Rationale: keeps a real,
broken-link-catching gate equivalent to the old strict build; alternative
config-only checks would not catch broken internal links.

**3. Mintlify-native versioning (vs. dropping versioning or keeping GitHub Pages).**
`docs.json` declares versions using Mintlify's built-in versioning; the
`mike`-based `docs-release.yml` GitHub Pages deploy is replaced by Mintlify
platform deployment (push-to-deploy via the GitHub app). Rationale: preserves
multi-version docs without maintaining the GitHub Pages branch and `mike`
tooling. This is the **BREAKING** part: the published docs URL and versioning
mechanism change.

**4. Packaging and guard cleanup.**
Remove the `docs` dependency group (`mike`, `mkdocs-material`,
`mkdocstrings[python]`); remove `/mkdocs.yml` from the sdist include and delete
`mkdocs.yml`; in `scripts/verify_release.py` replace `mkdocs.yml` with `docs.json`
in the required-file set; and remove the mkdocs* entries from
`FORBIDDEN_BASE_REQUIREMENTS` in `scripts/check_base_dependencies.py` (those
dependencies no longer exist to forbid). Update `README.md` and
`docs/development/contributing.md` build/release instructions.

**Page mapping (Markdown → MDX, same nav groups):**

| Source | Mintlify page | Nav group |
| --- | --- | --- |
| `docs/index.md` | `index` | Home |
| `docs/getting-started.md` | `getting-started` | Home |
| `docs/errors.md` | `errors` | Home |
| `docs/guides/*.md` (8) | `guides/*` | Guides |
| `docs/reference/api.md` | `reference/api` | API Reference |
| `docs/development/*.md` (3) | `development/*` | Development |

MDX migration notes: MkDocs admonitions (`!!! note`) → Mintlify callout
components (`<Note>`, `<Warning>`, `<Tip>`); `pymdownx.superfences` fenced blocks →
standard MDX code fences; relative `.md` links → Mintlify path-style links.

## Risks / Trade-offs

- **Hand-written API reference drifts from the source package.** → The spec
  requires every documented object to resolve via a supported import path; review
  the reference against the installed package at release time, alongside the
  existing import/example conformance.
- **Node toolchain added to the `documentation` CI job.** → Scoped to that single
  job; the Python test/quality/package jobs are unchanged and gain nothing new.
- **MDX conversion can silently break callouts/links across 15 pages.** → The
  `mint broken-links` gate catches broken links; render-preview each converted
  page with `mint dev` before merge.
- **Versioning/URL change is user-visible (BREAKING).** → Call it out in the
  release notes/CHANGELOG; the Mintlify platform connection and any redirect from
  the old GitHub Pages URL are handled in operational setup.

## Migration Plan

1. Author `docs.json` and convert all pages to MDX; hand-write the API reference.
2. Remove `mkdocs.yml`, the `docs` dep group, and all repo references; update the
   two workflows, the two scripts, README, and contributing guide.
3. Validate locally with `mint dev` / `mint broken-links`; run the example
   conformance test.
4. Connect the repo to Mintlify (GitHub app) — operational, one-time.
5. Rollback: the change is documentation-only and revertable by restoring
   `mkdocs.yml`, the `docs` dependency group, and the original workflow/script
   lines from git history.

## Open Questions

- Final published documentation URL/subdomain on the Mintlify platform (decided
  during operational setup, not blocking artifact implementation).
- Whether to add a redirect from the existing GitHub Pages URL to the new site.
