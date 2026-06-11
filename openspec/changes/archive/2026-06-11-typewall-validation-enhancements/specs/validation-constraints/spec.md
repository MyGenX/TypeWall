## ADDED Requirements

### Requirement: String length constraints
String schemas SHALL support immutable `.min(length)` and `.max(length)` constraints measured in Python characters.

#### Scenario: String below minimum
- **WHEN** a string contains fewer characters than the configured minimum
- **THEN** parsing produces a `string_too_short` issue at the value path

#### Scenario: Inclusive string boundaries
- **WHEN** a string length equals a configured minimum or maximum
- **THEN** that boundary constraint succeeds

### Requirement: Numeric range and sign constraints
Integer and float schemas SHALL support inclusive `.min(value)`, inclusive `.max(value)`, `.positive()`, and `.negative()` constraints.

#### Scenario: Number outside range
- **WHEN** a valid numeric type is outside a configured range
- **THEN** parsing produces a stable range issue

#### Scenario: Zero with sign constraint
- **WHEN** zero is parsed by a positive or negative schema
- **THEN** the sign constraint fails

### Requirement: Email validation
String schemas SHALL support `.email()` using documented standards-aware validation and SHALL return the original string on success.

#### Scenario: Valid email address
- **WHEN** a syntactically valid supported email address is parsed
- **THEN** the email constraint succeeds without modifying the string

#### Scenario: Invalid email address
- **WHEN** a string does not satisfy the documented email syntax
- **THEN** parsing produces an `invalid_email` issue

### Requirement: URL validation
String schemas SHALL support `.url()` and require an absolute URL with a supported scheme and network location.

#### Scenario: Absolute HTTP URL
- **WHEN** a valid absolute HTTP or HTTPS URL is parsed
- **THEN** the URL constraint succeeds

#### Scenario: Relative URL
- **WHEN** a relative URL is parsed
- **THEN** parsing produces an `invalid_url` issue

### Requirement: UUID validation
String schemas SHALL support `.uuid()` and accept canonical UUID text for documented UUID versions.

#### Scenario: Canonical UUID
- **WHEN** a canonical supported UUID string is parsed
- **THEN** the UUID constraint succeeds and returns the string

#### Scenario: Malformed UUID
- **WHEN** malformed UUID text is parsed
- **THEN** parsing produces an `invalid_uuid` issue

### Requirement: Regex validation
String schemas SHALL support `.regex(pattern)` for string or compiled regular-expression patterns and SHALL use search semantics documented by the API.

#### Scenario: Regex match
- **WHEN** the configured pattern finds a match in the string
- **THEN** the regex constraint succeeds

#### Scenario: Invalid regex declaration
- **WHEN** a caller configures an invalid regex pattern
- **THEN** schema construction raises a configuration error before parsing
