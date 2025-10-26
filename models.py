import datetime

from markdown_it.rules_block import table
from sqlmodel import SQLModel, Field,Relationship
from utils import Rol
import uuid

class LibraryBase(SQLModel):
    name:str | None = Field(default=None,description="Library name")

    addres: str | None = Field(default=None,description="Library addres")

class UserBase(SQLModel):
    name:str | None = Field(description="User name")
    year : int | None = Field(description="User year")
    rol: Rol | None = Field(description="Rol", default=Rol.READER)
    is_active: bool | None = Field(description="Active User", default=True)


class User(UserBase, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)


class Library(LibraryBase, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    date:datetime.datetime | None = Field(default_factory=datetime.datetime.now)

class

class CreateUser(UserBase):
    pass

class UpdateUser(LibraryBase):
    pass


class CreateLibrary(LibraryBase):
    pass

class UpdateLibrary(LibraryBase):
    pass

