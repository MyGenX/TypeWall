import types
from contextlib import suppress
from dataclasses import MISSING as DATACLASS_MISSING
from dataclasses import fields, is_dataclass
from typing import (
    Any,
    Dict,
    ForwardRef,
    List,
    Literal,
    NoReturn,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from typing_extensions import NotRequired, Required, is_typeddict

from ._context import ParseContext
from ._sentinels import INVALID
from .composition import LazySchema
from .primitives import BooleanSchema, FloatSchema, IntegerSchema, StringSchema
from .schema import Schema
from .structured import ListSchema, ObjectSchema

T = TypeVar("T")


class DataclassSchema(Schema[T]):
    __slots__ = ("dataclass_type", "object_schema")

    dataclass_type: Type[T]
    object_schema: ObjectSchema

    def __init__(self, dataclass_type: Type[T], object_schema: ObjectSchema) -> None:
        super().__init__()
        object.__setattr__(self, "dataclass_type", dataclass_type)
        object.__setattr__(self, "object_schema", object_schema)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        parsed = self.object_schema._parse(value, context)
        if parsed is INVALID:
            return INVALID
        return self.dataclass_type(**parsed)


class _TypeSchemaResolver:
    def __init__(self) -> None:
        self.cache: Dict[Any, Schema[Any]] = {}

    def build(self, annotation: Any, path: Tuple[str, ...] = ()) -> Schema[Any]:
        try:
            cached = self.cache.get(annotation)
        except TypeError:
            cached = None
        if cached is not None:
            return cached

        if annotation is Any:
            return self._remember(annotation, self._any_schema())
        if annotation is str:
            return self._remember(annotation, StringSchema())
        if annotation is int:
            return self._remember(annotation, IntegerSchema())
        if annotation is float:
            return self._remember(annotation, FloatSchema())
        if annotation is bool:
            return self._remember(annotation, BooleanSchema())
        if annotation is None or annotation is type(None):
            from .composition import NoneSchema

            return self._remember(annotation, NoneSchema())
        if isinstance(annotation, ForwardRef):
            self._unsupported(annotation, path)

        origin = get_origin(annotation)
        args = get_args(annotation)
        union_type = getattr(types, "UnionType", None)

        if origin in (list, List):
            if len(args) != 1:
                self._unsupported(annotation, path)
            return ListSchema(self.build(args[0], (*path, "item")))
        if origin in (dict, Dict):
            if len(args) != 2:
                self._unsupported(annotation, path)
            from .composition import DictSchema

            return DictSchema(
                self.build(args[0], (*path, "key")),
                self.build(args[1], (*path, "value")),
            )
        if origin in (tuple, Tuple):
            if not args or (len(args) == 2 and args[1] is Ellipsis):
                self._unsupported(annotation, path)
            from .composition import TupleSchema

            return TupleSchema(
                [
                    self.build(item, (*path, str(index)))
                    for index, item in enumerate(args)
                ]
            )
        if origin is Union or (union_type is not None and origin is union_type):
            from .composition import UnionSchema

            return UnionSchema(
                [
                    self.build(item, (*path, str(index)))
                    for index, item in enumerate(args)
                ]
            )
        if origin is Literal:
            from .composition import EnumSchema, LiteralSchema

            if len(args) == 1:
                return LiteralSchema(args[0])
            return EnumSchema(args)
        if is_typeddict(annotation):
            return self._build_typed_dict(annotation, path)
        if isinstance(annotation, type) and is_dataclass(annotation):
            return self._build_dataclass(annotation, path)

        self._unsupported(annotation, path)

    def _remember(self, annotation: Any, schema: Schema[Any]) -> Schema[Any]:
        with suppress(TypeError):
            self.cache[annotation] = schema
        return schema

    def _any_schema(self) -> Schema[Any]:
        from .composition import AnySchema

        return AnySchema()

    def _placeholder(self, annotation: Any) -> Tuple[LazySchema, Dict[str, Any]]:
        holder: Dict[str, Any] = {}
        placeholder = LazySchema(lambda: holder.get("schema"))
        self.cache[annotation] = placeholder
        return placeholder, holder

    def _build_typed_dict(
        self, annotation: Type[Any], path: Tuple[str, ...]
    ) -> ObjectSchema:
        _placeholder, holder = self._placeholder(annotation)
        try:
            hints = get_type_hints(annotation, include_extras=True)
            required_keys = set(getattr(annotation, "__required_keys__", ()))
            optional_keys = set(getattr(annotation, "__optional_keys__", ()))
            total = bool(getattr(annotation, "__total__", True))
            declared: Dict[str, Schema[Any]] = {}
            for name, field_annotation in hints.items():
                origin = get_origin(field_annotation)
                explicitly_required = origin is Required
                explicitly_optional = origin is NotRequired
                if explicitly_required or explicitly_optional:
                    field_annotation = get_args(field_annotation)[0]
                field_schema = self.build(field_annotation, (*path, name))
                required = explicitly_required or (
                    not explicitly_optional
                    and (name in required_keys or (not optional_keys and total))
                )
                declared[name] = field_schema if required else field_schema.optional()
            schema = ObjectSchema(declared)
        except Exception:
            self.cache.pop(annotation, None)
            raise
        holder["schema"] = schema
        self.cache[annotation] = schema
        return schema

    def _build_dataclass(
        self, annotation: Type[Any], path: Tuple[str, ...]
    ) -> DataclassSchema[Any]:
        _placeholder, holder = self._placeholder(annotation)
        try:
            hints = get_type_hints(annotation, include_extras=True)
            declared: Dict[str, Schema[Any]] = {}
            for field in fields(annotation):
                if not field.init:
                    continue
                if field.name not in hints:
                    self._unsupported(field.type, (*path, field.name))
                field_schema = self.build(hints[field.name], (*path, field.name))
                if field.default is not DATACLASS_MISSING:
                    field_schema = field_schema.default(field.default)
                elif field.default_factory is not DATACLASS_MISSING:
                    factory = cast(Any, field.default_factory)
                    field_schema = field_schema._with_default_factory(factory)
                declared[field.name] = field_schema
            schema = DataclassSchema(annotation, ObjectSchema(declared))
        except Exception:
            self.cache.pop(annotation, None)
            raise
        holder["schema"] = schema
        self.cache[annotation] = schema
        return schema

    def _unsupported(self, annotation: Any, path: Tuple[str, ...]) -> NoReturn:
        location = "$" if not path else "$." + ".".join(path)
        raise TypeError(f"Unsupported annotation at {location}: {annotation!r}")


def schema_from_type(annotation: Type[T]) -> Schema[T]:
    return cast(Schema[T], _TypeSchemaResolver().build(annotation))
