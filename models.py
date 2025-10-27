import datetime
from typing import List
from pydantic import EmailStr
from sqlmodel import SQLModel, Field,Relationship
from utils import Rol
import uuid

class LibraryBase(SQLModel):
    name:str | None = Field(default=None,description="Library name")

    addres: str | None = Field(default=None,description="Library addres")

class UserBase(SQLModel):
    name:str | None = Field(description="User name")
    email: EmailStr = Field(default=None, unique = True)
    password: str
    year : int | None = Field(description="User year")
    rol: Rol | None = Field(description="Rol", default=Rol.READER)


class User(UserBase, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    is_active: bool | None = Field(description="Active User", default=True)

    #ralacion con prestamos
    lends: list["Lend"] = Relationship(back_populates="user")

class Library(LibraryBase, table=True):
    id:uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    date:datetime.datetime | None = Field(default_factory=datetime.datetime.now)

class BookBase(SQLModel):
    title: str = Field(description="Book title")
    isbn: str = Field(unique=True,description="Unique ISBN")
    year: int = Field(description="Publication year")
    copies: int = Field(default=1, description="Number of copies available")

class Book(BookBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4,primary_key=True)
    is_active: bool | None = Field(description="Active Book", default=True)

    #relacion con prestamos
    lends : list["Lend"] = Relationship(back_populates="book")
    #relacion inversa con author
    author_id: uuid.UUID = Field(foreign_key="author.id", ondelete="CASCADE")
    author : "Author" = Relationship(back_populates="books")

class LendBookBase(SQLModel):
    loan_date: datetime.date = Field(default_factory=datetime.date.today)
    return_date: datetime.date | None = None
    fine: float | None = Field(default=0.0, description="Fine for late return")


class Lend(LendBookBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")#relacion entre clase lend y clase user
    book_id: uuid.UUID = Field(foreign_key="book.id")#relacion entre clase book y clase prestamo

    #relaciones hacia muchos usuarios y muchos libros
    user:"User" = Relationship(back_populates="lends")
    book:"Book" = Relationship(back_populates="lends")

class AuthorBase(SQLModel):
    name:str | None = Field(description="Authors name")
    origin_country:str | None = Field(description="Origin country")
    year: int | None = Field(description="Born year")

class Author(AuthorBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    #cascade delete reference https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/cascade-delete-relationships/?utm_source=chatgpt.com#configure-automatic-deletion
    books: List["Book"] = Relationship(back_populates="author", passive_deletes="all")


class CreateBook(LibraryBase):
    pass

class UpdateBook(LibraryBase):
    pass

class CreateAuthor(AuthorBase):
    pass

class UpdateAuthor(AuthorBase):
    pass


class CreateUser(UserBase):
    pass

class UpdateUser(UserBase):
    pass


class CreateLibrary(LibraryBase):
    pass

class UpdateLibrary(LibraryBase):
    pass

