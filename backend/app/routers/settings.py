from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from app.database import get_session
from app.models import Setting
from app.scheduler import send_reminders

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingsUpdate(BaseModel):
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None


@router.get("")
def get_settings(session: Session = Depends(get_session)):
    rows = session.exec(select(Setting)).all()
    return {r.key: r.value for r in rows}


@router.put("")
def update_settings(body: SettingsUpdate, session: Session = Depends(get_session)):
    updates = body.model_dump(exclude_none=False)
    for key, value in updates.items():
        row = session.exec(select(Setting).where(Setting.key == key)).first()
        if row:
            row.value = value
            session.add(row)
        else:
            session.add(Setting(key=key, value=value))
    session.commit()
    rows = session.exec(select(Setting)).all()
    return {r.key: r.value for r in rows}


@router.post("/test-telegram")
def test_telegram(session: Session = Depends(get_session)):
    """Trigger the reminder check manually."""
    send_reminders()
    return {"ok": True, "message": "Reminder check triggered"}
