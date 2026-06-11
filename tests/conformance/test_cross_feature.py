from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from typewall import schema_from_type, to_json_schema, w
from typewall.integrations.fastapi import request_body

ROOT = Path(__file__).resolve().parents[2]


def test_typing_derived_export_and_environment_defaults() -> None:
    @dataclass
    class Endpoint:
        host: str
        port: int = 443

    exported = to_json_schema(schema_from_type(Endpoint))
    assert "$defs" in exported

    settings = w.object({"HOST": w.str(), "PORT": w.int().default(443)})
    assert settings.parse_env({"HOST": "example.com"}) == {
        "HOST": "example.com",
        "PORT": 443,
    }


def test_cli_structured_errors_are_machine_readable() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "typewall.adapters.cli",
            "validate",
            "--json",
            "tests.integration.cli_targets:schema",
            "-",
        ],
        cwd=ROOT,
        input='{"name":1,"age":"secret-value"}',
        capture_output=True,
        text=True,
        check=False,
    )
    payload = json.loads(completed.stdout)
    assert completed.returncode == 1
    assert [issue["path"] for issue in payload["errors"]] == [["name"], ["age"]]
    assert "secret-value" not in completed.stdout


def test_fastapi_openapi_uses_exported_schema() -> None:
    app = FastAPI()
    schema = w.object({"name": w.str(), "age": w.int().default(18)})
    body = request_body(schema)

    @app.post("/users", openapi_extra=body.openapi_extra)
    async def create_user(user=Depends(body)):  # noqa: B008
        return user

    client = TestClient(app)
    assert client.post("/users", json={"name": "Ada"}).json()["age"] == 18
    operation = app.openapi()["paths"]["/users"]["post"]
    request_schema = operation["requestBody"]["content"]["application/json"]["schema"]
    assert "$defs" in request_schema
