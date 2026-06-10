## Why

Python developers need a lightweight, schema-first runtime validator that is readable without requiring model classes or framework dependencies. The MVP establishes TypeWall's stable parsing contract and enough primitive, object, and collection behavior to validate common API and configuration inputs.

## What Changes

- Create the `typewall` package with `w` as the preferred schema builder and `tw` as an alias.
- Add immutable, chainable schemas for strings, integers, floats, booleans, objects, and lists.
- Add `parse()` for exception-based validation and `safe_parse()` for result-based validation.
- Add required, optional, and default value semantics for object fields.
- Add structured validation issues with deterministic nested paths and dictionary serialization.
- Establish the initial automated test suite, supported Python versions, linting, typing, and package build checks.
- Keep the MVP independent of web frameworks, environment loaders, schema export formats, and advanced composition.

## Capabilities

### New Capabilities

- `schema-parsing`: Public builder API, schema immutability, `parse()`, `safe_parse()`, and parse result behavior.
- `primitive-validation`: Strict runtime validation for string, integer, float, and boolean values.
- `structured-validation`: Object and list schemas, required fields, optional fields, defaults, nested parsing, and unknown-key policy.
- `validation-errors`: Structured issues, nested path tracking, exception behavior, and serializable error output.

### Modified Capabilities

None.

## Impact

- Introduces the initial Python package, public API, exception types, result types, and schema internals.
- Establishes compatibility and quality gates that every later phase must preserve.
- Provides the prerequisite contracts for `typewall-validation-enhancements`.
- Adds no required runtime framework dependency.
