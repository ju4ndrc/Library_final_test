from fastapi import FastAPI
from .auth import auth_router
from .routers import library, users, authors, book
from db import create_tables

app = FastAPI(lifespan=create_tables,title="Library",version="0.0.1")

app.include_router(library.router)
app.include_router(auth_router.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(book.router)
@app.get("/")
async def root():
    return{"Hello":"world"}