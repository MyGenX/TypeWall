from fastapi import Depends, FastAPI

from typewall import w
from typewall.integrations.fastapi import request_body

app = FastAPI()
user_body = request_body(w.object({"name": w.str(), "age": w.int().optional()}))


@app.post("/users", openapi_extra=user_body.openapi_extra)
async def create_user(user=Depends(user_body)):  # noqa: B008
    return user
