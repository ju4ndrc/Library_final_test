from fastapi import APIRouter,status,HTTPException
from sqlmodel import select
from models import Library , CreateLibrary , UpdateLibrary
from db import SessionDep
import uuid

router = APIRouter(prefix="/library",tags=["Library"])

@router.post("/",response_model = Library ,status_code=status.HTTP_201_CREATED)
async def create_library(library_data:CreateLibrary,session:SessionDep):
    existing_library = session.exec(select(Library)).first()
    if existing_library :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only be one library")
    library = Library.model_validate(library_data.model_dump())
    session.add(library)
    session.commit()
    session.refresh(library)
    return library

@router.get("/show",response_model = list[Library],status_code=status.HTTP_200_OK)
async def show_library(session:SessionDep):
    response = session.exec(select(Library)).all()
    return response

@router.patch("/update_id/{library_id}",response_model=Library,status_code=status.HTTP_201_CREATED)
async def updateLibrary(library_id: uuid.UUID,library_data:UpdateLibrary,session:SessionDep):
    library_db = session.get(Library, library_id)

    if not library_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Library not found")
    library_data_dict = library_data.model_dump(exclude_unset=True)
    

    library_db.sqlmodel_update(library_data_dict)
    session.add(library_db)
    session.commit()
    session.refresh(library_db)
    return library_db