from __future__ import annotations

import json
from collections.abc import Mapping as MappingABC
from typing import Any

from ..core.context import ParseContext
from ..core.schema import Schema
from ..core.sentinels import INVALID
from ..schemas.composition import AnySchema, NoneSchema
from ..schemas.primitives import BooleanSchema, FloatSchema, IntegerSchema, StringSchema


def _invalid_env_value(
    context: ParseContext,
    expected: str,
    raw: Any,
    *,
    code: str,
    message: str,
) -> Any:
    context.add_issue(
        code=code,
        message=message,
        expected=expected,
        received_type=type(raw).__name__,
    )
    return INVALID


def _json_error(context: ParseContext, raw: Any, expected: str) -> Any:
    return _invalid_env_value(
        context,
        expected,
        raw,
        code="invalid_json",
        message=f"Invalid JSON for {expected}",
    )


def _convert_scalar(schema: Schema[Any], raw: Any, context: ParseContext) -> Any:
    if isinstance(schema, StringSchema):
        if not isinstance(raw, str):
            return _invalid_env_value(
                context,
                "str",
                raw,
                code="invalid_env_value",
                message="Invalid string environment value",
            )
        return raw
    if isinstance(schema, BooleanSchema):
        if not isinstance(raw, str):
            return _invalid_env_value(
                context,
                "bool",
                raw,
                code="invalid_env_value",
                message="Invalid boolean environment value",
            )
        normalized = raw.strip().lower()
        if normalized in {"true", "1"}:
            return True
        if normalized in {"false", "0"}:
            return False
        return _invalid_env_value(
            context,
            "bool",
            raw,
            code="invalid_env_value",
            message="Invalid boolean environment value",
        )
    if isinstance(schema, IntegerSchema):
        if not isinstance(raw, str):
            return _invalid_env_value(
                context,
                "int",
                raw,
                code="invalid_env_value",
                message="Invalid integer environment value",
            )
        text = raw.strip()
        if not text or any(character.isspace() for character in text):
            return _invalid_env_value(
                context,
                "int",
                raw,
                code="invalid_env_value",
                message="Invalid integer environment value",
            )
        try:
            return int(text)
        except ValueError:
            return _invalid_env_value(
                context,
                "int",
                raw,
                code="invalid_env_value",
                message="Invalid integer environment value",
            )
    if isinstance(schema, FloatSchema):
        if not isinstance(raw, str):
            return _invalid_env_value(
                context,
                "float",
                raw,
                code="invalid_env_value",
                message="Invalid float environment value",
            )
        text = raw.strip()
        try:
            return float(text)
        except ValueError:
            return _invalid_env_value(
                context,
                "float",
                raw,
                code="invalid_env_value",
                message="Invalid float environment value",
            )
    if isinstance(schema, NoneSchema):
        if not isinstance(raw, str):
            return _invalid_env_value(
                context,
                "None",
                raw,
                code="invalid_env_value",
                message="Invalid none environment value",
            )
        normalized = raw.strip().lower()
        if normalized in {"", "none", "null"}:
            return None
        return _invalid_env_value(
            context,
            "None",
            raw,
            code="invalid_env_value",
            message="Invalid none environment value",
        )
    if isinstance(schema, AnySchema):
        return raw
    return raw


def _convert_structured(schema: Schema[Any], raw: Any, context: ParseContext) -> Any:
    if not isinstance(raw, str):
        return raw
    from ..schemas.composition import DictSchema, TupleSchema
    from ..schemas.structured import ListSchema, ObjectSchema

    if isinstance(schema, (DictSchema, TupleSchema, ListSchema, ObjectSchema)):
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as error:
            context.record_cause(error)
            return _json_error(context, raw, type(schema).__name__)

        if isinstance(schema, TupleSchema):
            if not isinstance(parsed, list):
                return _json_error(context, raw, "tuple")
            return tuple(parsed)
        if isinstance(schema, ListSchema):
            if not isinstance(parsed, list):
                return _json_error(context, raw, "list")
            return parsed
        if isinstance(schema, DictSchema):
            if not isinstance(parsed, MappingABC):
                return _json_error(context, raw, "mapping")
            return dict(parsed)
        if isinstance(schema, ObjectSchema):
            if not isinstance(parsed, MappingABC):
                return _json_error(context, raw, "mapping")
            return dict(parsed)
    return raw


def convert_env_value(schema: Schema[Any], raw: Any, context: ParseContext) -> Any:
    structured = _convert_structured(schema, raw, context)
    if structured is INVALID:
        return INVALID
    scalar = _convert_scalar(schema, structured, context)
    if scalar is INVALID:
        return INVALID
    return scalar
