## ADDED Requirements

### Requirement: JSON Schema export
Supported schemas SHALL export deterministic JSON Schema 2020-12 documents that represent their runtime types, required fields, defaults, constraints, and nested structure.

#### Scenario: Export nested object schema
- **WHEN** a caller exports a nested object containing required, optional, defaulted, list, and constrained fields
- **THEN** the document contains equivalent nested JSON Schema keywords

#### Scenario: Deterministic export
- **WHEN** the same schema is exported repeatedly
- **THEN** structurally equivalent documents are produced with stable ordering where ordering is observable

### Requirement: OpenAPI-compatible export
Supported schemas SHALL export schema objects compatible with OpenAPI 3.1 and SHALL preserve shared schema references without infinite recursion.

#### Scenario: Export reusable nested schema
- **WHEN** the same nested schema is referenced multiple times
- **THEN** export can use stable component references rather than duplicating recursive structures

### Requirement: Unsupported behavior handling
Export SHALL fail with `SchemaExportError` when runtime behavior cannot be represented accurately and no explicit export metadata is provided.

#### Scenario: Export custom transform
- **WHEN** a transformed schema lacks explicit export metadata
- **THEN** export fails and identifies the non-representable schema path

### Requirement: Export validation tests
Generated documents SHALL be checked against a standards-aware schema validator and representative payload conformance tests.

#### Scenario: Exported schema conformance
- **WHEN** export conformance tests run for a supported TypeWall schema
- **THEN** valid and invalid payload outcomes match TypeWall runtime behavior for representable rules
