from sqlalchemy.orm import Session
from database.db_models import *
from typing import Optional
from datetime import datetime

"""
Collection of scripts to uupdate entities in database.
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
        "message": f"Updated employee {employee_id}" 
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

def update_attestation(
    db_session: Session,
    attestation_id: int,
    emplyee_id: int,
    new_type_id:int,
    new_status: int,
    new_date: Date,
    new_examination_date: Date
):
    attestation= db_session.query(Attestation).filter(
            Attestation.id == attestation_id,
            Attestation.employee_id == emplyee_id,
        ).first()
    
    if not attestation:
        return {
            "success": False,
            "error": f"AttestationType with id {attestation_type_id} does not exist"
        }
    
    attestation.type_id=new_type_id
    attestation.status = new_status
    attestation.date= new_date 
    attestation.examination_date=new_examination_date 
    
    db_session.flush() 
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated attestation {attestation.id} for employee {emplyee_id} with",
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
    }

def update_exercise_type(
    db_session: Session,
    type_id: int,
    new_name: str,
):

    exercise_type= db_session.query(ExerciseType).filter(ExerciseType.id == type_id).first()
    
    if not  exercise_type:
        return {
            "success": False,
            "error": f"ExerciseType with id {type_id} does not exist!"
        }
    
    exercise_type.name = new_name
    
    db_session.flush() 
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated exercise_type {exercise_type.id} to name {exercise_type.name}",
    }

def update_exercise_report(
    db_session,
    exercise_report_id: int,
    new_start_date: DateTime,
    new_finish_date: DateTime,
    new_count_plan: int,
    new_count_actual: int,
    new_count_reason: str,
    new_comment: str
):

    exercise_report = db_session.query(ExerciseReport).filter(
        ExerciseReport.id == exercise_report_id,
    ).first()
    
    if not exercise_report:
        return {
            "success": False,
            "error": f"ExerciseReport does not exists!"
        }

    valid_count_reason =  [
            'Отсутствие ХП-И', 
            'Отсутствие кислорода', 
            'Отсутствие воздуха', 
            'Пожар', 
            'Запрет выездов', 
            'Прочее']

    if new_count_reason not in valid_count_reason:
        return {
            "success": False,
            "error": f" {'Count reason should be one of: '.join(valid_count_reason)}!"
        }

    exercise_report.start_date = new_start_date,
    exercise_report.finish_date = new_finish_date,
    exercise_report.count_plan = new_count_plan,
    exercise_report.count_actual = new_count_actual,
    exercise_report.count_reason = new_count_reason,
    exercise_report.comment = new_comment
    
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Updated exercise report with id {exercise_report.id}!"
    }

def update_exercise(
    db_session: Session,
    employee_id: int,
    exercise_id: int,
    exercise_type_id: int,
    date: DateTime,
    address: str,
    comment: str,
):
    exercise = db_session.query(PendingExercise).filter(PendingExercise.id == exercise_id).first()
    
    if not exercise:
        return {
            "success": False,
            "error": f"Exercise with id {exercise_id} does not exist"
        }
    
    # Update fields that were provided
    if employee_id is not None:
        # Check if employee exists
        employee = db_session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return {
                "success": False,
                "error": f"Employee with id {employee_id} does not exist"
            }
        exercise.employee_id = employee_id
    
    if exercise_type_id is not None:
        exercise_type = db_session.query(ExerciseType).filter(ExerciseType.id == exercise_type_id).first()
        if not exercise_type:
            return {
                "success": False,
                "message": f"Exercise type with id {exercise_type_id} does not exist"
            }

    exercise.exercise_type_id = exercise_type_id

    exercise.date = date
    
    exercise.address = address
    
    exercise.comment = comment
    
    # Commit changes
    db_session.commit()
    
    return {
        "success": True,
        "message": f"Successfully updated exercise {exercise_id}",
    }
