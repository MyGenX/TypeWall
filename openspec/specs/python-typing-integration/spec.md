# Python Typing Integration

## Purpose

Define how TypeWall derives runtime schemas from supported Python typing annotations and preserves the parsed output type.

## Requirements

### Requirement: Generic schema outputs
The public typing API SHALL represent schemas by their parsed output type and SHALL preserve or update that type through builders, wrappers, collections, objects, and transforms.

#### Scenario: Primitive inference
- **WHEN** a type checker analyzes `w.str().parse(value)`
- **THEN** the inferred return type is `str`

#### Scenario: Transform inference
- **WHEN** a typed transform changes a string into an integer
- **THEN** the transformed schema's parsed output type is inferred as `int`

### Requirement: Schema generation entry point
`schema_from_type(annotation)` SHALL create a TypeWall schema for supported standard-library annotations and fail during construction for unsupported annotations.

#### Scenario: Supported nested annotation
- **WHEN** a caller provides a supported nested annotation
- **THEN** the generated schema enforces its complete nested structure

#### Scenario: Unsupported annotation
- **WHEN** a caller provides an unsupported annotation
- **THEN** construction raises `TypeError` identifying the unsupported annotation path

### Requirement: TypedDict support
Schema generation SHALL support `TypedDict`, including required keys, `total=False`, `Required`, and `NotRequired`.

#### Scenario: TypedDict required and optional keys
- **WHEN** a generated TypedDict schema parses a mapping
- **THEN** required keys must be present and optional keys may be absent

#### Scenario: TypedDict nested error
- **WHEN** a nested TypedDict value is invalid
- **THEN** the validation issue contains the full field path

### Requirement: Dataclass support
Schema generation SHALL support dataclass fields, nested dataclasses, declared defaults, and default factories without instantiating defaults at schema construction.

#### Scenario: Dataclass parse
- **WHEN** a mapping satisfies a generated dataclass schema
- **THEN** parsing returns an instance of the dataclass

#### Scenario: Default factory isolation
- **WHEN** a dataclass field uses a mutable default factory and multiple values are parsed
- **THEN** each parsed instance receives an independent default

### Requirement: Recursive declaration safety
Schema generation SHALL detect recursive declarations and either resolve supported recursion lazily or raise a clear construction error.

#### Scenario: Recursive annotation
- **WHEN** schema generation encounters a recursive type declaration
- **THEN** it does not terminate with an unbounded recursion error

### Requirement: Static typing conformance
The project SHALL include positive and negative MyPy and Pyright fixtures for the documented typing contract.

#### Scenario: Typing test suite
- **WHEN** the static typing checks run
- **THEN** valid usage passes and intentionally invalid usage produces the expected diagnostics
