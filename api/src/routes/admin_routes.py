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


# TODO make model for this
@router.get("/list_privileges")
def admin_liist_privileges(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"mesasge": "Not implimented"}


# TODO make model for this
@router.put("/change_privileges")
def admin_change_privileges(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(
            [admin_user_credentials.ADMIN_PRIVILEGE_NAME]))
    ):
    return {"mesasge": "Not implimented"}



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
