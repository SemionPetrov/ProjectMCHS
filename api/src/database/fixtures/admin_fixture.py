from database.db_connector import  SessionLocal
from config.admin_user import admin_user_credentials
from database.db_entity_creation_scripts import create_privilege, create_user, grant_privilege_by_names


def setup_admin_fixture():
    """Main function to set up admin fixture."""
    db = SessionLocal()
    try:
        create_user(
                db,
                admin_user_credentials.ADMIN_USERNAME,
                admin_user_credentials.ADMIN_PASSWORD
        )
        create_privilege(
                db,
                admin_user_credentials.ADMIN_PRIVILEGE_NAME
        )
        grant_privilege_by_names(
                db,
                admin_user_credentials.ADMIN_USERNAME,
                admin_user_credentials.ADMIN_PRIVILEGE_NAME
        )
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
