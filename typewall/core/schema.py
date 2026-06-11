from abc import ABC, abstractmethod
from collections.abc import Mapping as MappingABC
from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Dict, Generic, Mapping, Optional, Tuple, TypeVar, cast

from .context import ParseContext
from .errors import ValidationError, ValidationIssue, issues_to_dict
from .sentinels import INVALID, MISSING

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True)
class Refinement(Generic[T]):
    predicate: Callable[[T], bool]
    message: str
    code: str


@dataclass(frozen=True)
class ParseResult(Generic[T]):
    ok: bool
    data: Optional[T] = None
    errors: Tuple[ValidationIssue, ...] = ()

    def to_dict(self) -> Dict[str, list[str]]:
        return issues_to_dict(self.errors)


class Schema(ABC, Generic[T]):
    __slots__ = (
        "_default",
        "_default_factory",
        "_export_schema",
        "_optional",
        "_refinements",
        "_transforms",
    )

    _default: Any
    _default_factory: Optional[Callable[[], Any]]
    _export_schema: Optional[Mapping[str, Any]]
    _optional: bool
    _refinements: Tuple[Refinement[Any], ...]
    _transforms: Tuple[Callable[[Any], Any], ...]

    def __init__(
        self,
        optional: bool = False,
        default: Any = MISSING,
        default_factory: Optional[Callable[[], Any]] = None,
    ) -> None:
        object.__setattr__(self, "_optional", optional)
        object.__setattr__(self, "_default", default)
        object.__setattr__(self, "_default_factory", default_factory)
        object.__setattr__(self, "_export_schema", None)
        object.__setattr__(self, "_refinements", ())
        object.__setattr__(self, "_transforms", ())

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Schema instances are immutable")

    @property
    def is_optional(self) -> bool:
        return self._optional

    @property
    def has_default(self) -> bool:
        return self._default is not MISSING or self._default_factory is not None

    def optional(self) -> "Schema[T]":
        clone = self._clone()
        object.__setattr__(clone, "_optional", True)
        return clone

    def default(self, value: T) -> "Schema[T]":
        clone = self._clone()
        object.__setattr__(clone, "_optional", False)
        object.__setattr__(clone, "_default", deepcopy(value))
        object.__setattr__(clone, "_default_factory", None)
        return clone

    def copy_default(self) -> Any:
        if self._default_factory is not None:
            return self._default_factory()
        return deepcopy(self._default)

    def _with_default_factory(self, factory: Callable[[], T]) -> "Schema[T]":
        clone = self._clone()
        object.__setattr__(clone, "_optional", False)
        object.__setattr__(clone, "_default", MISSING)
        object.__setattr__(clone, "_default_factory", factory)
        return clone

    def refine(
        self,
        predicate: Callable[[T], bool],
        message: str,
        code: str = "custom",
    ) -> "Schema[T]":
        if not callable(predicate):
            raise TypeError("Refinement predicate must be callable")
        if not message:
            raise ValueError("Refinement message must not be empty")
        if not code:
            raise ValueError("Refinement code must not be empty")
        clone = self._clone()
        refinement = Refinement(predicate=predicate, message=message, code=code)
        object.__setattr__(clone, "_refinements", (*self._refinements, refinement))
        return clone

    def transform(self, callback: Callable[[T], U]) -> "Schema[U]":
        if not callable(callback):
            raise TypeError("Transform callback must be callable")
        clone = self._clone()
        object.__setattr__(clone, "_transforms", (*self._transforms, callback))
        return cast("Schema[U]", clone)

    def with_export_schema(self, schema: Mapping[str, Any]) -> "Schema[T]":
        if not isinstance(schema, MappingABC):
            raise TypeError("Export schema metadata must be a mapping")
        clone = self._clone()
        object.__setattr__(
            clone, "_export_schema", MappingProxyType(deepcopy(dict(schema)))
        )
        return clone

    def parse(self, value: Any) -> T:
        context = ParseContext()
        parsed = self._parse(value, context)
        if context.issues:
            error = ValidationError(context.issues)
            if context.causes:
                raise error from context.causes[0]
            raise error
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

    def _parse(self, value: Any, context: ParseContext) -> Any:
        issue_count = len(context.issues)
        parsed = self._parse_value(value, context)
        if parsed is INVALID or len(context.issues) != issue_count:
            return INVALID

        for refinement in self._refinements:
            try:
                accepted = refinement.predicate(cast(T, parsed))
            except Exception as error:
                context.record_cause(error)
                context.add_issue(
                    code="callback_error",
                    message=f"Refinement callback raised {type(error).__name__}",
                    received_type=type(error).__name__,
                )
                return INVALID
            if not accepted:
                context.add_issue(code=refinement.code, message=refinement.message)
                return INVALID

        transformed = parsed
        for callback in self._transforms:
            try:
                transformed = callback(transformed)
            except Exception as error:
                context.record_cause(error)
                context.add_issue(
                    code="callback_error",
                    message=f"Transform callback raised {type(error).__name__}",
                    received_type=type(error).__name__,
                )
                return INVALID
        return transformed

    @abstractmethod
    def _parse_value(self, value: Any, context: ParseContext) -> Any:
        raise NotImplementedError
