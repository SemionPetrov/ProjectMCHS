from fastapi import APIRouter, Depends
from sqlalchemy import Date, select
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import Optional, Dict, cast
from datetime import datetime, date

from starlette.requests import empty_receive

from database.db_connector import get_db
from authentication.auth import PermissionChecker
from database.db_entity_creation_scripts import create_employee, create_position, create_rang
from database.db_entity_deletion_scripts import delete_employee, delete_position, delete_rang
from database.db_entity_updation_scripts import update_employee, update_position, update_rang
from database.db_models import Employee, Position, Rang

router = APIRouter(
        prefix="/personnel",
    )


class EmployeeCreate(BaseModel):
    last_name: str
    first_name: str
    surname: Optional[str]
    birthday: Optional[Date]
    position_id: int
    rang_id: int
    comment: Optional[str]

    class Config:
        arbitrary_types_allowed = True

class EmployeeList(BaseModel):
    id: int
    last_name: str
    first_name: str
    surname: Optional[str]
    birthday: Optional[datetime]
    position_id: int
    rang_id: int
    comment: Optional[str]
    position: Dict[str, str]
    rang: Dict[str, str]

    class Config:
        from_attributes=True

class EmployeeUpdate(BaseModel):
    last_name: Optional[str]
    first_name: Optional[str]
    surname: Optional[str]
    birthday: Optional[date]
    position_id: Optional[int]
    rang_id: Optional[int]
    comment: Optional[str]


@router.post("/add_new_employee", tags=["employee"])
def add_employee(
        last_name: str,
        first_name: str,
        surname: str | None,
        birthday: date,
        position_id: int,
        rang_id: int,
        comment: str | None,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
        db: Session = Depends(get_db)
    ):
    """
    Добавить сотрудника

    Returns: 
        Dict: result
    """
    result = create_employee(
        db_session=db,
        last_name=last_name,
        first_name=first_name,
        surname=surname,
        birthday=cast(Date, birthday),
        position_id=position_id,
        rang_id=rang_id,
        comment=comment
    )
    return result    


@router.get("/get_employee_list", tags=["employee"])
def get_personnel_list(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:read"])),
        db: Session = Depends(get_db)
    ):
     
    """
    Получить списко всех сотрудников

    Returns: 
        Dict: result
    """
    query = select(Employee, Position, Rang).select_from(Employee).outerjoin(
        Position, Position.id == Employee.position_id
    ).outerjoin(
        Rang, Rang.id == Employee.rang_id
    ).order_by(
        Employee.last_name,
        Employee.first_name,
        Employee.id
    )
    
    result = db.execute(query)
    employees_data = result.all()
    
    return {
        "success": True,
        "data": [
            {
                "id": emp.id,
                "last_name": emp.last_name,
                "first_name": emp.first_name,
                "surname": emp.surname,
                "birthday": emp.birthday,
                "comment": emp.comment,
                "position": {
                    "name": pos.name,
                    "group_position": pos.group_position
                } if pos else None,
                "rang": {
                    "name": rang.name
                } if rang else None
            }
            for emp, pos, rang in employees_data
        ]
    }


@router.delete("/{employee_id}", tags=["employee"])
def delete_employee_route(
    employee_id: int,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
    ):

    """
   Удалить сотрудника

    Returns: 
        Dict: result
    """
    result = delete_employee(db, employee_id)
    
    return result



@router.put("/employees/{employee_id}", tags=["employee"])
def update_employee_route(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
):

    """
   Обновить данные сотрудника

    Returns: 
        Dict: result
    """
    result = update_employee(
        db_session=db,
        employee_id=employee_id,
        **employee_data.model_dump(exclude_none=True)
    )
    
    return result

@router.post("/positions/new", tags=["positions"])
def add_position(
        name: str,
        group_position: str,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
        db: Session = Depends(get_db)
    ):
    
    """
    Добавить позицию 

    Returns: 
        Dict: result
    """
    result = create_position(
        db_session=db,
        name=name,
        group_position = group_position
    )
    return result    


@router.put("/positions/{position_id}", tags=["positions"])
def update_position_route(
    position_id: int,
    new_name: Optional[str] = None,
    group_position: Optional[str] = None,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
):

    """
    Обновить позицию 

    Returns: 
        Dict: result
    """
    result = update_position(db_session=db, position_id=position_id, name = new_name, group_position=group_position)

    return result    


@router.delete("/positions/{position_id}", tags=["positions"])
def delete_position_route(
    position_id: int,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
):

    """
    Удалить позицию 

    Returns: 
        Dict: result
    """
    result = delete_position(db_session=db, position_id=position_id)
    return result    


@router.get("/all", tags=["positions"])
def get_positions_list(
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:read"])),
    ):

    """
    Поулчить все доступные позиции

    Returns: 
        Dict: result
    """
    stmt = select(Position).\
        order_by(Position.id, Position.name, Position.group_position)
    
    result = db.execute(stmt)
    positions = result.scalars().all()
    
    return positions 


@router.post("/rangs/new", tags=["rangs"])
def create_rang_route(
        name: str,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
        db: Session = Depends(get_db)
    ):

    """
    Создать ранг 

    Returns: 
        Dict: result
    """

    result = create_rang(
        db_session=db,
        name=name,
    )
    return result    


@router.get("/rangs", tags=["rangs"])
def get_rangs_list(
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:read"])),
        ):

    """
    Получить список все рангов 

    Returns: 
        Dict: result
    """
    stmt = select(Rang).\
        order_by(Rang.id, Rang.name)
    
    result = db.execute(stmt)
    positions = result.scalars().all()
    
    return positions 


@router.put("/rangs/{rang_id}", tags=["rangs"])
def update_rang_route(
    rang_id: int,
    new_name: str,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
):

    """
    Обновить ранг

    Returns: 
        Dict: result
    """
    result = update_rang(db_session=db, rang_id=rang_id, name = new_name)
    
    return result

@router.delete("/rangs/{rang_id}", tags=["rangs"])
def delete_rang_route(
    rang_id: int,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["personnel:write", "personnel:read"])),
):

    """
    Удалить ранг

    Returns: 
        Dict: result
    """
    result = delete_rang(db_session=db, rang_id=rang_id)
    
    return result
