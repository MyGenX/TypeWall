from dataclasses import FrozenInstanceError

import pytest

from typewall import ValidationError, ValidationIssue, w


def test_validation_issue_is_immutable_and_structured() -> None:
    result = w.object({"age": w.int()}).safe_parse({"age": "secret-42"})
    issue = result.errors[0]

    assert issue == ValidationIssue(
        path=("age",),
        code="type_error",
        message="Expected int, got str",
        expected="int",
        received_type="str",
    )
    with pytest.raises(FrozenInstanceError):
        issue.code = "changed"  # type: ignore[misc]


def test_issue_order_is_deterministic_for_fields_and_indexes() -> None:
    schema = w.object({"name": w.str(), "items": w.list(w.object({"count": w.int()}))})
    value = {"name": 1, "items": [{"count": "zero"}, {"count": "one"}]}

    first = schema.safe_parse(value)
    second = schema.safe_parse(value)

    expected = [("name",), ("items", 0, "count"), ("items", 1, "count")]
    assert [issue.path for issue in first.errors] == expected
    assert [issue.path for issue in second.errors] == expected


def test_validation_error_retains_issues_and_has_concise_string() -> None:
    with pytest.raises(ValidationError) as captured:
        w.object({"name": w.str(), "age": w.int()}).parse({"name": 1, "age": "old"})

    error = captured.value
    assert len(error.issues) == 2
    assert str(error) == (
        "Validation failed with 2 issues: name: Expected str, got int; "
        "age: Expected int, got str"
    )


def test_nested_errors_serialize_to_dot_paths() -> None:
    schema = w.object(
        {
            "profile": w.object({"address": w.object({"city": w.str()})}),
            "items": w.list(w.object({"name": w.str()})),
        }
    )
    result = schema.safe_parse(
        {
            "profile": {"address": {"city": 1}},
            "items": [{"name": "ok"}, {"name": "ok"}, {"name": 2}],
        }
    )

    assert result.to_dict() == {
        "profile.address.city": ["Expected str, got int"],
        "items.2.name": ["Expected str, got int"],
    }


def test_root_errors_use_documented_root_key() -> None:
    with pytest.raises(ValidationError) as captured:
        w.int().parse("not-an-int")

    assert captured.value.to_dict() == {"$": ["Expected int, got str"]}


def test_error_output_does_not_echo_sensitive_values() -> None:
    secret = "super-secret-token-value"

    with pytest.raises(ValidationError) as captured:
        w.int().parse(secret)

    error = captured.value
    assert secret not in str(error)
    assert secret not in repr(error.to_dict())
    assert error.issues[0].received_type == "str"
