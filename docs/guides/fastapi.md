# FastAPI

Install `typewall[fastapi]`, then use the canonical integration path:

```python
from fastapi import Depends, FastAPI
from typewall import w
from typewall.integrations.fastapi import request_body

app = FastAPI()
body = request_body(w.object({"name": w.str()}))

@app.post("/users", openapi_extra=body.openapi_extra)
async def create_user(user=Depends(body)):
    return user
```

Validation failures use HTTP 422 with body-relative paths and TypeWall issue codes.
