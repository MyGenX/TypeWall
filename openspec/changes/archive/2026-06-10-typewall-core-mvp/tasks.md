## 1. Project Foundation

- [x] 1.1 Create `pyproject.toml` with the root-level `typewall` package, supported Python range, PEP 517 build backend, and base project metadata
- [x] 1.2 Configure the unit test, coverage, lint, format, and static typing tools used by the MVP
- [x] 1.3 Add a supported-Python CI matrix that installs the package and runs the MVP quality commands
- [x] 1.4 Add package import and wheel/sdist build smoke tests

## 2. Core Schema Protocol

- [x] 2.1 Implement the generic base `Schema` protocol and internal missing-value sentinel
- [x] 2.2 Implement immutable schema cloning/configuration so every chainable method returns a new instance
- [x] 2.3 Implement a per-parse context carrying tuple paths and ordered issue accumulation
- [x] 2.4 Implement `parse()` with successful return behavior and aggregated `ValidationError` raising
- [x] 2.5 Implement `safe_parse()` with mutually exclusive success-data and failure-errors states
- [x] 2.6 Add tests for schema immutability, repeated reuse, parse state isolation, and parse/safe-parse parity

## 3. Public Builder API

- [x] 3.1 Implement the builder namespace with `str`, `int`, `float`, `bool`, `object`, and `list` constructors
- [x] 3.2 Export `w` and the behaviorally identical `tw` alias from the package root
- [x] 3.3 Add public import tests and minimal typing assertions for builder constructor return types

## 4. Primitive Schemas

- [x] 4.1 Implement strict string validation with stable type mismatch metadata
- [x] 4.2 Implement strict integer validation that explicitly rejects booleans
- [x] 4.3 Implement strict float validation that rejects integers and booleans
- [x] 4.4 Implement strict boolean validation without truthiness coercion
- [x] 4.5 Add parameterized positive and negative tests covering runtime subclasses and Python edge cases for every primitive schema

## 5. Structured Schemas

- [x] 5.1 Implement object schema declaration validation and mapping input checks
- [x] 5.2 Implement required field detection using the missing-value sentinel
- [x] 5.3 Implement `.optional()` absence behavior without accepting invalid supplied values
- [x] 5.4 Implement `.default(value)` with defensive copying and validation through the underlying schema
- [x] 5.5 Implement unknown-key rejection with key-specific issue paths
- [x] 5.6 Implement list validation with per-index paths, all-item traversal, and parsed list output
- [x] 5.7 Add tests for nested objects, nested lists, object-in-list paths, list-in-object paths, and simultaneous sibling failures
- [x] 5.8 Add tests proving mutable defaults are independent across fields, schemas, and parse calls

## 6. Error Model

- [x] 6.1 Implement immutable `ValidationIssue` with path, code, message, expected metadata, and received type metadata
- [x] 6.2 Implement `ValidationError` with issue retention and concise deterministic string formatting
- [x] 6.3 Implement dot-path grouping for `ValidationError.to_dict()` and failed parse results, including root and integer-index paths
- [x] 6.4 Ensure default error formatting and serialization do not expose complete rejected values
- [x] 6.5 Add snapshot or exact-value tests for issue codes, paths, ordering, string output, dictionary output, and sensitive values

## 7. MVP Conformance Tests

- [x] 7.1 Convert every scenario in the four MVP capability specs into a named automated test or parameterized case
- [x] 7.2 Add property-oriented tests for repeated schema reuse, nested path construction, issue ordering, and mutable default isolation
- [x] 7.3 Add regression tests for Python's `bool`/`int` relationship and mapping/list subclass inputs
- [x] 7.4 Run coverage and add missing branch tests for failure aggregation and nested parsing

## 8. Phase Completion Gate

- [x] 8.1 Run formatter, lint, static typing, unit tests, coverage, and package build checks locally
- [x] 8.2 Install the built wheel in a clean environment and execute the README-level MVP example
- [x] 8.3 Confirm all MVP spec scenarios pass and no enhancement or integration APIs were added prematurely
- [x] 8.4 Record the stable public API and known deferred behavior for the enhancement phase
