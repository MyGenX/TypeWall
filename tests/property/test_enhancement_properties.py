import re
import string
from typing import List
from uuid import UUID

from hypothesis import given
from hypothesis import strategies as st
from typing_extensions import TypedDict

from typewall import schema_from_type, w


class GeneratedPayload(TypedDict):
    name: str
    scores: List[int]


@given(st.integers(), st.integers())
def test_integer_minimum_boundary_matches_python_comparison(
    value: int, minimum: int
) -> None:
    assert w.int().min(minimum).safe_parse(value).ok is (value >= minimum)


@given(st.one_of(st.text(), st.integers()))
def test_union_branch_selection_is_deterministic(value: object) -> None:
    schema = w.union(
        [
            w.str().transform(lambda item: ("str", item)),
            w.int().transform(lambda item: ("int", item)),
        ]
    )
    first = schema.safe_parse(value)
    second = schema.safe_parse(value)
    assert first == second


@given(
    st.text(alphabet=string.ascii_letters, min_size=1),
    st.integers(),
    st.integers(),
)
def test_dictionary_casefold_collision_never_overwrites(
    key: str, first: int, second: int
) -> None:
    upper = key.upper()
    lower = key.lower()
    if upper == lower:
        return
    result = w.dict(w.str().transform(str.lower), w.int()).safe_parse(
        {upper: first, lower: second}
    )
    assert result.ok is False
    assert result.errors[0].code == "key_collision"


@given(st.text(), st.text())
def test_regex_search_matches_python_re(pattern_text: str, value: str) -> None:
    try:
        pattern = re.compile(pattern_text)
    except re.error:
        return
    assert w.str().regex(pattern).safe_parse(value).ok is (
        pattern.search(value) is not None
    )


@given(st.uuids())
def test_canonical_uuid_strings_are_accepted(value: UUID) -> None:
    assert w.str().uuid().parse(str(value)) == str(value)


@given(st.text())
def test_relative_text_without_scheme_is_not_a_url(value: str) -> None:
    if "://" not in value:
        assert w.str().url().safe_parse(value).ok is False


@given(st.text(), st.lists(st.integers()))
def test_typing_derived_schema_accepts_generated_payloads(
    name: str, scores: list[int]
) -> None:
    payload: GeneratedPayload = {"name": name, "scores": scores}
    assert schema_from_type(GeneratedPayload).parse(payload) == payload
