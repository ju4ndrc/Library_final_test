from fastapi import FastAPI
from .auth import auth_router
from .routers import library, users
from db import create_tables

app = FastAPI(lifespan=create_tables,title="Library",version="0.0.1")

app.include_router(library.router)
app.include_router(auth_router.router)
app.include_router(users.router)
@app.get("/")
async def root():
    return{"Hello":"world"}