from collections.abc import Mapping as MappingABC
from typing import Any, Dict, Generic, List, Optional, Sequence, Tuple, TypeVar, cast

from ..core.context import ParseContext
from ..core.schema import Schema
from ..core.sentinels import INVALID
from .primitives import _type_error

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def _same_literal(left: Any, right: Any) -> bool:
    return type(left) is type(right) and left == right


class LiteralSchema(Schema[T], Generic[T]):
    __slots__ = ("literal",)

    literal: T

    def __init__(self, literal: T) -> None:
        super().__init__()
        object.__setattr__(self, "literal", literal)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not _same_literal(value, self.literal):
            context.add_issue(
                code="invalid_literal",
                message="Expected the declared literal value",
                expected=repr(self.literal),
                received_type=type(value).__name__,
            )
            return INVALID
        return value


class EnumSchema(Schema[T], Generic[T]):
    __slots__ = ("values",)

    values: Tuple[T, ...]

    def __init__(self, values: Sequence[T]) -> None:
        if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
            raise TypeError("Enum values must be a sequence")
        copied = tuple(values)
        if not copied:
            raise ValueError("Enum values must not be empty")
        for index, value in enumerate(copied):
            if any(_same_literal(value, previous) for previous in copied[:index]):
                raise ValueError("Enum values must not contain duplicates")
        super().__init__()
        object.__setattr__(self, "values", copied)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not any(_same_literal(value, member) for member in self.values):
            context.add_issue(
                code="invalid_enum",
                message="Expected one of the declared enum values",
                received_type=type(value).__name__,
            )
            return INVALID
        return value


class TupleSchema(Schema[T], Generic[T]):
    __slots__ = ("item_schemas",)

    item_schemas: Tuple[Schema[Any], ...]

    def __init__(self, item_schemas: Sequence[Schema[Any]]) -> None:
        if not isinstance(item_schemas, Sequence):
            raise TypeError("Tuple schemas must be a sequence")
        copied = tuple(item_schemas)
        if any(not isinstance(schema, Schema) for schema in copied):
            raise TypeError("Tuple items must contain Schema instances")
        super().__init__()
        object.__setattr__(self, "item_schemas", copied)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, tuple):
            _type_error(context, "tuple", value)
            return INVALID
        if len(value) != len(self.item_schemas):
            context.add_issue(
                code="tuple_length",
                message=(
                    f"Expected tuple length {len(self.item_schemas)}, got {len(value)}"
                ),
                expected=str(len(self.item_schemas)),
                received_type="tuple",
            )
            return INVALID

        output: List[Any] = []
        has_errors = False
        for index, (item, schema) in enumerate(zip(value, self.item_schemas)):
            parsed = schema._parse(item, context.child(index))
            if parsed is INVALID:
                has_errors = True
            else:
                output.append(parsed)
        return INVALID if has_errors else tuple(output)


class DictSchema(Schema[Dict[K, V]], Generic[K, V]):
    __slots__ = ("key_schema", "value_schema")

    key_schema: Schema[K]
    value_schema: Schema[V]

    def __init__(self, key_schema: Schema[K], value_schema: Schema[V]) -> None:
        if not isinstance(key_schema, Schema) or not isinstance(value_schema, Schema):
            raise TypeError("Dictionary key and value schemas must be Schema instances")
        super().__init__()
        object.__setattr__(self, "key_schema", key_schema)
        object.__setattr__(self, "value_schema", value_schema)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, MappingABC):
            _type_error(context, "mapping", value)
            return INVALID

        output: Dict[K, V] = {}
        has_errors = False
        for input_key, input_value in value.items():
            path_key = str(input_key)
            parsed_key = self.key_schema._parse(
                input_key, context.child(path_key).child("$key")
            )
            parsed_value = self.value_schema._parse(
                input_value, context.child(path_key)
            )
            if parsed_key is INVALID or parsed_value is INVALID:
                has_errors = True
                continue
            try:
                collision = parsed_key in output
            except TypeError:
                context.child(path_key).child("$key").add_issue(
                    code="invalid_key",
                    message="Parsed dictionary key is not hashable",
                    received_type=type(parsed_key).__name__,
                )
                has_errors = True
                continue
            if collision:
                context.child(path_key).child("$key").add_issue(
                    code="key_collision",
                    message="Parsed dictionary key collides with an existing key",
                    received_type=type(parsed_key).__name__,
                )
                has_errors = True
                continue
            output[cast(K, parsed_key)] = cast(V, parsed_value)
        return INVALID if has_errors else output


class UnionSchema(Schema[T], Generic[T]):
    __slots__ = ("members",)

    members: Tuple[Schema[Any], ...]

    def __init__(self, members: Sequence[Schema[Any]]) -> None:
        if not isinstance(members, Sequence):
            raise TypeError("Union members must be a sequence")
        copied = tuple(members)
        if not copied:
            raise ValueError("Union must contain at least one schema")
        if any(not isinstance(member, Schema) for member in copied):
            raise TypeError("Union members must contain Schema instances")
        super().__init__()
        object.__setattr__(self, "members", copied)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        branch_issues: List[Tuple[Any, ...]] = []
        for member in self.members:
            branch_context = ParseContext(path=context.path)
            parsed = member._parse(value, branch_context)
            if not branch_context.issues and parsed is not INVALID:
                return parsed
            branch_issues.append(tuple(branch_context.issues))
            if branch_context.causes:
                context.record_cause(branch_context.causes[0])
        context.add_issue(
            code="union_error",
            message="Value did not match any union member",
            branch_issues=tuple(branch_issues),
        )
        return INVALID


class IntersectionSchema(Schema[T], Generic[T]):
    __slots__ = ("members",)

    members: Tuple[Schema[Any], ...]

    def __init__(self, members: Sequence[Schema[Any]]) -> None:
        if not isinstance(members, Sequence):
            raise TypeError("Intersection members must be a sequence")
        copied = tuple(members)
        if len(copied) < 2:
            raise ValueError("Intersection must contain at least two schemas")
        if any(not isinstance(member, Schema) for member in copied):
            raise TypeError("Intersection members must contain Schema instances")
        super().__init__()
        object.__setattr__(self, "members", copied)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        outputs: List[Any] = []
        branch_issues: List[Tuple[Any, ...]] = []
        object_fields: Any = None
        if isinstance(value, MappingABC):
            from .structured import ObjectSchema

            if all(isinstance(member, ObjectSchema) for member in self.members):
                object_fields = {
                    key
                    for member in self.members
                    for key in cast(ObjectSchema, member).fields
                }
        for member in self.members:
            branch_context = ParseContext(path=context.path)
            branch_value = value
            if object_fields is not None:
                from .structured import ObjectSchema

                object_member = cast(ObjectSchema, member)
                branch_value = {
                    key: item
                    for key, item in value.items()
                    if key in object_member.fields
                }
            parsed = member._parse(branch_value, branch_context)
            if branch_context.issues or parsed is INVALID:
                branch_issues.append(tuple(branch_context.issues))
                if branch_context.causes:
                    context.record_cause(branch_context.causes[0])
            else:
                outputs.append(parsed)
                branch_issues.append(())
        if any(branch_issues):
            context.add_issue(
                code="intersection_error",
                message="Value did not satisfy every intersection member",
                branch_issues=tuple(branch_issues),
            )
            return INVALID

        if object_fields is not None:
            unknown_keys = [key for key in value if key not in object_fields]
            if unknown_keys:
                for key in unknown_keys:
                    context.child(str(key)).add_issue(
                        code="unknown_key",
                        message="Unknown field",
                        expected="declared field",
                        received_type=type(key).__name__,
                    )
                return INVALID

        first = outputs[0]
        if all(isinstance(output, MappingABC) for output in outputs):
            merged: Dict[Any, Any] = {}
            for output in outputs:
                for key, item in output.items():
                    if key in merged and merged[key] != item:
                        context.add_issue(
                            code="intersection_conflict",
                            message=f"Intersection outputs conflict at key {key!r}",
                        )
                        return INVALID
                    merged[key] = item
            return merged
        if any(output != first for output in outputs[1:]):
            context.add_issue(
                code="intersection_conflict",
                message="Intersection members produced conflicting outputs",
            )
            return INVALID
        return first


class NullableSchema(Schema[Optional[T]], Generic[T]):
    __slots__ = ("inner",)

    inner: Schema[T]

    def __init__(self, inner: Schema[T]) -> None:
        if not isinstance(inner, Schema):
            raise TypeError("Nullable schema must wrap a Schema instance")
        super().__init__()
        object.__setattr__(self, "inner", inner)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if value is None:
            return None
        return self.inner._parse(value, context)


class AnySchema(Schema[Any]):
    __slots__ = ()

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        return value


class NoneSchema(Schema[None]):
    __slots__ = ()

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if value is not None:
            _type_error(context, "None", value)
            return INVALID
        return None


class LazySchema(Schema[Any]):
    __slots__ = ("resolver",)

    resolver: Any

    def __init__(self, resolver: Any) -> None:
        super().__init__()
        object.__setattr__(self, "resolver", resolver)

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        schema = self.resolver()
        if not isinstance(schema, Schema) or schema is self:
            raise TypeError("Recursive schema could not be resolved")
        return schema._parse(value, context)
