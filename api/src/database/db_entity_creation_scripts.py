from operator import pos
from os import execle
from starlette.requests import empty_receive
from database.db_models import *
import bcrypt
from datetime import datetime
from config.db_timezone import prefered_timezone
from typing import List, Optional
from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Session

"""
Collection of scripts to create entities in database.
Used for fixtures and by api. 
"""

def create_privilege(
    db_session: Session, 
    privilege_name: str
    ):

    privilege = db_session.query(Privilege).filter(
        Privilege.name == privilege_name
    ).first()
    
    if privilege:
        return {
            "success": False,
            "message": f"Privilege {privilege_name} already exists",
            "privilege_id": privilege.id
        }
    
    privilege = Privilege(name=privilege_name)
    db_session.add(privilege)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Created privilege {privilege_name}!",
        "id": privilege.id
    }


def grant_privilege_by_ids(
    db_session: Session, 
    user_id: int, 
    privilege_id: int 
    ):
    user = db_session.query(User).filter(User.id == user_id).first()
    
    if not user:
        return {
            "success": False,
            "message": f"User with login {user.login} and id {user.id} does not exist",
        }
    
    privilege = db_session.query(Privilege).filter(Privilege.id == privilege_id).first()
    
    if not privilege:
        return {
            "success": False,
            "message": f"{privilege.name} privilege not found!"
        }
    
    if privilege in user.privileges:
        return {
            "success": False,
            "message": f"Privilege {privilege.name} already exists for user {user.login}",
            "priv_id": privilege.id
        }
    
    user.privileges.append(privilege)
    db_session.commit()
    return {
        "success": True,
        "message": f"Granted user {user.login} id {user_id} privilege {privilege.name} with id {privilege.id}" ,
        "user_id": user.id,
        "privilege_id": privilege_id
    }

def grant_privilege_by_names(
    db_session: Session, 
    user_login: str, 
    privilege_name: str
    ):
    user = db_session.query(User).filter(User.login == user_login).first()
    
    if not user:
        return {
            "success": False,
            "message": f"User with login {user_login} does not exist"
        }
    
    privilege = db_session.query(Privilege).filter(Privilege.name == privilege_name).first()
    
    if not privilege:
        return {
            "success": False,
            "message": f"{privilege_name} privilege not found!"
        }
    
    if privilege in user.privileges:
        return {
            "success": False,
            "message": f"Privilege {privilege_name} already exists for user {user_login}",
            "priv_id":privilege.id
        }
    
    user.privileges.append(privilege)
    db_session.commit()
    return {
        "success": True,
        "message": f"Granted user {user.login} privilege {privilege.name}!",
        "user_id": user.id,
        "priv_id": privilege.id
    }

def create_user(
    db_session: Session, 
    user_login: str, 
    password: str, 
    employee_id: Optional[int] = None, 
    contact_info: Optional[str] = None
):
    # Validate required parameters
    if not user_login or not password:
        return {
            "success": False,
            "message": "User login and password are required!"
        }
    
    # Check if user exists
    user = db_session.query(User).filter(
        User.login == user_login
    ).first()
    
    if user:
        # exposing id seems like a bad idea
        return {
            "success": False,
            "message": "User already exists!"
        }
    
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()
    
    # Create user with proper typing
    user = User(
        login=user_login,
        password_hash=password_hash,
        employee_id=employee_id,
        contact_info=contact_info,
        created=datetime.now(prefered_timezone),
        updated_at=datetime.now(prefered_timezone)
    )

    db_session.add(user)
    db_session.flush()
    db_session.commit()
    
    return {
        "success": True,
        "message": f"Created user {user.login}!",
        "user_id": user.id
    }


def create_employee(
    db_session: Session,
    last_name: str,
    first_name: str,
    surname: Optional[str],
    birthday: Optional[Date],
    position_id: int,
    rang_id: int,
    comment: Optional[str]
):
    position = db_session.query(Position).filter(
        Position.id == position_id
    ).first()
    
    if not position:
        return {
            "success": False,
            "message": f"Position with id {position_id} does not exist"
        }
    
    rang = db_session.query(Rang).filter(
        Rang.id == rang_id
    ).first()
    
    if not rang:
        return {
            "success": False,
            "message": f"Rang with id {rang_id} does not exist"
        }
    
    existing_employee = db_session.query(Employee).filter(
        Employee.last_name == last_name,
        Employee.first_name == first_name,
        Employee.surname == surname
    ).first()
    
    if existing_employee:
        return {
            "success": False,
            "message": f"Employee with name {last_name} {first_name} {surname} already exists",
            "employee_id": existing_employee.id
        }
    
    employee = Employee(
        last_name=last_name,
        first_name=first_name,
        surname=surname,
        birthday=birthday,
        position_id=position_id,
        rang_id=rang_id,
        comment=comment
    )
    db_session.add(employee)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Created employee {employee.first_name} {employee.last_name} {employee.surname} on position {employee.position} with rang {employee.rang} and comment {employee.comment}",
        "employee_id": employee.id
    }

def create_position(
    db_session: Session,
    name: str,
    group_position: str
):
    existing_position = db_session.query(Position).filter(
        Position.name == name
    ).first()
    
    if existing_position:
        return {
            "success": False,
            "message": f"Position with name '{name}' already exists",
            "position_id":existing_position.id

        }
    
    valid_groups = ['среднего и старшего начальствующего состава',
                    'рядового и младшего начальствующего состава',
                    'работников']
    
    if group_position not in valid_groups:
        return {
            "success": False,
            "message": f"Invalid group position. Must be one of: {', '.join(valid_groups)}"
        }
    
    position = Position(
        name=name,
        group_position=group_position
    )
    db_session.add(position)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Added position {position.name}!",
        "position_id":position.id
    }

def create_exercise_type(
    db_session: Session,
    name: str
):
    exercise_type = db_session.query(ExerciseType).filter(
        ExerciseType.name == name,
    ).first()
    
    if exercise_type:
        return {
            "success": False,
            "message": f"ExerciseType with name {name} already exist with id {exercise_type.id}!",
            "exercise_type_id":exercise_type.id
        }
    
    exercise_type = ExerciseType(
        name = name
    )

    db_session.add(exercise_type)
    db_session.flush() 
    db_session.commit()
    return {
        "success": True,
        "message": f"Created exercise_type {exercise_type.name} with id {exercise_type.id}",
        "exercise_type_id":exercise_type.id
    }


def create_rang(
    db_session: Session,
    name: str,
):
    existing_rang = db_session.query(Rang).filter(
        Rang.name == name
    ).first()
    
    if existing_rang:
        return {
            "success": False,
            "message": f"Rang with name '{name}' already exists",
            "rang_id":existing_rang.id
        }
    
    rang = Rang(
        name=name,
    )
    db_session.add(rang)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Added rang {rang.name}!",
        "rang_id":rang.id
    }


def create_exercise(
    db_session: Session,
    employee_id:int,
    exercise_type_id: int,
    date: DateTime,
    address: str,
    comment: Optional[str] = None
    ):

    exercise = db_session.query(PendingExercise).filter(
        PendingExercise.date == date,
        PendingExercise.address == address,
        PendingExercise.employee_id == employee_id
    ).first()
    
    if exercise:
        return {
            "success": False,
            "message": f"Exercise {exercise.id} already exists for employee {employee_id}!",
            "exercise_id": exercise.id,
            "employee_id":employee_id

        }
    
    exercise = PendingExercise(
        employee_id=employee_id,
        exercise_type_id=exercise_type_id,
        date=date,
        address=address,
        comment=comment
    ) 
    db_session.add(exercise)
    db_session.commit()
    return {
        "success": True,
        "message": f"Added exercise {exercise.id} for employee {employee_id}!",
        "exercise_id":exercise.id
    }

def create_exercise_report(
    db_session: Session,
    exercise_id:int,
    start_date: DateTime,
    finish_date: DateTime,
    count_plan: int,
    count_actual: int,
    count_reason: str,
    comment: Optional[str] = None,
):

    exercise = db_session.query(PendingExercise).filter(
        PendingExercise.id== exercise_id,
    ).first()


    if not exercise:
        return {
            "success": False,
            "message": f"ExerciseReport could be only created for existing exercise, exercise {exercise_id} does not exists!"
        }

    exercise_report = db_session.query(ExerciseReport).filter(
        ExerciseReport.exercise_id== exercise_id,
    ).first()
    
    if exercise_report:
        return {
            "success": False,
            "message": f"ExerciseReport already exists with id {exercise_report.id}!",
            "exercise_report_id": exercise_report.id
        }
    valid_count_reason =  [
            'Отсутствие ХП-И', 
            'Отсутствие кислорода', 
            'Отсутствие воздуха', 
            'Пожар', 
            'Запрет выездов', 
            'Прочее']

    if count_reason not in valid_count_reason:
        return {
            "success": False,
            "message": f" {'Count reason should be one of: '.join(valid_count_reason)}!"
        }
    exercise_report = ExerciseReport(
        start_date=start_date,
        finish_date=finish_date,
        count_plan=count_plan,
        count_actual=count_actual,
        count_reason=count_reason,
        comment=comment
    )

    db_session.add(exercise_report)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Created exercise report with id {exercise_report.id}!",
        "exercise_report_id": exercise_report.id

    }


def create_attestation(
    db_session: Session,
    employee_id: int,
    type_id: int,
    status: int,
    date: Date,
    examination_date: Optional[Date]
):

    attestation = db_session.query(Attestation).filter(
        Attestation.employee_id == employee_id,
        Attestation.type_id == type_id,
        Attestation.status == status,
        Attestation.date == date
    ).first()
    
    if attestation:
        return {
            "success": False,
            "message": f"Attestation already exists for employee {employee_id} with id {attestation.id}!",
            "employee_id":employee_id,
            "attestation_id": attestation.id
        }

    attestation_type = db_session.query(AttestationType).filter(
        AttestationType.id == type_id 
    ).first()
    
    if attestation:
        return {
            "success": False,
            "message": f"Attestation already exists with id {attestation.id} for employee {employee_id}!",
            "employee_id":employee_id,
            "attestation_id": attestation.id
        }

    if not attestation_type:
        return {
            "success": False,
            "message": f"Attestation type {type_id} does not exists!",
        }

    attestation = Attestation(
        employee_id=employee_id,
        type_id=type_id,
        status=status,
        date=date,
        examination_date=examination_date
    )

    db_session.add(attestation)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Added attestation {attestation.id} for employee {employee_id} on date {date}!",
        "attestation_type":attestation.id
    }

def create_attestation_type(
    db_session: Session,
    name: str
):
    attestation_type = db_session.query(AttestationType).filter(
        AttestationType.name == name
    ).first()
    
    if attestation_type:
        return {
            "success": False,
            "message": f"Attestation type {name} already exists with id {attestation_type.id}!",
            "attestation_type_id": attestation_type.id
        }
    
    attestation_type = AttestationType(
        name=name
    )
    db_session.add(attestation_type)
    db_session.commit()
    db_session.flush()
    return {
        "success": True,
        "message": f"Added attestation type {name} with id {attestation_type.id}!",
        "attestation_type_id": attestation_type.id
    }
