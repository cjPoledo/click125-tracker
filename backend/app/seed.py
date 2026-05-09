from sqlmodel import Session, select
from app.database import engine
from app.models import MaintenanceItem, Motorcycle, Setting

ITEMS = [
    {"name": "Engine Oil Change",          "interval_km": 6000,  "interval_months": 12,   "notes": "Honda recommends 10W-30 or 0W-30. First change at 1,000 km.",                                                                       "maintenance_level": "Standard"},
    {"name": "Air Cleaner Element",        "interval_km": None,  "interval_months": 12,   "notes": "Dealer service only — viscous element, no DIY cleaning.",                                                                            "maintenance_level": "Technical"},
    {"name": "Spark Plug",                 "interval_km": 12000, "interval_months": None, "notes": "Inspect at 6,000 km.",                                                                                                               "maintenance_level": "Intermediate"},
    {"name": "Valve Clearance",            "interval_km": 12000, "interval_months": None, "notes": "Dealer service.",                                                                                                                    "maintenance_level": "Technical"},
    {"name": "Engine Idle Speed",          "interval_km": 12000, "interval_months": None, "notes": "Inspect and adjust.",                                                                                                                "maintenance_level": "Intermediate"},
    {"name": "Throttle Operation",         "interval_km": 6000,  "interval_months": None, "notes": "Inspect.",                                                                                                                           "maintenance_level": "Standard"},
    {"name": "Fuel Line",                  "interval_km": None,  "interval_months": 24,   "notes": "Inspect; replace every 6 years.",                                                                                                   "maintenance_level": "Technical"},
    {"name": "Engine Oil Strainer Screen", "interval_km": 12000, "interval_months": None, "notes": "Clean at first 1,000 km, then every 12,000 km.",                                                                                    "maintenance_level": "Intermediate"},
    {"name": "Crankcase Breather",         "interval_km": None,  "interval_months": 12,   "notes": "Service more frequently when riding in rain, at full throttle, or after washing/overturning the vehicle.",                          "maintenance_level": "Intermediate"},
    {"name": "Radiator Coolant",           "interval_km": None,  "interval_months": 36,   "notes": "First replacement at 3 years; then every 2 years.",                                                                                 "maintenance_level": "Technical"},
    {"name": "Cooling System",             "interval_km": None,  "interval_months": 12,   "notes": "Check coolant level and hoses.",                                                                                                    "maintenance_level": "Intermediate"},
    {"name": "Brake Fluid",                "interval_km": None,  "interval_months": 24,   "notes": "Inspect level every 6,000 km.",                                                                                                     "maintenance_level": "Technical"},
    {"name": "Front Brake Pads",           "interval_km": 6000,  "interval_months": None, "notes": "Inspect for wear.",                                                                                                                  "maintenance_level": "Standard"},
    {"name": "Rear Brake Shoes",           "interval_km": 6000,  "interval_months": None, "notes": "Inspect for wear.",                                                                                                                  "maintenance_level": "Standard"},
    {"name": "Brake System",              "interval_km": None,  "interval_months": 12,   "notes": "General inspection.",                                                                                                                "maintenance_level": "Standard"},
    {"name": "Brake Lock Operation",       "interval_km": None,  "interval_months": None, "notes": "Inspect periodically.",                                                                                                              "maintenance_level": "Standard"},
    {"name": "Headlight Aim",             "interval_km": 12000, "interval_months": None, "notes": "Inspect and adjust.",                                                                                                                "maintenance_level": "Intermediate"},
    {"name": "Clutch Shoes Wear",          "interval_km": None,  "interval_months": 12,   "notes": "Inspect for wear.",                                                                                                                  "maintenance_level": "Technical"},
    {"name": "Side Stand",                "interval_km": 12000, "interval_months": None, "notes": "Inspect.",                                                                                                                           "maintenance_level": "Standard"},
    {"name": "Suspension",                "interval_km": 12000, "interval_months": None, "notes": "Inspect front fork and rear.",                                                                                                       "maintenance_level": "Intermediate"},
    {"name": "Nuts & Bolts",              "interval_km": 12000, "interval_months": None, "notes": "Check tightness.",                                                                                                                   "maintenance_level": "Standard"},
    {"name": "Wheels & Tyres",            "interval_km": None,  "interval_months": 12,   "notes": "Check pressure, tread, and condition.",                                                                                              "maintenance_level": "Standard"},
    {"name": "Steering Head Bearings",    "interval_km": 12000, "interval_months": None, "notes": "Inspect.",                                                                                                                           "maintenance_level": "Technical"},
    {"name": "Drive Belt",                "interval_km": None,  "interval_months": 12,   "notes": "Inspect condition and tension.",                                                                                                     "maintenance_level": "Technical"},
    {"name": "Final Drive Oil",            "interval_km": None,  "interval_months": None, "notes": "Consult dealer — dealer service recommended.",                                                                                       "maintenance_level": "Technical"},
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
