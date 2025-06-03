from database.db_connector import  SessionLocal
import bcrypt
from datetime import datetime, timezone

from database.db_models import User, Privilege
from config.admin_user import admin_user_credentials


def create_admin_privilege(db_session):
    """Creates the ADMIN privilege if it doesn't exist."""
    admin_privilege = db_session.query(Privilege).filter(
        Privilege.name == admin_user_credentials.ADMIN_PRIVILEGE_NAME
    ).first()
    
    if not admin_privilege:
        admin_privilege = Privilege(name=admin_user_credentials.ADMIN_PRIVILEGE_NAME)
        db_session.add(admin_privilege)
        db_session.flush()
    
    return admin_privilege

def grant_admin_privilege(db_session):
    """Grant admin privilege to a user."""
    admin_user = db_session.query(User).filter(User.login == admin_user_credentials.ADMIN_USERNAME).first()
    
    if not admin_user:
        raise ValueError(f"Admin user not found! User with login {admin_user_credentials.ADMIN_USERNAME} does not exist")
    
    admin_privilege = db_session.query(Privilege).filter(Privilege.name == admin_user_credentials.ADMIN_PRIVILEGE_NAME).first()
    
    if not admin_privilege:
        raise ValueError(f"{admin_user_credentials.ADMIN_PRIVILEGE_NAME} privilege not found! Please create the ADMIN privilege first")
    
    admin_user.privileges.append(admin_privilege)
    db_session.commit()


def create_admin_user(db_session):
    """Creates admin user with ADMIN privilege."""
    # Check if admin user already exists
    admin_user = db_session.query(User).filter(
        User.login == admin_user_credentials.ADMIN_USERNAME
    ).first()
    
    if admin_user:
        return admin_user
    
    # Create admin user
    admin_privilege = create_admin_privilege(db_session)
    
    password_hash = bcrypt.hashpw(
        admin_user_credentials.ADMIN_PASSWORD.encode(),
        bcrypt.gensalt()
    ).decode()
    
    admin_user = User(
        login=admin_user_credentials.ADMIN_USERNAME,
        password_hash=password_hash,
        created=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db_session.add(admin_user)
    db_session.flush()
    
    # Assign ADMIN privilege
    admin_user.privileges.append(admin_privilege)
    db_session.commit()
    
    return admin_user

def setup_admin_fixture():
    """Main function to set up admin fixture."""
    db = SessionLocal()
    try:
        create_admin_user(db)
        grant_admin_privilege(db)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
