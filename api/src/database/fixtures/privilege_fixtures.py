from database.db_connector import  SessionLocal
from config.admin_user import admin_user_credentials
from database.db_entity_creation_scripts import create_privilege, create_user, grant_privilege_by_names
from database.db_models import Attestation


def setup_privileges():
    """Function to set up privileges."""
    db = SessionLocal()
    try:
        create_privilege(
                db,
                "personnel:read"
        )
        create_privilege(
                db,
                "exercise:read"
        )
        create_privilege(
                db,
                "attestation:read"
        )
        create_privilege(
                db,
                "backend info:read"
        )
        create_privilege(
                db,
                "privilege:read"
        )

        create_privilege(
                db,
                "personnel:write"
        )
        create_privilege(
                db,
                "exercise:write"
        )
        create_privilege(
                db,
                "attestation:write"
        )

        create_privilege(
                db,
                "db query"
        )
        create_privilege(
                db,
                "privilege:write"
        )
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

