from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union

from typewall import (
    DataclassSchema,
    DictSchema,
    LiteralSchema,
    NullableSchema,
    Schema,
    TupleSchema,
    UnionSchema,
    schema_from_type,
    w,
)


@dataclass
class User:
    name: str
    age: int


literal_schema: LiteralSchema[str] = w.literal("admin")
dictionary_schema: DictSchema[str, int] = w.dict(w.str(), w.int())
tuple_schema: TupleSchema[Tuple[str, int]] = w.tuple((w.str(), w.int()))
union_schema: UnionSchema[Union[str, int]] = w.union((w.str(), w.int()))
nullable_schema: NullableSchema[str] = w.nullable(w.str())
dataclass_schema: Schema[User] = schema_from_type(User)

role: str = literal_schema.parse("admin")
counts: Dict[str, int] = dictionary_schema.parse({"one": 1})
pair: Tuple[str, int] = tuple_schema.parse(("age", 37))
identifier: Union[str, int] = union_schema.parse(37)
nickname: Optional[str] = nullable_schema.parse(None)
user: User = dataclass_schema.parse({"name": "Ada", "age": 37})
length_schema: Schema[int] = w.str().transform(len)
length: int = length_schema.parse("Ada")

assert isinstance(schema_from_type(User), DataclassSchema)
