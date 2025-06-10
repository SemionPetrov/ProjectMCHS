from database.db_models import User, Privilege
import bcrypt
from datetime import datetime
from config.db_timezone import prefered_timezone

"""
Collection of scripts to create entities in database.
Used for fixtures and by api. 
"""


def create_privilege(db_session, privilege_name: str):
    """Creates the privilege if it doesn't exist."""
    privilege= db_session.query(Privilege).filter(
        Privilege.name == privilege_name
    ).first()
    
    if not privilege:
        privilege = Privilege(name=privilege_name)
        db_session.add(privilege)
        db_session.flush()
    
    return privilege 


def grant_privilege_by_names(db_session, user_login: str, privilege_name: str):
    """Grant privilege to given user by names of both"""
    user = db_session.query(User).filter(User.login == user_login).first()
    
    if not user:
        raise ValueError(f"User with login {user_login} does not exist, could not grant {privilege_name}!")
    
    privilege = db_session.query(Privilege).filter(Privilege.name == privilege_name).first()
    
    if not privilege:
        raise ValueError(f"{privilege_name} privilege not found! Please create it first!")
    
    # Check if privilege already exists
    if privilege in user.privileges:
        print(f"Privilege {privilege_name} already exists for user {user_login}")
        return
    
    user.privileges.append(privilege)
    db_session.commit()


def grant_privilege_by_entities(db_session, user: User, privilege: Privilege):
    """Grant privilege to given user."""
    
    if not user:
        raise ValueError(f"User with login {user.login} does not exist, could not grant {privilege.name}!")
    
    privilege = db_session.query(Privilege).filter(Privilege.name == privilege.name).first()
    
    if not privilege:
        raise ValueError(f"{privilege.name} privilege not found! Please create it first!")
    
    # Check if privilege already exists
    if privilege in user.privileges:
        print(f"Privilege {privilege.name} already exists for user {user.login}")
        return
    
    user.privileges.append(privilege)
    db_session.commit()

def create_user(db_session, user_login: str, password: str, employee_id: int|None = None, contact_info: str| None = None):
    """Create user from login, password, optional employee_id"""

    user = db_session.query(User).filter(
        User.login == user_login
    ).first()
    
    if user:
        return user
    
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()
    
    user = User(
        login=user_login,
        password_hash=password_hash,
        employee_id=employee_id,
        created=datetime.now(prefered_timezone),
        updated_at=datetime.now(prefered_timezone)
    )

    db_session.add(user)
    db_session.flush()
    db_session.commit()
    
    return user

