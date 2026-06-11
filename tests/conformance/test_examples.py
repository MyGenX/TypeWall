from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

from examples.config_validation import main as config_main
from examples.fastapi_app import app

ROOT = Path(__file__).resolve().parents[2]


def test_config_example_runs() -> None:
    config_main()


def test_cli_example_runs() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "typewall.cli",
            "validate",
            "examples.cli.schema:User",
            "examples/cli/user.json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr


def test_fastapi_example_runs() -> None:
    response = TestClient(app).post("/users", json={"name": "Ada", "age": 37})
    assert response.status_code == 200
    assert response.json() == {"name": "Ada", "age": 37}
