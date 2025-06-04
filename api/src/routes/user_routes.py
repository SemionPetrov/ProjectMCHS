from fastapi import APIRouter, HTTPException, Depends, status
from database.db_connector import get_db
from authentication.auth import LoginRequest, authenticate_user, create_access_token, PermissionChecker
from config.admin_user import admin_user_credentials
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from authentication.auth import oauth2_scheme, get_payload_secret_key, get_user_by_login
import jwt


class UserPrivilegesResponse(BaseModel):
    privileges: List[str]


router = APIRouter(
        prefix="/user",
        tags=["user"])

@router.get("/privileges", response_model=UserPrivilegesResponse)
def get_user_privileges(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Extract username from token
    try:
        payload = jwt.decode(token, get_payload_secret_key(), algorithms=["HS256"])
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
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

    # Get user and their privileges
    user = get_user_by_login(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get privileges from either token or database
    privileges_from_token = payload.get("permissions", [])
    if privileges_from_token:
        privileges = privileges_from_token
    else:
        privileges = [privilege.name for privilege in get_user_privileges(db, user.id)]

    return UserPrivilegesResponse(privileges=privileges)
