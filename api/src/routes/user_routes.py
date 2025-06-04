from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
import jwt

from authentication.auth import oauth2_scheme, get_payload_secret_key, get_user_by_login
from database.db_connector import get_db
from models.pydantic_models import  UserPrivilegesResponse


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
