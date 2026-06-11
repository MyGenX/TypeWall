# project-documentation Specification

## Purpose
TBD - created by archiving change typewall-project-hardening. Update Purpose after archive.
## Requirements
### Requirement: Public documentation site
TypeWall SHALL provide a Mintlify documentation site, configured by `docs.json`
and authored in MDX, covering installation, scope, quick start, errors,
constraints, composition, custom processing, typing, environment parsing, CLI,
schema export, and FastAPI. The site SHALL use Mintlify-native versioning to
publish documentation versions.

#### Scenario: Documentation link and config check
- **WHEN** CI runs the Mintlify CLI link and configuration check against the docs
  sources
- **THEN** the `docs.json` configuration is valid and navigation, internal links,
  and references resolve with no broken links reported

### Requirement: Generated API reference
Documentation SHALL describe public builders, schemas, results, issues,
exceptions, export functions, adapters, and integrations through a maintained MDX
API reference whose entries map to importable package objects.

#### Scenario: API reference resolves importable objects
- **WHEN** the API reference is reviewed against the installed package
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

