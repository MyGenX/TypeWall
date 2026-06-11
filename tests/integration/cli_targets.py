from dataclasses import dataclass

from typewall import schema_from_type, w

schema = w.object({"name": w.str(), "age": w.int()})
not_a_schema = object()
none_schema = w.none()
tuple_schema = w.tuple((w.str(), w.int()))
tuple_output_schema = w.list(w.int()).transform(tuple)


@dataclass
class User:
    name: str
    age: int


dataclass_schema = schema_from_type(User)
