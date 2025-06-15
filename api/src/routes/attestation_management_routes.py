from fastapi import APIRouter, Depends
from sqlalchemy import select, Date
from sqlalchemy.orm import Session
from typing import List, cast, Optional

from database.db_connector import get_db
from database.db_entity_creation_scripts import create_attestation, create_attestation_type
from database.db_entity_deletion_scripts import delete_attestation_tpye, delete_attestation
from database.db_entity_updation_scripts import update_attestation_type, update_attestation
from database.db_models import AttestationType, Attestation
from authentication.auth import PermissionChecker

router = APIRouter(
        prefix="/attestation",
    )


@router.get("/attestation/all", tags=["attestation"])
def get_attestations_route(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["attestation:read"])),
        db: Session = Depends(get_db)
    ):

    """
    Получить все доступные аттестации

    Returns:
        Dict: result, message, <entity_id>
    """
    stmt = select(Attestation).\
        order_by(Attestation.id)
    
    result = db.execute(stmt)
    attestations= result.scalars().all()

    return attestations


@router.post("/attestation_type/{attestation_type_name}", tags=["attestation type"])
def add_attestation_type_route(
        attestation_type_name: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read","attestation:write" ])),
        db: Session = Depends(get_db)
    ):
    """
    Добавить тип аттестации

    Returns:
        Dict: result, message, <entity_id>
    """
    result = create_attestation_type(db, attestation_type_name)
    return result


@router.delete("/attestation_type/{attestation_type_id}", tags=["attestation type"])
def delete_attestation_type_route(
        attestation_type_id: int,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read","attestation:write"])),
        db: Session = Depends(get_db)
    ):
    """
    Удалить тип аттестации

    Returns:
        Dict: result, message, <entity_id>
    """
    result = delete_attestation_tpye(db, attestation_type_id)
    return  result


@router.put("/attestation_type/{attestation_type_id}", tags=["attestation type"])
def update_attestation_tpye_route(
        attestation_type_id: int,
        new_name: str,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read","attestation:write"])),
        db: Session = Depends(get_db)
    ):

    """
    Обновить тип аттестации

    Returns:
        Dict: result, message, <entity_id>
    """
    result = update_attestation_type(db, attestation_type_id, new_name)
    return  result


@router.get("/attestation_types/all", tags=["attestation type"])
def get_attestations_types_route(
        permission_checker: PermissionChecker = 
        Depends(PermissionChecker(["attestation:read"])),
        db: Session = Depends(get_db)
    ):

    """
    Получить все доступные типы аттестаций

    Returns:
        Dict: result, message, <entity_id>
    """
    stmt = select(AttestationType).\
        order_by(AttestationType.id, AttestationType.name)
    
    result = db.execute(stmt)
    attestation_types= result.scalars().all()

    return attestation_types


@router.post("/attestation", tags=["attestation"])
def add_attestation(
        emplyee_list: List[int],
        type_id: int,
        status: int,
        date: str,
        examination_date: Optional[str] = None,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read", "attestation:write"])),
        db: Session = Depends(get_db)
    ):
    """
    Добавить сотруднику аттестацию

    Returns:
        Dict: result, message, <entity_id>
    """
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


@router.delete("/attestation/{attestation_id}", tags=["attestation"])
def delete_attestation_route(
        attestation_id: int,
        employee_id_list: List[int],
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read", "attestation:write"])),
        db: Session = Depends(get_db)
    ):
    """
    Удалить аттестацию сотрудника 

    Returns:
        Dict: result, message, <entity_id>
    """
    results: List = []
    for employee_id in employee_id_list:
        result = delete_attestation(
                db,
                attestation_id,
                employee_id
                ) 
        results.append(result)
    return results


@router.put("/attestation/{attestation_id}/{emplyee_id}", tags=["attestation"])
def change_attestation(
        attestation_id: int,
        emplyee_id: int,
        type_id: Optional[int] = None,
        status: Optional[int] = None,
        date: Optional[str] = None,
        examination_date: Optional[str] = None,
        permission_checker: PermissionChecker = 
            Depends(PermissionChecker(["attestation:read", "attestation:write"])),
        db: Session = Depends(get_db)
    ):

    """
    Изменить аттестацию сотрудника 

    Returns:
        Dict: result, message, <entity_id>
    """
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
