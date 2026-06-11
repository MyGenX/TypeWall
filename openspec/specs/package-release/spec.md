# package-release Specification

## Purpose
TBD - created by archiving change typewall-integrations-release. Update Purpose after archive.
## Requirements
### Requirement: Installable distribution
The project SHALL build a wheel and source distribution named `typewall`, and both artifacts SHALL install into clean supported Python environments.

#### Scenario: Install built artifacts
- **WHEN** CI installs the wheel and source distribution independently
- **THEN** importing `typewall`, constructing a schema, and running a parse smoke test succeed

### Requirement: Lightweight dependency model
The base distribution SHALL declare only dependencies required by core runtime behavior, while CLI, FastAPI, documentation, and development dependencies SHALL be separated appropriately.

#### Scenario: Inspect base installation
- **WHEN** the base wheel is installed without extras
- **THEN** optional framework and documentation packages are not installed as requirements

### Requirement: Public documentation
The release SHALL include a README and versioned documentation covering installation, core parsing, errors, constraints, composition, typing, environment parsing, CLI usage, schema export, and FastAPI integration.

#### Scenario: Documentation examples
- **WHEN** documentation tests execute supported code examples
- **THEN** the examples pass against the release candidate package

### Requirement: Continuous integration gates
CI SHALL run formatting or lint checks, unit and integration tests, static typing tests, package builds, artifact installation tests, documentation checks, and supported-Python matrix tests.

#### Scenario: Required gate fails
- **WHEN** any required quality check fails
- **THEN** the release workflow does not publish artifacts

### Requirement: Benchmark coverage
The project SHALL include reproducible benchmarks for primitive, object, nested collection, successful, and failing validation workloads and SHALL retain machine-readable results for comparison.

#### Scenario: Benchmark suite
- **WHEN** benchmark jobs run under the documented environment
- **THEN** they record results for every representative workload without changing validation behavior

### Requirement: Versioned release process
The project SHALL document and automate a reproducible release process driven by GitHub release tags with version consistency checks, changelog or release notes, artifact verification, and authenticated publishing separated from build verification.

#### Scenario: Release candidate verification
- **WHEN** a release candidate is built from a clean tagged revision
- **THEN** version metadata, package contents, tests, and installation checks all agree before publishing is allowed

#### Scenario: GitHub release publishing
- **WHEN** a GitHub release tag matches the package version
- **THEN** the release workflow can publish a prerelease to TestPyPI or a stable release to PyPI after build and smoke-test verification

#### Scenario: Tag and version mismatch
- **WHEN** the GitHub release tag does not match the package version
- **THEN** the release workflow fails before publishing

