from importlib.metadata import version

from .adapters.export import (
    SchemaExportError,
    inline_refs,
    to_json_schema,
    to_openapi_schema,
)
from .core.errors import ValidationError, ValidationIssue
from .core.schema import ParseResult, Schema
from .schemas.builder import SchemaBuilder, tw, w
from .schemas.composition import (
    AnySchema,
    DictSchema,
    EnumSchema,
    IntersectionSchema,
    LiteralSchema,
    NoneSchema,
    NullableSchema,
    TupleSchema,
    UnionSchema,
)
from .schemas.constraints import ConstraintRule
from .schemas.primitives import BooleanSchema, FloatSchema, IntegerSchema, StringSchema
from .schemas.structured import ListSchema, ObjectSchema
from .schemas.typing import DataclassSchema, schema_from_type

__version__ = version("typewall")

__all__ = [
    "AnySchema",
    "BooleanSchema",
    "ConstraintRule",
    "DataclassSchema",
    "DictSchema",
    "EnumSchema",
    "FloatSchema",
    "IntegerSchema",
    "IntersectionSchema",
    "ListSchema",
    "LiteralSchema",
    "NoneSchema",
    "NullableSchema",
    "ObjectSchema",
    "ParseResult",
    "Schema",
    "SchemaBuilder",
    "SchemaExportError",
    "StringSchema",
    "TupleSchema",
    "UnionSchema",
    "ValidationError",
    "ValidationIssue",
    "__version__",
    "inline_refs",
    "schema_from_type",
    "to_json_schema",
    "to_openapi_schema",
    "tw",
    "w",
]
