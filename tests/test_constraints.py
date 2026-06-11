import re

import pytest

from typewall import ConstraintRule, ValidationError, w


def test_string_length_constraints_are_inclusive_and_immutable() -> None:
    base = w.str()
    constrained = base.min(2).max(4)

    assert constrained.parse("ab") == "ab"
    assert constrained.parse("abcd") == "abcd"
    assert base.parse("") == ""
    assert [issue.code for issue in constrained.safe_parse("a").errors] == [
        "string_too_short"
    ]
    assert [issue.code for issue in constrained.safe_parse("abcde").errors] == [
        "string_too_long"
    ]


@pytest.mark.parametrize("invalid", [-1, True, 1.5, "2"])
def test_string_length_rejects_invalid_configuration(invalid: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        w.str().min(invalid)  # type: ignore[arg-type]


def test_numeric_range_constraints_are_inclusive() -> None:
    integer = w.int().min(1).max(3)
    floating = w.float().min(1).max(3.5)

    assert integer.parse(1) == 1
    assert integer.parse(3) == 3
    assert floating.parse(1.0) == 1.0
    assert floating.parse(3.5) == 3.5
    assert integer.safe_parse(0).errors[0].code == "number_too_small"
    assert integer.safe_parse(4).errors[0].code == "number_too_large"


def test_positive_and_negative_reject_zero() -> None:
    assert w.int().positive().safe_parse(0).errors[0].code == "not_positive"
    assert w.int().negative().safe_parse(0).errors[0].code == "not_negative"
    assert w.float().positive().parse(0.1) == 0.1
    assert w.float().negative().parse(-0.1) == -0.1


@pytest.mark.parametrize("invalid", [True, "1", None])
def test_numeric_constraints_reject_invalid_configuration(invalid: object) -> None:
    with pytest.raises(TypeError):
        w.int().min(invalid)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        w.float().max(invalid)  # type: ignore[arg-type]


def test_constraint_order_and_metadata_are_stable() -> None:
    schema = w.str().min(2).max(4).email()

    assert [rule.kind for rule in schema.rules] == [
        "string_min",
        "string_max",
        "email",
    ]
    assert dict(schema.rules[0].metadata) == {
        "kind": "string_min",
        "code": "string_too_short",
        "value": 2,
    }
    with pytest.raises(TypeError):
        schema.rules[0].metadata["value"] = 3  # type: ignore[index]
    regex_metadata = dict(
        w.str().regex(re.compile("cat", re.IGNORECASE)).rules[0].metadata
    )
    assert regex_metadata["pattern"] == "cat"
    assert regex_metadata["flags"] & re.IGNORECASE


@pytest.mark.parametrize(
    "email",
    ["ada@example.com", "δοκιμή@παράδειγμα.δοκιμή", "user+tag@example.co.uk"],
)
def test_email_accepts_supported_syntax_without_normalizing(email: str) -> None:
    parsed = w.str().email().parse(email)
    assert parsed == email
    assert parsed is email


@pytest.mark.parametrize(
    "email", ["not-an-email", "missing@", "@example.com", "two@@example.com"]
)
def test_email_rejects_invalid_syntax(email: str) -> None:
    assert w.str().email().safe_parse(email).errors[0].code == "invalid_email"


@pytest.mark.parametrize(
    "url",
    ["https://example.com/path?q=1", "http://localhost:8080", "https://例え.テスト"],
)
def test_url_accepts_absolute_http_urls(url: str) -> None:
    assert w.str().url().parse(url) == url


@pytest.mark.parametrize(
    "url",
    ["/relative/path", "example.com", "ftp://example.com", "https://", "https://a b"],
)
def test_url_rejects_relative_or_malformed_values(url: str) -> None:
    assert w.str().url().safe_parse(url).errors[0].code == "invalid_url"


def test_url_rejects_invalid_port() -> None:
    assert w.str().url().safe_parse("https://example.com:99999").errors[0].code == (
        "invalid_url"
    )


def test_uuid_accepts_canonical_text_and_case_variation() -> None:
    lower = "8d74b7d1-0f36-42da-a5fc-f24e5827d1c3"
    upper = lower.upper()
    assert w.str().uuid().parse(lower) == lower
    assert w.str().uuid().parse(upper) == upper


@pytest.mark.parametrize(
    "value",
    [
        "not-a-uuid",
        "8d74b7d10f3642daa5fcf24e5827d1c3",
        "{8d74b7d1-0f36-42da-a5fc-f24e5827d1c3}",
    ],
)
def test_uuid_rejects_noncanonical_or_malformed_text(value: str) -> None:
    assert w.str().uuid().safe_parse(value).errors[0].code == "invalid_uuid"


def test_regex_uses_search_semantics_for_string_and_compiled_patterns() -> None:
    assert w.str().regex("cat").parse("concatenate") == "concatenate"
    assert w.str().regex(re.compile(r"\d+")).parse("item-42") == "item-42"
    assert w.str().regex("cat").safe_parse("dog").errors[0].code == "invalid_string"


def test_regex_rejects_invalid_declarations_before_parsing() -> None:
    with pytest.raises(ValueError, match="Invalid regex pattern"):
        w.str().regex("[")
    with pytest.raises(TypeError, match="Regex pattern"):
        w.str().regex(42)


def test_unknown_constraint_kind_fails_defensively() -> None:
    with pytest.raises(RuntimeError, match="Unknown constraint"):
        ConstraintRule("unknown", "unknown", "unknown").accepts("value")


def test_all_constraint_configuration_branches() -> None:
    with pytest.raises(ValueError):
        w.str().max(-1)
    with pytest.raises(TypeError):
        w.int().max(1.5)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        w.float().min("1")  # type: ignore[arg-type]
    assert w.float().min(2).safe_parse(1.5).errors[0].code == "number_too_small"


def test_constraints_run_only_after_strict_type_validation() -> None:
    result = w.str().email().safe_parse(42)
    assert [issue.code for issue in result.errors] == ["type_error"]


def test_constraint_failure_is_at_the_nested_value_path() -> None:
    result = w.object({"profile": w.object({"name": w.str().min(2)})}).safe_parse(
        {"profile": {"name": "A"}}
    )
    assert result.errors[0].path == ("profile", "name")


def test_validation_error_remains_the_public_failure_type() -> None:
    with pytest.raises(ValidationError):
        w.int().positive().parse(0)
