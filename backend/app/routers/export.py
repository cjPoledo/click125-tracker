from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.database import get_session
from app.models import MaintenanceItem, MaintenanceLog, Motorcycle

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("")
def export_data(session: Session = Depends(get_session)):
    moto = session.exec(select(Motorcycle)).first()
    items = session.exec(select(MaintenanceItem).order_by(MaintenanceItem.id)).all()
    logs = session.exec(select(MaintenanceLog).order_by(MaintenanceLog.done_date.desc())).all()

    return {
        "motorcycle": moto.model_dump() if moto else None,
        "maintenance_items": [i.model_dump() for i in items],
        "maintenance_log": [
            {**l.model_dump(), "done_date": str(l.done_date),
             "created_at": l.created_at.isoformat() if l.created_at else None}
            for l in logs
        ],
    }
