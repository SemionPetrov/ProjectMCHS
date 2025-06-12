from database.db_models import *
import bcrypt
from datetime import datetime
from config.db_timezone import prefered_timezone
from typing import List, Optional
from sqlalchemy import DateTime, Enum

"""
Collection of scripts to create entities in database.
Used for fixtures and by api. 
"""

def create_privilege(
    db_session, 
    privilege_name: str
):
    privilege = db_session.query(Privilege).filter(
        Privilege.name == privilege_name
    ).first()
    
    if privilege:
        return {
            "success": False,
            "error": f"Privilege {privilege_name} already exists"
        }
    
    privilege = Privilege(name=privilege_name)
    db_session.add(privilege)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "data": privilege
    }


def grant_privilege_by_ids(
    db_session, 
    user_id: int, 
    privilege_id: int 
):
    user = db_session.query(User).filter(User.id == user_id).first()
    
    if not user:
        return {
            "success": False,
            "error": f"User with login {user.login} and id {user.id} does not exist"
        }
    
    privilege = db_session.query(Privilege).filter(Privilege.id == privilege_id).first()
    
    if not privilege:
        return {
            "success": False,
            "error": f"{privilege.name} privilege not found!"
        }
    
    if privilege in user.privileges:
        return {
            "success": False,
            "error": f"Privilege {privilege.name} already exists for user {user.login}"
        }
    
    user.privileges.append(privilege)
    db_session.commit()
    return {
        "success": True,
        "data": privilege
    }

def grant_privilege_by_names(
    db_session, 
    user_login: str, 
    privilege_name: str
    ):
    user = db_session.query(User).filter(User.login == user_login).first()
    
    if not user:
        return {
            "success": False,
            "error": f"User with login {user_login} does not exist"
        }
    
    privilege = db_session.query(Privilege).filter(Privilege.name == privilege_name).first()
    
    if not privilege:
        return {
            "success": False,
            "error": f"{privilege_name} privilege not found!"
        }
    
    if privilege in user.privileges:
        return {
            "success": False,
            "error": f"Privilege {privilege_name} already exists for user {user_login}"
        }
    
    user.privileges.append(privilege)
    db_session.commit()
    return {
        "success": True,
        "data": privilege
    }


def create_user(
    db_session, 
    user_login: str, 
    password: str, 
    employee_id: int|None = None, 
    contact_info: str|None = None
):
    user = db_session.query(User).filter(
        User.login == user_login
    ).first()
    
    if user:
        return {
            "success": False,
            "error": "User already exists!"
        }
    
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()
    
    user = User(
        login=user_login,
        password_hash=password_hash,
        employee_id=employee_id,
        contact_info = contact_info,
        created=datetime.now(prefered_timezone),
        updated_at=datetime.now(prefered_timezone)
    )

    db_session.add(user)
    db_session.flush()
    db_session.commit()
    
    return {
        "success": True,
        "data": user
    }

def create_user_with_privileges(
    db_session,
    user_login: str,
    password: str,
    privilege_names: List[str]
):
    try:
        user = create_user(db_session, user_login, password)
        for privilege_name in privilege_names:
            grant_privilege_by_names(db_session, user_login, privilege_name)
        return user
    except Exception as e:
        db_session.rollback()
        return {
            "success": False,
            "error": str(e)
        }


def create_employee(
    db_session,
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
            "error": f"Position with id {position_id} does not exist"
        }
    
    rang = db_session.query(Rang).filter(
        Rang.id == rang_id
    ).first()
    
    if not rang:
        return {
            "success": False,
            "error": f"Rang with id {rang_id} does not exist"
        }
    
    existing_employee = db_session.query(Employee).filter(
        Employee.last_name == last_name,
        Employee.first_name == first_name,
        Employee.surname == surname
    ).first()
    
    if existing_employee:
        return {
            "success": False,
            "error": f"Employee with name {last_name} {first_name} {surname} already exists"
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
        "data": employee
    }

def create_position(
    db_session,
    name: str,
    group_position: str
):
    existing_position = db_session.query(Position).filter(
        Position.name == name
    ).first()
    
    if existing_position:
        return {
            "success": False,
            "error": f"Position with name '{name}' already exists"
        }
    
    valid_groups = ['среднего и старшего начальствующего состава',
                    'рядового и младшего начальствующего состава',
                    'работников']
    
    if group_position not in valid_groups:
        return {
            "success": False,
            "error": f"Invalid group position. Must be one of: {', '.join(valid_groups)}"
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
        "message": f"Added position {position.name}!" 
    }

def create_rang(
    db_session,
    name: str,
):
    existing_rang = db_session.query(Rang).filter(
        Rang.name == name
    ).first()
    
    if existing_rang:
        return {
            "success": False,
            "error": f"Rang with name '{name}' already exists"
        }
    
    rang = Rang(
        name=name,
    )
    db_session.add(rang)
    db_session.flush()
    db_session.commit()
    return {
        "success": True,
        "message": f"Added rang {rang.name}"
    }


def create_exercise(
    db_session,
    employee_id: List[int],
    exercise_type_id: int,
    date: DateTime,
    address: str,
    comment: str
):
    exercise = db_session.query(PendingExercise).filter(
        PendingExercise.date == date,
        PendingExercise.address == address
    ).first()
    
    if exercise:
        return {
            "success": True,
            "data": exercise
        }
    
    for employee in employee_id:
        exercise = PendingExercise(
            employee_id=employee,
            exercise_type_id=exercise_type_id,
            date=date,
            address=address,
            comment=comment
        )
        db_session.add(exercise)
    
    db_session.commit()
    return {
        "success": True,
        "data": exercise
    }

def create_exercise_report(
    db_session,
    exercise_id: int,
    start_date: DateTime,
    finish_date: DateTime,
    count_plan: int,
    count_actual: int,
    count_reason: Enum,
    comment: str
):
    exercise_report = db_session.query(ExerciseReport).filter(
        ExerciseReport.exercise_id == exercise_id
    ).first()
    
    if exercise_report:
        return {
            "success": True,
            "data": exercise_report
        }
    
    exercise_report = ExerciseReport(
        exercise_id=exercise_id,
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
        "data": exercise_report
    }


def create_attestation(
    db_session,
    employee_id: int,
    type_id: int,
    status: int,
    no_attestation_reason: Optional[str],
    date: Date,
    examination_date: Optional[Date]
):
    attestation = Attestation(
        employee_id=employee_id,
        type_id=type_id,
        status=status,
        no_attestation_reason=no_attestation_reason,
        date=date,
        examination_date=examination_date
    )
    db_session.add(attestation)
    db_session.flush()
    return {
        "success": True,
        "data": attestation
    }

def create_attestation_type(
    db_session,
    name: str
):
    attestation_type = db_session.query(AttestationType).filter(
        AttestationType.name == name
    ).first()
    
    if attestation_type:
        return {
            "success": True,
            "data": attestation_type
        }
    
    attestation_type = AttestationType(
        name=name
    )
    db_session.add(attestation_type)
    db_session.flush()
    return {
        "success": True,
        "data": attestation_type
    }
