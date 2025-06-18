# backend/app/schemas/support_case.py
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.support_case import CaseStatus, CasePriority

# Esquema base para la creación o actualización
class SupportCaseBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10)
    status: CaseStatus = CaseStatus.OPEN
    priority: CasePriority = CasePriority.MEDIUM

# Esquema para crear un nuevo caso (hereda de Base)
class SupportCaseCreate(SupportCaseBase):
    pass

# Esquema para actualizar un caso (todos los campos son opcionales)
class SupportCaseUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=10)
    status: CaseStatus | None = None
    priority: CasePriority | None = None

# Esquema para la respuesta de la API (incluye ID y fechas)
class SupportCase(SupportCaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Permite mapear de modelos ORM a Pydantic