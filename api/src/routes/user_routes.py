from fastapi import APIRouter, Depends
from sqlalchemy import select, Date
from sqlalchemy.orm import Session
from models.pydantic_models import  UserPrivilegesResponse
from typing import Optional, cast

from authentication.auth import get_user_from_token, oauth2_scheme, PermissionChecker
from database.db_connector import get_db
from database.db_entity_selection_scripts import get_user_privs_with_ids
from database.db_entity_updation_scripts import update_employee 
from database.db_models import PendingExercise, Attestation

router = APIRouter(
        prefix="/user",
        tags=["account"]
    )


@router.get("/attestations")
def get_user_attestations(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
    ):
    user = get_user_from_token(token, db)

    if user.employee_id is None:
        return {
                "success": False,
                "message": "User has no employee_id!"
                }

    stmt = select(Attestation.employee_id).\
        where(Attestation.employee_id== user.employee_id).\
        order_by(
                Attestation.id,
                Attestation.employee_id,
        )
    
    result = db.execute(stmt)
    attestations= result.scalars().all()
    
    return attestations 


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
        List: exercises
    """
    user = get_user_from_token(token, db)
    print(user.id)
    if user.employee_id is None:
        return {
                "success": False,
                "message": "User has no employee_id!"
                }

    stmt = select(PendingExercise.employee_id).\
        where(PendingExercise.employee_id== user.employee_id).\
        order_by(
                PendingExercise.id,
                PendingExercise.employee_id,
        )
    
    result = db.execute(stmt)
    exercises= result.scalars().all()
    
    return exercises


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
