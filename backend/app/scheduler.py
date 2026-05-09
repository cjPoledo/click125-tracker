from datetime import date
from sqlmodel import Session, select
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import engine
from app.models import MaintenanceItem, MaintenanceLog, Motorcycle, Setting
from app.due_logic import compute_status
from app.telegram import send_telegram_message

scheduler = BackgroundScheduler()


def send_reminders():
    with Session(engine) as session:
        token_row = session.exec(select(Setting).where(Setting.key == "telegram_bot_token")).first()
        chat_row = session.exec(select(Setting).where(Setting.key == "telegram_chat_id")).first()

        if not token_row or not token_row.value or not chat_row or not chat_row.value:
            return

        bot_token = token_row.value
        chat_id = chat_row.value

        moto = session.exec(select(Motorcycle)).first()
        if not moto:
            return

        current_km = moto.current_odometer_km
        today = date.today()
        items = session.exec(select(MaintenanceItem)).all()

        for item in items:
            last_log = session.exec(
                select(MaintenanceLog)
                .where(MaintenanceLog.item_id == item.id)
                .order_by(MaintenanceLog.done_date.desc())
            ).first()

            status = compute_status(item, last_log, current_km, today)
            if status in ("overdue", "due_soon"):
                last_km = str(last_log.done_at_km) + " km" if last_log else "never"
                last_date = str(last_log.done_date) if last_log else "never"
                emoji = "🔴" if status == "overdue" else "⚠️"
                text = (
                    f"{emoji} <b>Honda Click 125i</b> — {item.name} is "
                    f"{'overdue' if status == 'overdue' else 'due soon'}!\n"
                    f"Last done: {last_km} / {last_date}\n"
                    f"Currently at: {current_km} km"
                )
                send_telegram_message(bot_token, chat_id, text)


def start_scheduler():
    scheduler.add_job(send_reminders, "cron", hour=7, minute=0, id="daily_reminders", replace_existing=True)
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown(wait=False)
