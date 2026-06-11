# Schema Export

`to_json_schema()` emits JSON Schema 2020-12. `to_openapi_schema()` emits an OpenAPI 3.1-compatible schema object.

```python
from typewall import to_json_schema, w

schema = w.object({"name": w.str().min(2), "age": w.int().optional()})
document = to_json_schema(schema)
assert document["$schema"].endswith("2020-12/schema")
```

Non-representable refinements and transforms raise `SchemaExportError` rather than producing a misleading contract.
