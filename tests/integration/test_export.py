from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import pytest
from jsonschema import Draft202012Validator

from typewall import (
    Schema,
    SchemaExportError,
    schema_from_type,
    to_json_schema,
    to_openapi_schema,
    w,
)
from typewall.core.context import ParseContext
from typewall.schemas.composition import LazySchema


@dataclass
class RecursiveNode:
    value: int
    child: Optional["RecursiveNode"] = None


def test_nested_export_is_valid_and_deterministic() -> None:
    address = w.object({"city": w.str().min(2), "postal": w.str().optional()})
    schema = w.object(
        {
            "name": w.str().min(2),
            "age": w.int().min(0).optional(),
            "address": address,
            "history": w.list(address).default([]),
        }
    )
    first = to_json_schema(schema)
    second = to_json_schema(schema)

    Draft202012Validator.check_schema(first)
    assert first == second
    validator = Draft202012Validator(first)
    assert validator.is_valid({"name": "Ada", "address": {"city": "London"}})
    assert not validator.is_valid({"name": "A", "address": {"city": "L"}})


def test_runtime_only_behavior_requires_or_uses_explicit_metadata() -> None:
    runtime_only = w.str().transform(str.strip)
    with pytest.raises(SchemaExportError):
        to_json_schema(runtime_only)

    documented = runtime_only.with_export_schema({"type": "string", "minLength": 1})
    assert to_json_schema(documented)["minLength"] == 1


def test_typing_derived_schema_exports() -> None:
    @dataclass
    class User:
        name: str
        age: int = 18

    exported = to_json_schema(schema_from_type(User))
    Draft202012Validator.check_schema(exported)


def test_recursive_typing_derived_schema_uses_stable_references() -> None:
    exported = to_json_schema(schema_from_type(RecursiveNode))
    Draft202012Validator.check_schema(exported)
    assert exported["$ref"] == "#/$defs/schema_1"
    assert to_json_schema(schema_from_type(RecursiveNode))["$ref"] == "#/$defs/schema_1"


def test_export_maps_composition_and_primitive_constraints() -> None:
    schema = w.object(
        {
            "email": w.str().email(),
            "url": w.str().url(),
            "uuid": w.str().uuid(),
            "code": w.str().regex(r"^[A-Z]+$").max(8),
            "count": w.int().min(1).max(10),
            "positive": w.float().positive(),
            "negative": w.int().negative(),
            "enabled": w.bool(),
            "nothing": w.none(),
            "anything": w.any(),
            "literal": w.literal("fixed"),
            "role": w.enum(("admin", "user")),
            "pair": w.tuple((w.str(), w.int())),
            "labels": w.dict(w.str().regex(r"^[a-z]+$"), w.int()),
            "maybe": w.nullable(w.str()),
            "choice": w.union((w.str(), w.int())),
            "both": w.intersection(
                (
                    w.object({"name": w.str()}),
                    w.object({"age": w.int()}),
                )
            ),
        }
    )
    exported = to_json_schema(schema)

    Draft202012Validator.check_schema(exported)
    serialized = str(exported)
    for keyword in (
        "format",
        "pattern",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "prefixItems",
        "propertyNames",
        "anyOf",
        "allOf",
    ):
        assert keyword in serialized


def test_openapi_export_omits_json_schema_dialect() -> None:
    exported = to_openapi_schema(w.object({"name": w.str()}))
    assert "$schema" not in exported
    assert exported["$ref"] == "#/$defs/schema_1"


def test_export_rejects_invalid_dictionary_keys_and_unresolved_lazy_schema() -> None:
    with pytest.raises(SchemaExportError, match="string-compatible"):
        to_json_schema(w.dict(w.int(), w.str()))

    lazy = LazySchema(lambda: lazy)
    with pytest.raises(SchemaExportError, match="could not be resolved"):
        to_json_schema(lazy)


def test_export_rejects_refinements_and_unknown_schema_types() -> None:
    with pytest.raises(SchemaExportError, match="Refinements"):
        to_json_schema(w.str().refine(bool, "required"))

    class UnknownSchema(Schema[str]):
        def _parse_value(self, value: Any, context: ParseContext) -> Any:
            return value

    with pytest.raises(SchemaExportError, match="Unsupported schema type"):
        to_json_schema(UnknownSchema())


def test_export_metadata_is_copied_and_requires_a_mapping() -> None:
    metadata = {"type": "string", "examples": ["value"]}
    schema = w.str().transform(str.strip).with_export_schema(metadata)
    metadata["examples"].append("changed")

    assert to_json_schema(schema)["examples"] == ["value"]
    with pytest.raises(TypeError, match="mapping"):
        w.str().with_export_schema([])  # type: ignore[arg-type]
