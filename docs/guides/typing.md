---
title: "Python Typing"
description: "Derive schemas from annotations, TypedDict, and dataclasses"
---

`schema_from_type()` derives schemas from supported standard annotations, `TypedDict`, and dataclasses.

```python
from dataclasses import dataclass

from typewall import schema_from_type

@dataclass
class User:
    name: str
    age: int = 18

UserSchema = schema_from_type(User)
assert UserSchema.parse({"name": "Ada"}) == User(name="Ada")
```

<Note>
MyPy and Pyright fixtures verify the public generic output contract.
</Note>
