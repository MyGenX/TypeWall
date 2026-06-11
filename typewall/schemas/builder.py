import builtins
from typing import Any, Mapping, Sequence, Tuple, TypeVar, Union, overload

from ..core.schema import Schema
from .composition import (
    AnySchema,
    DictSchema,
    EnumSchema,
    IntersectionSchema,
    LiteralSchema,
    NoneSchema,
    NullableSchema,
    TupleSchema,
    UnionSchema,
)
from .primitives import BooleanSchema, FloatSchema, IntegerSchema, StringSchema
from .structured import ListSchema, ObjectSchema

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


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

    def literal(self, value: T) -> LiteralSchema[T]:
        return LiteralSchema(value)

    def enum(self, values: Sequence[T]) -> EnumSchema[T]:
        return EnumSchema(values)

    @overload
    def tuple(self, items: Tuple[Schema[T], Schema[U]]) -> TupleSchema[Tuple[T, U]]: ...

    @overload
    def tuple(
        self, items: Tuple[Schema[T], Schema[U], Schema[V]]
    ) -> TupleSchema[Tuple[T, U, V]]: ...

    @overload
    def tuple(self, items: Sequence[Schema[Any]]) -> TupleSchema[Tuple[Any, ...]]: ...

    def tuple(self, items: Sequence[Schema[Any]]) -> TupleSchema[Any]:
        return TupleSchema(items)

    def dict(self, key_schema: Schema[T], value_schema: Schema[U]) -> DictSchema[T, U]:
        return DictSchema(key_schema, value_schema)

    @overload
    def union(
        self, schemas: Tuple[Schema[T], Schema[U]]
    ) -> UnionSchema[Union[T, U]]: ...

    @overload
    def union(
        self, schemas: Tuple[Schema[T], Schema[U], Schema[V]]
    ) -> UnionSchema[Union[T, U, V]]: ...

    @overload
    def union(self, schemas: Sequence[Schema[Any]]) -> UnionSchema[Any]: ...

    def union(self, schemas: Sequence[Schema[Any]]) -> UnionSchema[Any]:
        return UnionSchema(schemas)

    def intersection(self, schemas: Sequence[Schema[T]]) -> IntersectionSchema[T]:
        return IntersectionSchema(schemas)

    def nullable(self, schema: Schema[T]) -> NullableSchema[T]:
        return NullableSchema(schema)

    def any(self) -> AnySchema:
        return AnySchema()

    def none(self) -> NoneSchema:
        return NoneSchema()


w = SchemaBuilder()
tw = w
