from typing import Any, Tuple, Union, cast

from ..core.context import ParseContext
from ..core.schema import Schema
from ..core.sentinels import INVALID
from .constraints import ConstraintRule, compile_pattern


def _type_error(context: ParseContext, expected: str, value: Any) -> None:
    received = type(value).__name__
    context.add_issue(
        code="type_error",
        message=f"Expected {expected}, got {received}",
        expected=expected,
        received_type=received,
    )


class StringSchema(Schema[str]):
    __slots__ = ("rules",)

    rules: Tuple[ConstraintRule, ...]

    def __init__(self, rules: Tuple[ConstraintRule, ...] = ()) -> None:
        super().__init__()
        object.__setattr__(self, "rules", rules)

    def _with_rule(self, rule: ConstraintRule) -> "StringSchema":
        clone = self._clone()
        object.__setattr__(clone, "rules", (*self.rules, rule))
        return cast("StringSchema", clone)

    def min(self, length: int) -> "StringSchema":
        if isinstance(length, bool) or not isinstance(length, int) or length < 0:
            raise ValueError("String minimum length must be a non-negative integer")
        return self._with_rule(
            ConstraintRule(
                kind="string_min",
                code="string_too_short",
                message=f"Expected at least {length} characters",
                parameter=length,
            )
        )

    def max(self, length: int) -> "StringSchema":
        if isinstance(length, bool) or not isinstance(length, int) or length < 0:
            raise ValueError("String maximum length must be a non-negative integer")
        return self._with_rule(
            ConstraintRule(
                kind="string_max",
                code="string_too_long",
                message=f"Expected at most {length} characters",
                parameter=length,
            )
        )

    def email(self) -> "StringSchema":
        return self._with_rule(
            ConstraintRule("email", "invalid_email", "Invalid email address")
        )

    def url(self) -> "StringSchema":
        return self._with_rule(ConstraintRule("url", "invalid_url", "Invalid URL"))

    def uuid(self) -> "StringSchema":
        return self._with_rule(ConstraintRule("uuid", "invalid_uuid", "Invalid UUID"))

    def regex(self, pattern: Any) -> "StringSchema":
        compiled = compile_pattern(pattern)
        return self._with_rule(
            ConstraintRule(
                kind="regex",
                code="invalid_string",
                message="String does not match the required pattern",
                pattern=compiled,
            )
        )

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, str):
            _type_error(context, "str", value)
            return INVALID
        for rule in self.rules:
            if not rule.accepts(value):
                context.add_issue(code=rule.code, message=rule.message)
                return INVALID
        return value


class IntegerSchema(Schema[int]):
    __slots__ = ("rules",)

    rules: Tuple[ConstraintRule, ...]

    def __init__(self, rules: Tuple[ConstraintRule, ...] = ()) -> None:
        super().__init__()
        object.__setattr__(self, "rules", rules)

    def _with_rule(self, rule: ConstraintRule) -> "IntegerSchema":
        clone = self._clone()
        object.__setattr__(clone, "rules", (*self.rules, rule))
        return cast("IntegerSchema", clone)

    def min(self, value: int) -> "IntegerSchema":
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Integer minimum must be an int")
        return self._with_rule(
            ConstraintRule(
                "number_min", "number_too_small", f"Expected at least {value}", value
            )
        )

    def max(self, value: int) -> "IntegerSchema":
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Integer maximum must be an int")
        return self._with_rule(
            ConstraintRule(
                "number_max", "number_too_large", f"Expected at most {value}", value
            )
        )

    def positive(self) -> "IntegerSchema":
        return self._with_rule(
            ConstraintRule("positive", "not_positive", "Expected a positive number")
        )

    def negative(self) -> "IntegerSchema":
        return self._with_rule(
            ConstraintRule("negative", "not_negative", "Expected a negative number")
        )

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if isinstance(value, bool) or not isinstance(value, int):
            _type_error(context, "int", value)
            return INVALID
        for rule in self.rules:
            if not rule.accepts(value):
                context.add_issue(code=rule.code, message=rule.message)
                return INVALID
        return value


class FloatSchema(Schema[float]):
    __slots__ = ("rules",)

    rules: Tuple[ConstraintRule, ...]

    def __init__(self, rules: Tuple[ConstraintRule, ...] = ()) -> None:
        super().__init__()
        object.__setattr__(self, "rules", rules)

    def _with_rule(self, rule: ConstraintRule) -> "FloatSchema":
        clone = self._clone()
        object.__setattr__(clone, "rules", (*self.rules, rule))
        return cast("FloatSchema", clone)

    def min(self, value: Union[int, float]) -> "FloatSchema":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Float minimum must be an int or float")
        return self._with_rule(
            ConstraintRule(
                "number_min", "number_too_small", f"Expected at least {value}", value
            )
        )

    def max(self, value: Union[int, float]) -> "FloatSchema":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Float maximum must be an int or float")
        return self._with_rule(
            ConstraintRule(
                "number_max", "number_too_large", f"Expected at most {value}", value
            )
        )

    def positive(self) -> "FloatSchema":
        return self._with_rule(
            ConstraintRule("positive", "not_positive", "Expected a positive number")
        )

    def negative(self) -> "FloatSchema":
        return self._with_rule(
            ConstraintRule("negative", "not_negative", "Expected a negative number")
        )

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if not isinstance(value, float):
            _type_error(context, "float", value)
            return INVALID
        for rule in self.rules:
            if not rule.accepts(value):
                context.add_issue(code=rule.code, message=rule.message)
                return INVALID
        return value


class BooleanSchema(Schema[bool]):
    __slots__ = ()

    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        if type(value) is not bool:
            _type_error(context, "bool", value)
            return INVALID
        return value
