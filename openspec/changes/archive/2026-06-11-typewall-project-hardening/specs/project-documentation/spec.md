## ADDED Requirements

### Requirement: Public documentation site
TypeWall SHALL provide a versioned MkDocs site covering installation, scope, quick start, errors, constraints, composition, custom processing, typing, environment parsing, CLI, schema export, and FastAPI.

#### Scenario: Strict documentation build
- **WHEN** CI builds the documentation with warnings treated as errors
- **THEN** navigation, internal links, API references, and code references resolve successfully

### Requirement: Generated API reference
Documentation SHALL describe public builders, schemas, results, issues, exceptions, export functions, adapters, and integrations from importable package objects.

#### Scenario: API reference generation
- **WHEN** mkdocstrings renders the reference against the installed package
- **THEN** every documented public object resolves through a supported import path

### Requirement: Runnable examples
The repository SHALL include runnable configuration, CLI, and FastAPI examples that demonstrate supported behavior rather than pseudo-code.

#### Scenario: Examples from built wheel
- **WHEN** CI installs the built wheel and executes each example with its declared extras
- **THEN** all examples complete with their documented outputs and exit codes

### Requirement: Current README
The README SHALL describe implemented capabilities, installation extras, supported Python versions, basic usage, error inspection, and links to detailed guides.

#### Scenario: Package index rendering
- **WHEN** the built distribution metadata is inspected
- **THEN** its README contains valid relative or absolute links and does not describe shipped integrations as deferred
