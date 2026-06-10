from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Generic, Optional, Tuple, TypeVar, cast

from ._context import ParseContext
from ._sentinels import INVALID, MISSING
from .errors import ValidationError, ValidationIssue, issues_to_dict

T = TypeVar("T")


@dataclass(frozen=True)
class ParseResult(Generic[T]):
    ok: bool
    data: Optional[T] = None
    errors: Tuple[ValidationIssue, ...] = ()

    def to_dict(self) -> Dict[str, list[str]]:
        return issues_to_dict(self.errors)


class Schema(ABC, Generic[T]):
    __slots__ = ("_default", "_optional")

    _default: Any
    _optional: bool

    def __init__(self, optional: bool = False, default: Any = MISSING) -> None:
        object.__setattr__(self, "_optional", optional)
        object.__setattr__(self, "_default", default)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Schema instances are immutable")

    @property
    def is_optional(self) -> bool:
        return self._optional

    @property
    def has_default(self) -> bool:
        return self._default is not MISSING

    def optional(self) -> "Schema[T]":
        clone = self._clone()
        object.__setattr__(clone, "_optional", True)
        return clone

    def default(self, value: T) -> "Schema[T]":
        clone = self._clone()
        object.__setattr__(clone, "_optional", False)
        object.__setattr__(clone, "_default", deepcopy(value))
        return clone

    def copy_default(self) -> Any:
        return deepcopy(self._default)

    def parse(self, value: Any) -> T:
        context = ParseContext()
        parsed = self._parse(value, context)
        if context.issues:
            raise ValidationError(context.issues)
        if parsed is INVALID:
            raise RuntimeError("Schema returned no value without a validation issue")
        return cast(T, parsed)

    def safe_parse(self, value: Any) -> ParseResult[T]:
        context = ParseContext()
        parsed = self._parse(value, context)
        if context.issues:
            return ParseResult(ok=False, errors=tuple(context.issues))
        if parsed is INVALID:
            raise RuntimeError("Schema returned no value without a validation issue")
        return ParseResult(ok=True, data=cast(T, parsed))

    def _clone(self) -> "Schema[T]":
        clone = object.__new__(type(self))
        for cls in type(self).__mro__:
            slots = cls.__dict__.get("__slots__", ())
            if isinstance(slots, str):
                slots = (slots,)
            for slot in slots:
                if slot.startswith("__") or not hasattr(self, slot):
                    continue
                object.__setattr__(clone, slot, getattr(self, slot))
        return clone

    @abstractmethod
    def _parse(self, value: Any, context: ParseContext) -> Any:
        raise NotImplementedError
