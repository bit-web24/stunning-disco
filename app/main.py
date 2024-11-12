from fastapi import FastAPI
from .routers import user, auth

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
