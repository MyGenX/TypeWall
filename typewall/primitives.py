from typing import Any

from ._context import ParseContext
from ._sentinels import INVALID
from .schema import Schema


def _type_error(context: ParseContext, expected: str, value: Any) -> None:
    received = type(value).__name__
    context.add_issue(
        code="type_error",
        message=f"Expected {expected}, got {received}",
        expected=expected,
        received_type=received,
    )


class StringSchema(Schema[str]):
    __slots__ = ()

    def _parse(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, str):
            _type_error(context, "str", value)
            return INVALID
        return value


class IntegerSchema(Schema[int]):
    __slots__ = ()

    def _parse(self, value: Any, context: ParseContext) -> Any:
        if isinstance(value, bool) or not isinstance(value, int):
            _type_error(context, "int", value)
            return INVALID
        return value


class FloatSchema(Schema[float]):
    __slots__ = ()

    def _parse(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, float):
            _type_error(context, "float", value)
            return INVALID
        return value


class BooleanSchema(Schema[bool]):
    __slots__ = ()

    def _parse(self, value: Any, context: ParseContext) -> Any:
        if type(value) is not bool:
            _type_error(context, "bool", value)
            return INVALID
        return value
