import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Dict, Mapping, Optional, Pattern, Union
from urllib.parse import urlsplit
from uuid import UUID

from email_validator import EmailNotValidError, validate_email


@dataclass(frozen=True)
class ConstraintRule:
    kind: str
    code: str
    message: str
    parameter: Any = None
    pattern: Optional[Pattern[str]] = None

    @property
    def metadata(self) -> Mapping[str, Any]:
        values: Dict[str, Any] = {"kind": self.kind, "code": self.code}
        if self.parameter is not None:
            values["value"] = self.parameter
        if self.pattern is not None:
            values["pattern"] = self.pattern.pattern
            values["flags"] = self.pattern.flags
        return MappingProxyType(values)

    def accepts(self, value: Any) -> bool:
        if self.kind == "string_min":
            return bool(len(value) >= self.parameter)
        if self.kind == "string_max":
            return bool(len(value) <= self.parameter)
        if self.kind == "number_min":
            return bool(value >= self.parameter)
        if self.kind == "number_max":
            return bool(value <= self.parameter)
        if self.kind == "positive":
            return bool(value > 0)
        if self.kind == "negative":
            return bool(value < 0)
        if self.kind == "email":
            try:
                validate_email(value, check_deliverability=False)
            except EmailNotValidError:
                return False
            return True
        if self.kind == "url":
            if any(character.isspace() for character in value):
                return False
            try:
                parsed = urlsplit(value)
                _ = parsed.port
            except ValueError:
                return False
            return parsed.scheme.lower() in {"http", "https"} and bool(parsed.hostname)
        if self.kind == "uuid":
            try:
                parsed_uuid = UUID(value)
            except (ValueError, AttributeError):
                return False
            return bool(str(parsed_uuid) == value.lower())
        if self.kind == "regex":
            assert self.pattern is not None
            return bool(self.pattern.search(value) is not None)
        raise RuntimeError(f"Unknown constraint kind: {self.kind}")


def compile_pattern(pattern: Union[str, Pattern[str]]) -> Pattern[str]:
    if isinstance(pattern, re.Pattern):
        return pattern
    if not isinstance(pattern, str):
        raise TypeError("Regex pattern must be a string or compiled pattern")
    try:
        return re.compile(pattern)
    except re.error as error:
        raise ValueError(f"Invalid regex pattern: {error}") from error
