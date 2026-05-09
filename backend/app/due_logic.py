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
    purchase_date: Optional[date] = None,
) -> str:
    statuses: list[str] = []

    if item.interval_km is not None:
        if last_log is None and purchase_date is None:
            statuses.append("overdue")
        else:
            baseline_km = last_log.done_at_km if last_log else 0
            remaining_km = (baseline_km + item.interval_km) - current_km
            if remaining_km < 0:
                statuses.append("overdue")
            elif remaining_km < DUE_SOON_KM:
                statuses.append("due_soon")
            else:
                statuses.append("ok")

    if item.interval_months is not None:
        baseline_date = last_log.done_date if last_log else purchase_date
        if baseline_date is None:
            statuses.append("overdue")
        else:
            due_date = baseline_date + relativedelta(months=item.interval_months)
            remaining_days = (due_date - today).days
            if remaining_days < 0:
                statuses.append("overdue")
            elif remaining_days < DUE_SOON_DAYS:
                statuses.append("due_soon")
            else:
                statuses.append("ok")

    if item.replace_months is not None:
        replace_d = replace_days_remaining(item, last_log, purchase_date, today)
        if replace_d is not None:
            if replace_d < 0:
                statuses.append("overdue")
            elif replace_d < DUE_SOON_DAYS:
                statuses.append("due_soon")
            else:
                statuses.append("ok")

    if not statuses:
        return "inspect"
    if "overdue" in statuses:
        return "overdue"
    if "due_soon" in statuses:
        return "due_soon"
    return "ok"


def km_remaining(
    item: MaintenanceItem,
    last_log: Optional[MaintenanceLog],
    current_km: int,
    purchase_date: Optional[date] = None,
) -> Optional[int]:
    if item.interval_km is None:
        return None
    if last_log is None and purchase_date is None:
        return None
    baseline_km = last_log.done_at_km if last_log else 0
    return (baseline_km + item.interval_km) - current_km


def days_remaining(
    item: MaintenanceItem,
    last_log: Optional[MaintenanceLog],
    today: date,
    purchase_date: Optional[date] = None,
) -> Optional[int]:
    if item.interval_months is None:
        return None
    baseline_date = last_log.done_date if last_log else purchase_date
    if baseline_date is None:
        return None
    due_date = baseline_date + relativedelta(months=item.interval_months)
    return (due_date - today).days


def replace_days_remaining(
    item: MaintenanceItem,
    last_log: Optional[MaintenanceLog],
    purchase_date: Optional[date] = None,
    today: Optional[date] = None,
) -> Optional[int]:
    if item.replace_months is None:
        return None
    baseline = last_log.done_date if last_log else purchase_date
    if baseline is None:
        return None
    if today is None:
        today = date.today()
    due = baseline + relativedelta(months=item.replace_months)
    return (due - today).days
