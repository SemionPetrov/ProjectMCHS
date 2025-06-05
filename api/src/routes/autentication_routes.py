import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from authentication.auth import authenticate_user, create_access_token
from sqlalchemy.orm import Session
from datetime import datetime, timezone


from models.pydantic_models import LoginRequest
from database.db_connector import get_db
from database.db_models import User

router = APIRouter(
        prefix="/auth",
        tags=["authentication"])


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(request.username, request.password, db)
    token = create_access_token(user, db)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup")
def signup(request: LoginRequest, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(
    ).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Username!"
        )
    password_hash = bcrypt.hashpw(
        request.password.encode(),
        bcrypt.gensalt()
    )
    new_user = User(
        login = request.username,
        password_hash = password_hash,
        created = datetime.now(timezone.utc),
        updated = datetime.now(timezone.utc),
    )

    db.add(new_user)
    db.flush()
    return "{result: success}"

