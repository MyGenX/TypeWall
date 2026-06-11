# Custom Processing

## Purpose

Define how TypeWall schemas run custom refinement and transform callbacks after built-in validation.

## Requirements

### Requirement: Custom refinements
Schemas SHALL support immutable `.refine(predicate, message, code=...)` rules that run after built-in validation and succeed only when the predicate returns a truthy value.

#### Scenario: Refinement rejection
- **WHEN** built-in validation succeeds and the refinement predicate returns false
- **THEN** parsing produces an issue at the current path using the configured message and code

#### Scenario: Built-in failure skips refinement
- **WHEN** built-in validation fails
- **THEN** the refinement callback is not invoked for that value

### Requirement: Output transforms
Schemas SHALL support immutable `.transform(callback)` operations that run after successful validation and determine the parsed output.

#### Scenario: Successful transform
- **WHEN** all validation and refinement steps succeed
- **THEN** transforms run in declaration order and the final transformed value is returned

#### Scenario: Transform is skipped after failure
- **WHEN** validation or refinement fails
- **THEN** no transform callback runs for that value

### Requirement: Callback exception handling
Unexpected exceptions from refinement or transform callbacks SHALL become structured callback issues while preserving the original exception as the cause.

#### Scenario: Callback raises
- **WHEN** a custom callback raises an unexpected exception
- **THEN** parsing fails with a callback issue at the current path and chains the original exception

### Requirement: Custom processing isolation
Custom callbacks SHALL receive only the current successfully parsed value and SHALL NOT mutate schema configuration or parse context.

#### Scenario: Reused custom schema
- **WHEN** a schema with custom processing is reused across parse calls
- **THEN** callback behavior and schema configuration remain independent between calls
