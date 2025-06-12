from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import Null
from sqlalchemy.orm import Session
import jwt
from models.pydantic_models import  UserPrivilegesResponse

from authentication.auth import PermissionChecker, get_user_by_login 
from authentication.auth import get_user_from_token, oauth2_scheme, get_payload_secret_key, get_user_by_login
from database.db_connector import get_db
from database.db_entity_selection_scripts import get_user_privs_with_ids

router = APIRouter(
        prefix="/user",
        tags=["account"]
    )


@router.get("/attestations")
def get_user_attestations(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.put("/change_personal_data")
def change_personal_data(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None])),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ):
    
    user = get_user_from_token(token, db)
    
    #if user.employee_id:
        #return {
                #"message" : "Need to be employee_id to have personal data!"
                #}

    return {"Not implimented"}


@router.get("/pending_exercises")
def pending_exercises(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.get("/privileges", response_model=UserPrivilegesResponse)
def get_user_privileges(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
        ):
    user = get_user_from_token(token, db)
    
    privileges = [i["privilege_name"] for i in get_user_privs_with_ids(user, db)]

    return UserPrivilegesResponse(privileges=privileges) 
