from operator import ge
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt
from typing import List

from authentication.auth import get_user_by_login
from database.db_connector import get_db
from database.db_entity_creation_scripts import create_attestation_type
from database.db_entity_deletion_scripts import delete_attestation_tpye
from database.db_entity_updation_scripts import update_attestation_type
from database.db_models import AttestationType
from models.pydantic_models import  UserPrivilegesResponse
from authentication.auth import PermissionChecker

router = APIRouter(
        prefix="/attestation",
        tags=["attestation management"]
    )


@router.post("/add/{attestation_type_name}", tags=["attestation type"])
def add_attestation_tpye_route(
        attestation_type_name: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read","attestation:write" ])),
        db: Session = Depends(get_db)
    ):
    result = create_attestation_type(db, attestation_type_name)
    return result


@router.delete("/delete/{attestation_type_id}", tags=["attestation type"])
def delete_attestation_tpye_route(
        attestation_type_id: int,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read","attestation:write"])),
        db: Session = Depends(get_db)
    ):
    result = delete_attestation_tpye(db, attestation_type_id)
    return  result

@router.put("/update/{attestation_type_id}", tags=["attestation type"])
def update_attestation_tpye_route(
        attestation_type_id: int,
        new_name: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read","attestation:write"])),
        db: Session = Depends(get_db)
    ):
    result = update_attestation_type(db, attestation_type_id, new_name)
    return  result


@router.get("/all", tags=["attestation type"])
def get_attestations_types_route(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["attestation:read"])),
        db: Session = Depends(get_db)
    ):
    stmt = select(AttestationType).\
        order_by(AttestationType.id, AttestationType.name)
    
    result = db.execute(stmt)
    attestation_types= result.scalars().all()

    return attestation_types


@router.post("/add_attestation", tags=["attestation"])
def add_attestation(
        emplyee_list: List[str],
        type_id: int,
        status: int,
        date: str,
        examination_date: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"message": "Not implimented"}


@router.delete("/delete_attestation/{attestation_id}", tags=["attestation"])
def delete_attestation(
        attestation_id: int,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"message": "Not implimented"}


@router.put("/change_attestation/{attestation_id}", tags=["attestation"])
def change_attestation(
        attestation_id: int,
        emplyee_list: List[str],
        type_id: int,
        status: int,
        date: str,
        examination_date: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker([None]))
    ):
    return {"message": "Not implimented"}
