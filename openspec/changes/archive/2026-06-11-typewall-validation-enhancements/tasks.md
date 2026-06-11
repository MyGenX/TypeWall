## 1. Phase Prerequisite and Extension Points

- [x] 1.1 Confirm the complete `typewall-core-mvp` test suite and package build pass before changing schema behavior
- [x] 1.2 Review the MVP schema protocol and add only the internal rule/composition extension points required by this phase
- [x] 1.3 Add regression tests proving existing primitive, structured, parse, safe-parse, and error behavior remains unchanged

## 2. Constraint Infrastructure

- [x] 2.1 Implement immutable ordered constraint objects with stable codes and exportable metadata
- [x] 2.2 Implement string `.min()` and `.max()` with schema-construction validation for invalid bounds
- [x] 2.3 Implement numeric `.min()`, `.max()`, `.positive()`, and `.negative()` with inclusive range semantics
- [x] 2.4 Add boundary, invalid-configuration, chaining-order, and schema-reuse tests for length and numeric constraints

## 3. Formatted String Constraints

- [x] 3.1 Select and document the standards behavior and dependency decision for email validation
- [x] 3.2 Implement `.email()` with representative valid, invalid, Unicode, and edge-case fixtures
- [x] 3.3 Implement `.url()` with absolute URL, scheme, network-location, malformed, and relative URL tests
- [x] 3.4 Implement `.uuid()` with supported-version, canonical, malformed, and case-variation tests
- [x] 3.5 Implement `.regex()` for string and compiled patterns with search semantics and construction-time pattern errors
- [x] 3.6 Add tests proving formatted constraints preserve successful input strings and stable issue codes

## 4. Composition Schemas

- [x] 4.1 Implement literal validation with runtime type distinction and immutable literal metadata
- [x] 4.2 Implement non-empty enum validation with duplicate/configuration checks
- [x] 4.3 Implement fixed tuple validation with exact length, positional parsing, and indexed paths
- [x] 4.4 Implement dictionary key/value validation with path-aware errors and parsed-key collision detection
- [x] 4.5 Implement union validation with declaration-order success selection and retained per-branch failure details
- [x] 4.6 Implement intersection validation with mapping merge and explicit output-conflict behavior
- [x] 4.7 Implement nullable wrappers, `w.any()`, and `w.none()`
- [x] 4.8 Add focused tests for every composition success path, configuration error, nested path, union branch error, and intersection conflict

## 5. Custom Processing

- [x] 5.1 Implement `.refine()` with configurable message/code and execution after built-in constraints
- [x] 5.2 Implement `.transform()` with ordered output transformation and output generic propagation
- [x] 5.3 Wrap callback exceptions as structured issues while preserving exception chaining
- [x] 5.4 Ensure failed built-in validation skips refinements and any failure skips transforms
- [x] 5.5 Add tests for callback ordering, callback skipping, exception causes, transformed output, schema reuse, and nested callback paths

## 6. Runtime Typing Integration

- [x] 6.1 Define generic `Schema[T]` output typing across primitive, collection, object, wrapper, union, and transform builders
- [x] 6.2 Implement `schema_from_type()` dispatch for primitives, `Any`, `None`, lists, dictionaries, fixed tuples, unions/optionals, and literals
- [x] 6.3 Implement `TypedDict` generation with totality, `Required`, `NotRequired`, nesting, and unknown-key behavior
- [x] 6.4 Implement dataclass generation with nested fields, defaults, deferred default factories, and dataclass instance output
- [x] 6.5 Add recursion caching/lazy references for supported declarations and clear errors for unsupported cycles
- [x] 6.6 Add construction-time errors that identify the path to unsupported annotations
- [x] 6.7 Add runtime tests for every supported annotation family, nested failures, defaults, recursion, and unsupported declarations

## 7. Static Typing Conformance

- [x] 7.1 Add positive and negative MyPy fixtures for primitive, collection, object, optional, union, dataclass, and transformed outputs
- [x] 7.2 Add equivalent Pyright fixtures and document intentional differences between the type checkers
- [x] 7.3 Add CI jobs that fail when documented inference regresses or expected-invalid fixtures unexpectedly pass

## 8. Enhancement Conformance and Regression

- [x] 8.1 Convert every scenario in the four enhancement capability specs into a named automated test or parameterized case
- [x] 8.2 Add property-oriented tests for constraint boundaries, union determinism, dictionary collision safety, and schema immutability
- [x] 8.3 Add fuzz or generated-input tests for regex, URL, UUID, nested composition, and typing-derived schemas
- [x] 8.4 Run the full MVP and enhancement suites with branch coverage and address uncovered failure paths

## 9. Phase Completion Gate

- [x] 9.1 Run formatter, lint, MyPy, Pyright, unit tests, property tests, coverage, and package build checks
- [x] 9.2 Install the built wheel in a clean environment and run examples for constraints, composition, transforms, TypedDict, and dataclasses
- [x] 9.3 Confirm every enhancement spec scenario passes and core strict parsing has not gained implicit coercion
- [x] 9.4 Record representable schema metadata and non-representable custom behavior needed by the integration phase
