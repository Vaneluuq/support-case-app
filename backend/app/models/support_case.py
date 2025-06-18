# backend/app/models/support_case.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.db.session import Base
import enum

# Definir los estados y prioridades como enums
class CaseStatus(str, enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"
    RESOLVED = "Resolved"

class CasePriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class SupportCase(Base):
    __tablename__ = "support_cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN, nullable=False)
    priority = Column(Enum(CasePriority), default=CasePriority.MEDIUM, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())