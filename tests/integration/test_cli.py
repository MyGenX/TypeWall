from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_cli(*args: str, input_text: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "typewall.adapters.cli", *args],
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_validates_json_from_stdin() -> None:
    result = run_cli(
        "validate",
        "tests.integration.cli_targets:schema",
        "-",
        input_text='{"name":"Ada","age":37}',
    )

    assert result.returncode == 0
    assert "Validation passed" in result.stdout
    assert result.stderr == ""


def test_cli_reports_validation_failures_in_json_mode() -> None:
    result = run_cli(
        "validate",
        "--json",
        "tests.integration.cli_targets:schema",
        "-",
        input_text='{"name":"Ada","age":"old"}',
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["errors"][0]["path"] == ["age"]
    assert payload["errors"][0]["code"] == "type_error"


def test_cli_reports_invocation_errors_with_exit_code_two() -> None:
    result = run_cli(
        "validate", "tests.integration.cli_targets:missing", "-", input_text="{}"
    )

    assert result.returncode == 2
    assert "no attribute" in result.stderr


def test_cli_validates_unicode_json_file(tmp_path: Path) -> None:
    payload = tmp_path / "user.json"
    payload.write_text(
        '{"name":"\u0394\u03bf\u03ba\u03b9\u03bc\u03ae","age":37}', encoding="utf-8"
    )
    result = run_cli("validate", "tests.integration.cli_targets:schema", str(payload))

    assert result.returncode == 0
    assert "\u0394\u03bf\u03ba\u03b9\u03bc\u03ae" in result.stdout


def test_cli_reports_malformed_json_and_non_schema_targets() -> None:
    malformed = run_cli(
        "validate",
        "tests.integration.cli_targets:schema",
        "-",
        input_text="{",
    )
    wrong_target = run_cli(
        "validate", "tests.integration.cli_targets:not_a_schema", "-", input_text="{}"
    )

    assert malformed.returncode == 2
    assert "Invalid JSON input" in malformed.stderr
    assert wrong_target.returncode == 2
    assert "does not reference" in wrong_target.stderr


def test_cli_human_validation_failure_uses_exit_code_one() -> None:
    result = run_cli(
        "validate",
        "tests.integration.cli_targets:schema",
        "-",
        input_text='{"name":1,"age":"old"}',
    )

    assert result.returncode == 1
    assert "name: type_error" in result.stdout
    assert "age: type_error" in result.stdout
