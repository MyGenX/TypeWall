import os
from collections.abc import Mapping as MappingABC
from types import MappingProxyType
from typing import Any, Dict, Generic, List, Mapping, Optional, TypeVar, cast

from ._context import ParseContext
from ._sentinels import INVALID
from .environment import convert_env_value
from .errors import ValidationError
from .primitives import _type_error
from .schema import ParseResult, Schema

T = TypeVar("T")


class ObjectSchema(Schema[Dict[str, Any]]):
    __slots__ = ("fields",)

    fields: Mapping[str, Schema[Any]]

    def __init__(self, fields: Mapping[str, Schema[Any]]) -> None:
        if not isinstance(fields, MappingABC):
            raise TypeError("Object schema fields must be a mapping")
        super().__init__()
        copied: Dict[str, Schema[Any]] = {}
        for key, schema in fields.items():
            if not isinstance(key, str):
                raise TypeError("Object schema field names must be strings")
            if not isinstance(schema, Schema):
                raise TypeError("Object schema fields must contain Schema instances")
            copied[key] = schema
        object.__setattr__(self, "fields", MappingProxyType(copied))

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, Mapping):
            _type_error(context, "mapping", value)
            return INVALID

        output: Dict[str, Any] = {}
        has_errors = False
        for key, schema in self.fields.items():
            child = context.child(key)
            if key not in value:
                if schema.has_default:
                    parsed = schema._parse(schema.copy_default(), child)
                    if parsed is not INVALID:
                        output[key] = parsed
                    else:
                        has_errors = True
                elif schema.is_optional:
                    continue
                else:
                    child.add_issue(
                        code="missing",
                        message="Required field missing",
                        expected="present field",
                        received_type="missing",
                    )
                    has_errors = True
                continue

            parsed = schema._parse(value[key], child)
            if parsed is INVALID:
                has_errors = True
            else:
                output[key] = parsed

        for key in value:
            if key not in self.fields:
                context.child(str(key)).add_issue(
                    code="unknown_key",
                    message="Unknown field",
                    expected="declared field",
                    received_type=type(key).__name__,
                )
                has_errors = True

        return INVALID if has_errors else output

    def parse_env(
        self, mapping: Optional[Mapping[str, Any]] = None
    ) -> Dict[str, Any]:
        source = os.environ if mapping is None else mapping
        if not isinstance(source, MappingABC):
            raise TypeError("Environment source must be a mapping")

        context = ParseContext()
        output: Dict[str, Any] = {}
        for key, schema in self.fields.items():
            if key not in source:
                if schema.has_default:
                    parsed = schema._parse(schema.copy_default(), context.child(key))
                    if parsed is not INVALID:
                        output[key] = parsed
                elif not schema.is_optional:
                    context.child(key).add_issue(
                        code="missing",
                        message="Required field missing",
                        expected="present field",
                        received_type="missing",
                    )
                continue

            child = context.child(key)
            converted = convert_env_value(schema, source[key], child)
            if converted is INVALID:
                continue

            parsed = schema._parse(converted, child)
            if parsed is not INVALID:
                output[key] = parsed

        if context.issues:
            error = ValidationError(context.issues)
            if context.causes:
                raise error from context.causes[0]
            raise error
        return output

    def safe_parse_env(
        self, mapping: Optional[Mapping[str, Any]] = None
    ) -> ParseResult[Dict[str, Any]]:
        try:
            return ParseResult(ok=True, data=self.parse_env(mapping))
        except ValidationError as error:
            return ParseResult(ok=False, errors=error.issues)


class ListSchema(Schema[List[T]], Generic[T]):
    __slots__ = ("item_schema",)

    item_schema: Schema[T]

    def __init__(self, item_schema: Schema[T]) -> None:
        if not isinstance(item_schema, Schema):
            raise TypeError("List item schema must be a Schema instance")
        super().__init__()
        object.__setattr__(self, "item_schema", item_schema)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, list):
            _type_error(context, "list", value)
            return INVALID

        output: List[T] = []
        has_errors = False
        for index, item in enumerate(value):
            parsed = self.item_schema._parse(item, context.child(index))
            if parsed is INVALID:
                has_errors = True
            else:
                output.append(cast(T, parsed))
        return INVALID if has_errors else output
