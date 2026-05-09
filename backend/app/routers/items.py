from datetime import date
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import MaintenanceItem, MaintenanceLog, Motorcycle
from app.due_logic import compute_status, km_remaining, days_remaining, replace_days_remaining

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get("")
def list_items(session: Session = Depends(get_session)):
    moto = session.exec(select(Motorcycle)).first()
    current_km = moto.current_odometer_km if moto else 0
    purchase_date = moto.purchase_date if moto else None
    today = date.today()

    items = session.exec(select(MaintenanceItem).order_by(MaintenanceItem.id)).all()
    result = []

    for item in items:
        last_log = session.exec(
            select(MaintenanceLog)
            .where(MaintenanceLog.item_id == item.id)
            .order_by(MaintenanceLog.done_date.desc())
        ).first()

        last_replace_log = None
        if item.replace_months is not None:
            last_replace_log = session.exec(
                select(MaintenanceLog)
                .where(MaintenanceLog.item_id == item.id)
                .where(MaintenanceLog.log_type == "replace")
                .order_by(MaintenanceLog.done_date.desc())
            ).first()

        status = compute_status(item, last_log, current_km, today, purchase_date, last_replace_log)

        result.append({
            "id": item.id,
            "name": item.name,
            "interval_km": item.interval_km,
            "interval_months": item.interval_months,
            "replace_months": item.replace_months,
            "notes": item.notes,
            "maintenance_level": item.maintenance_level,
            "status": status,
            "last_done_km": last_log.done_at_km if last_log else None,
            "last_done_date": str(last_log.done_date) if last_log else None,
            "last_log_id": last_log.id if last_log else None,
            "km_remaining": km_remaining(item, last_log, current_km, purchase_date),
            "days_remaining": days_remaining(item, last_log, today, purchase_date),
            "replace_days_remaining": replace_days_remaining(item, last_replace_log, purchase_date, today),
            "last_replace_date": str(last_replace_log.done_date) if last_replace_log else None,
            "last_replace_km": last_replace_log.done_at_km if last_replace_log else None,
        })

    return result
