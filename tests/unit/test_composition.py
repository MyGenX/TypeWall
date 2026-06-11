import pytest

from typewall import ValidationError, w
from typewall.schemas.composition import LazySchema


def test_literal_distinguishes_boolean_from_integer() -> None:
    assert w.literal(1).parse(1) == 1
    result = w.literal(1).safe_parse(True)
    assert result.errors[0].code == "invalid_literal"


def test_enum_accepts_declared_member_and_rejects_configuration_errors() -> None:
    schema = w.enum(["admin", "user"])
    assert schema.parse("admin") == "admin"
    assert schema.safe_parse("guest").errors[0].code == "invalid_enum"
    with pytest.raises(ValueError, match="must not be empty"):
        w.enum([])
    with pytest.raises(ValueError, match="duplicates"):
        w.enum(["admin", "admin"])
    with pytest.raises(TypeError, match="sequence"):
        w.enum("admin")


def test_fixed_tuple_validates_length_and_positions() -> None:
    schema = w.tuple([w.str(), w.int()])
    assert schema.parse(("age", 42)) == ("age", 42)
    assert schema.safe_parse(("age",)).errors[0].code == "tuple_length"
    result = schema.safe_parse((1, "age"))
    assert [issue.path for issue in result.errors] == [(0,), (1,)]
    assert schema.safe_parse(["age", 42]).errors[0].code == "type_error"


def test_dictionary_reports_invalid_key_and_value_paths() -> None:
    result = w.dict(w.int(), w.bool()).safe_parse({"key": "value"})
    assert [(issue.path, issue.code) for issue in result.errors] == [
        (("key", "$key"), "type_error"),
        (("key",), "type_error"),
    ]
    assert w.dict(w.str(), w.int()).safe_parse([]).errors[0].expected == "mapping"


def test_dictionary_detects_transformed_key_collisions() -> None:
    schema = w.dict(w.str().transform(str.lower), w.int())
    result = schema.safe_parse({"A": 1, "a": 2})
    assert result.errors[0].path == ("a", "$key")
    assert result.errors[0].code == "key_collision"


def test_dictionary_rejects_unhashable_transformed_keys() -> None:
    schema = w.dict(w.str().transform(lambda value: [value]), w.int())
    result = schema.safe_parse({"key": 1})
    assert result.errors[0].code == "invalid_key"


def test_union_returns_first_successful_branch() -> None:
    schema = w.union(
        [
            w.str().transform(lambda value: f"first:{value}"),
            w.any().transform(lambda value: f"second:{value}"),
        ]
    )
    assert schema.parse("value") == "first:value"


def test_union_failure_retains_each_branch_issue() -> None:
    result = w.union([w.str(), w.int()]).safe_parse(1.5)
    issue = result.errors[0]
    assert issue.code == "union_error"
    assert len(issue.branch_issues) == 2
    assert [branch[0].expected for branch in issue.branch_issues] == ["str", "int"]


def test_union_requires_at_least_one_schema() -> None:
    with pytest.raises(ValueError, match="at least one"):
        w.union([])
    with pytest.raises(TypeError, match="sequence"):
        w.union(42)  # type: ignore[call-overload]
    with pytest.raises(TypeError, match="Schema instances"):
        w.union([w.str(), "invalid"])  # type: ignore[list-item]


def test_union_preserves_first_callback_exception_as_cause() -> None:
    first = RuntimeError("first")

    def fail(value: object) -> object:
        raise first

    schema = w.union([w.str().transform(fail), w.int().transform(fail)])
    with pytest.raises(ValidationError) as captured:
        schema.parse("value")
    assert captured.value.__cause__ is first


def test_intersection_merges_compatible_object_outputs() -> None:
    schema = w.intersection([w.object({"name": w.str()}), w.object({"age": w.int()})])
    assert schema.parse({"name": "Ada", "age": 37}) == {"name": "Ada", "age": 37}


def test_intersection_rejects_unknown_object_fields() -> None:
    schema = w.intersection([w.object({"name": w.str()}), w.object({"age": w.int()})])
    result = schema.safe_parse({"name": "Ada", "age": 37, "extra": True})
    assert result.errors[0].code == "unknown_key"
    assert result.errors[0].path == ("extra",)


def test_intersection_reports_member_failures_and_output_conflicts() -> None:
    failure = w.intersection([w.int().positive(), w.int().max(10)]).safe_parse(-1)
    assert failure.errors[0].code == "intersection_error"
    assert len(failure.errors[0].branch_issues) == 2

    conflict = w.intersection(
        [w.int().transform(lambda value: value + 1), w.int()]
    ).safe_parse(1)
    assert conflict.errors[0].code == "intersection_conflict"

    mapping_conflict = w.intersection(
        [
            w.any().transform(lambda value: {"key": 1}),
            w.any().transform(lambda value: {"key": 2}),
        ]
    ).safe_parse({})
    assert mapping_conflict.errors[0].code == "intersection_conflict"

    assert w.intersection([w.int(), w.int()]).parse(1) == 1


def test_intersection_requires_two_schemas() -> None:
    with pytest.raises(ValueError, match="at least two"):
        w.intersection([w.str()])
    with pytest.raises(TypeError, match="sequence"):
        w.intersection(42)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="Schema instances"):
        w.intersection([w.str(), "invalid"])  # type: ignore[list-item]


def test_intersection_callback_failure_is_chained() -> None:
    original = RuntimeError("callback")

    def fail(value: int) -> int:
        raise original

    schema = w.intersection([w.int().transform(fail), w.int()])
    with pytest.raises(ValidationError) as captured:
        schema.parse(1)
    assert captured.value.__cause__ is original


def test_nullable_any_and_none_schemas() -> None:
    assert w.nullable(w.str()).parse(None) is None
    assert w.nullable(w.str()).parse("value") == "value"
    marker = object()
    assert w.any().parse(marker) is marker
    assert w.none().parse(None) is None
    assert w.none().safe_parse(False).errors[0].code == "type_error"


def test_invalid_composition_declarations_fail_before_parsing() -> None:
    with pytest.raises(TypeError):
        w.tuple([w.str(), "invalid"])  # type: ignore[list-item]
    with pytest.raises(TypeError):
        w.dict(w.str(), "invalid")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        w.nullable("invalid")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        w.tuple(42)  # type: ignore[call-overload]
    with pytest.raises(TypeError):
        w.dict("invalid", w.int())  # type: ignore[arg-type]


def test_unresolved_lazy_schema_fails_clearly() -> None:
    with pytest.raises(TypeError, match="could not be resolved"):
        LazySchema(lambda: None).parse("value")


def test_composition_parse_still_raises_validation_error() -> None:
    with pytest.raises(ValidationError):
        w.union([w.str(), w.int()]).parse(None)
