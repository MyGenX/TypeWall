## ADDED Requirements

### Requirement: Optional FastAPI dependency
Importing and using the TypeWall core package SHALL NOT require FastAPI, and importing the FastAPI integration without its extra SHALL fail with an actionable dependency message.

#### Scenario: Core install without FastAPI
- **WHEN** TypeWall is installed without integration extras
- **THEN** core schema construction and parsing work without importing FastAPI

### Requirement: Request body validation
The FastAPI integration SHALL provide a documented helper that validates request bodies with a TypeWall schema and supplies the parsed result to the endpoint.

#### Scenario: Valid request body
- **WHEN** a request body satisfies the configured schema
- **THEN** the endpoint receives the parsed TypeWall output

#### Scenario: Invalid request body
- **WHEN** a request body violates the configured schema
- **THEN** FastAPI returns HTTP 422 with all issues mapped to body-relative locations

### Requirement: OpenAPI participation
The FastAPI integration SHALL use TypeWall's OpenAPI-compatible export so supported request schemas appear in the generated application document.

#### Scenario: Generated OpenAPI document
- **WHEN** an application includes an endpoint using the TypeWall helper
- **THEN** its generated OpenAPI operation describes the supported request schema

### Requirement: FastAPI compatibility tests
The integration SHALL be tested with real FastAPI test applications across the documented FastAPI compatibility range.

#### Scenario: Integration matrix
- **WHEN** CI runs the optional integration test group
- **THEN** request validation, 422 mapping, and OpenAPI generation pass for each supported dependency set
