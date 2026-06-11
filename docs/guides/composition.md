# Composition

TypeWall supports literals, enums, fixed tuples, typed dictionaries, unions, intersections, nullable values, any values, and `None`.

```python
from typewall import w

Identifier = w.union((w.int(), w.str().uuid()))
Coordinates = w.tuple((w.float(), w.float()))
Permissions = w.dict(w.str(), w.bool())
```

Union failures retain branch issues. Intersections require compatible parsed outputs.
