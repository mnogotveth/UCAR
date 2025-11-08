from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import Session, select

from app.database import engine, init_db
from app.models import (
    Incident,
    IncidentCreate,
    IncidentRead,
    IncidentStatus,
    IncidentStatusUpdate,
)

app = FastAPI(title="Incident Tracker API", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get("/", tags=["health"])
def healthcheck() -> dict:
    return {"status": "ok"}

@app.post("/incidents", response_model=IncidentRead, status_code=201, tags=["incidents"])
def create_incident(payload: IncidentCreate) -> IncidentRead:
    incident = Incident(**payload.model_dump())  
    with Session(engine) as session:
        session.add(incident)
        session.commit()
        session.refresh(incident)
        return incident

@app.get("/incidents", response_model=List[IncidentRead], tags=["incidents"])
def list_incidents(
    status: Optional[IncidentStatus] = Query(
        None,
        description="Фильтр по статусу. Без параметра вернёт все инциденты.",
    )
) -> List[IncidentRead]:
    stmt = select(Incident)
    if status is not None:
        stmt = stmt.where(Incident.status == status)
    with Session(engine) as session:
        return session.exec(stmt).all()

@app.get("/incidents/{incident_id}", response_model=IncidentRead, tags=["incidents"])
def get_incident(incident_id: int) -> IncidentRead:
    with Session(engine) as session:
        incident = session.get(Incident, incident_id)
        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")
        return incident

@app.patch("/incidents/{incident_id}/status", response_model=IncidentRead, tags=["incidents"])
def update_status(incident_id: int, payload: IncidentStatusUpdate) -> IncidentRead:
    with Session(engine) as session:
        incident = session.get(Incident, incident_id)
        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")
        incident.status = payload.status
        session.add(incident)
        session.commit()
        session.refresh(incident)
        return incident
