from datetime import date, datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Motorcycle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "Honda Click 125i"
    year: int = 2024
    current_odometer_km: int = 0
    last_odometer_update: Optional[datetime] = None


class MaintenanceItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    interval_km: Optional[int] = None
    interval_months: Optional[int] = None
    notes: Optional[str] = None


class MaintenanceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="maintenanceitem.id")
    done_at_km: int
    done_date: date
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Setting(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: Optional[str] = None
