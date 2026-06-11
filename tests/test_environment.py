import pytest

from typewall import w


def test_parse_env_uses_only_the_supplied_mapping(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("name", "env-value")
    schema = w.object({"name": w.str()})

    assert schema.parse_env({"name": "mapping-value"}) == {"name": "mapping-value"}


def test_parse_env_reads_from_os_environ_when_no_mapping_is_supplied(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("name", "Ada")
    schema = w.object({"name": w.str()})

    assert schema.parse_env() == {"name": "Ada"}


def test_parse_env_converts_canonical_primitives() -> None:
    schema = w.object(
        {
            "name": w.str(),
            "age": w.int(),
            "ratio": w.float(),
            "active": w.bool(),
        }
    )

    assert schema.parse_env(
        {
            "name": "Ada",
            "age": "37",
            "ratio": "2.5",
            "active": "true",
        }
    ) == {"name": "Ada", "age": 37, "ratio": 2.5, "active": True}


def test_parse_env_rejects_noncanonical_boolean() -> None:
    result = w.object({"active": w.bool()}).safe_parse_env({"active": "yes"})

    assert result.errors[0].path == ("active",)
    assert result.errors[0].code == "invalid_env_value"


def test_parse_env_supports_nested_json_values() -> None:
    schema = w.object(
        {
            "profile": w.object(
                {
                    "name": w.str(),
                    "tags": w.list(w.str()).default([]),
                }
            )
        }
    )

    assert schema.parse_env({"profile": '{"name": "Ada", "tags": ["python"]}'}) == {
        "profile": {"name": "Ada", "tags": ["python"]}
    }


def test_parse_env_applies_defaults_and_missing_fields() -> None:
    schema = w.object(
        {
            "name": w.str(),
            "tags": w.list(w.str()).default([]),
            "alias": w.str().optional(),
        }
    )

    assert schema.parse_env({"name": "Ada"}) == {"name": "Ada", "tags": []}


def test_parse_env_reports_secret_like_values_without_echoing_them() -> None:
    secret = "super-secret-token-value"
    result = w.object({"age": w.int()}).safe_parse_env({"age": secret})

    assert secret not in str(result.errors[0])
    assert result.errors[0].path == ("age",)
    assert result.errors[0].code == "invalid_env_value"
