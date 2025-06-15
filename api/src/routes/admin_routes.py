from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy import ReturnsRows, select
from sqlalchemy.orm import Session

from authentication.auth import  PermissionChecker
from config.admin_user import admin_user_credentials
from database.db_connector import get_db
from database.db_models import User


router = APIRouter(
        prefix="/admin",
        tags=["admin"]
        )


@router.get("/dashboard")
def admin_dashboard(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                ["backend info:read"])),
            db: Session = Depends(get_db)
    ):
    """
    Получить базовую информацию о работе api

    Returns:
        dict: Api runtime info
    """
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


@router.get("/users/all")
def admin_list_users(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                ["privilege:read"])),
        db: Session = Depends(get_db)
    ):
    """
    Получить список пользователей

    Returns:
        List: All users
    """
    users_query = db.query(User)
    users = users_query.all()
    return users



@router.get("/privileges/all", tags=["privilege"])
def admin_list_privileges(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                ["privilege:read"])),
        db: Session = Depends(get_db)
    ):
    """
    Получить список привилегий

    Returns:
        Dict: user_id, login, privilege_id, privilege_name
    """
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


@router.get("/privileges/{user_id}", tags=["privilege"])
def admin_user_list_privileges(
        user_id: str,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME])),
        db: Session = Depends(get_db)
    ):
    """
    Получить списко привилегий пользоватетя по id 

    Returns:
        Dict: user_id, login, privilege_id, privilege_name
    """
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

    privileges_list = []
    for row in rows:
        privileges_list.append({
            'user_id': row.user_id,
            'login': row.login,
            'privilege_id': row.privilege_id,
            'privilege_name': row.privilege_name
        })
    return privileges_list


@router.get("/privileges/all", tags=["privilege"])
def get_all_privileges(
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            ["privilege:read"])),
    ):
    """
    Получить список доступных привилегий

    Returns:
        dict: id, name 
    """
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


@router.delete("/privilege/{user_id}/{privilege_id}", tags=["privilege"])
def admin_revoke_privilege(
        user_id: int,
        privilege_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            ["privilege:read","privilege:read"])),
        db: Session = Depends(get_db)
    ):
    """
    Удалить привилегию у пользоватетя

    Returns:
        Dict: result, message, <entity_id>
    """
    from database.db_entity_deletion_scripts import revoke_privilege_by_ids
    result = revoke_privilege_by_ids(db, user_id, privilege_id)
    
    return result

@router.delete("/privilege/{privilege_id}", tags=["privilege"])
def admin_delete_privilege(
        privilege_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            ["privilege:read","privilege:read"])),
        db: Session = Depends(get_db)
    ):
    """
    Удалить привилегию.
    Удаление не произойдет если привилегия есть хотя бы у одного пользоватетя

    Returns:
        Dict: result, message, <entity_id>
    """
    from database.db_entity_deletion_scripts import delete_privilege 
    result = delete_privilege(db, privilege_id)
    
    return result


@router.post("/privileges/create/{privilege_name}", tags=["privilege"])
def create_privilege(
    privilege_name: str,
    db: Session = Depends(get_db),
    permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            ["privilege:read","privilege:read"])),
):
    """
    Создать привилегию

    Returns:
        Dict: result, message, <entity_id>
    """
    from database.db_entity_creation_scripts import create_privilege
    result = create_privilege(db, privilege_name)
    
    return result


@router.post("/privileges/{user_id}/{privilege_id}", tags=["privilege"])
def admin_grant_privilege(
        user_id: int,
        privilege_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            ["privilege:read","privilege:read"])),
        db: Session = Depends(get_db)
    ):
    """
    Выдать привилегию пользователю по ID обоих сущностей

    Returns:
        Dict: result, message, <entity_id>
    """
    from database.db_entity_creation_scripts import grant_privilege_by_ids

    result = grant_privilege_by_ids(db, user_id, privilege_id)
    
    return result


@router.post("/db_run_query")
def execute_query(
        query:str, 
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                ["db query"]))
    ):
    """
    Выполнить SQL запрос в бд

    Returns:
        Dict: status, query, result
    """
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
