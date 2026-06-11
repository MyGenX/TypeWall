from __future__ import annotations

import subprocess
import sys

import typewall
from typewall import composition, errors, schema
from typewall.core import errors as core_errors
from typewall.core import schema as core_schema
from typewall.schemas import composition as schema_composition


def test_legacy_modules_export_canonical_objects() -> None:
    assert schema.Schema is core_schema.Schema is typewall.Schema
    assert schema.ParseResult is core_schema.ParseResult is typewall.ParseResult
    assert errors.ValidationError is core_errors.ValidationError
    assert composition.UnionSchema is schema_composition.UnionSchema


def test_fastapi_legacy_and_canonical_helpers_are_identical() -> None:
    from typewall.fastapi import request_body as legacy_request_body
    from typewall.integrations.fastapi import request_body

    assert legacy_request_body is request_body


def test_public_modules_import_in_fresh_interpreters() -> None:
    modules = (
        "typewall",
        "typewall.core",
        "typewall.schemas",
        "typewall.adapters",
        "typewall.schema",
        "typewall.composition",
        "typewall.environment",
        "typewall.export",
        "typewall.cli",
    )
    for module in modules:
        completed = subprocess.run(
            [sys.executable, "-c", f"import {module}"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
