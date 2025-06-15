from typing import cast, List, Optional

from sqlalchemy import Boolean, Date, DateTime
from database.db_connector import SessionLocal, get_db
from config.admin_user import admin_user_credentials
from database.db_entity_creation_scripts import create_attestation, create_attestation_type, create_employee, create_exercise_report, create_exercise_type, create_position, create_privilege, create_user, grant_privilege_by_names, create_rang, grant_privilege_by_ids, create_exercise
from database.fixtures import admin_fixture


def grant_admin_all_privs():
    db = SessionLocal() 
    from database.fixtures.privilege_fixtures import priv_list
    for priv in priv_list:
        grant_privilege_by_names(
            db,
            admin_user_credentials.ADMIN_USERNAME,
            priv
        )

def create_test_entities(
        db,
        position_name: str,
        rang_name: str,
        employee_first_name: str,
        employee_last_name: str,
        user_login: str,
        user_password: str,
        privlieges_to_grant: Optional[List[str]] = None,
        attestation_type_to_give: Optional[str] = None,
        exercise_type_to_give: Optional[str] = None,
        create_report = False
        ):

        position_id = create_position(
                db,
                position_name,
                'среднего и старшего начальствующего состава'
            )["position_id"]
        rang_id = create_rang(
            db,
            rang_name,
            )["rang_id"]
        
        employee_id = create_employee(
                db,
                employee_last_name,
                employee_first_name,
                "test",
                cast(Date,"2000.12.05"),
                position_id,
                rang_id,
                "test employee"
                )["employee_id"]

        user_id= create_user(
                db,
                user_login,
                user_password,
                employee_id
            )["user_id"]

        if privlieges_to_grant != None:
            for priv in privlieges_to_grant:
                grant_privilege_by_names(
                    db,
                    user_login,
                    priv,
                )
        if attestation_type_to_give != None:
            attestation_type_id = create_attestation_type(
                    db,
                    attestation_type_to_give
                    )["attestation_type_id"]

            attestation_id = create_attestation(
                    db,
                    employee_id,
                    attestation_type_id,
                    0,
                    cast(Date, "2025-12-18"),
                    cast(Date, "2025-12-20")
                    )
        if exercise_type_to_give != None:
            exercise_type_id = create_exercise_type(
                    db,
                    exercise_type_to_give
                )["exercise_type_id"]

            exercise_id = create_exercise(
                    db,
                    employee_id,
                    exercise_type_id,
                    cast(DateTime,"2025-12-04T15:50:00"),
                    "4 18",
                    "test exercise "
                    )["exercise_id"]

            if create_report:
                exercise_report_id = create_exercise_report(
                    db,
                    exercise_id,
                    cast(DateTime,"2025-12-04T15:50:00"),
                    cast(DateTime,"2025-12-04T19:50:00"),
                    1,
                    0,
                    "Прочее",
                    "testing creation so no one came"
                        )

            
def setup_test_fixture():
    db = SessionLocal() 
    try:
        create_test_entities(db, 
            "hr manager test position",
            "hr manager rang",
            "HR",
            "Manager",
            "HumanResources",
            "pwd123",
            ["personnel:read", "personnel:write"]
        )

        create_test_entities(db, 
            "exercise/attestation test position",
            "teacher test rang",
            "Teacher",
            "test",
            "AttestationMgr",
            "pwd123",
            [
                "personnel:read", 

                "exercise:read",
                "exercise:write",

                "attestation:read",
                "attestation:write",

                "exercise:read",
                "exercise:write",
            ]
        )
        
        create_test_entities(db, 
            "Test worker position",
            "1st test rang",
            "Worker",
            "12",
            "worker",
            "pwd123",
            None,
            "test attestation type 1",
            "test_exersie type1",
            True
        )

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
