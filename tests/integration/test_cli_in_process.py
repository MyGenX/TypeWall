from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pytest

from typewall.adapters.cli import main


def invoke(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *args: str,
    input_text: str = "",
) -> tuple[int, str, str]:
    monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))
    code = main(list(args))
    output = capsys.readouterr()
    return code, output.out, output.err


def test_in_process_cli_success_modes(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    human = invoke(
        monkeypatch,
        capsys,
        "validate",
        "tests.integration.cli_targets:schema",
        "-",
        input_text='{"name":"Ada","age":37}',
    )
    structured = invoke(
        monkeypatch,
        capsys,
        "validate",
        "--json",
        "tests.integration.cli_targets:dataclass_schema",
        "-",
        input_text='{"name":"Ada","age":37}',
    )
    none_value = invoke(
        monkeypatch,
        capsys,
        "validate",
        "tests.integration.cli_targets:none_schema",
        "-",
        input_text="null",
    )

    assert human[0] == 0 and "{'name': 'Ada', 'age': 37}" in human[1]
    assert json.loads(structured[1])["data"] == {"name": "Ada", "age": 37}
    assert none_value == (0, "Validation passed\n", "")


def test_in_process_cli_validation_failure_modes(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    human = invoke(
        monkeypatch,
        capsys,
        "validate",
        "tests.integration.cli_targets:schema",
        "-",
        input_text='{"name":1,"age":"old"}',
    )
    structured = invoke(
        monkeypatch,
        capsys,
        "validate",
        "--json",
        "tests.integration.cli_targets:schema",
        "-",
        input_text='{"name":1,"age":"old"}',
    )

    assert human[0] == 1 and "name: type_error" in human[1]
    payload = json.loads(structured[1])
    assert structured[0] == 1
    assert [issue["path"] for issue in payload["errors"]] == [["name"], ["age"]]


def test_in_process_cli_file_and_collection_output(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    payload = tmp_path / "tuple.json"
    payload.write_text("[1,2]", encoding="utf-8")
    code, stdout, stderr = invoke(
        monkeypatch,
        capsys,
        "validate",
        "--json",
        "tests.integration.cli_targets:tuple_output_schema",
        str(payload),
    )

    assert code == 0 and stderr == ""
    assert json.loads(stdout)["data"] == [1, 2]


@pytest.mark.parametrize(
    ("args", "input_text", "message"),
    [
        ((), "", "usage:"),
        (("validate", "invalid", "-"), "{}", "module:attribute"),
        (("validate", ":missing", "-"), "{}", "module:attribute"),
        (("validate", "missing.module:schema", "-"), "{}", "No module"),
        (
            ("validate", "tests.integration.cli_targets:not_a_schema", "-"),
            "{}",
            "does not reference",
        ),
        (
            ("validate", "tests.integration.cli_targets:schema", "-"),
            "{",
            "Invalid JSON input",
        ),
    ],
)
def test_in_process_cli_invocation_errors(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    args: tuple[str, ...],
    input_text: str,
    message: str,
) -> None:
    code, stdout, stderr = invoke(monkeypatch, capsys, *args, input_text=input_text)

    assert code == 2
    assert stdout == ""
    assert message in stderr
