from datetime import date
from typing import Optional
from dateutil.relativedelta import relativedelta
from app.models import MaintenanceItem, MaintenanceLog

DUE_SOON_KM = 500
DUE_SOON_DAYS = 30


def compute_status(
    item: MaintenanceItem,
    last_log: Optional[MaintenanceLog],
    current_km: int,
    today: date,
) -> str:
    if last_log is None:
        return "overdue"

    statuses: list[str] = []

    if item.interval_km is not None:
        remaining_km = (last_log.done_at_km + item.interval_km) - current_km
        if remaining_km < 0:
            statuses.append("overdue")
        elif remaining_km < DUE_SOON_KM:
            statuses.append("due_soon")
        else:
            statuses.append("ok")

    if item.interval_months is not None:
        due_date = last_log.done_date + relativedelta(months=item.interval_months)
        remaining_days = (due_date - today).days
        if remaining_days < 0:
            statuses.append("overdue")
        elif remaining_days < DUE_SOON_DAYS:
            statuses.append("due_soon")
        else:
            statuses.append("ok")

    if not statuses:
        return "ok"
    if "overdue" in statuses:
        return "overdue"
    if "due_soon" in statuses:
        return "due_soon"
    return "ok"


def km_remaining(item: MaintenanceItem, last_log: Optional[MaintenanceLog], current_km: int) -> Optional[int]:
    if last_log is None or item.interval_km is None:
        return None
    return (last_log.done_at_km + item.interval_km) - current_km


def days_remaining(item: MaintenanceItem, last_log: Optional[MaintenanceLog], today: date) -> Optional[int]:
    if last_log is None or item.interval_months is None:
        return None
    due_date = last_log.done_date + relativedelta(months=item.interval_months)
    return (due_date - today).days
