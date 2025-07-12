from fastapi import FastAPI
from app.api.v1 import routes_users

import app.db.models

app = FastAPI()

app.include_router(routes_users.router, prefix="/api/v1", tags=["users"])