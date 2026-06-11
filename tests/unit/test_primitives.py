from typing import Any, Type

import pytest

from typewall import ValidationError, w
from typewall.core.schema import Schema


class Text(str):
    pass


class Count(int):
    pass


class Ratio(float):
    pass


@pytest.mark.parametrize(
    ("schema", "value", "expected_type"),
    [
        (w.str(), "hello", str),
        (w.str(), Text("hello"), Text),
        (w.int(), 5, int),
        (w.int(), Count(5), Count),
        (w.float(), 1.5, float),
        (w.float(), Ratio(1.5), Ratio),
        (w.bool(), True, bool),
        (w.bool(), False, bool),
    ],
)
def test_primitive_schema_returns_valid_value_unchanged(
    schema: Schema[Any], value: Any, expected_type: Type[Any]
) -> None:
    parsed = schema.parse(value)
    assert parsed is value
    assert type(parsed) is expected_type


@pytest.mark.parametrize(
    ("schema", "value", "expected"),
    [
        (w.str(), 1, "str"),
        (w.str(), None, "str"),
        (w.int(), True, "int"),
        (w.int(), False, "int"),
        (w.int(), 1.0, "int"),
        (w.int(), "1", "int"),
        (w.float(), 1, "float"),
        (w.float(), True, "float"),
        (w.float(), "1.0", "float"),
        (w.bool(), 1, "bool"),
        (w.bool(), "yes", "bool"),
        (w.bool(), [], "bool"),
    ],
)
def test_primitive_schema_rejects_without_coercion(
    schema: Schema[Any], value: Any, expected: str
) -> None:
    with pytest.raises(ValidationError) as captured:
        schema.parse(value)

    issue = captured.value.issues[0]
    assert issue.code == "type_error"
    assert issue.expected == expected
    assert issue.received_type == type(value).__name__
    assert issue.path == ()
