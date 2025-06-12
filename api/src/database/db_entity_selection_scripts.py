from database.db_models import *
import bcrypt
from datetime import datetime
from config.db_timezone import prefered_timezone
from config.admin_user import admin_user_credentials
from typing import List, Optional
from sqlalchemy import DateTime, Enum, select
from sqlalchemy.orm import Session
from typing import Tuple, List


"""
Collection of scripts to select entities in database.
Used for fixtures and by api. 
"""

def get_user_privs_with_ids(user: User, db: Session) -> List:
    from database.db_models import User, Privilege, user_privileges
    
    stmt = select(User.id.label('user_id'),
                 User.login.label('login'),
                 Privilege.id.label('privilege_id'),
                 Privilege.name.label('privilege_name')).\
        select_from(User).\
        outerjoin(user_privileges).\
        outerjoin(Privilege).\
        where(User.id == user.id).\
        order_by(User.id, Privilege.id)
    
    result = db.execute(stmt)
    rows = result.all()

    privileges_list = []
    for row in rows:
        privileges_list.append({
            'user_id': row.user_id,
            'login': row.login,
            'privilege_id': row.privilege_id,
            'privilege_name': row.privilege_name
        })
    return privileges_list
