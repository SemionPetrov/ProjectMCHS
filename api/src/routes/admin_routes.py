from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from authentication.auth import  PermissionChecker
from config.admin_user import admin_user_credentials
from database.db_connector import get_db

router = APIRouter(
        prefix="/admin",
        tags=["admin"]
        )

@router.get("/dashboard")
def admin_dashboard(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
            db: Session = Depends(get_db)
    ):

    from datetime import datetime
    from config.db_timezone import prefered_timezone
    from database.db_models import User
    import psutil

    return {
        "server time" : datetime.now(prefered_timezone),
        "memory usage" : psutil.virtual_memory().percent,
        "last reboot" : datetime.fromtimestamp(psutil.boot_time()),
        "db status" : "connected" if db else "disconnected",
        "user accounts" : db.query(User).count()
        }


@router.get("/list_privileges")
def admin_list_privileges(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
        db: Session = Depends(get_db)
    ):

    from database.db_models import User, Privilege, user_privileges
    stmt = select(User.id.label('user_id'),
                 User.login.label('login'),
                 Privilege.id.label('privilege_id'),
                 Privilege.name.label('privilege_name')).\
        select_from(User).\
        outerjoin(user_privileges).\
        outerjoin(Privilege).\
        order_by(User.id, Privilege.id)
    
    result = db.execute(stmt)
    rows = result.all()

    print(rows) 

    privileges_list = []
    for row in rows:
        privileges_list.append({
            'user_id': row.user_id,
            'login': row.login,
            'privilege_id': row.privilege_id,
            'privilege_name': row.privilege_name
        })
    return privileges_list

@router.get("/list_privileges/{user_id}")
def admin_user_list_privileges(
        user_id: str,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
        db: Session = Depends(get_db)
    ):

    from database.db_models import User, Privilege, user_privileges
    stmt = select(User.id.label('user_id'),
                 User.login.label('login'),
                 Privilege.id.label('privilege_id'),
                 Privilege.name.label('privilege_name')).\
        select_from(User).\
        outerjoin(user_privileges).\
        outerjoin(Privilege).\
        where(User.id == user_id).\
        order_by(User.id, Privilege.id)
    
    result = db.execute(stmt)
    rows = result.all()

    print(rows) 

    privileges_list = []
    for row in rows:
        privileges_list.append({
            'user_id': row.user_id,
            'login': row.login,
            'privilege_id': row.privilege_id,
            'privilege_name': row.privilege_name
        })
    return privileges_list

@router.get("/privileges/all")
def get_all_privileges(
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
    ):

    from database.db_models import Privilege
    result = db.execute(
        select(Privilege.id, Privilege.name)
    )
    
    privileges_list = []
    for row in result.all():
        privileges_list.append({
            "id": row.id,
            "name": row.name
        })
    
    return privileges_list

@router.delete("/privileges/{user_id}/{privilege_id}")
def admin_delete_privilege(
        user_id: int,
        privilege_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
        db: Session = Depends(get_db)
    ):
    from database.db_entity_deletion_scripts import revoke_privilege_by_ids
    result = revoke_privilege_by_ids(db, user_id, privilege_id)
    
    # Handle the response based on success/error
    if not result["success"]:
        return {
            "success": False,
            "error": result["error"]
        }
    
    return {
        "success": True,
        "message": f"Successfully revoked privilege {privilege_id} from user {user_id}"
    }

@router.post("/privileges/create/{privilege_name}")
def create_privilege(
    privilege_name: str,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
):
    from database.db_entity_creation_scripts import create_privilege
    result = create_privilege(db, privilege_name)
    
    # Handle the response based on success/error
    if not result["success"]:
        return {
            "success": False,
            "error": result["error"]
        }
    
    return {
        "success": True,
        "message": f"Successfully created privilege {privilege_name}"
    }


@router.post("/privileges/{user_id}/{privilege_id}")
def admin_grant_privilege(
        user_id: int,
        privilege_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
        db: Session = Depends(get_db)
    ):
    from database.db_entity_creation_scripts import grant_privilege_by_ids

    result = grant_privilege_by_ids(db, user_id, privilege_id)
    
    if not result["success"]:
        return {
            "success": False,
            "error": result["error"]
        }
    
    return {
        "success": True,
        "message": f"Successfully granted privilege {privilege_id} to user {user_id}"
    }


@router.post("/db_run_query", tags=["dangerous"])
def execute_query(
        query:str, 
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):

    from sqlalchemy import text
    from database.db_connector import engine 


    with engine.connect() as connection:
        try:
            ready_query = text(query)
            result = connection.execute(ready_query)
            
            # Convert result rows to lists of strings
            rows = [[str(value) for value in row] for row in result.fetchall()]
            
            # Format the output as a string
            if not rows:
                formatted_output = "Query executed successfully, but returned no rows."
            else:
                formatted_output = " ".join([", ".join(row) for row in rows])
                
            return {
                "status": "success",
                "query": query,
                "results": formatted_output
            }
        except Exception as e:
            return {
                "status": "failure",
                "query": query,
                "error": str(e)
            } 
