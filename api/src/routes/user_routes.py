from fastapi import APIRouter
from database.db_connector import get_db

router = APIRouter(
        prefix="/user")


@router.get("/api/login")
def api_login():
    return "Not implemented"
