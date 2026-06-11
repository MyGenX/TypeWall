from __future__ import annotations

import subprocess
import sys

import typewall
from typewall.core import errors as core_errors
from typewall.core import schema as core_schema
from typewall.integrations import fastapi as integrations_fastapi
from typewall.schemas import composition as schema_composition


def test_root_package_exposes_canonical_objects() -> None:
    assert typewall.Schema is core_schema.Schema
    assert typewall.ParseResult is core_schema.ParseResult
    assert typewall.ValidationError is core_errors.ValidationError
    assert typewall.UnionSchema is schema_composition.UnionSchema


def test_fastapi_helper_reachable_via_canonical_path() -> None:
    assert hasattr(integrations_fastapi, "request_body")


def test_public_modules_import_in_fresh_interpreters() -> None:
    modules = (
        "typewall",
        "typewall.core",
        "typewall.schemas",
        "typewall.adapters",
        "typewall.integrations",
    )
    for module in modules:
        completed = subprocess.run(
            [sys.executable, "-c", f"import {module}"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
