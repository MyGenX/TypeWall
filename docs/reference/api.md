---
title: "API Reference"
description: "Public builders, schemas, results, errors, and integrations"
---

Every object below is importable from the top-level `typewall` package unless a
more specific import path is noted. The canonical builder entry point is
`from typewall import w` (the alias `tw` is equivalent).

## Builder entry point

| Object | Import | Summary |
| --- | --- | --- |
| `w` | `from typewall import w` | Schema builder facade for constructing schemas. |
| `tw` | `from typewall import tw` | Alias of `w`. |
| `SchemaBuilder` | `from typewall import SchemaBuilder` | Type of the `w`/`tw` builder facade. |

Common builder methods include `w.str()`, `w.int()`, `w.float()`, `w.bool()`,
`w.object()`, `w.list()`, `w.dict()`, `w.tuple()`, `w.union()`, `w.literal()`,
and `w.enum()`. Each returns an immutable `Schema`; constraint and processing
methods (such as `.min()`, `.max()`, `.default()`, `.optional()`, `.refine()`,
`.transform()`) return new schemas rather than mutating the original.

## Core contracts

| Object | Import | Summary |
| --- | --- | --- |
| `Schema` | `from typewall import Schema` | Immutable, reusable validation schema. Exposes `parse()`, `safe_parse()`, and (for object schemas) `parse_env()`. |
| `ParseResult` | `from typewall import ParseResult` | Result type returned by `safe_parse()` describing success or aggregated issues. |

<Note>
`Schema.parse()` is strict and non-coercing: it raises `ValidationError` on
invalid input. `safe_parse()` returns a `ParseResult` instead of raising.
</Note>

## Errors

| Object | Import | Summary |
| --- | --- | --- |
| `ValidationError` | `from typewall import ValidationError` | Raised by `parse()`; exposes an ordered `issues` tuple. |
| `ValidationIssue` | `from typewall import ValidationIssue` | A single failure with `path`, `code`, `message`, `expected`, and `received_type`. |

## Primitive schemas

| Object | Import | Summary |
| --- | --- | --- |
| `StringSchema` | `from typewall import StringSchema` | String schema with length, email, URL, UUID, and regex constraints. |
| `IntegerSchema` | `from typewall import IntegerSchema` | Integer schema with inclusive ranges and sign checks. |
| `FloatSchema` | `from typewall import FloatSchema` | Float schema with inclusive ranges and sign checks. |
| `BooleanSchema` | `from typewall import BooleanSchema` | Strict boolean schema. |
| `ConstraintRule` | `from typewall import ConstraintRule` | Reusable constraint rule applied by primitive schemas. |

## Structured schemas

| Object | Import | Summary |
| --- | --- | --- |
| `ObjectSchema` | `from typewall import ObjectSchema` | Keyed object schema; rejects unknown keys by default. |
| `ListSchema` | `from typewall import ListSchema` | Homogeneous list schema. |

## Composition schemas

| Object | Import | Summary |
| --- | --- | --- |
| `LiteralSchema` | `from typewall import LiteralSchema` | Matches an exact literal value. |
| `EnumSchema` | `from typewall import EnumSchema` | Matches a member of an enumeration. |
| `TupleSchema` | `from typewall import TupleSchema` | Fixed-length, positionally typed tuple. |
| `DictSchema` | `from typewall import DictSchema` | Mapping with typed keys and values. |
| `UnionSchema` | `from typewall import UnionSchema` | Accepts any one branch; retains branch issues on failure. |
| `IntersectionSchema` | `from typewall import IntersectionSchema` | Requires compatible parsed outputs from all members. |
| `NullableSchema` | `from typewall import NullableSchema` | Allows `None` in addition to the wrapped schema. |
| `NoneSchema` | `from typewall import NoneSchema` | Matches `None` only. |
| `AnySchema` | `from typewall import AnySchema` | Accepts any value. |

## Typing integration

| Object | Import | Summary |
| --- | --- | --- |
| `schema_from_type` | `from typewall import schema_from_type` | Derives a schema from standard annotations, `TypedDict`, and dataclasses. |
| `DataclassSchema` | `from typewall import DataclassSchema` | Schema produced for dataclass types. |

## Export adapter

| Object | Import | Summary |
| --- | --- | --- |
| `to_json_schema` | `from typewall import to_json_schema` | Emits a JSON Schema 2020-12 document. |
| `to_openapi_schema` | `from typewall import to_openapi_schema` | Emits an OpenAPI 3.1-compatible schema object. |
| `SchemaExportError` | `from typewall import SchemaExportError` | Raised when a schema cannot be faithfully represented (for example, non-representable refinements or transforms). |

## FastAPI integration

Requires the `fastapi` extra (`pip install typewall[fastapi]`).

| Object | Import | Summary |
| --- | --- | --- |
| `request_body` | `from typewall.integrations.fastapi import request_body` | Builds a FastAPI dependency that validates request bodies, returning HTTP 422 with body-relative paths and TypeWall issue codes on failure. |

## Version

| Object | Import | Summary |
| --- | --- | --- |
| `__version__` | `from typewall import __version__` | Installed package version string. |
