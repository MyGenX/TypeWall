from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, input_text: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "typewall.cli", *args],
        cwd=ROOT,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_validates_json_from_stdin() -> None:
    result = run_cli(
        "validate",
        "tests.cli_targets:schema",
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
        "tests.cli_targets:schema",
        "-",
        input_text='{"name":"Ada","age":"old"}',
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["errors"][0]["path"] == ["age"]
    assert payload["errors"][0]["code"] == "type_error"


def test_cli_reports_invocation_errors_with_exit_code_two() -> None:
    result = run_cli("validate", "tests.cli_targets:missing", "-", input_text="{}")

    assert result.returncode == 2
    assert "no attribute" in result.stderr
