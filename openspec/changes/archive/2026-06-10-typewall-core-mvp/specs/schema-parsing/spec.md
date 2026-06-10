## ADDED Requirements

### Requirement: Public schema builder
The package SHALL export `w` as the preferred schema builder and `tw` as an alias referencing the same builder behavior.

#### Scenario: Import preferred builder
- **WHEN** a caller imports `w` from `typewall`
- **THEN** the caller can construct every schema included in the MVP

#### Scenario: Import alias
- **WHEN** a caller imports `tw` from `typewall`
- **THEN** `tw` exposes the same constructors and behavior as `w`

### Requirement: Immutable chainable schemas
Every schema configuration method SHALL return a new schema and SHALL NOT modify the existing schema.

#### Scenario: Reuse a base schema
- **WHEN** a caller derives optional and defaulted schemas from one base schema
- **THEN** parsing with the base schema retains its original required behavior

### Requirement: Exception-based parsing
Every schema SHALL provide `parse(value)` that returns the parsed value on success and raises `ValidationError` containing all discovered issues on failure.

#### Scenario: Successful parse
- **WHEN** a value satisfies a schema
- **THEN** `parse()` returns the validated value

#### Scenario: Failed parse
- **WHEN** a value violates multiple independently reachable requirements
- **THEN** `parse()` raises one `ValidationError` containing the ordered issues

### Requirement: Result-based parsing
Every schema SHALL provide `safe_parse(value)` that does not raise for validation failures and returns a result with an unambiguous success or failure state.

#### Scenario: Safe parse success
- **WHEN** a value satisfies a schema
- **THEN** the result has `ok` equal to `True`, contains parsed `data`, and has no errors

#### Scenario: Safe parse failure
- **WHEN** a value violates a schema
- **THEN** the result has `ok` equal to `False`, contains no data, and exposes the ordered validation issues

### Requirement: Schema reuse
Parsing SHALL keep all per-call path and error state outside schema instances.

#### Scenario: Repeated parsing
- **WHEN** the same schema parses a failing value and then a valid value
- **THEN** the second result is not affected by issues from the first call
