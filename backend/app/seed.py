from sqlmodel import Session, select
from app.database import engine
from app.models import MaintenanceItem, Motorcycle, Setting

ITEMS = [
    {"name": "Engine Oil Change",           "interval_km": 6000,  "interval_months": 12,  "notes": "Honda recommends 10W-30 or 0W-30. First change at 1,000 km."},
    {"name": "Air Cleaner Element",         "interval_km": None,  "interval_months": 12,  "notes": "Dealer service only — viscous element, no DIY cleaning."},
    {"name": "Spark Plug",                  "interval_km": 12000, "interval_months": 24,  "notes": "Inspect at 6,000 km."},
    {"name": "Valve Clearance",             "interval_km": 12000, "interval_months": 24,  "notes": "Dealer service."},
    {"name": "Engine Idle Speed",           "interval_km": 12000, "interval_months": 24,  "notes": "Inspect and adjust."},
    {"name": "Throttle Operation",          "interval_km": 12000, "interval_months": 24,  "notes": "Inspect."},
    {"name": "Radiator Coolant",            "interval_km": None,  "interval_months": 36,  "notes": "First replacement at 3 years; then every 2 years."},
    {"name": "Brake Fluid",                 "interval_km": None,  "interval_months": 24,  "notes": "Inspect level every 6,000 km."},
    {"name": "Front Brake Pads",            "interval_km": 12000, "interval_months": None, "notes": "Inspect for wear."},
    {"name": "Rear Brake Shoes",            "interval_km": 12000, "interval_months": None, "notes": "Inspect for wear."},
    {"name": "Brake System",               "interval_km": 6000,  "interval_months": 12,  "notes": "General inspection."},
    {"name": "Headlight Aim",              "interval_km": 12000, "interval_months": None, "notes": "Inspect and adjust."},
    {"name": "Clutch System",              "interval_km": 12000, "interval_months": 24,  "notes": "Inspect."},
    {"name": "Side Stand",                 "interval_km": 12000, "interval_months": 24,  "notes": "Inspect."},
    {"name": "Suspension",                 "interval_km": 12000, "interval_months": 24,  "notes": "Inspect front fork and rear."},
    {"name": "Nuts & Bolts",               "interval_km": 12000, "interval_months": 24,  "notes": "Check tightness."},
    {"name": "Wheels & Tyres",             "interval_km": 6000,  "interval_months": 12,  "notes": "Check pressure, tread, and condition."},
    {"name": "Steering Head Bearings",     "interval_km": 12000, "interval_months": 24,  "notes": "Inspect."},
    {"name": "Drive Belt & Rollers (CVT)", "interval_km": 24000, "interval_months": None, "notes": "Inspect; replace as needed."},
    {"name": "Battery",                    "interval_km": None,  "interval_months": 12,  "notes": "Inspect electrolyte level."},
]


def seed_items():
    with Session(engine) as session:
        for item_data in ITEMS:
            existing = session.exec(
                select(MaintenanceItem).where(MaintenanceItem.name == item_data["name"])
            ).first()
            if not existing:
                session.add(MaintenanceItem(**item_data))

        if not session.exec(select(Motorcycle)).first():
            session.add(Motorcycle())

        for key in ("telegram_bot_token", "telegram_chat_id"):
            if not session.exec(select(Setting).where(Setting.key == key)).first():
                session.add(Setting(key=key, value=None))

        session.commit()
