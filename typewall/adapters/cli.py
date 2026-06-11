from __future__ import annotations

import argparse
import importlib
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Optional, Sequence, cast

from ..core.errors import ValidationError
from ..core.schema import Schema


def _load_schema(target: str) -> Schema[Any]:
    if ":" not in target:
        raise ValueError("Target must be in module:attribute form")
    module_name, attribute_name = target.split(":", 1)
    if not module_name or not attribute_name:
        raise ValueError("Target must be in module:attribute form")
    module = importlib.import_module(module_name)
    try:
        candidate = getattr(module, attribute_name)
    except AttributeError as error:
        raise AttributeError(
            f"Module {module_name!r} has no attribute {attribute_name!r}"
        ) from error
    if not isinstance(candidate, Schema):
        raise TypeError(f"{target!r} does not reference a TypeWall schema")
    return candidate


def _read_json(path: Optional[str]) -> Any:
    if path in (None, "-"):
        payload = sys.stdin.read()
    else:
        assert path is not None
        payload = Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(payload)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON input: {error.msg}") from error


def _issue_to_dict(issue: Any) -> dict[str, Any]:
    return {
        "path": [str(segment) for segment in issue.path],
        "code": issue.code,
        "message": issue.message,
        "expected": issue.expected,
        "received_type": issue.received_type,
        "branch_issues": [
            [_issue_to_dict(branch_issue) for branch_issue in branch]
            for branch in issue.branch_issues
        ],
    }


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _to_jsonable(asdict(cast(Any, value)))
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value


def _print_human_success(data: Any) -> None:
    print("Validation passed")
    if data is not None:
        print(repr(data))


def _print_human_failure(error: ValidationError) -> None:
    print("Validation failed", file=sys.stdout)
    for issue in error.issues:
        print(
            f"{'.'.join(str(segment) for segment in issue.path) or '$'}: "
            f"{issue.code}: {issue.message}",
            file=sys.stdout,
        )


def _print_json_success(data: Any) -> None:
    print(
        json.dumps(
            {"ok": True, "data": _to_jsonable(data)},
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def _print_json_failure(error: ValidationError) -> None:
    print(
        json.dumps(
            {
                "ok": False,
                "errors": [_issue_to_dict(issue) for issue in error.issues],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="typewall")
    subparsers = parser.add_subparsers(dest="command")

    validate = subparsers.add_parser("validate", help="Validate JSON with a schema")
    validate.add_argument("target", help="module:attribute schema target")
    validate.add_argument("path", nargs="?", default="-", help="JSON file or -")
    validate.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command != "validate":
        parser.print_help(sys.stderr)
        return 2

    try:
        schema = _load_schema(args.target)
        payload = _read_json(args.path)
    except (OSError, AttributeError, ImportError, TypeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2

    try:
        data = schema.parse(payload)
    except ValidationError as error:
        if args.json_output:
            _print_json_failure(error)
        else:
            _print_human_failure(error)
        return 1

    if args.json_output:
        _print_json_success(data)
    else:
        _print_human_success(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
