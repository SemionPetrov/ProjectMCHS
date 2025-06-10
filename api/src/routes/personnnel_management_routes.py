from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import jwt

from authentication.auth import get_user_by_login
from database.db_connector import get_db
from models.pydantic_models import  UserPrivilegesResponse
from authentication.auth import PermissionChecker

router = APIRouter(
        prefix="/personnel",
        tags=["personnel"]
    )


@router.get("/pending_exercises")
def get_personnel_list(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


# TODO make model for that
@router.post("/change_personnel_data")
def change_personal_data(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}

