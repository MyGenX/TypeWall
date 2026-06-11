## Context

TypeWall currently exposes a stable root API but stores core parsing, schema implementations, adapters, and framework integration in one flat package. Tests are similarly flat, the README still describes integrations as deferred, and CI does not yet verify documentation, benchmark artifacts, dependency boundaries, or all integration scenarios. This change follows the adapter implementation phase and prepares the repository for maintainable public releases while retaining Python 3.9 through 3.14 support.

## Goals / Non-Goals

**Goals:**

- Establish explicit dependency layers for core parsing, schemas, adapters, and optional integrations.
- Preserve root imports and existing direct module imports during the migration.
- Give documentation, examples, benchmarks, and test categories stable repository locations.
- Make documented behavior and distribution artifacts continuously verifiable.
- Add reproducible performance evidence without making noisy timing thresholds a release blocker.

**Non-Goals:**

- Changing parsing, coercion, error ordering, issue paths, or schema semantics.
- Removing legacy import paths in this release.
- Adding integrations beyond the existing environment, CLI, export, and FastAPI adapters.
- Publishing to TestPyPI or PyPI.

## Decisions

1. **Use four implementation layers.** `typewall.core` owns parsing contracts and errors; `typewall.schemas` owns schema types and builders; `typewall.adapters` owns environment, export, and CLI boundaries; `typewall.integrations` owns optional frameworks. Dependencies flow in that order and optional frameworks never enter lower layers. A flat layout was rejected because it obscures dependency ownership as integrations grow.

2. **Preserve old module paths with explicit shims.** Root exports and modules such as `typewall.schema`, `typewall.composition`, and `typewall.fastapi` re-export the relocated objects. Canonical documentation uses the root API and `typewall.integrations.fastapi`. Immediate removal was rejected because direct imports already appear in tests and may exist in early adopters.

3. **Keep compatibility identity, not wrappers.** Shims import the relocated classes and functions directly so old and new paths reference identical objects and exceptions. This avoids divergent `isinstance` behavior.

4. **Organize tests by responsibility.** Unit, property, integration, conformance, distribution, and typing suites receive explicit locations and pytest markers. CI can run focused jobs while a full-suite job prevents marker drift.

5. **Use MkDocs Material and mkdocstrings.** Markdown guides stay approachable while API pages are generated from the installed package. Snippets are mirrored by executable examples and tests; documentation builds treat warnings as failures.

6. **Use pytest-benchmark for measurements.** Benchmarks cover representative success and failure workloads, emit JSON, and record Python, platform, dependency, and configuration metadata. CI uploads results for comparison but does not fail solely on a fixed runtime delta.

7. **Verify built artifacts as products.** Wheel and sdist are installed independently, base dependencies are inspected, CLI and examples run from isolated environments, and project/tag/version consistency is checked before publication workflows can run.

8. **Separate external release operations.** This change supplies release readiness only. Name ownership, credentials, staging publication, and final publication belong to `typewall-0-2-0-release` because they require external state.

## Risks / Trade-offs

- [Compatibility shims increase temporary module count] -> Keep them declarative and test object identity so they can be removed deliberately in a later major release.
- [Moves can introduce circular imports] -> Enforce layer direction and test isolated imports in fresh interpreters.
- [Test reorganization can hide tests from collection] -> Assert expected suite collection and run an unfiltered full suite in CI.
- [Executable documentation can duplicate examples] -> Make files under `examples/` the runnable source and reference or mirror only short snippets in guides.
- [Benchmark results vary by runner] -> Store environment metadata and comparison artifacts without a hard microbenchmark regression threshold.

## Migration Plan

Move modules dependency-first, update internal imports, add compatibility shims, and run API identity plus full regression tests after each layer. Then reorganize tests, add project content, and expand CI. Rollback consists of restoring implementations to the compatibility module paths; no persisted data or user configuration migration is required.

## Open Questions

None. Removal timing for compatibility modules is deferred to a future breaking-change proposal.
