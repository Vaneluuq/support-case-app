# backend/app/crud/crud_support_case.py
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime

from app.models.support_case import SupportCase
from app.schemas.support_case import SupportCaseCreate, SupportCaseUpdate

class CRUDSupportCase:
    # Obtener un caso por ID
    def get(self, db: Session, case_id: int) -> Optional[SupportCase]:
        return db.query(SupportCase).filter(SupportCase.id == case_id).first()

    # Obtener múltiples casos
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[SupportCase]:
        return db.query(SupportCase).offset(skip).limit(limit).all()

    # Crear un nuevo caso
    def create(self, db: Session, obj_in: SupportCaseCreate) -> SupportCase:
        db_obj = SupportCase(
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
            priority=obj_in.priority,
            updated_at= datetime.datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj) # Actualiza el objeto para obtener el ID y las fechas generadas por la DB
        return db_obj

    # Actualizar un caso existente
    def update(self, db: Session, db_obj: SupportCase, obj_in: SupportCaseUpdate) -> SupportCase:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value) # Actualiza los atributos del objeto de DB
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Eliminar un caso
    def remove(self, db: Session, case_id: int) -> Optional[SupportCase]:
        obj = db.query(SupportCase).get(case_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

# Instancia para usar en los endpoints
support_case_crud = CRUDSupportCase()