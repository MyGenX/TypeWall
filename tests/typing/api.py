from typing import Dict, List

from typewall import (
    BooleanSchema,
    FloatSchema,
    IntegerSchema,
    ListSchema,
    ObjectSchema,
    StringSchema,
    w,
)

string_schema: StringSchema = w.str()
integer_schema: IntegerSchema = w.int()
float_schema: FloatSchema = w.float()
boolean_schema: BooleanSchema = w.bool()
list_schema: ListSchema[str] = w.list(w.str())
object_schema: ObjectSchema = w.object({"name": w.str()})

name: str = string_schema.parse("Ada")
age: int = integer_schema.parse(37)
ratio: float = float_schema.parse(1.5)
active: bool = boolean_schema.parse(True)
tags: List[str] = list_schema.parse(["python"])
user: Dict[str, object] = object_schema.parse({"name": "Ada"})
