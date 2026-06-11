## Context

This phase depends on stable runtime and enhancement APIs. It exposes TypeWall at application boundaries and prepares the project for public distribution while keeping integrations optional and core parsing independent.

## Goals / Non-Goals

**Goals:**

- Export supported schemas to machine-readable contracts.
- Validate environment and command-line JSON inputs with explicit conversion behavior.
- Integrate cleanly with FastAPI without requiring it for core users.
- Prepare a reproducible, documented, tested `0.2.0` package.

**Non-Goals:**

- Supporting every JSON Schema dialect or web framework.
- Reading secrets from remote stores or managing `.env` files directly.
- Generating application code from schemas.
- Guaranteeing backward compatibility beyond the documented `0.x` policy.

## Decisions

1. **Target JSON Schema 2020-12 and OpenAPI 3.1-compatible schema objects.** OpenAPI 3.1 aligns closely with modern JSON Schema, reducing duplicate mapping logic. Earlier OpenAPI dialects are out of scope.

2. **Use a visitor over schema metadata for export.** Runtime schemas remain the source of truth. Non-representable refinements and transforms fail export explicitly unless a documented metadata override is supplied.

3. **Keep environment coercion adapter-specific.** `ObjectSchema.parse_env()` reads a supplied mapping or `os.environ`, converts documented primitive text forms, then delegates to normal parsing. Core `parse()` remains strict.

4. **Treat environment values as sensitive in failures.** Errors identify variable names, expected types, and parse reasons but do not echo complete values by default.

5. **Expose a schema import target in the CLI.** `typewall validate module:attribute [path|-]` loads a schema, reads JSON, validates it, and emits either human or JSON output. Stable exit codes distinguish valid input, validation failure, and invocation/load errors.

6. **Implement FastAPI as an optional extra.** Integration modules import FastAPI lazily and provide a dependency/helper that maps TypeWall paths into FastAPI's 422 detail shape and contributes exported schemas to OpenAPI.

7. **Use a single PEP 517 package with optional dependency groups.** The base install contains only core runtime requirements; integrations are installed through extras. Wheel and sdist contents are verified in CI.

8. **Make release checks reproducible.** CI runs unit, integration, typing, lint, package-build, install-from-artifact, documentation, and CLI smoke tests across supported Python versions. Benchmarks record trends but do not use an unstable microbenchmark threshold as the sole release gate.

## Risks / Trade-offs

- [Runtime behavior may not be representable in JSON Schema] -> Fail loudly and document metadata escape hatches instead of publishing misleading contracts.
- [Importing arbitrary CLI schema targets executes module code] -> Document the trust boundary and never treat untrusted schema modules as sandboxed.
- [Environment coercion can hide configuration mistakes] -> Support only explicit canonical forms and report source-aware failures.
- [FastAPI changes independently] -> Pin a tested compatibility range for the optional extra and run integration tests against supported versions.
- [Package name availability or publishing credentials may block release] -> Verify ownership before release and keep build/signing/publishing steps separable.

## Migration Plan

Implement schema export first because FastAPI depends on it, followed by environment parsing and CLI, then FastAPI. Finish documentation and release automation only after all adapter conformance tests pass. Build release candidates from clean tags and verify installation from both wheel and sdist before publishing.

## Open Questions

- Confirm PyPI ownership and availability for the `typewall` distribution name before publication.
- Choose the documentation site generator based on maintenance cost and API reference support.
