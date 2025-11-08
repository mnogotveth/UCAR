from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel

class IncidentStatus(str, Enum):
    new = "new"
    investigating = "investigating"
    resolved = "resolved"
    closed = "closed"

class IncidentSource(str, Enum):
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"

class IncidentBase(SQLModel):
    description: str = Field(min_length=1, max_length=10_000)
    source: IncidentSource

class IncidentCreate(IncidentBase):
    status: IncidentStatus = IncidentStatus.new

class Incident(IncidentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: IncidentStatus = Field(default=IncidentStatus.new, nullable=False, index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

class IncidentRead(IncidentBase):
    id: int
    status: IncidentStatus
    created_at: datetime

class IncidentStatusUpdate(SQLModel):
    status: IncidentStatus
