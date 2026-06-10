from hypothesis import given
from hypothesis import strategies as st

from typewall import w


@given(st.lists(st.integers()))
def test_integer_list_round_trips_without_reusing_output(values: list[int]) -> None:
    parsed = w.list(w.int()).parse(values)
    assert parsed == values
    assert parsed is not values


@given(st.lists(st.one_of(st.integers(), st.text()), max_size=30))
def test_invalid_list_paths_are_ordered_indexes(values: list[object]) -> None:
    result = w.list(w.int()).safe_parse(values)
    expected = [
        index for index, value in enumerate(values) if not isinstance(value, int)
    ]
    assert [issue.path for issue in result.errors] == [(index,) for index in expected]


@given(st.text(), st.integers())
def test_reusing_schema_has_no_state_leak(name: str, age: int) -> None:
    schema = w.object({"name": w.str(), "age": w.int()})
    failed = schema.safe_parse({"name": age, "age": name})
    succeeded = schema.safe_parse({"name": name, "age": age})

    assert failed.ok is False
    assert succeeded.ok is True
    assert succeeded.data == {"name": name, "age": age}


@given(st.lists(st.text()))
def test_mutable_default_is_isolated_for_arbitrary_mutations(values: list[str]) -> None:
    schema = w.object({"items": w.list(w.str()).default([])})
    first = schema.parse({})
    first["items"].extend(values)
    second = schema.parse({})

    assert second == {"items": []}
