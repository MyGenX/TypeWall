import json
from dataclasses import dataclass
from typing import Any, Dict

try:
    from fastapi import HTTPException, Request
except ImportError as error:  # pragma: no cover - exercised when extra is absent
    raise RuntimeError(
        "FastAPI integration requires the `typewall[fastapi]` extra"
    ) from error

from ..adapters.export import to_openapi_schema
from ..core.errors import ValidationError
from ..core.schema import Schema


def _detail(issue: Any) -> Dict[str, Any]:
    return {
        "loc": ["body", *[str(segment) for segment in issue.path]],
        "msg": issue.message,
        "type": issue.code,
    }


@dataclass(frozen=True)
class ValidatedBody:
    schema: Schema[Any]

    @property
    def openapi_extra(self) -> Dict[str, Any]:
        return {
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": to_openapi_schema(self.schema),
                    }
                },
            }
        }

    async def __call__(self, request: Request) -> Any:
        try:
            payload = await request.json()
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "loc": ["body"],
                        "msg": "Invalid JSON body",
                        "type": "value_error.json",
                    }
                ],
            ) from error

        try:
            return self.schema.parse(payload)
        except ValidationError as error:
            raise HTTPException(
                status_code=422,
                detail=[_detail(issue) for issue in error.issues],
            ) from error


def request_body(schema: Schema[Any]) -> ValidatedBody:
    return ValidatedBody(schema)


__all__ = ["ValidatedBody", "request_body"]
