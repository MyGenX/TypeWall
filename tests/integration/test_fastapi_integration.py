from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from typewall import w
from typewall.integrations.fastapi import request_body


def test_fastapi_dependency_validates_request_body() -> None:
    app = FastAPI()
    body = request_body(w.object({"name": w.str(), "age": w.int()}))

    @app.post("/users", openapi_extra=body.openapi_extra)
    async def create_user(payload=Depends(body)) -> dict[str, object]:  # noqa: B008
        return payload

    client = TestClient(app)
    response = client.post("/users", json={"name": "Ada", "age": 37})

    assert response.status_code == 200
    assert response.json() == {"name": "Ada", "age": 37}


def test_fastapi_dependency_maps_validation_errors_to_422_details() -> None:
    app = FastAPI()
    body = request_body(w.object({"name": w.str(), "age": w.int()}))

    @app.post("/users", openapi_extra=body.openapi_extra)
    async def create_user(payload=Depends(body)) -> dict[str, object]:  # noqa: B008
        return payload

    client = TestClient(app)
    response = client.post("/users", json={"name": 1, "age": "old"})

    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"] == [
        {"loc": ["body", "name"], "msg": "Expected str, got int", "type": "type_error"},
        {"loc": ["body", "age"], "msg": "Expected int, got str", "type": "type_error"},
    ]


def test_fastapi_dependency_contributes_openapi_schema() -> None:
    app = FastAPI()
    body = request_body(w.object({"name": w.str(), "age": w.int()}))

    @app.post("/users", openapi_extra=body.openapi_extra)
    async def create_user(payload=Depends(body)) -> dict[str, object]:  # noqa: B008
        return payload

    client = TestClient(app)
    openapi = client.get("/openapi.json").json()

    schema = openapi["paths"]["/users"]["post"]["requestBody"]["content"][
        "application/json"
    ]["schema"]
    assert schema["$ref"] == "#/$defs/schema_1"


def test_fastapi_dependency_rejects_malformed_json() -> None:
    app = FastAPI()
    body = request_body(w.object({"name": w.str()}))

    @app.post("/users")
    async def create_user(payload=Depends(body)) -> dict[str, object]:  # noqa: B008
        return payload

    response = TestClient(app).post(
        "/users", content="{", headers={"content-type": "application/json"}
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "value_error.json"
