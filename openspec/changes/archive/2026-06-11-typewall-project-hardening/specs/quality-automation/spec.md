## ADDED Requirements

### Requirement: Supported Python quality gates
CI SHALL verify Python 3.9 through 3.14 using formatting, linting, static typing, unit, property, integration, conformance, branch coverage, documentation, package build, and artifact installation checks.

#### Scenario: Required check failure
- **WHEN** any required quality gate fails
- **THEN** the associated CI job fails and release readiness is not reported

### Requirement: Distribution metadata completeness
The package SHALL include accurate metadata, license, classifiers, typed-package marker, project URLs, version source, and explicit wheel and source-distribution contents.

#### Scenario: Inspect built metadata
- **WHEN** wheel and sdist metadata and contents are inspected
- **THEN** required files and Python compatibility declarations are present and consistent with the project configuration

### Requirement: Optional dependency isolation
Base installation requirements SHALL exclude documentation, benchmark, test, and optional framework dependencies.

#### Scenario: Inspect base wheel installation
- **WHEN** the wheel is installed without extras in an isolated environment
- **THEN** core parsing works and optional frameworks are absent from the installed dependency set

### Requirement: Independent artifact verification
Wheel and source distributions SHALL be independently installed and smoke-tested across the supported Python matrix.

#### Scenario: Artifact smoke matrix
- **WHEN** CI installs each artifact under a supported Python version
- **THEN** root imports, parsing, typing marker presence, and the CLI entry point work from the installed artifact

### Requirement: Version and release-note consistency
The project SHALL maintain a changelog and automated checks that compare project version, release tag, built metadata, and release notes.

#### Scenario: Inconsistent release version
- **WHEN** any release-facing version or notes entry disagrees with the project version
- **THEN** release verification fails before publication
