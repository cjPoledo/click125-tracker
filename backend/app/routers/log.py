from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select, func

from app.database import get_session
from app.models import MaintenanceItem, MaintenanceLog

router = APIRouter(prefix="/api/log", tags=["log"])


class LogCreate(BaseModel):
    item_id: int
    done_at_km: int
    done_date: date
    notes: Optional[str] = None


class LogUpdate(BaseModel):
    done_at_km: Optional[int] = None
    done_date: Optional[date] = None
    notes: Optional[str] = None


def log_with_item_name(log: MaintenanceLog, session: Session) -> dict:
    item = session.get(MaintenanceItem, log.item_id)
    return {
        "id": log.id,
        "item_id": log.item_id,
        "item_name": item.name if item else None,
        "done_at_km": log.done_at_km,
        "done_date": str(log.done_date),
        "notes": log.notes,
        "created_at": log.created_at.isoformat() if log.created_at else None,
    }


@router.get("")
def list_log(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    session: Session = Depends(get_session),
):
    total = session.exec(select(func.count()).select_from(MaintenanceLog)).one()
    logs = session.exec(
        select(MaintenanceLog)
        .order_by(MaintenanceLog.done_date.desc(), MaintenanceLog.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [log_with_item_name(log, session) for log in logs],
    }


@router.post("", status_code=201)
def create_log(body: LogCreate, session: Session = Depends(get_session)):
    if not session.get(MaintenanceItem, body.item_id):
        raise HTTPException(status_code=404, detail="Maintenance item not found")
    log = MaintenanceLog(**body.model_dump())
    session.add(log)
    session.commit()
    session.refresh(log)
    return log_with_item_name(log, session)


@router.get("/{log_id}")
def get_log(log_id: int, session: Session = Depends(get_session)):
    log = session.get(MaintenanceLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return log_with_item_name(log, session)


@router.put("/{log_id}")
def update_log(log_id: int, body: LogUpdate, session: Session = Depends(get_session)):
    log = session.get(MaintenanceLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(log, field, value)
    session.add(log)
    session.commit()
    session.refresh(log)
    return log_with_item_name(log, session)


@router.delete("/{log_id}", status_code=204)
def delete_log(log_id: int, session: Session = Depends(get_session)):
    log = session.get(MaintenanceLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    session.delete(log)
    session.commit()
