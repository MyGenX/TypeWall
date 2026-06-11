from dataclasses import dataclass
from typing import List

from typewall import schema_from_type, w


@dataclass
class User:
    name: str


wrong_string: int = w.str().parse("Ada")
wrong_list: List[int] = w.list(w.str()).parse(["Ada"])
wrong_transform: str = w.str().transform(len).parse("Ada")
wrong_dataclass: str = schema_from_type(User).parse({"name": "Ada"})
