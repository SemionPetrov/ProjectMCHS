from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from authentication.auth import authenticate_user, create_access_token
from sqlalchemy.orm import Session

from models.pydantic_models import LoginRequest
from database.db_connector import get_db
from database.db_entity_creation_scripts import create_user


router = APIRouter(
        prefix="/auth",
        tags=["authentication"]
        )


@router.post("/login",  responses={
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation Error"}
})
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
    ):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user, db)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup")
def signup(
        request: LoginRequest, 
        db: Session = Depends(get_db)
    ):

    result = create_user(db, request.username, request.password)
    return result

