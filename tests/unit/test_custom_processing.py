import pytest

from typewall import ValidationError, w


def test_refinement_rejection_uses_configured_message_and_code() -> None:
    schema = w.int().refine(lambda value: value % 2 == 0, "Expected even", "even")
    result = schema.safe_parse(3)

    assert [(issue.path, issue.code, issue.message) for issue in result.errors] == [
        ((), "even", "Expected even")
    ]


def test_builtin_failure_skips_refinement() -> None:
    calls: list[object] = []
    schema = w.int().refine(lambda value: not calls.append(value), "unused")

    assert schema.safe_parse("not-int").errors[0].code == "type_error"
    assert calls == []


def test_transforms_run_in_declaration_order() -> None:
    schema = w.str().transform(str.strip).transform(str.upper).transform(len)
    assert schema.parse("  Ada  ") == 3


def test_transform_is_skipped_after_refinement_failure() -> None:
    calls: list[str] = []
    schema = (
        w.str()
        .refine(lambda value: False, "Rejected")
        .transform(lambda value: calls.append(value))
    )
    assert schema.safe_parse("value").errors[0].code == "custom"
    assert calls == []


@pytest.mark.parametrize("stage", ["refinement", "transform"])
def test_callback_exception_is_structured_and_chained(stage: str) -> None:
    original = RuntimeError("sensitive callback detail")

    def raise_error(value: object) -> object:
        raise original

    if stage == "refinement":
        schema = w.str().refine(raise_error, "unused")  # type: ignore[arg-type]
    else:
        schema = w.str().transform(raise_error)

    with pytest.raises(ValidationError) as captured:
        schema.parse("value")

    assert captured.value.issues[0].code == "callback_error"
    assert captured.value.__cause__ is original
    assert "sensitive callback detail" not in str(captured.value)


def test_custom_processing_keeps_nested_path() -> None:
    schema = w.object(
        {"age": w.int().refine(lambda value: value >= 18, "Adult required")}
    )
    assert schema.safe_parse({"age": 12}).errors[0].path == ("age",)


def test_custom_schema_reuse_and_configuration_are_isolated() -> None:
    base = w.str()
    refined = base.refine(str.islower, "Lowercase required")
    transformed = refined.transform(str.upper)

    assert base.parse("UPPER") == "UPPER"
    assert refined.parse("lower") == "lower"
    assert transformed.parse("lower") == "LOWER"
    assert transformed.safe_parse("UPPER").ok is False
    assert transformed.parse("lower") == "LOWER"


def test_invalid_callback_configuration_fails_early() -> None:
    with pytest.raises(TypeError):
        w.str().refine("invalid", "message")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        w.str().refine(lambda value: True, "")
    with pytest.raises(ValueError):
        w.str().refine(lambda value: True, "message", "")
    with pytest.raises(TypeError):
        w.str().transform("invalid")  # type: ignore[arg-type]
