from fastapi import FastAPI
from .routers import library
from db import create_tables

app = FastAPI(lifespan=create_tables,title="Library",version="0.0.1")

app.include_router(library.router)

@app.get("/")
async def root():
    return{"Hello":"world"}