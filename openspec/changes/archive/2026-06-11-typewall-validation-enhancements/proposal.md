## Why

The core MVP validates basic shapes but is not yet expressive enough for production API, configuration, or typed Python workflows. This phase builds on the completed MVP with common constraints, advanced composition, custom processing, and standard-library typing integration.

## What Changes

- Add chainable string and numeric constraints, including length/range, email, URL, UUID, and regex validation.
- Add literal, enum, tuple, dictionary, union, intersection, nullable, any, and explicit none schemas.
- Add custom refinement and transformation hooks with predictable ordering and error behavior.
- Improve nested and branch-related issue detail without changing the MVP's public error inspection contract.
- Add generic schema output typing and schema generation from `TypedDict` and dataclass declarations.
- Add comprehensive unit, property-oriented, typing, and regression tests for every enhancement.
- Require `typewall-core-mvp` to be implemented first.

## Capabilities

### New Capabilities

- `validation-constraints`: Reusable string and numeric constraints with chainable, immutable schema declarations.
- `schema-composition`: Literal, enum, tuple, dictionary, union, intersection, nullable, any, and none schemas.
- `custom-processing`: User-defined refinements and transforms with structured failures and deterministic execution.
- `python-typing-integration`: Generic schema output types plus `TypedDict` and dataclass schema generation.

### Modified Capabilities

None. This change depends on, but does not redefine, the MVP capability contracts.

## Impact

- Extends the public builder namespace and schema type hierarchy.
- Adds standard-library introspection for supported typing constructs.
- May use small, well-maintained validation dependencies only when they provide standards-compliant behavior and are justified in design.
- Provides the prerequisite capabilities for `typewall-integrations-release`.
