## ADDED Requirements

### Requirement: Environment parsing entry point
Object schemas SHALL provide `parse_env(mapping=None)` that reads from the supplied string mapping or from `os.environ` when no mapping is supplied.

#### Scenario: Parse supplied environment mapping
- **WHEN** a caller supplies a mapping of environment names to strings
- **THEN** only that mapping is used as the input source

### Requirement: Explicit environment coercion
Environment parsing SHALL support documented canonical conversions for strings, integers, floats, booleans, and JSON-encoded structured values before delegating to normal schema validation.

#### Scenario: Canonical primitive values
- **WHEN** environment text uses a documented integer, float, or boolean form
- **THEN** it is converted to the corresponding Python runtime type

#### Scenario: Non-canonical boolean
- **WHEN** a boolean variable contains an undocumented truthy string
- **THEN** parsing fails instead of applying general truthiness

### Requirement: Missing environment values
Missing variables SHALL follow the same required, optional, and default behavior as ordinary object parsing.

#### Scenario: Defaulted environment variable
- **WHEN** a variable is absent and its field has a default
- **THEN** the independently copied default is used

### Requirement: Environment error safety
Environment failures SHALL identify the variable path and conversion or validation reason without including the complete raw value by default.

#### Scenario: Invalid secret value
- **WHEN** a secret-like environment value cannot be parsed
- **THEN** default error output does not echo the complete environment value

### Requirement: Environment parser tests
The test suite SHALL isolate process environment changes and cover conversion, missing values, defaults, nested JSON, and sensitive error output.

#### Scenario: Isolated environment test
- **WHEN** an environment parsing test modifies process variables
- **THEN** the original process environment is restored after the test
