from datetime import date
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import MaintenanceItem, MaintenanceLog, Motorcycle
from app.due_logic import compute_status

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("")
def get_status(session: Session = Depends(get_session)):
    moto = session.exec(select(Motorcycle)).first()
    current_km = moto.current_odometer_km if moto else 0
    today = date.today()

    items = session.exec(select(MaintenanceItem)).all()
    counts = {"ok": 0, "due_soon": 0, "overdue": 0}

    for item in items:
        last_log = session.exec(
            select(MaintenanceLog)
            .where(MaintenanceLog.item_id == item.id)
            .order_by(MaintenanceLog.done_date.desc())
        ).first()
        status = compute_status(item, last_log, current_km, today)
        counts[status] += 1

    return {
        "current_odometer_km": current_km,
        "total_items": len(items),
        **counts,
    }
