from sqlalchemy.orm import Session
from sqlalchemy import delete
from database.db_models import *
from config.admin_user import admin_user_credentials
from typing import Optional
from datetime import datetime

"""
Collection of scripts to create entities in database.
Used for fixtures and by api. 
"""
def update_employee(
    db_session,
    employee_id: int,
    last_name: Optional[str] = None,
    first_name: Optional[str] = None,
    surname: Optional[str] = None,
    birthday: Optional[datetime] = None,
    position_id: Optional[int] = None,
    rang_id: Optional[int] = None,
    comment: Optional[str] = None
):
    # First check if employee exists
    employee = db_session.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        return {
            "success": False,
            "error": f"Employee with id {employee_id} does not exist"
        }
    
    # Update fields that were provided
    if last_name is not None:
        employee.last_name = last_name
    if first_name is not None:
        employee.first_name = first_name
    if surname is not None:
        employee.surname = surname
    if birthday is not None:
        employee.birthday = birthday
    if position_id is not None:
        # Check if position exists
        position = db_session.query(Position).filter(Position.id == position_id).first()
        if not position:
            return {
                "success": False,
                "error": f"Position with id {position_id} does not exist"
            }
        employee.position_id = position_id
    if rang_id is not None:
        # Check if rang exists
        rang = db_session.query(Rang).filter(Rang.id == rang_id).first()
        if not rang:
            return {
                "success": False,
                "error": f"Rang with id {rang_id} does not exist"
            }
        employee.rang_id = rang_id
    if comment is not None:
        employee.comment = comment
    
    # Commit changes
    db_session.commit()
    
    return {
        "success": True,
        "data": employee
    }

def update_position(
    db_session,
    position_id: int,
    name: str,
    group_position: str
):
    position = db_session.query(Position).filter(Position.id == position_id).first()
    
    valid_groups = ['среднего и старшего начальствующего состава',
                    'рядового и младшего начальствующего состава',
                    'работников']
    if not position:
        return {
            "success": False,
            "error": f"Position with id {position_id} does not exist"
        }

    if name is not None:
        position.name = name

    if group_position is not None and group_position not in valid_groups:
        return {
            "success": False,
            "error": f"Invalid name. Must be one of: {', '.join(valid_groups)}"
        }
    else:
        position.group_position = group_position
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated position {position.name}",
        "data": position
    }

def update_rang(
    db_session: Session,
    rang_id: int,
    name: str,
):
    rang = db_session.query(Rang).filter(Rang.id == rang_id).first()
    
    if not rang:
        return {
            "success": False,
            "error": f"Rang with id {rang_id} does not exist"
        }
    
    rang.name = name
    
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated rang {rang.name}",
        "data": rang
    }


def update_attestation_type(
    db_session: Session,
    attestation_type_id: int,
    new_name: str,
):
    attestation_type= db_session.query(AttestationType).filter(AttestationType.id == attestation_type_id).first()
    
    if not attestation_type:
        return {
            "success": False,
            "error": f"AttestationType with id {attestation_type_id} does not exist"
        }
    
    attestation_type.name = new_name
    
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated attestation {attestation_type.name} with id {attestation_type_id}",
    }
