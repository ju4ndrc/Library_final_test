from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import select
from db import SessionDep
from models import User
from app.auth.hash import verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBasic()


current_sessions = {}


@router.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security), session: SessionDep = None):
    statement = select(User).where(User.email == credentials.username)
    user = session.exec(statement).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    current_sessions[user.email] = user.role
    return {"message": f"Welcome {user.username}", "role": user.role}


# Logout
@router.post("/logout")
async def logout(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in current_sessions:
        del current_sessions[credentials.username]
        return {"message": "Logged out successfully"}
    raise HTTPException(status_code=401, detail="User not logged in")


#Validar usuario
def get_current_user(credentials: HTTPBasicCredentials = Depends(security), session: SessionDep = None):
    statement = select(User).where(User.email == credentials.username)
    user = session.exec(statement).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


# proteccion de endpoints
def admin_required(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user