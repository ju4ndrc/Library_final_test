from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, text
from typing import Annotated

db_name = "library.sqlite3"
db_url = f"sqlite:///{db_name}"

engine = create_engine(db_url,echo=True)

def create_tables(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]