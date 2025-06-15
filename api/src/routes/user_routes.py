from re import A
from fastapi import APIRouter, Depends
from sqlalchemy import select, Date
from sqlalchemy.orm import Session
from models.pydantic_models import  UserPrivilegesResponse
from typing import Optional, cast

from authentication.auth import get_user_from_token, oauth2_scheme, PermissionChecker
from database.db_connector import get_db
from database.db_entity_selection_scripts import get_user_privs_with_ids
from database.db_entity_updation_scripts import update_employee 
from database.db_models import PendingExercise, ExerciseType, Attestation, AttestationType , User, Employee, Position, Rang

router = APIRouter(
        prefix="/user",
        tags=["account"]
    )


@router.get("/me")
async def get_personal_info(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
        ):
    """
    Получить личную информацию текущего пользователя
    
    Returns:
        Dict: Информация о пользователе и связанном с ним сотруднике
    """
    user = get_user_from_token(token, db)
    
    if not user:
        return
    
    query = select(User, Employee, Position, Rang).select_from(User).outerjoin(
        Employee, User.employee_id == Employee.id
    ).outerjoin(
        Position, Employee.position_id == Position.id
    ).outerjoin(
        Rang, Employee.rang_id == Rang.id
    ).where(User.id == user.id)
    
    result = db.execute(query)
    user_data = result.first()
    
    if user_data is None:
        return 

    user, employee, position, rang = user_data
    
    response = {
        "user": {
            "id": user.id,
            "login": user.login,
            "contact_info": user.contact_info,
            "password_expiration": user.password_expiration,
            "created": user.created,
            "updated_at": user.updated_at
        }
    }
    
    if employee:
        response["employee"] = {
            "id": employee.id,
            "last_name": employee.last_name,
            "first_name": employee.first_name,
            "surname": employee.surname,
            "birthday": employee.birthday,
            "comment": employee.comment,
            "position": {
                "name": position.name,
                "group_position": position.group_position
            } if position else None,
            "rang": {
                "name": rang.name
            } if rang else None
        }
    
    return response


@router.get("/attestations")
def get_user_attestations(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
    ):
    """
    Получить список аттестаций которые есть у сотрудника с id
    привязанному к пользователю.

    Returns:
        Dict: Result
    """
    user = get_user_from_token(token, db)

    if user.employee_id is None:
        return {
            "success": False,
            "message": "User has no employee_id!"
        }

    stmt = select(Attestation).\
        join(AttestationType).\
        where(Attestation.employee_id == user.employee_id).\
        order_by(
            Attestation.id,
            Attestation.employee_id,
            Attestation.date,
            Attestation.examination_date,
            Attestation.status,
            Attestation.no_attestation_reason
        )
    
    result = db.execute(stmt)
    attestations = result.scalars().all()
    
    return {
        "success": True,
        "data": [
            {
                "id": att.id,
                "employee_id": att.employee_id,
                "type_name": att.type.name,  # Using type name instead of id
                "status": att.status,
                "no_attestation_reason": att.no_attestation_reason,
                "date": att.date,
                "examination_date": att.examination_date
            }
            for att in attestations
        ]
    }


@router.put("/change_personal_data")
def change_personal_data(
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        surname: Optional[str] = None,
        birthday: Optional[str] = None,
        position_id: Optional[int] = None,
        rang_id: Optional[int] = None,
        comment: Optional[str] = None,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None])),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ):
    """
    Изменить данные сотрудника.
    Пользователь должен иметь employee_id чтобы поменять свои данные

    Returns:
        Dict: Result
    """
    user = get_user_from_token(token, db)
    if user.employee_id is None:
        return {
                "success": False,
                "message": "User has no employee_id!"
                }

    result = update_employee(
            db,
            user.employee_id,
            last_name,
            first_name,
            surname,
            cast(Date,birthday),
            position_id,
            rang_id,
            comment
            ) 

    return result


@router.get("/exercises")
def get_exercises(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
    ):
    """
    Получить список занятий сотрудника к которому привязан пользователь

    Returns:
        Dict: exercises data
    """
    user = get_user_from_token(token, db)
    print(user.id)
    if user.employee_id is None:
        return {
                "success": False,
                "message": "User has no employee_id!"
                }

    stmt = select(PendingExercise).\
        join(ExerciseType).\
        where(PendingExercise.employee_id == user.employee_id).\
        order_by(
                PendingExercise.id,
                PendingExercise.employee_id,
                PendingExercise.date
        )
    
    result = db.execute(stmt)
    exercises = result.scalars().all()
    
    return {
        "success": True,
        "data": [
            {
                "id": ex.id,
                "employee_id": ex.employee_id,
                "type_name": ex.type.name,  # Используем название вместо ID
                "date": ex.date,
                "address": ex.address,
                "comment": ex.comment
            }
            for ex in exercises
        ]
    }

@router.get("/privileges", response_model=UserPrivilegesResponse)
def get_user_privileges(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
        ):

    """
    Получить список привилегий пользователя

    Returns:
        List: privileges
    """
    user = get_user_from_token(token, db)
    
    privileges = [i["privilege_name"] for i in get_user_privs_with_ids(user, db)]

    return UserPrivilegesResponse(privileges=privileges) 
