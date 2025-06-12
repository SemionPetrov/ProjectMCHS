from database.db_models import *
import bcrypt
from datetime import datetime
from config.db_timezone import prefered_timezone
from config.admin_user import admin_user_credentials
from typing import List, Optional
from sqlalchemy import DateTime, Enum

"""
Collection of scripts to create entities in database.
Used for fixtures and by api. 
"""

def revoke_privilege_by_ids(
    db_session,
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
