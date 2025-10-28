import uuid

from fastapi import APIRouter,HTTPException,status
from sqlmodel import select
from db import SessionDep
from models import Author,CreateAuthor,UpdateAuthor

router = APIRouter(prefix="/authors",tags=["Authors"])

@router.post("/",response_model=Author,status_code=status.HTTP_201_CREATED)
async def createAuthor(author_data: CreateAuthor, session:SessionDep):
    author = Author.model_validate(author_data.model_dump())
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

@router.get("/",response_model=list[Author])
async def show_all_authors(session:SessionDep):
    response = session.exec(select(Author)).all()
    return response

@router.patch("/{author_id}",response_model=Author,status_code=status.HTTP_201_CREATED)
async def createAuthor(author_id:uuid.UUID,author_data: UpdateAuthor, session:SessionDep):
    author_db = session.get(Author, author_id)
    if not author_data:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    author_data_dict = author_data.model_dump(exclude_unset=True)
    author_db.sqlmodel_update(author_data_dict)
    session.add(author_db)
    session.commit()
    session.refresh(author_db)
    return author_db

@router.delete("/{author_id}",status_code=status.HTTP_204_NO_CONTENT)
async def cascade_delete(author_id:uuid.UUID, session:SessionDep):
    author = session.get(Author,author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(author)
    session.commit()
    return {"message":"cascade delete successfully"}