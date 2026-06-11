# Changelog

All notable changes to TypeWall are recorded here. The project follows semantic versioning while the API is in the `0.x` development series.

## [Unreleased]

- Reorganize package internals into explicit core, schema, adapter, and integration layers.
- Add documentation, examples, benchmarks, conformance tests, and expanded CI verification.

## [0.2.1] - 2026-06-11

- Fix FastAPI OpenAPI generation: `request_body(...).openapi_extra` now emits a self-contained, inlined schema so Swagger UI can resolve it (previously embedded `#/$defs/...` references that resolved against the OpenAPI document root and failed).
- Add `inline_refs(document)` helper and a `to_openapi_schema(schema, inline=True)` option to flatten `$defs`/`$ref` into a self-contained schema. Recursive schemas, which cannot be inlined, raise `SchemaExportError`.

## [0.2.0] - 2026-06-11

- Add JSON Schema and OpenAPI export.
- Add environment parsing and the validation CLI.
- Add optional FastAPI request validation.
- Add constraints, composition, custom processing, and Python typing integration.

[Unreleased]: https://github.com/MyGenX/TypeWall/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/MyGenX/TypeWall/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/MyGenX/TypeWall/releases/tag/v0.2.0
