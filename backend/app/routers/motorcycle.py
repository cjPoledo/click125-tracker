from datetime import date, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models import Motorcycle

router = APIRouter(prefix="/api/motorcycle", tags=["motorcycle"])


class OdometerUpdate(BaseModel):
    current_odometer_km: int


class PurchaseDateUpdate(BaseModel):
    purchase_date: Optional[date] = None


@router.get("")
def get_motorcycle(session: Session = Depends(get_session)):
    moto = session.exec(select(Motorcycle)).first()
    if not moto:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    return moto


@router.put("/odometer")
def update_odometer(body: OdometerUpdate, session: Session = Depends(get_session)):
    moto = session.exec(select(Motorcycle)).first()
    if not moto:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    if body.current_odometer_km < 0:
        raise HTTPException(status_code=422, detail="Odometer cannot be negative")
    moto.current_odometer_km = body.current_odometer_km
    moto.last_odometer_update = datetime.utcnow()
    session.add(moto)
    session.commit()
    session.refresh(moto)
    return moto


@router.put("/purchase-date")
def update_purchase_date(body: PurchaseDateUpdate, session: Session = Depends(get_session)):
    moto = session.exec(select(Motorcycle)).first()
    if not moto:
        raise HTTPException(status_code=404, detail="Motorcycle not found")
    moto.purchase_date = body.purchase_date
    session.add(moto)
    session.commit()
    session.refresh(moto)
    return moto
