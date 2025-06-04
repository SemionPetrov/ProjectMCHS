from fastapi import APIRouter
from database.db_connector import get_db
from authentication.auth import authenticate_user, create_access_token
from fastapi import Depends
from sqlalchemy.orm import Session
from models.pydantic_models import LoginRequest

router = APIRouter(
        prefix="/auth",
        tags=["authentication"])


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(request.username, request.password, db)
    token = create_access_token(user, db)
    return {"access_token": token, "token_type": "bearer"}


