from fastapi import APIRouter
from database.db_connector import get_db
from authentication.auth import LoginRequest, authenticate_user, create_access_token, PermissionChecker
from config.admin_user import admin_user_credentials
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(
        prefix="/user")

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(request.username, request.password, db)
    token = create_access_token(user, db)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/admin_dashboard")
def admin_dashboard(db: Session = Depends(get_db), permission_checker: PermissionChecker = Depends(PermissionChecker(["Admin"]))):
    return {"message": "Welcome to admin dashboard!"}
