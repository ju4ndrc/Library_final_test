import uuid
from http.client import responses

from fastapi import APIRouter,HTTPException,status
from sqlmodel import select
from db import SessionDep
from models import Book, CreateBook, UpdateBook, Author

router = APIRouter(prefix="/books",tags=["Books"])

@router.post("/",response_model=Book,status_code=status.HTTP_201_CREATED)
async def create_book(book_data:CreateBook,session:SessionDep):
    author_db = session.get(Author,book_data.author_id)
    if not author_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    book = Book.model_validate(book_data.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
@router.get("/",response_model=list[Book])
async def show_all_books(session:SessionDep):
    response = session.exec(select(Book)).all()
    return response
@router.patch("/{book_id}",response_model=Book,status_code=status.HTTP_201_CREATED)
async def update_book(book_id:uuid.UUID,book_data:UpdateBook, session:SessionDep):
    author_db = session.get(Author,book_data.author_id)
    book_db = session.get(Book,book_id)
    if not author_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not book_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    book_data_dict = book_data.model_dump(exclude_unset=True)
    book_db.sqlmodel_update(book_data_dict)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    return book_db