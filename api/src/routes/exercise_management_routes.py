from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import jwt

from authentication.auth import get_user_by_login
from database.db_connector import get_db
from models.pydantic_models import  UserPrivilegesResponse
from authentication.auth import PermissionChecker

router = APIRouter(
        prefix="/exercise",
        tags=["exercise management"]
    )


@router.get("/list_exercise_reports", tags=["exercise report"])
def get_exercise_reports(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


# TODO make model for that
@router.post("/add_exercise_report", tags=["exercise report"])
def add_exercise_report(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.delete("/delete_exercise_report", tags=["exercise report"])
def delete_exercise_report(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.put("/change_exercise_report", tags=["exercise report"])
def change_exercise_report(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.get("/list_pending_exercises", tags=["exercise"])
def get_exercises(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


# TODO make model for that
@router.post("/add_exercise", tags=["exercise"])
def add_exercise(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.delete("/delete_exercise", tags=["exercise"])
def delete_exercise(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.put("/change_exercise", tags=["exercise"])
def change_exercise(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}
