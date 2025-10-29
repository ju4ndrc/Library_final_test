import uuid
from fastapi import APIRouter,HTTPException,status
from sqlmodel import select
from db import SessionDep
from models import Lend, CreateLend, UpdateLend, Book, User


router = APIRouter(prefix="/lends",tags=["Lends"])

@router.post("/",response_model=Lend,status_code=status.HTTP_201_CREATED)
async def new_lend(lend_data:CreateLend,session:SessionDep):
    user = session.get(User,lend_data.user_id)
    book = session.get(Book, lend_data.book_id)

    if not user:
        raise HTTPException(status_code=404, detail="we cant find this user")
    if not book:
        raise HTTPException(status_code=404, detail="we cant find this user")
    if book.copies <= 0:
        raise HTTPException(status_code=400, detail="There are no copies of the book")
    lend = Lend(
        user_id = user.id,
        book_id = book.id,
        return_date = lend_data.return_date,
    )
    book.copies = book.copies - 1
    session.add(lend)
    session.commit()
    session.refresh(lend)
    return lend

@router.get("/{lend_id}",response_model=Lend)
async def show_id_lend(lend_id:uuid.UUID, session:SessionDep):
    lend = session.get(Lend, lend_id)
    if not lend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return lend

@router.get("/",response_model=list[Lend])
async def show_all_lends(session:SessionDep):
    lend = session.exec(select(Lend)).all()
    return lend
@router.patch("/{lend_id}",response_model=Lend)
async def update_lend(lend_id:uuid.UUID,lend_data: UpdateLend,session:SessionDep):
    lend = session.get(Lend,lend_id)
    if not lend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


    book = session.get(Book, lend.book_id)

    if lend_data.return_date:
        lend.return_date = lend_data.return_date
        book.copies = book.copies + 1

        days = (lend.return_date - lend.lend_date).days
        if days > 3:
            lend.fine = (days - 3) * 1.5
        else:
            lend.fine = 0

    session.add(lend)
    session.commit()
    session.refresh(lend)
    return lend
@router.delete("/{lend_id}",status_code=status.HTTP_200_OK)
async def eliminate_lend(lend_id:uuid.UUID,session:SessionDep):
    lend = session.get(Lend,lend_id)
    if not lend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(lend)
    session.commit()
    return {"message":"This lend was deleted"}