# package-architecture Specification

## Purpose
TBD - created by archiving change typewall-project-hardening. Update Purpose after archive.
## Requirements
### Requirement: Layered implementation packages
TypeWall SHALL organize implementation code into `core`, `schemas`, `adapters`, and `integrations` packages whose dependencies flow from core toward optional integrations.

#### Scenario: Core imports without optional frameworks
- **WHEN** `typewall.core` is imported in an environment containing only base dependencies
- **THEN** the import succeeds without importing FastAPI or other optional frameworks

### Requirement: Stable public imports
The root package SHALL expose the same public classes, functions, builders, results, issues, and exceptions, each resolving to the canonical object defined in its layered package.

#### Scenario: Root and canonical object identity
- **WHEN** a public object is imported from the root package and from its canonical layered module
- **THEN** both imports resolve to the identical Python object

### Requirement: Canonical integration paths
Optional framework helpers SHALL be exposed under `typewall.integrations`.

#### Scenario: FastAPI helper canonical path
- **WHEN** `request_body` is imported from `typewall.integrations.fastapi`
- **THEN** the helper is available and preserves the optional-dependency error contract

### Requirement: Isolated module imports
Every public package layer SHALL import successfully in a fresh interpreter under its documented dependency set without circular-import failures.

#### Scenario: Fresh interpreter import sweep
- **WHEN** CI imports each public module in a separate process
- **THEN** all imports complete successfully or produce only the documented missing-extra error

