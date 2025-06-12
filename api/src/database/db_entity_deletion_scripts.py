from sqlalchemy.orm import Session, session
from sqlalchemy import delete
from database.db_models import *
from config.admin_user import admin_user_credentials

"""
Collection of scripts to create entities in database.
Used for fixtures and by api. 
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
            "error": f"Can not delete admin privilege from admin!\n\
                    If access is lost or credentials are compromised:\n\
                    1. Change adimn user data in local.env.\n\
                    2. Restart the docker api container.\n\
                    This will create new admin user and will allow deletion of old user."
        }
     
    if not user:
        return {
            "success": False,
            "error": f"User with login {user.login} does not exist"
        }
    
    
    if not privilege:
        return {
            "success": False,
            "error": f"{privilege.name} privilege not found!"
        }
    
    if privilege not in user.privileges:
        return {
            "success": False,
            "error": f"User with id {user_id} does not have privilege {privilege_id}"
        }
    
    user.privileges.remove(privilege)
    db_session.commit()
    return {
        "success": True,
        "data": privilege_id
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
            "error": f"{e}"
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
                "Success" : True,
                "message" : f"Deleted position {position_id}"
                }
    
    except Exception as e:
        db_session.rollback()

        return {
                "Success" : False,
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
