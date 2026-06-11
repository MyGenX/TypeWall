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
The root package and legacy direct module paths SHALL continue to expose the same public classes, functions, builders, results, issues, and exceptions after relocation.

#### Scenario: Legacy and canonical object identity
- **WHEN** a public object is imported through its legacy path and its canonical path
- **THEN** both imports resolve to the identical Python object

### Requirement: Canonical integration paths
Optional framework helpers SHALL be documented under `typewall.integrations` while their existing direct paths remain compatible.

#### Scenario: FastAPI helper migration
- **WHEN** `request_body` is imported from `typewall.fastapi` and `typewall.integrations.fastapi`
- **THEN** both names reference the same helper and preserve the optional-dependency error contract

### Requirement: Isolated module imports
Every public package layer and compatibility module SHALL import successfully in a fresh interpreter under its documented dependency set without circular-import failures.

#### Scenario: Fresh interpreter import sweep
- **WHEN** CI imports each public module in a separate process
- **THEN** all imports complete successfully or produce only the documented missing-extra error

