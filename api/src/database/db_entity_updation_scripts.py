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
    birthday: Optional[Date] = None,
    position_id: Optional[int] = None,
    rang_id: Optional[int] = None,
    comment: Optional[str] = None
):
    # First check if employee exists
    employee = db_session.query(Employee).filter(Employee.id == employee_id).first()
    
    if not employee:
        return {
            "success": False,
            "message": f"Employee with id {employee_id} does not exist!"
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
                "message": f"Position with id {position_id} does not exist!"
            }
        employee.position_id = position_id
    if rang_id is not None:
        # Check if rang exists
        rang = db_session.query(Rang).filter(Rang.id == rang_id).first()
        if not rang:
            return {
                "success": False,
                "message": f"Rang with id {rang_id} does not exist!"
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
    name: Optional[str] = None,
    group_position: Optional[str] = None
):
    position = db_session.query(Position).filter(Position.id == position_id).first()
    
    if not position:
        return {
            "success": False,
            "message": f"Position with id {position_id} does not exist"
        }

    valid_groups = ['среднего и старшего начальствующего состава',
                    'рядового и младшего начальствующего состава',
                    'работников']

    if name is not None:
        position.name = name

    if group_position is not None:
        if group_position not in valid_groups:
            return {
                "success": False,
                "message": f"Invalid group position. Must be one of: {', '.join(valid_groups)}"
            }
        position.group_position = group_position
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated position {position.name}",
    }

def update_attestation_type(
    db_session: Session,
    attestation_type_id: int,
    new_name: Optional[str] = None,
):
    attestation_type = db_session.query(AttestationType).filter(
        AttestationType.id == attestation_type_id
    ).first()
    
    if not attestation_type:
        return {
            "success": False,
            "message": f"AttestationType with id {attestation_type_id} does not exist"
        }
    
    if new_name is not None:
        attestation_type.name = new_name
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated attestation type {attestation_type.name}",
    }


def update_attestation(
    db_session: Session,
    attestation_id: int,
    emplyee_id: int,
    new_status: Optional[int] = None,
    new_date: Optional[Date] = None,
    new_examination_date: Optional[Date] = None
):
    attestation = db_session.query(Attestation).filter(
        Attestation.id == attestation_id,
        Attestation.employee_id == emplyee_id,
    ).first()
    
    if not attestation:
        return {
            "success": False,
            "message": f"Attestation with id {attestation_id} does not exist!"
        }
    
    if new_status is not None:
        attestation.status = new_status
    if new_date is not None:
        attestation.date = new_date
    if new_examination_date is not None:
        attestation.examination_date = new_examination_date
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated attestation {attestation.id}",
    }


def update_rang(
    db_session: Session,
    rang_id: int,
    name: Optional[str] = None,
):
    rang = db_session.query(Rang).filter(Rang.id == rang_id).first()
    
    if not rang:
        return {
            "success": False,
            "message": f"Rang with id {rang_id} does not exist"
        }
    
    if name is not None:
        rang.name = name
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated rang {rang.name}",
    }

def update_exercise_type(
    db_session: Session,
    type_id: int,
    new_name: Optional[str] = None,
):
    exercise_type = db_session.query(ExerciseType).filter(
        ExerciseType.id == type_id
    ).first()
    
    if not exercise_type:
        return {
            "success": False,
            "message": f"ExerciseType with id {type_id} does not exist"
        }
    
    if new_name is not None:
        exercise_type.name = new_name
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated exercise type {exercise_type.name}",
    }


def update_exercise_report(
    db_session,
    exercise_report_id: int,
    new_start_date: Optional[DateTime] = None,
    new_finish_date: Optional[DateTime] = None,
    new_count_plan: Optional[int] = None,
    new_count_actual: Optional[int] = None,
    new_count_reason: Optional[str] = None,
    new_comment: Optional[str] = None
):
    exercise_report = db_session.query(ExerciseReport).filter(
        ExerciseReport.id == exercise_report_id,
    ).first()
    
    if not exercise_report:
        return {
            "success": False,
            "message": f"ExerciseReport does not exist"
        }

    valid_count_reason = [
        'Отсутствие ХП-И', 
        'Отсутствие кислорода', 
        'Отсутствие воздуха', 
        'Пожар', 
        'Запрет выездов', 
        'Прочее'
    ]

    if new_count_reason is not None:
        if new_count_reason not in valid_count_reason:
            return {
                "success": False,
                "message": f"Invalid count reason. Must be one of: {', '.join(valid_count_reason)}"
            }
        exercise_report.count_reason = new_count_reason

    if new_start_date is not None:
        exercise_report.start_date = new_start_date
    if new_finish_date is not None:
        exercise_report.finish_date = new_finish_date
    if new_count_plan is not None:
        exercise_report.count_plan = new_count_plan
    if new_count_actual is not None:
        exercise_report.count_actual = new_count_actual
    if new_comment is not None:
        exercise_report.comment = new_comment
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Updated exercise report with id {exercise_report.id}",
    }


def update_exercise(
    db_session: Session,
    exercise_id: int,
    employee_id: Optional[int] = None,
    exercise_type_id: Optional[int] = None,
    date: Optional[DateTime] = None,
    address: Optional[str] = None,
    comment: Optional[str] = None
):
    exercise = db_session.query(PendingExercise).filter(
        PendingExercise.id == exercise_id
    ).first()
    
    if not exercise:
        return {
            "success": False,
            "message": f"Exercise with id {exercise_id} does not exist"
        }

    if employee_id is not None:
        employee = db_session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return {
                "success": False,
                "message": f"Employee with id {employee_id} does not exist"
            }
        exercise.employee_id = employee_id

    if exercise_type_id is not None:
        exercise_type = db_session.query(ExerciseType).filter(
            ExerciseType.id == exercise_type_id
        ).first()
        if not exercise_type:
            return {
                "success": False,
                "message": f"Exercise type with id {exercise_type_id} does not exist"
            }
        exercise.exercise_type_id = exercise_type_id

    if date is not None:
        exercise.date = date
    if address is not None:
        exercise.address = address
    if comment is not None:
        exercise.comment = comment
    
    db_session.commit()
    return {
        "success": True,
        "message": f"Successfully updated exercise {exercise_id}",
    }
