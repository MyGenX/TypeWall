## ADDED Requirements

### Requirement: String validation
`w.str()` SHALL accept Python `str` values and reject values of every other runtime type without coercion.

#### Scenario: Valid string
- **WHEN** `w.str()` parses a string
- **THEN** it returns the unchanged string

#### Scenario: Non-string value
- **WHEN** `w.str()` parses a non-string value
- **THEN** parsing fails with a `type_error` issue that expects `str`

### Requirement: Integer validation
`w.int()` SHALL accept Python `int` values except `bool` and SHALL reject other values without coercion.

#### Scenario: Valid integer
- **WHEN** `w.int()` parses an integer that is not a boolean
- **THEN** it returns the unchanged integer

#### Scenario: Boolean is not an integer
- **WHEN** `w.int()` parses `True` or `False`
- **THEN** parsing fails with a `type_error` issue that expects `int`

### Requirement: Float validation
`w.float()` SHALL accept Python `float` values and SHALL reject integers, booleans, strings, and other values without coercion.

#### Scenario: Valid float
- **WHEN** `w.float()` parses a float
- **THEN** it returns the unchanged float

#### Scenario: Integer is not a float
- **WHEN** `w.float()` parses an integer
- **THEN** parsing fails with a `type_error` issue that expects `float`

### Requirement: Boolean validation
`w.bool()` SHALL accept only the Python singleton values `True` and `False` and SHALL perform no truthiness coercion.

#### Scenario: Valid boolean
- **WHEN** `w.bool()` parses `True` or `False`
- **THEN** it returns the unchanged boolean

#### Scenario: Truthy non-boolean
- **WHEN** `w.bool()` parses a truthy non-boolean value
- **THEN** parsing fails with a `type_error` issue that expects `bool`
