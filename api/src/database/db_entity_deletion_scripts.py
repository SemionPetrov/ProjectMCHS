from sqlalchemy.orm import Session, session
from sqlalchemy import delete
from database.db_models import *
from config.admin_user import admin_user_credentials

"""
Collection of scripts to remove entities in database.
Used by api. 
"""

def revoke_privilege_by_ids(
    db_session: Session,
    user_id: int,
    privilege_id: int 
):
    user = db_session.query(User).filter(User.id == user_id).first()
    
    privilege = db_session.query(Privilege).filter(Privilege.id == privilege_id).first()

    if user.login == admin_user_credentials.ADMIN_USERNAME and \
            privilege.name == admin_user_credentials.ADMIN_PRIVILEGE_NAME:
        return {
            "success": False,
            "message": f"Can not delete admin privilege from admin!\n\
                    If access is lost or credentials are compromised:\n\
                    1. Change adimn user data in local.env.\n\
                    2. Restart the docker api container.\n\
                    This will create new admin user and will allow deletion of old user."
        }
     
    if not user:
        return {
            "success": False,
            "message": f"User with login {user.login} does not exist"
        }
    
    
    if not privilege:
        return {
            "success": False,
            "message": f"{privilege.name} privilege not found!"
        }
    
    if privilege not in user.privileges:
        return {
            "success": False,
            "message": f"User with {user.login} does not have privilege {privilege.name}!",
            "user_id": user.id,
            "privilege_id": privilege.id
        }
    
    user.privileges.remove(privilege)
    db_session.commit()
    return {
        "success": True,
        "message": f"Removed {privilege.name} from {user.login}!",
        "user_id": user.id,
        "privilege_id": privilege.id
    }

def delete_employee(db: Session, employee_id: int):
    try:
        stmt = delete(Employee).where(Employee.id == employee_id)
        db.execute(stmt)
        
        db.commit()
        
        return {
            "success": True,
            "message": f'Deleted employee {employee_id}'
        }
    
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "message": f"{e}"
        }


def delete_privilege(
    db_session,
    privilege_id: int
):
    try:
        stmt = delete(Privilege).where(Privilege.id == privilege_id)
        db_session.execute(stmt)
        
        db_session.commit()
        
        return {
                "success" : True,
                "message" : f"deleted privilege {privilege_id}",
                "privilege_id": privilege_id
                }
    
    except Exception as e:
        db_session.rollback()

        return {
                "success" : False,
                "message" : f"{e}"
                }


def delete_position(
    db_session,
    position_id: int
):
    try:
        stmt = delete(Position).where(Position.id == position_id)
        db_session.execute(stmt)
        
        db_session.commit()
        
        return {
                "success" : True,
                "message" : f"deleted position {position_id}",
                "position_id": position_id
                }
    
    except Exception as e:
        db_session.rollback()

        return {
                "success" : False,
                "message" : f"{e}"
                }

def delete_rang(
    db_session,
    rang_id: int
):
    try:
        # Delete the rang
        stmt = delete(Rang).where(Rang.id == rang_id)
        db_session.execute(stmt)
        
        db_session.commit()
        
        return {
                "Success" : True,
                "message" : f"Deleted rang {rang_id}"
                }
    
    except Exception as e:
        db_session.rollback()
        return {
                "Success" : False,
                "message" : f"{e}"
                }
def delete_attestation_tpye(
    db_session:Session,
    attestation_type_id: int
):
    try:
        stmt = delete(AttestationType).where(AttestationType.id == attestation_type_id)
        db_session.execute(stmt)
        db_session.commit()
        
        return {
                "Success" : True,
                "message" : f"Deleted attestation type with id {attestation_type_id}"
                }
    
    except Exception as e:
        db_session.rollback()
        return {
                "Success" : False,
                "message" : f"{e}"
                }


def delete_attestation(
    db_session:Session,
    attestation_id: int,
    employee_id: int
):
    try:
        stmt = delete(Attestation).where(
                Attestation.id == attestation_id,
                Attestation.employee_id == employee_id)
        db_session.execute(stmt)
        db_session.commit()
        
        return {
                "Success" : True,
                "message" : f"Deleted attestation with id {attestation_id} for employee {employee_id}"
                }
    
    except Exception as e:
        db_session.rollback()
        return {
                "Success" : False,
                "message" : f"{e}"
                }

def delete_exercise_type(
    db_session:Session,
    exercise_type_id: int,
):
    try:
        stmt = delete(ExerciseType).where(
                ExerciseType.id == exercise_type_id
        )
        db_session.execute(stmt)
        db_session.flush()
        db_session.commit()
        
        return {
                "Success" : True,
                "message" : f"Deleted exercise_type with id {exercise_type_id}!"
                }
    
    except Exception as e:
        db_session.rollback()
        return {
                "Success" : False,
                "message" : f"{e}"
                }


def delete_exercise_report(
    db_session:Session,
    exercise_report_id: int,
):
    try:
        stmt = delete(ExerciseReport).where(
                ExerciseReport.id ==exercise_report_id 
        )
        db_session.execute(stmt)
        db_session.flush()
        db_session.commit()
        
        return {
                "Success" : True,
                "message" : f"Deleted exercise report with id {exercise_report_id}!"
                }
    
    except Exception as e:
        db_session.rollback()
        return {
                "Success" : False,
                "message" : f"{e}"
                }

def delete_exercise(
    db_session: Session,
    exercise_id: int
):
    try:
        exercise = db_session.query(PendingExercise).filter(PendingExercise.id == exercise_id).first()
        
        if not exercise:
            return {
                "success": False,
                "message": f"Exercise with id {exercise_id} does not exist"
            }
            
        stmt = delete(PendingExercise).where(PendingExercise.id == exercise_id)
        db_session.execute(stmt)
        
        db_session.commit()
        
        return {
            "success": True,
            "message": f"Deleted exercise {exercise_id}"
        }
    
    except Exception as e:
        db_session.rollback()
        return {
            "success": False,
            "message": f"{str(e)}"
        }
