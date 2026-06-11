## 1. Phase Prerequisites and Optional Dependency Layout

- [x] 1.1 Confirm the complete MVP and enhancement test suites pass before implementing adapters
- [x] 1.2 Define optional dependency groups for FastAPI, CLI-only dependencies if any, documentation, testing, and development
- [x] 1.3 Add clean-environment tests proving the base install imports and parses without optional frameworks

## 2. Schema Export Foundation

- [x] 2.1 Implement a schema visitor and deterministic definition/reference registry for export
- [x] 2.2 Map primitive, object, list, required, optional, default, constraint, literal, enum, tuple, dictionary, union, intersection, nullable, any, and none schemas to JSON Schema 2020-12
- [x] 2.3 Implement OpenAPI 3.1-compatible schema output using the same canonical mapping layer
- [x] 2.4 Detect refinements, transforms, or other non-representable runtime behavior and raise path-aware `SchemaExportError`
- [x] 2.5 Add explicit export metadata hooks for documented non-representable cases without changing runtime validation
- [x] 2.6 Add standards-validator tests, recursive/reference tests, deterministic snapshot tests, and runtime-versus-export conformance cases

## 3. Environment Parsing

- [x] 3.1 Implement `ObjectSchema.parse_env(mapping=None)` with supplied-mapping and `os.environ` source selection
- [x] 3.2 Implement canonical string, integer, float, and boolean conversions with no general truthiness coercion
- [x] 3.3 Implement documented JSON decoding for structured object, list, tuple, and dictionary environment values
- [x] 3.4 Delegate converted values through normal object parsing so required, optional, default, unknown-key, and nested errors remain consistent
- [x] 3.5 Ensure environment conversion errors identify variable paths without echoing complete raw values
- [x] 3.6 Add isolated tests for conversions, defaults, missing values, malformed JSON, nested values, unknown variables, and secret-like inputs

## 4. Validation CLI

- [x] 4.1 Add the `typewall` console entry point and `validate module:attribute [path|-]` command parser
- [x] 4.2 Implement trusted Python import-target loading with clear missing-module, missing-attribute, and non-schema errors
- [x] 4.3 Implement UTF-8 JSON input from files and standard input with concise I/O and JSON parse errors
- [x] 4.4 Implement human-readable success/failure output and structured JSON issue output
- [x] 4.5 Implement exit codes `0`, `1`, and `2` for success, validation failure, and invocation/load/input failure
- [x] 4.6 Add subprocess tests for files, stdin, malformed JSON, invalid targets, output modes, Unicode input, and every exit code
- [x] 4.7 Install the built wheel in an isolated environment and smoke-test the actual console script

## 5. FastAPI Integration

- [x] 5.1 Implement lazy optional imports with an actionable error when the FastAPI extra is absent
- [x] 5.2 Implement the documented request-body validation helper and parsed-value injection
- [x] 5.3 Map TypeWall issues to FastAPI HTTP 422 body-relative detail entries without losing issue codes or paths
- [x] 5.4 Attach TypeWall OpenAPI-compatible request schemas to generated endpoint documentation
- [x] 5.5 Add real FastAPI test applications for successful requests, multi-error 422 responses, nested paths, defaults, transforms, and OpenAPI generation
- [x] 5.6 Add a CI compatibility matrix for the documented FastAPI and supporting dependency ranges

## 6. Documentation and Examples

- [x] 6.1 Write the README with installation, project scope, quick start, error inspection, and links to detailed documentation
- [x] 6.2 Create versioned guides for constraints, composition, custom processing, typing integration, environment parsing, CLI, export, and FastAPI
- [x] 6.3 Add an API reference covering public builders, schemas, results, issues, exceptions, and adapters
- [x] 6.4 Add runnable example projects or fixtures for config validation, CLI validation, and FastAPI request validation
- [x] 6.5 Execute documentation code blocks or mirrored examples in CI against the built package

## 7. Packaging and Quality Automation

- [x] 7.1 Complete package metadata, license, classifiers, typed-package marker, URLs, version source, and artifact inclusion rules
- [x] 7.2 Configure required CI gates for lint, format, unit, integration, property, typing, coverage, documentation, package build, and artifact installation
- [x] 7.3 Test wheel and source distribution installation independently across the supported Python matrix
- [x] 7.4 Add dependency and build metadata checks that prevent optional frameworks from entering the base requirements
- [x] 7.5 Add a changelog or release notes workflow and version consistency verification

## 8. Benchmarks

- [x] 8.1 Add reproducible benchmarks for primitive, flat object, nested collection, successful, and aggregated-failure validation
- [x] 8.2 Record interpreter, platform, dependency, and benchmark configuration with machine-readable results
- [x] 8.3 Add a CI benchmark job that stores or publishes comparison artifacts without using a noisy microbenchmark threshold as the only release gate
- [x] 8.4 Document how to run and compare benchmarks locally

## 9. Integration Conformance Tests

- [x] 9.1 Convert every scenario in the five integration and release capability specs into a named automated test, documentation test, or release verification
- [x] 9.2 Add cross-feature tests for exported typing-derived schemas, environment defaults, CLI structured errors, and FastAPI OpenAPI output
- [x] 9.3 Run security-focused tests confirming errors do not expose environment secrets or full rejected values
- [x] 9.4 Run the complete MVP, enhancement, and integration suites with branch coverage

## 10. Release Readiness

- [x] 10.1 Build `0.2.0` wheel and source distribution and verify package contents
- [x] 10.2 Verify versions, hashes, installation, CLI, documentation examples, and smoke tests from release artifacts
- [x] 10.3 Add GitHub release-driven publishing workflow with version verification and prerelease/stable index routing
- [x] 10.4 Defer package-index ownership, staging publication, and stable publication to `typewall-0-2-0-release`
