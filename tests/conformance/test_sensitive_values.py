from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from typewall import ValidationError, w
from typewall.integrations.fastapi import request_body

ROOT = Path(__file__).resolve().parents[2]
SECRET = "super-secret-token-12345"


def test_environment_error_does_not_expose_secret() -> None:
    schema = w.object({"API_TOKEN": w.int()})
    try:
        schema.parse_env({"API_TOKEN": SECRET})
    except ValidationError as error:
        assert SECRET not in str(error)
        assert SECRET not in repr(error.issues)
    else:
        raise AssertionError("Expected validation failure")


def test_cli_error_does_not_expose_rejected_value() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "typewall.cli",
            "validate",
            "tests.integration.cli_targets:schema",
            "-",
        ],
        cwd=ROOT,
        input=f'{{"name":"Ada","age":"{SECRET}"}}',
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 1
    assert SECRET not in completed.stdout
    assert SECRET not in completed.stderr


def test_fastapi_error_does_not_expose_rejected_value() -> None:
    app = FastAPI()
    body = request_body(w.object({"token": w.int()}))

    @app.post("/tokens")
    async def create_token(token=Depends(body)):  # noqa: B008
        return token

    response = TestClient(app).post("/tokens", json={"token": SECRET})
    assert response.status_code == 422
    assert SECRET not in response.text
