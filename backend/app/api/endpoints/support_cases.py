# backend/app/api/endpoints/support_cases.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db # Importar la dependencia de la DB
from app.schemas.support_case import SupportCase, SupportCaseCreate, SupportCaseUpdate
from app.crud.crud_support_case import support_case_crud # Importar las funciones CRUD

router = APIRouter(prefix="/cases", tags=["Support Cases"])

@router.post("/", response_model=SupportCase, status_code=status.HTTP_201_CREATED)
def create_support_case(
    case_in: SupportCaseCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo caso de soporte.
    """
    return support_case_crud.create(db, obj_in=case_in)

@router.get("/", response_model=List[SupportCase])
def read_support_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener una lista de casos de soporte.
    """
    cases = support_case_crud.get_multi(db, skip=skip, limit=limit)
    return cases

@router.get("/{case_id}", response_model=SupportCase)
def read_support_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un caso de soporte específico por ID.
    """
    case = support_case_crud.get(db, case_id=case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=SupportCase)
def update_support_case(
    case_id: int,
    case_in: SupportCaseUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un caso de soporte existente.
    """
    case = support_case_crud.get(db, case_id=case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return support_case_crud.update(db, db_obj=case, obj_in=case_in)

@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_support_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un caso de soporte.
    """
    case = support_case_crud.get(db, case_id=case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    support_case_crud.remove(db, case_id=case_id)
    return {"message": "Case deleted successfully"}