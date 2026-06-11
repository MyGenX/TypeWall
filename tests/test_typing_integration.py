from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, ForwardRef, List, Literal, Optional, Tuple, Union

import pytest
from typing_extensions import NotRequired, Required, TypedDict

from typewall import DataclassSchema, schema_from_type


class Address(TypedDict):
    city: str


class UserInput(TypedDict):
    name: str
    address: Address
    nickname: NotRequired[str]


class PartialInput(TypedDict, total=False):
    identifier: Required[int]
    note: str


class UnsupportedInput(TypedDict):
    tags: set[str]


@dataclass
class User:
    name: str
    age: int = 18
    tags: List[str] = field(default_factory=list)


@dataclass
class Node:
    value: int
    child: Optional[Node] = None


@dataclass
class WithIgnoredField:
    name: str
    normalized: str = field(init=False, default="ready")


@dataclass
class UnsupportedDataclass:
    tags: set[str]


def test_schema_from_type_supports_nested_standard_annotations() -> None:
    annotation = List[Dict[str, Tuple[int, bool]]]
    schema = schema_from_type(annotation)

    value = [{"entry": (1, True)}]
    assert schema.parse(value) == value
    result = schema.safe_parse([{"entry": (True, 1)}])
    union_issue_paths = [issue.path for issue in result.errors]
    assert union_issue_paths == [(0, "entry", 0), (0, "entry", 1)]


def test_schema_from_type_supports_union_literal_any_and_none() -> None:
    schema = schema_from_type(Union[Literal["auto", "manual"], int, None])
    assert schema.parse("auto") == "auto"
    assert schema.parse(2) == 2
    assert schema.parse(None) is None
    assert schema.safe_parse(1.5).errors[0].code == "union_error"
    marker = object()
    assert schema_from_type(Any).parse(marker) is marker
    assert schema_from_type(float).parse(1.5) == 1.5
    assert schema_from_type(Literal["only"]).parse("only") == "only"


def test_unsupported_annotation_identifies_nested_path() -> None:
    with pytest.raises(TypeError, match=r"\$\.tags"):
        schema_from_type(UnsupportedInput)
    with pytest.raises(TypeError, match=r"\$"):
        schema_from_type(set[int])
    with pytest.raises(TypeError, match="ForwardRef"):
        schema_from_type(ForwardRef("Missing"))  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        schema_from_type([])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        schema_from_type(List)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        schema_from_type(Dict)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        schema_from_type(Tuple[int, ...])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match=r"\$\.tags"):
        schema_from_type(UnsupportedDataclass)


def test_typed_dict_required_optional_and_total_false_behavior() -> None:
    schema = schema_from_type(UserInput)
    assert schema.parse({"name": "Ada", "address": {"city": "London"}}) == {
        "name": "Ada",
        "address": {"city": "London"},
    }
    assert schema.safe_parse({"address": {"city": "London"}}).errors[0].path == (
        "name",
    )
    assert schema.safe_parse(
        {"name": "Ada", "address": {"city": "London"}, "nickname": 1}
    ).errors[0].path == ("nickname",)

    partial = schema_from_type(PartialInput)
    assert partial.parse({"identifier": 1}) == {"identifier": 1}
    assert partial.safe_parse({}).errors[0].path == ("identifier",)


def test_typed_dict_nested_errors_keep_full_path() -> None:
    result = schema_from_type(UserInput).safe_parse(
        {"name": "Ada", "address": {"city": 42}}
    )
    assert result.errors[0].path == ("address", "city")


def test_dataclass_schema_returns_instances_and_applies_defaults() -> None:
    schema = schema_from_type(User)
    assert isinstance(schema, DataclassSchema)

    first = schema.parse({"name": "Ada"})
    second = schema.parse({"name": "Grace"})
    assert first == User(name="Ada")
    assert second == User(name="Grace")
    first.tags.append("changed")
    assert second.tags == []


def test_recursive_dataclass_is_resolved_lazily() -> None:
    schema = schema_from_type(Node)
    parsed = schema.parse({"value": 1, "child": {"value": 2, "child": None}})
    assert parsed == Node(value=1, child=Node(value=2))


def test_recursive_dataclass_reports_nested_error_without_recursion_overflow() -> None:
    result = schema_from_type(Node).safe_parse(
        {"value": 1, "child": {"value": "invalid", "child": None}}
    )
    union_issue = result.errors[0]
    assert union_issue.path == ("child",)
    assert union_issue.code == "union_error"
    assert union_issue.branch_issues[0][0].path == ("child", "value")


def test_dataclass_ignores_non_init_fields() -> None:
    parsed = schema_from_type(WithIgnoredField).parse({"name": "Ada"})
    assert parsed == WithIgnoredField(name="Ada")
