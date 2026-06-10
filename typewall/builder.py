import builtins
from typing import Any, Mapping, TypeVar

from .primitives import BooleanSchema, FloatSchema, IntegerSchema, StringSchema
from .schema import Schema
from .structured import ListSchema, ObjectSchema

T = TypeVar("T")


class SchemaBuilder:
    __slots__ = ()

    def str(self) -> StringSchema:
        return StringSchema()

    def int(self) -> IntegerSchema:
        return IntegerSchema()

    def float(self) -> FloatSchema:
        return FloatSchema()

    def bool(self) -> BooleanSchema:
        return BooleanSchema()

    def object(self, fields: Mapping[builtins.str, Schema[Any]]) -> ObjectSchema:
        return ObjectSchema(fields)

    def list(self, item_schema: Schema[T]) -> ListSchema[T]:
        return ListSchema(item_schema)


w = SchemaBuilder()
tw = w
