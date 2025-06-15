from database.db_connector import  SessionLocal
from database.db_entity_creation_scripts import create_privilege


priv_list = [
            "personnel:read",
            "personnel:write",

            "exercise:read",
            "exercise:write",

            "attestation:read",
            "attestation:write",

            "privilege:read",
            "privilege:write",

            "backend info:read",
            "db query"
        ]

def setup_privileges():
    """Function to set up privileges."""
    db = SessionLocal()
    try:
        for priv in priv_list:
            create_privilege(
                    db,
                    priv
            )
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

