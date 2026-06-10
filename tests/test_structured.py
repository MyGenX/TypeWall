from collections import UserDict, UserList
from typing import Any, Iterator

from typewall import w


class MappingSubclass(dict):
    pass


class ListSubclass(list):
    pass


def test_object_parses_mapping_into_a_new_dict() -> None:
    source = MappingSubclass(name="Ada", age=37)
    parsed = w.object({"name": w.str(), "age": w.int()}).parse(source)

    assert parsed == {"name": "Ada", "age": 37}
    assert type(parsed) is dict
    assert parsed is not source


def test_object_accepts_general_mapping_implementations() -> None:
    source = UserDict({"name": "Ada"})
    assert w.object({"name": w.str()}).parse(source) == {"name": "Ada"}


def test_non_mapping_object_input_stops_at_the_object_path() -> None:
    result = w.object({"name": w.str()}).safe_parse([("name", "Ada")])

    assert [issue.path for issue in result.errors] == [()]
    assert result.errors[0].expected == "mapping"


def test_required_optional_and_default_fields() -> None:
    schema = w.object(
        {
            "name": w.str(),
            "age": w.int().optional(),
            "tags": w.list(w.str()).default([]),
        }
    )

    assert schema.parse({"name": "Ada"}) == {"name": "Ada", "tags": []}

    result = schema.safe_parse({})
    assert [(issue.path, issue.code) for issue in result.errors] == [
        (("name",), "missing")
    ]


def test_optional_field_still_validates_when_present() -> None:
    result = w.object({"age": w.int().optional()}).safe_parse({"age": "unknown"})
    assert [(issue.path, issue.code) for issue in result.errors] == [
        (("age",), "type_error")
    ]


def test_invalid_default_is_reported_at_field_path() -> None:
    schema = w.object({"name": w.str().default(1)})  # type: ignore[arg-type]
    result = schema.safe_parse({})

    assert [(issue.path, issue.code) for issue in result.errors] == [
        (("name",), "type_error")
    ]


def test_default_values_are_copied_per_parse() -> None:
    schema = w.object({"tags": w.list(w.str()).default([])})

    first = schema.parse({})
    second = schema.parse({})
    first["tags"].append("changed")

    assert first == {"tags": ["changed"]}
    assert second == {"tags": []}
    assert first["tags"] is not second["tags"]


def test_default_is_copied_when_the_schema_is_declared() -> None:
    declared_default: list[str] = []
    schema = w.object({"tags": w.list(w.str()).default(declared_default)})
    declared_default.append("outside")

    assert schema.parse({}) == {"tags": []}


def test_unknown_fields_are_rejected_after_declared_field_issues() -> None:
    schema = w.object({"name": w.str(), "age": w.int()})
    result = schema.safe_parse({"name": 1, "age": "old", "extra": True})

    assert [(issue.path, issue.code) for issue in result.errors] == [
        (("name",), "type_error"),
        (("age",), "type_error"),
        (("extra",), "unknown_key"),
    ]


def test_non_string_unknown_key_has_a_safe_string_path() -> None:
    result = w.object({}).safe_parse({1: "value"})
    assert result.errors[0].path == ("1",)
    assert result.errors[0].code == "unknown_key"


def test_list_returns_new_list_and_accepts_list_subclasses() -> None:
    source = ListSubclass([1, 2, 3])
    parsed = w.list(w.int()).parse(source)

    assert parsed == [1, 2, 3]
    assert type(parsed) is list
    assert parsed is not source


def test_user_list_is_rejected_because_it_is_not_a_python_list() -> None:
    result = w.list(w.int()).safe_parse(UserList([1, 2]))
    assert result.errors[0].path == ()
    assert result.errors[0].expected == "list"


def test_list_reports_every_invalid_index() -> None:
    result = w.list(w.int()).safe_parse(["zero", 1, "two"])

    assert [issue.path for issue in result.errors] == [(0,), (2,)]


def test_nested_object_inside_list_tracks_full_path() -> None:
    schema = w.object(
        {"users": w.list(w.object({"profile": w.object({"city": w.str()})}))}
    )
    result = schema.safe_parse(
        {"users": [{"profile": {"city": "Paris"}}, {"profile": {"city": 2}}]}
    )

    assert [issue.path for issue in result.errors] == [("users", 1, "profile", "city")]


def test_nested_list_inside_object_tracks_indexes() -> None:
    schema = w.object({"groups": w.list(w.list(w.bool()))})
    result = schema.safe_parse({"groups": [[True], [False, 1]]})
    assert [issue.path for issue in result.errors] == [("groups", 1, 1)]


def test_mapping_iteration_order_does_not_change_declared_issue_order() -> None:
    class ReversedMapping(dict):
        def __iter__(self) -> Iterator[Any]:
            return reversed(list(super().__iter__()))

    schema = w.object({"first": w.str(), "second": w.int()})
    result = schema.safe_parse(ReversedMapping(first=1, second="two"))

    assert [issue.path for issue in result.errors] == [("first",), ("second",)]
