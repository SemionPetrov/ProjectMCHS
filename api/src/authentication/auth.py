from datetime import datetime, timezone, timedelta
from typing import List
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import bcrypt
from database.db_models import User, Privilege
from database.db_connector import get_db
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user_by_login(db: Session, login: str):
    return db.query(User).filter(User.login == login).first()

def get_user_privileges(db: Session, user_id: int):
    return db.query(Privilege).join(
        User, Privilege.users
    ).filter(User.id == user_id).all()

def authenticate_user(login: str, password: str, db: Session = Depends(get_db)) -> User:
    login_candidate = get_user_by_login(db, login)
    
    if not login_candidate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    if not bcrypt.checkpw(password.encode(), login_candidate.password_hash.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    return login_candidate

def get_payload_secret_key():
    return "secret_key"

def create_access_token(user: User, db: Session = Depends(get_db)) -> str:
    privileges = [privilege.name for privilege in get_user_privileges(db, user.id)]
    
    payload = {
        "sub": user.login,
        "permissions": privileges,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, get_payload_secret_key(), algorithm="HS256")
    return token

class PermissionChecker:
    def __init__(self, required_permissions: List[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, token: str = Depends(oauth2_scheme)) -> None:
        try:
            payload = jwt.decode(token, get_payload_secret_key(), algorithms=["HS256"])
            user_permissions = payload.get("permissions", [])
            
            # Fix: Check permissions as whole strings, not individual characters
            missing_permissions = [
                perm for perm in self.required_permissions 
                if perm not in user_permissions
            ]
            
            if missing_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permissions: {', '.join(missing_permissions)}"
                )
                
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

class LoginRequest(BaseModel):
    username: str
    password: str
