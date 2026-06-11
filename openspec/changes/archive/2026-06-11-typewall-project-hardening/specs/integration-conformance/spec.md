## ADDED Requirements

### Requirement: Specification scenario traceability
Every scenario in the environment, CLI, schema export, FastAPI, and package-release integration specifications SHALL map to a named automated test, documentation test, or release verification.

#### Scenario: Conformance inventory
- **WHEN** the conformance inventory is checked
- **THEN** every integration scenario identifies an executable verification target

### Requirement: Cross-feature verification
Conformance tests SHALL cover typing-derived schema export, environment defaults, CLI structured errors, and FastAPI OpenAPI generation using shared schemas where applicable.

#### Scenario: Shared schema across boundaries
- **WHEN** a supported schema is exercised through export, CLI, environment, or FastAPI boundaries
- **THEN** each boundary preserves the documented validation shape, paths, defaults, and machine-readable contract

### Requirement: Sensitive-value safety
Integration errors SHALL identify failing sources and paths without exposing complete environment secrets or complete rejected sensitive values.

#### Scenario: Rejected secret-like input
- **WHEN** environment, CLI, or framework validation rejects a secret-like value
- **THEN** captured exceptions, structured output, human output, and logs do not contain the complete raw value

### Requirement: Full regression coverage
The complete MVP, enhancement, integration, and conformance suites SHALL run with branch coverage at or above the configured project threshold.

#### Scenario: Full hardening gate
- **WHEN** the hardening CI gate runs
- **THEN** all suites pass and branch coverage meets the configured minimum
