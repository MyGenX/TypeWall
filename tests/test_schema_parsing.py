import pytest

from typewall import ValidationError, w
from typewall._context import ParseContext
from typewall._sentinels import INVALID, MISSING
from typewall.schema import Schema


def test_parse_returns_validated_value() -> None:
    assert w.str().parse("value") == "value"


def test_parse_raises_one_error_with_all_reachable_issues() -> None:
    schema = w.object({"name": w.str(), "scores": w.list(w.int())})

    with pytest.raises(ValidationError) as captured:
        schema.parse({"name": 10, "scores": ["one", "two"]})

    assert [issue.path for issue in captured.value.issues] == [
        ("name",),
        ("scores", 0),
        ("scores", 1),
    ]


def test_safe_parse_success_has_data_and_no_errors() -> None:
    result = w.int().safe_parse(42)

    assert result.ok is True
    assert result.data == 42
    assert result.errors == ()
    assert result.to_dict() == {}


def test_safe_parse_failure_has_errors_and_no_data() -> None:
    result = w.int().safe_parse("42")

    assert result.ok is False
    assert result.data is None
    assert len(result.errors) == 1
    assert result.to_dict() == {"$": ["Expected int, got str"]}


def test_base_schema_is_unchanged_by_optional_and_default_builders() -> None:
    base = w.str()
    optional = base.optional()
    defaulted = base.default("fallback")

    assert base is not optional
    assert base is not defaulted
    assert base.is_optional is False
    assert base.has_default is False
    assert optional.is_optional is True
    assert optional.has_default is False
    assert defaulted.is_optional is False
    assert defaulted.has_default is True

    schema = w.object({"base": base, "optional": optional, "defaulted": defaulted})
    result = schema.safe_parse({})
    assert result.ok is False
    assert [issue.path for issue in result.errors] == [("base",)]


def test_schema_reuse_does_not_leak_parse_state() -> None:
    schema = w.object({"name": w.str()})

    failed = schema.safe_parse({"name": 1})
    succeeded = schema.safe_parse({"name": "Ada"})

    assert failed.ok is False
    assert succeeded.ok is True
    assert succeeded.data == {"name": "Ada"}
    assert succeeded.errors == ()


def test_schema_instances_reject_direct_mutation() -> None:
    schema = w.str()

    with pytest.raises(AttributeError, match="immutable"):
        schema._optional = True  # type: ignore[misc]


def test_sentinel_repr_is_stable_for_debugging() -> None:
    assert repr(MISSING) == "MISSING"
    assert repr(INVALID) == "INVALID"


class BrokenSchema(Schema[str]):
    __slots__ = ()

    def _parse(self, value: object, context: ParseContext) -> object:
        return INVALID


def test_schema_defensively_rejects_invalid_result_without_issue() -> None:
    schema = BrokenSchema()

    with pytest.raises(RuntimeError, match="without a validation issue"):
        schema.parse("value")
    with pytest.raises(RuntimeError, match="without a validation issue"):
        schema.safe_parse("value")
