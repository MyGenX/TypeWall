# validation-cli Specification

## Purpose
TBD - created by archiving change typewall-integrations-release. Update Purpose after archive.
## Requirements
### Requirement: CLI schema target
The package SHALL install a `typewall` command supporting `typewall validate module:attribute [path|-]`, where the target resolves to a TypeWall schema.

#### Scenario: Load schema target
- **WHEN** a valid import target references a schema
- **THEN** the command loads that schema and validates the selected JSON input

#### Scenario: Invalid schema target
- **WHEN** the target cannot be imported or does not reference a schema
- **THEN** the command reports a concise load error and exits with the invocation error code

### Requirement: CLI input sources
The validation command SHALL read UTF-8 JSON from a file path or standard input.

#### Scenario: Validate standard input
- **WHEN** the input path is omitted or `-`
- **THEN** the command reads one JSON document from standard input

#### Scenario: Malformed JSON
- **WHEN** the selected input is not valid JSON
- **THEN** the command reports a parse error and exits with the invocation error code

### Requirement: CLI output modes
The command SHALL support concise human-readable output and a machine-readable JSON mode containing structured issue paths, codes, and messages.

#### Scenario: JSON validation failure output
- **WHEN** validation fails with JSON output enabled
- **THEN** standard output contains valid JSON describing every issue

### Requirement: CLI exit codes
The command SHALL exit with `0` for valid input, `1` for schema validation failure, and `2` for usage, import, I/O, or JSON parsing errors.

#### Scenario: Automation distinguishes failures
- **WHEN** validation and invocation failures are triggered separately
- **THEN** their process exit codes are `1` and `2` respectively

### Requirement: CLI end-to-end tests
The test suite SHALL execute the installed console entry point against fixture modules, files, and standard input.

#### Scenario: Installed CLI smoke test
- **WHEN** the built wheel is installed into an isolated environment
- **THEN** the `typewall validate` command successfully validates a known-good fixture

