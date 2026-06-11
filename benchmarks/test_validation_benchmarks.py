from __future__ import annotations

from typing import Any, Callable

from typewall import ValidationError, w


def test_primitive_validation(benchmark: Callable[..., Any]) -> None:
    schema = w.int().min(0)
    benchmark(schema.parse, 42)


def test_flat_object_validation(benchmark: Callable[..., Any]) -> None:
    schema = w.object(
        {"name": w.str(), "age": w.int(), "active": w.bool(), "score": w.float()}
    )
    payload = {"name": "Ada", "age": 37, "active": True, "score": 0.95}
    benchmark(schema.parse, payload)


def test_nested_collection_validation(benchmark: Callable[..., Any]) -> None:
    schema = w.object(
        {
            "teams": w.list(
                w.object(
                    {
                        "name": w.str(),
                        "members": w.list(w.object({"id": w.int(), "name": w.str()})),
                    }
                )
            )
        }
    )
    payload = {
        "teams": [
            {
                "name": "core",
                "members": [
                    {"id": index, "name": f"user-{index}"} for index in range(20)
                ],
            }
        ]
    }
    benchmark(schema.parse, payload)


def test_successful_union_validation(benchmark: Callable[..., Any]) -> None:
    schema = w.union((w.int(), w.str().uuid(), w.object({"id": w.int()})))
    benchmark(schema.parse, {"id": 7})


def test_aggregated_failure_validation(benchmark: Callable[..., Any]) -> None:
    schema = w.object(
        {
            "name": w.str().min(2),
            "age": w.int().min(0),
            "flags": w.list(w.bool()),
        }
    )
    payload = {"name": "", "age": -1, "flags": [1, "true", None]}

    def parse_failure() -> int:
        try:
            schema.parse(payload)
        except ValidationError as error:
            return len(error.issues)
        raise AssertionError("Expected validation failure")

    benchmark(parse_failure)
