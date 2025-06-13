from fastapi import APIRouter, Depends
from sqlalchemy.engine import result
from sqlalchemy.orm import Session
from sqlalchemy import select, DateTime
from typing import cast, Optional

from sqlalchemy.orm.attributes import OP_APPEND

from database.db_connector import get_db
from database.db_entity_creation_scripts import create_exercise_report, create_exercise_type, create_exercise
from database.db_entity_deletion_scripts import delete_exercise_report, delete_exercise_type, delete_exercise
from database.db_entity_updation_scripts import update_exercise_type, update_exercise_report, update_exercise
from database.db_models import ExerciseType, ExerciseReport, PendingExercise
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


@router.post("/reports/add/{exercise_id}", tags=["exercise report"])
def add_exercise_report_route(
        exercise_id: int,
        start_date: str,
        finish_date: str,
        count_plan: int,
        count_actual: int,
        count_reason: str,
        comment: Optional[str] = None,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"])),
        db: Session = Depends(get_db)
    ):
    result = create_exercise_report(
                db,
                exercise_id,
                cast(DateTime,start_date),
                cast(DateTime,finish_date),
                count_plan,
                count_actual,
                count_reason,
                comment
            )
    return  result


@router.get("/reports/all", tags=["exercise report"])
def get_exercise_reports(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read"])),
        db: Session = Depends(get_db)
    ):

    stmt = select(ExerciseReport).\
        order_by(
                ExerciseReport.start_date,
                ExerciseReport.finish_date,
                ExerciseReport.count_plan,
                ExerciseReport.count_actual
        )
    
    result = db.execute(stmt)
    exercise_reports= result.scalars().all()
    
    return exercise_reports


@router.delete("/reports/delete/{report_id}", tags=["exercise report"])
def delete_exercise_report_route(
      report_id: int,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"])),
        db: Session = Depends(get_db)
    ):

    result = delete_exercise_report(db,report_id)
    return result    


@router.put("/reports/change{report_id}", tags=["exercise report"])
def update_exercise_report_route(
        report_id: int,
        new_start_date: Optional[str] = None,
        new_finish_date: Optional[str] = None,
        new_count_plan: Optional[int] = None,
        new_count_actual: Optional[int] = None,
        new_count_reason: Optional[str] = None,
        new_comment: Optional[str] = None,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read", "exercise:write"])),
        db: Session = Depends(get_db)
    ):

    result = update_exercise_report(
            db,
            report_id,
            cast(DateTime, new_start_date),
            cast(DateTime,new_finish_date),
            new_count_plan,
            new_count_actual,
            new_count_reason,
            new_comment)
    return result    


@router.post("/add_exercise", tags=["exercise"])
def add_exercise(
    employee_id: int,
    exercise_type_id: int,
    date: str,
    address: str,
    comment: Optional[str] = None,
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["exercise:read", "exercise:write"])),
    db: Session = Depends(get_db)
):
    result = create_exercise(
        db,
        employee_id,
        exercise_type_id,
        cast(DateTime, date),
        address,
        comment
    )
    return result


@router.put("/change_exercise", tags=["exercise"])
def update_exercise_route(
    exercise_id: int,
    employee_id: int,
    exercise_type_id: Optional[int] = None,
    date: Optional[str] = None,
    address: Optional[str] = None,
    comment: Optional[str] = None,
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["exercise:read", "exercise:write"])),
    db: Session = Depends(get_db)
):
    result = update_exercise(
        db,
        exercise_id,
        employee_id,
        exercise_type_id,
        cast(DateTime, date) if date is not None else None,
        address,
        comment
    )
    return result


@router.delete("/delete_exercise", tags=["exercise"])
def delete_exercise_route(
    exercise_id: int,
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["exercise:read", "exercise:write"])),
    db: Session = Depends(get_db)
):
    result = delete_exercise(db, exercise_id)
    return result


@router.get("/all", tags=["exercise"])
def get_exercises(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["exercise:read"])),
        db: Session = Depends(get_db)
    ):

    stmt = select(PendingExercise).\
        order_by(
                PendingExercise.id,
                PendingExercise.employee_id,
        )
    
    result = db.execute(stmt)
    exercise_reports= result.scalars().all()
    
    return exercise_reports


