## Why

After the core runtime and validation language are stable, TypeWall needs boundary adapters, machine-readable schema export, framework integration, and release automation to be useful as a public package. Keeping these concerns in a final phase prevents external systems from constraining the core API prematurely.

## What Changes

- Add JSON Schema export and an OpenAPI-compatible schema representation for supported TypeWall schemas.
- Add environment-variable parsing with explicit coercion rules and source-aware errors.
- Add a CLI that validates JSON input and reports machine-readable or human-readable failures with meaningful exit codes.
- Add an optional FastAPI integration for request validation and OpenAPI participation without making FastAPI a core dependency.
- Add public documentation, examples, packaging metadata, CI, compatibility tests, benchmarks, and reproducible `0.2.0` release readiness.
- Require `typewall-core-mvp` and `typewall-validation-enhancements` to be implemented first.

## Capabilities

### New Capabilities

- `schema-export`: JSON Schema and OpenAPI-compatible export for supported schemas and constraints.
- `environment-parsing`: Environment mapping validation with explicit coercion, defaults, optional values, and path-aware failures.
- `validation-cli`: Command-line validation of JSON documents with stable output modes and exit codes.
- `fastapi-integration`: Optional FastAPI request validation and schema integration.
- `package-release`: Installable package metadata, documentation, CI quality gates, benchmarks, and release verification.

### Modified Capabilities

None. This phase consumes the stable contracts established by the prior changes.

## Impact

- Adds optional dependency groups for CLI and FastAPI features while preserving a lightweight core install.
- Introduces serialization/export modules, adapters, command entry points, documentation, CI workflows, and release tooling.
- Defines public compatibility expectations for the first PyPI release.
