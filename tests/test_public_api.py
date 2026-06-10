from typewall import (
    BooleanSchema,
    FloatSchema,
    IntegerSchema,
    ListSchema,
    ObjectSchema,
    StringSchema,
    tw,
    w,
)


def test_preferred_builder_constructs_every_mvp_schema() -> None:
    assert isinstance(w.str(), StringSchema)
    assert isinstance(w.int(), IntegerSchema)
    assert isinstance(w.float(), FloatSchema)
    assert isinstance(w.bool(), BooleanSchema)
    assert isinstance(w.object({"name": w.str()}), ObjectSchema)
    assert isinstance(w.list(w.str()), ListSchema)


def test_tw_is_the_same_builder_alias() -> None:
    assert tw is w
    assert type(tw.str()) is type(w.str())


def test_object_schema_copies_its_declaration() -> None:
    fields = {"name": w.str()}
    schema = w.object(fields)
    fields["age"] = w.int()

    assert schema.parse({"name": "Ada"}) == {"name": "Ada"}


def test_invalid_schema_declarations_fail_early() -> None:
    try:
        w.object([])  # type: ignore[arg-type]
    except TypeError as error:
        assert str(error) == "Object schema fields must be a mapping"
    else:
        raise AssertionError("Expected invalid object declaration to fail")

    try:
        w.object({1: w.str()})  # type: ignore[dict-item]
    except TypeError as error:
        assert str(error) == "Object schema field names must be strings"
    else:
        raise AssertionError("Expected non-string field name to fail")

    try:
        w.object({"name": "not-a-schema"})  # type: ignore[dict-item]
    except TypeError as error:
        assert str(error) == "Object schema fields must contain Schema instances"
    else:
        raise AssertionError("Expected non-schema field to fail")

    try:
        w.list("not-a-schema")  # type: ignore[arg-type]
    except TypeError as error:
        assert str(error) == "List item schema must be a Schema instance"
    else:
        raise AssertionError("Expected invalid list declaration to fail")
