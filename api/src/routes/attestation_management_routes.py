from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import jwt

from authentication.auth import get_user_by_login
from database.db_connector import get_db
from models.pydantic_models import  UserPrivilegesResponse
from authentication.auth import PermissionChecker

router = APIRouter(
        prefix="/attestation",
        tags=["attestation management"]
    )


@router.get("/list_all_attestations", tags=["attestation"])
def get_attestations(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


# TODO make model for that
@router.post("/add_attestation", tags=["attestation"])
def add_attestation(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}

@router.delete("/delete_attestation", tags=["attestation"])
def delete_attestation(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.put("/change_attestation", tags=["attestation"])
def change_attestation(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.get("/list_pending_attestations", tags=["planned attestation"])
def get_pending_attestations(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


# TODO make model for that
@router.post("/plan_attestation", tags=["planned attestation"])
def plan_attestation(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.delete("/cancel_attestation", tags=["planned attestation"])
def cancel_attestation(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}


@router.put("/change_pending_attestation", tags=["planned attestation"])
def change_pending_attestation(
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"Not implimented"}
