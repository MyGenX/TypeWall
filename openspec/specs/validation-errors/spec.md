# Validation Errors

## Purpose

Define structured validation issues, deterministic ordering, exception access, safe formatting, and path-based serialization.

## Requirements

### Requirement: Structured validation issues
Each validation issue SHALL expose an immutable path, stable code, human-readable message, expected metadata when applicable, and a received type description that is safe to inspect.

#### Scenario: Inspect an issue
- **WHEN** parsing produces a type mismatch
- **THEN** callers can inspect the issue path, code, message, expected type, and received type without parsing message text

### Requirement: Deterministic issue ordering
Validation issues SHALL be ordered by schema declaration order for object fields and ascending index order for list items.

#### Scenario: Multiple nested failures
- **WHEN** an input has failures across several fields and list items
- **THEN** repeated parses produce issues in the same deterministic order

### Requirement: Validation exception
`ValidationError` SHALL retain the ordered issues and provide a concise string representation without discarding structured details.

#### Scenario: Catch validation exception
- **WHEN** a caller catches `ValidationError`
- **THEN** the caller can access all original issue objects

### Requirement: Dictionary error serialization
`ValidationError.to_dict()` and failed parse results SHALL support grouping messages by dot-delimited paths, including integer list indexes.

#### Scenario: Serialize nested errors
- **WHEN** issues occur at `profile.address.city` and `items.2.name`
- **THEN** dictionary serialization maps each dot-delimited path to its ordered list of messages

#### Scenario: Root-level error
- **WHEN** an issue occurs at the root value
- **THEN** dictionary serialization uses a documented root key consistently

### Requirement: Safe received-value reporting
Error serialization and string formatting SHALL NOT include full input values by default.

#### Scenario: Sensitive invalid value
- **WHEN** parsing rejects a value containing sensitive text
- **THEN** default error output identifies its type without echoing the complete value
