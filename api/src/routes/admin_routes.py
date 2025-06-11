from fastapi import APIRouter, Depends

from authentication.auth import  PermissionChecker
from config.admin_user import admin_user_credentials


router = APIRouter(
        prefix="/admin",
        tags=["admin"]
        )

@router.get("/dashboard")
def admin_dashboard(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(
                [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"message": "Welcome to admin dashboard!"}


@router.get("/list_privileges")
def admin_list_privileges(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"mesasge": "Not implimented"}


@router.get("/list_privileges/{user_id}")
def admin_user_list_privileges(
        user_id: str,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"mesasge": f"privileges for user {user_id}"}

@router.delete("/privileges/{user_id}/{priv_id}")
def admin_delete_privilege(
        user_id: int,
        priv_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"mesasge": f"removing {priv_id} from {user_id}"}


@router.post("/privileges/{user_id}/{priv_id}")
def admin_add_privilege(
        user_id: int,
        priv_id: int,
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"mesasge": f"adding {priv_id} from {user_id}"}


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
