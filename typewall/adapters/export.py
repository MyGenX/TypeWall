from __future__ import annotations

from collections import OrderedDict
from copy import deepcopy
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Tuple, cast

from ..core.schema import Schema
from ..schemas.composition import (
    AnySchema,
    DictSchema,
    EnumSchema,
    IntersectionSchema,
    LazySchema,
    LiteralSchema,
    NoneSchema,
    NullableSchema,
    TupleSchema,
    UnionSchema,
)
from ..schemas.primitives import BooleanSchema, FloatSchema, IntegerSchema, StringSchema
from ..schemas.structured import ListSchema, ObjectSchema


class SchemaExportError(ValueError):
    def __init__(self, message: str, path: Tuple[str, ...] = ()) -> None:
        self.path = path
        super().__init__(message)


class _Exporter:
    def __init__(self, openapi: bool) -> None:
        self.openapi = openapi
        self.definitions: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
        self.visiting: set[int] = set()
        self.names: Dict[int, str] = {}
        self.counter = 0

    def export(self, schema: Schema[Any]) -> Dict[str, Any]:
        root = self._visit(schema, ())
        if self.definitions:
            root = dict(root)
            root["$defs"] = dict(self.definitions)
        if not self.openapi and "$schema" not in root:
            root = dict(root)
            root["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        return root

    def _visit(self, schema: Schema[Any], path: Tuple[str, ...]) -> Dict[str, Any]:
        override = getattr(schema, "_export_schema", None)
        if override is not None:
            return deepcopy(dict(override))
        self._check_representable(schema, path)
        schema_id = id(schema)
        if schema_id in self.names:
            return {"$ref": f"#/$defs/{self.names[schema_id]}"}
        if isinstance(
            schema,
            (
                AnySchema,
                BooleanSchema,
                FloatSchema,
                IntegerSchema,
                StringSchema,
                LiteralSchema,
                EnumSchema,
                NoneSchema,
            ),
        ):
            return self._inline(schema, path)

        if isinstance(schema, LazySchema):
            if schema_id in self.visiting:
                raise SchemaExportError("Recursive schema could not be resolved", path)
            self.visiting.add(schema_id)
            try:
                resolved = schema.resolver()
                if not isinstance(resolved, Schema):
                    raise SchemaExportError("Recursive schema could not be resolved", path)
                return self._visit(resolved, path)
            finally:
                self.visiting.discard(schema_id)

        name = self._name(schema)
        self.names[schema_id] = name
        self.visiting.add(schema_id)
        try:
            exported = self._inline(schema, path)
            self.definitions[name] = exported
        finally:
            self.visiting.discard(schema_id)
        return {"$ref": f"#/$defs/{name}"}

    def _name(self, schema: Schema[Any]) -> str:
        self.counter += 1
        return f"schema_{self.counter}"

    def _check_representable(self, schema: Schema[Any], path: Tuple[str, ...]) -> None:
        if getattr(schema, "_refinements", ()):
            raise SchemaExportError("Refinements are not representable in export", path)
        if getattr(schema, "_transforms", ()):
            raise SchemaExportError("Transforms are not representable in export", path)

    def _inline(self, schema: Schema[Any], path: Tuple[str, ...]) -> Dict[str, Any]:
        if isinstance(schema, StringSchema):
            return self._string(schema)
        if isinstance(schema, IntegerSchema):
            return self._integer(schema)
        if isinstance(schema, FloatSchema):
            return self._float(schema)
        if isinstance(schema, BooleanSchema):
            return {"type": "boolean"}
        if isinstance(schema, AnySchema):
            return {}
        if isinstance(schema, NoneSchema):
            return {"type": "null"}
        if isinstance(schema, LiteralSchema):
            return {"const": _jsonable(schema.literal)}
        if isinstance(schema, EnumSchema):
            return {"enum": [_jsonable(value) for value in schema.values]}
        if isinstance(schema, NullableSchema):
            return {
                "anyOf": [
                    self._visit(schema.inner, (*path, "inner")),
                    {"type": "null"},
                ]
            }
        if isinstance(schema, TupleSchema):
            items = [
                self._visit(item, (*path, str(index)))
                for index, item in enumerate(schema.item_schemas)
            ]
            return {
                "type": "array",
                "prefixItems": items,
                "minItems": len(items),
                "maxItems": len(items),
            }
        if isinstance(schema, ListSchema):
            return {
                "type": "array",
                "items": self._visit(schema.item_schema, (*path, "items")),
            }
        if isinstance(schema, DictSchema):
            exported: Dict[str, Any] = {
                "type": "object",
                "additionalProperties": self._visit(
                    schema.value_schema, (*path, "value")
                ),
            }
            key_schema = schema.key_schema
            if isinstance(key_schema, (StringSchema, LiteralSchema, EnumSchema)):
                exported["propertyNames"] = self._visit(key_schema, (*path, "key"))
            else:
                raise SchemaExportError(
                    "Dictionary key schemas must be string-compatible for export", path
                )
            return exported
        if isinstance(schema, ObjectSchema):
            properties: Dict[str, Any] = {}
            required: list[str] = []
            for key, field_schema in schema.fields.items():
                properties[key] = self._visit(field_schema, (*path, key))
                if not field_schema.is_optional and not field_schema.has_default:
                    required.append(key)
                if field_schema.has_default:
                    properties[key]["default"] = _jsonable(field_schema.copy_default())
            exported = {
                "type": "object",
                "properties": properties,
                "additionalProperties": False,
            }
            if required:
                exported["required"] = required
            return exported
        from ..schemas.typing import DataclassSchema

        if isinstance(schema, DataclassSchema):
            return self._inline(schema.object_schema, path)
        if isinstance(schema, IntersectionSchema):
            return {
                "allOf": [
                    self._visit(member, (*path, str(index)))
                    for index, member in enumerate(schema.members)
                ]
            }
        if isinstance(schema, UnionSchema):
            return {
                "anyOf": [
                    self._visit(member, (*path, str(index)))
                    for index, member in enumerate(schema.members)
                ]
            }
        raise SchemaExportError(
            f"Unsupported schema type for export: {type(schema).__name__}", path
        )

    def _string(self, schema: StringSchema) -> Dict[str, Any]:
        exported: Dict[str, Any] = {"type": "string"}
        for rule in schema.rules:
            if rule.kind == "string_min":
                exported["minLength"] = rule.parameter
            elif rule.kind == "string_max":
                exported["maxLength"] = rule.parameter
            elif rule.kind == "email":
                exported["format"] = "email"
            elif rule.kind == "url":
                exported["format"] = "uri"
            elif rule.kind == "uuid":
                exported["format"] = "uuid"
            elif rule.kind == "regex" and rule.pattern is not None:
                exported["pattern"] = rule.pattern.pattern
        return exported

    def _integer(self, schema: IntegerSchema) -> Dict[str, Any]:
        exported: Dict[str, Any] = {"type": "integer"}
        for rule in schema.rules:
            if rule.kind == "number_min":
                exported["minimum"] = rule.parameter
            elif rule.kind == "number_max":
                exported["maximum"] = rule.parameter
            elif rule.kind == "positive":
                exported["exclusiveMinimum"] = 0
            elif rule.kind == "negative":
                exported["exclusiveMaximum"] = 0
        return exported

    def _float(self, schema: FloatSchema) -> Dict[str, Any]:
        exported: Dict[str, Any] = {"type": "number"}
        for rule in schema.rules:
            if rule.kind == "number_min":
                exported["minimum"] = rule.parameter
            elif rule.kind == "number_max":
                exported["maximum"] = rule.parameter
            elif rule.kind == "positive":
                exported["exclusiveMinimum"] = 0
            elif rule.kind == "negative":
                exported["exclusiveMaximum"] = 0
        return exported


def _jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(cast(Any, value)))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def to_json_schema(schema: Schema[Any]) -> Dict[str, Any]:
    return _Exporter(openapi=False).export(schema)


def to_openapi_schema(schema: Schema[Any], *, inline: bool = False) -> Dict[str, Any]:
    document = _Exporter(openapi=True).export(schema)
    if inline:
        return inline_refs(document)
    return document


def _inline_node(node: Any, defs: Dict[str, Any], stack: Tuple[str, ...]) -> Any:
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/$defs/"):
            name = ref.rsplit("/", 1)[-1]
            if name in stack:
                raise SchemaExportError(
                    f"Cannot inline recursive schema reference {ref!r}; "
                    "recursive schemas require the non-inline export"
                )
            if name not in defs:
                raise SchemaExportError(f"Unresolved schema reference {ref!r}")
            resolved = _inline_node(defs[name], defs, (*stack, name))
            if not isinstance(resolved, dict):
                raise SchemaExportError(
                    f"Cannot apply sibling keys to non-object schema reference {ref!r}"
                )
            # Sibling keys (e.g. an object field's ``default``) override the definition.
            for key, value in node.items():
                if key != "$ref":
                    resolved[key] = _inline_node(value, defs, stack)
            return resolved
        return {key: _inline_node(value, defs, stack) for key, value in node.items()}
    if isinstance(node, list):
        return [_inline_node(item, defs, stack) for item in node]
    return node


def inline_refs(document: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve a document's ``#/$defs/...`` references into a self-contained schema.

    The exporter names every composite sub-schema under a top-level ``$defs`` and
    points at it with ``$ref``. Embedded under an OpenAPI path's ``requestBody`` those
    refs resolve against the OpenAPI document root (which has no ``$defs``), so tools
    like Swagger UI fail to dereference them. Inlining produces a flat, self-contained
    schema with no ``$ref``/``$defs``. Raises ``SchemaExportError`` for recursive
    schemas, which cannot be fully inlined.
    """
    working = deepcopy(document)
    defs = working.pop("$defs", {})
    return cast(Dict[str, Any], _inline_node(working, defs, ()))
