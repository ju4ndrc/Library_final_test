from fastapi import APIRouter, status, HTTPException, Query, Depends
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