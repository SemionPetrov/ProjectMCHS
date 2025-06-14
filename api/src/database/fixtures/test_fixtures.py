from database.db_connector import  SessionLocal
from config.admin_user import admin_user_credentials
from database.db_entity_creation_scripts import create_employee, create_position, create_privilege, create_user, grant_privilege_by_names


def setup_test_fixture():
    db = SessionLocal()
    try:
        create_position(
                db,
                "HR manager",
                'среднего и старшего начальствующего состава'
            )
        #create_employee(
        #        db,
        #        "Human Resource",
        #        "Manager",
        #        "User",
        #        "2000.12.05",
        #        )
        create_user(
                db,
                "Human Resource Manager",
                "hr123"
            )

        grant_privilege_by_names(
                db,
                admin_user_credentials.ADMIN_USERNAME,
                "db query"
        )
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
