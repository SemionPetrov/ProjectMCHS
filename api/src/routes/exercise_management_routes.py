from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from database.db_connector import get_db
from database.db_entity_creation_scripts import create_exercise_type
from database.db_entity_deletion_scripts import delete_exercise_type
from database.db_entity_updation_scripts import update_exercise_type
from database.db_models import ExerciseType
from authentication.auth import PermissionChecker

router = APIRouter(
        prefix="/exercise",
        tags=["exercise management"]
    )

@router.post("/type/add", tags=["exercise type"])
def add_exercise_type(
        exercise_type_name: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"])),
        db: Session = Depends(get_db)
        ):
    result = create_exercise_type(db, exercise_type_name)
    return result


@router.get("/type/all", tags=["exercise type"])
def get_all_exercise_types(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read"])),
        db: Session = Depends(get_db)
    ):

    stmt = select(ExerciseType).\
        order_by(ExerciseType.id, ExerciseType.name)
    
    result = db.execute(stmt)
    exercise_types= result.scalars().all()
    
    return exercise_types 

@router.delete("/type/delete/{type_id}", tags=["exercise type"])
def delete_exercise_type_route(
        type_id: int,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"])),
        db: Session = Depends(get_db)
    ):
    result = delete_exercise_type(db,type_id)
    return result    


@router.put("/update/{type_id}", tags=["exercise type"])
def update_exercise_type_route(
        type_id: int,
        new_name: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"])),
        db: Session = Depends(get_db)
    ):
    result = update_exercise_type(db, type_id, new_name)
    return result


@router.post("/reports/add", tags=["exercise report"])
def add_exercise_report(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"]))
    ):
    return {"Not implimented"}


@router.get("/reports/all", tags=["exercise report"])
def get_exercise_reports(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["exercise:read"]))
    ):
    return {"Not implimented"}


@router.delete("/reports/delete", tags=["exercise report"])
def delete_exercise_report(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"]))
    ):
    return {"Not implimented"}


@router.put("/reports/change", tags=["exercise report"])
def change_exercise_report(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"]))
    ):
    return {"Not implimented"}


@router.get("/reports/all", tags=["exercise"])
def get_exercises(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read"]))
    ):
    return {"Not implimented"}


# TODO make model for that
@router.post("/add_exercise", tags=["exercise"])
def add_exercise(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"]))
    ):
    return {"Not implimented"}


@router.delete("/delete_exercise", tags=["exercise"])
def delete_exercise(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"]))
    ):
    return {"Not implimented"}


@router.put("/change_exercise", tags=["exercise"])
def change_exercise(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"]))
    ):
    return {"Not implimented"}
