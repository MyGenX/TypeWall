## ADDED Requirements

### Requirement: Object schema validation
`w.object(fields)` SHALL require a mapping input, parse each declared field with its schema, and return a new dictionary containing parsed field values.

#### Scenario: Valid object
- **WHEN** all declared fields in a mapping satisfy their schemas
- **THEN** parsing returns a new dictionary with the parsed field values

#### Scenario: Non-mapping object input
- **WHEN** an object schema receives a non-mapping value
- **THEN** parsing fails at the object path and does not attempt child fields

### Requirement: Required fields
Object fields SHALL be required unless their schema is marked optional or has a default.

#### Scenario: Missing required field
- **WHEN** an input mapping omits a required field
- **THEN** parsing adds a `missing` issue at that field path

### Requirement: Optional fields
Calling `.optional()` SHALL allow a field to be absent but SHALL NOT make an explicitly supplied invalid value valid.

#### Scenario: Optional field omitted
- **WHEN** an input mapping omits an optional field
- **THEN** the output omits that field and no issue is produced

#### Scenario: Optional field supplied with wrong type
- **WHEN** an optional field is present with an invalid value
- **THEN** its underlying schema produces a validation issue

### Requirement: Default values
Calling `.default(value)` SHALL use a copied default when a field is absent and SHALL validate the default through the underlying schema.

#### Scenario: Default applied
- **WHEN** an input mapping omits a field with a valid default
- **THEN** the output contains an independently copied default value

#### Scenario: Invalid declared default
- **WHEN** a missing field causes an invalid default to be applied
- **THEN** parsing fails at the field path

### Requirement: Unknown object fields
Object schemas SHALL reject input keys that are not declared in the schema.

#### Scenario: Unknown field supplied
- **WHEN** an input mapping contains an undeclared key
- **THEN** parsing adds an `unknown_key` issue at that key path

### Requirement: List schema validation
`w.list(item_schema)` SHALL require a Python list, parse every item with the supplied schema, and return a new list of parsed values.

#### Scenario: Valid list
- **WHEN** every list item satisfies the item schema
- **THEN** parsing returns a new list with parsed item values in input order

#### Scenario: Multiple invalid list items
- **WHEN** multiple items violate the item schema
- **THEN** parsing reports an issue for each invalid item using its integer index in the path

### Requirement: Nested structured parsing
Object and list schemas SHALL compose recursively while preserving full paths and deterministic declaration or index order.

#### Scenario: Nested field failure
- **WHEN** a nested object field inside a list is invalid
- **THEN** the issue path contains every parent field and list index leading to the value
