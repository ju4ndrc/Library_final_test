import uuid

from dotenv.cli import unset
from fastapi import APIRouter, status, HTTPException, Query, Depends
from sqlalchemy.orm import deferred

from app.auth.auth_router import admin_required
from app.auth.hash import hash_password
from sqlmodel import select
from db import SessionDep
from models import User, CreateUser, UpdateUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
async def createUser(user_data: CreateUser, session:SessionDep):
    hash_pw = hash_password(user_data.password)
    user = User.model_validate({
        **user_data.model_dump(),
        "password": hash_pw
    })
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/",response_model=list[User])
async def show_all_users(session:SessionDep):
    response = session.exec(select(User)).all()
    return response

@router.get("/active",response_model=list[User])
async def show_active_users(session:SessionDep):
    users = session.exec(select(User).where(User.is_active == True)).all()
    return users


@router.get("/inactive",response_model=list[User])
async def show_inactive_users(session:SessionDep):
    users = session.exec(select(User).where(User.is_active == False)).all()
    return users

@router.patch("/update_id/{user_id}",response_model=User,status_code=status.HTTP_201_CREATED)
async def update_user(user_id: uuid.UUID , user_data:UpdateUser,session:SessionDep, user : User = Depends(admin_required)):
    user_db = session.get(User, user_id)

    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_data_dict = user_data.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data_dict)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.delete("/delete_user/{user_id}", response_model=User,status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: uuid.UUID ,session:SessionDep, user : User = Depends(admin_required)):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not user_db.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is innactive")
    user_db.is_active = False
    session.add(user_db)
    session.commit()
    return {"message":"User desactivated","user_id":user_id}
@router.patch("/active_user/{user_id}", response_model=User,status_code=status.HTTP_202_ACCEPTED)
async def active_user(user_id: uuid.UUID ,session:SessionDep, user : User = Depends(admin_required)):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if user_db.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is active")
    user_db.is_active = True
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return {"message":"User activated","user_id":user_id}
