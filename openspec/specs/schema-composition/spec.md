# Schema Composition

## Purpose

Define TypeWall's composite schema behavior for literals, enums, tuples, dictionaries, unions, intersections, and wrapper schemas.

## Requirements

### Requirement: Literal and enum schemas
`w.literal(value)` SHALL accept only an equal value of a compatible runtime type, and `w.enum(values)` SHALL accept one member from a non-empty declared collection.

#### Scenario: Literal type distinction
- **WHEN** a literal integer schema parses a boolean with an equal numeric value
- **THEN** parsing fails because the runtime types are incompatible

#### Scenario: Enum member
- **WHEN** an enum schema parses a declared member
- **THEN** it returns that member unchanged

### Requirement: Tuple schemas
`w.tuple(items)` SHALL require a tuple of exactly the declared length and validate each position with its corresponding schema.

#### Scenario: Valid fixed tuple
- **WHEN** tuple length and all positional values match
- **THEN** parsing returns a tuple of parsed values

#### Scenario: Tuple length mismatch
- **WHEN** tuple length differs from the declared schema length
- **THEN** parsing produces a tuple length issue

### Requirement: Dictionary schemas
`w.dict(key_schema, value_schema)` SHALL require a mapping and validate every key and value while preserving valid parsed key-value associations.

#### Scenario: Invalid dictionary key and value
- **WHEN** a mapping contains an invalid key and an invalid value
- **THEN** parsing reports path-aware issues for both failures

#### Scenario: Parsed key collision
- **WHEN** distinct input keys parse to the same output key
- **THEN** parsing fails with a collision issue instead of silently overwriting data

### Requirement: Union schemas
`w.union(schemas)` SHALL require at least one member and return the result from the first successful member in declaration order.

#### Scenario: First successful union branch
- **WHEN** more than one union member could accept a value
- **THEN** the first successful member determines the output

#### Scenario: All union branches fail
- **WHEN** no union member accepts a value
- **THEN** parsing produces a union issue retaining each branch's issues

### Requirement: Intersection schemas
`w.intersection(schemas)` SHALL require at least two members and require the original input to satisfy every member.

#### Scenario: Compatible mapping intersection
- **WHEN** all members return mappings with no conflicting overlapping values
- **THEN** parsing returns their merged mapping

#### Scenario: Conflicting intersection output
- **WHEN** members produce unequal non-mapping results or conflicting mapping values
- **THEN** parsing produces an intersection conflict issue

### Requirement: Nullable, any, and none schemas
The builder SHALL provide nullable wrappers, an any-value schema, and an explicit none schema.

#### Scenario: Nullable value
- **WHEN** a nullable schema parses `None`
- **THEN** it succeeds without invoking the wrapped schema

#### Scenario: Any value
- **WHEN** `w.any()` parses any Python value
- **THEN** it returns the value unchanged

#### Scenario: Explicit none
- **WHEN** `w.none()` parses a non-`None` value
- **THEN** parsing fails with a type issue
