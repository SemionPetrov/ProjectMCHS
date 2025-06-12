from fastapi import APIRouter, Depends
from sqlalchemy import select, Date
from sqlalchemy.orm import Session
from typing import List, cast

from database.db_connector import get_db
from database.db_entity_creation_scripts import create_attestation, create_attestation_type
from database.db_entity_deletion_scripts import delete_attestation_tpye, delete_attestation
from database.db_entity_updation_scripts import update_attestation_type, update_attestation
from database.db_models import AttestationType
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
        emplyee_list: List[int],
        type_id: int,
        status: int,
        date: str,
        examination_date: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read", "attestation:write"])),
        db: Session = Depends(get_db)
    ):
    results: List = []
    for employee_id in emplyee_list:
        result = create_attestation(
                db, 
                employee_id,
                type_id,
                status,
                cast(Date,date),
                cast(Date,examination_date)
                )
        results.append(result)
    return results


@router.delete("/delete_attestation/{attestation_id}", tags=["attestation"])
def delete_attestation_route(
        attestation_id: int,
        employee_id_list: List[int],
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read", "attestation:write"])),
        db: Session = Depends(get_db)
    ):

    results: List = []
    for employee_id in employee_id_list:
        result = delete_attestation(
                db,
                attestation_id,
                employee_id
                ) 
        results.append(result)
    return results


@router.put("/change_attestation/{attestation_id}/{emplyee_id}", tags=["attestation"])
def change_attestation(
        attestation_id: int,
        emplyee_id: int,
        type_id: int,
        status: int,
        date: str,
        examination_date: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read", "attestation:write"])),
        db: Session = Depends(get_db)
    ):
    result = update_attestation(
            db,
            attestation_id,
            emplyee_id,
            type_id,
            status,
            cast(Date,date),
            cast(Date,examination_date)
            )
    return result
