## MODIFIED Requirements

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
