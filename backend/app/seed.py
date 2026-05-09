from sqlmodel import Session, select
from app.database import engine
from app.models import MaintenanceItem, Motorcycle, Setting

# Honda Click 125i 2024 maintenance schedule — owner's manual pp. 56-57
# interval_km    : km-based inspection trigger (None = no km interval)
# interval_months: annual check trigger (None = no annual check)
# replace_months : mandatory time-based replacement interval (separate from inspection)
# maintenance_level: Standard | Intermediate | Technical
ITEMS = [
    {
        "name": "Engine Oil Change",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Replace engine oil. Use JASO T903 MB, SAE 10W-30, API SJ or higher. First change at 1,000 km, then every 6,000 km or 12 months — whichever comes first. Reset the OIL CHANGE indicator on the dashboard after every change.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Air Cleaner Element",
        "interval_km": 18000, "interval_months": None, "replace_months": None,
        "notes": "Replace the viscous air filter element every 18,000 km. Do not clean with air blow or any liquid — this permanently degrades the element. Dealer service required.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Spark Plug",
        "interval_km": 6000, "interval_months": None, "replace_months": None,
        "notes": "Inspect electrode gap and condition every 6,000 km; replace every 12,000 km. Replace earlier if worn, fouled, or damaged.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Valve Clearance",
        "interval_km": 6000, "interval_months": None, "replace_months": None,
        "notes": "Inspect and adjust intake and exhaust valve clearance every 6,000 km. Incorrect clearance causes poor performance and engine damage. Dealer service — requires feeler gauges and shop manual procedure.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Engine Idle Speed",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect idle RPM and adjust if outside spec. Also check at 1,000 km. Every 6,000 km or annually — whichever comes first.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Throttle Operation",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Check that the throttle opens smoothly and snaps fully closed in all steering positions. Also check freeplay. Every 6,000 km or annually — whichever comes first.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Fuel Line",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect fuel line for cracks, hardening, leaks, and loose connections. Every 6,000 km or annually — whichever comes first.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Engine Oil Strainer Screen",
        "interval_km": 12000, "interval_months": None, "replace_months": None,
        "notes": "Clean the oil strainer screen to remove debris and maintain oil flow. Every 12,000 km.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Crankcase Breather",
        "interval_km": 6000, "interval_months": None, "replace_months": None,
        "notes": "Clean the crankcase breather drain tube every 6,000 km. Service more frequently when riding in rain, at full throttle, or after washing or overturning the vehicle.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Radiator Coolant",
        "interval_km": 12000, "interval_months": 12, "replace_months": 36,
        "notes": "Inspect coolant level and condition every 12,000 km and annually. Replace every 3 years with Honda Pre-Mix Coolant only — do not dilute with water.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Cooling System",
        "interval_km": 12000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect coolant hoses and connections for cracks, leaks, and deterioration. Check reserve tank level is between MIN and MAX. Every 12,000 km or annually — whichever comes first.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Brake Fluid",
        "interval_km": 6000, "interval_months": 12, "replace_months": 24,
        "notes": "Inspect brake fluid level and condition every 6,000 km and annually. Replace every 2 years — brake fluid absorbs moisture over time, reducing braking effectiveness. Use Honda DOT 3 or DOT 4.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Front Brake Pads",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect brake pad thickness through the inspection port every 6,000 km or annually. Replace before pads wear to the wear indicator.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Rear Brake Shoes",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect brake shoe thickness and check lever freeplay every 6,000 km or annually; adjust if necessary.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Brake System",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "General inspection of the entire brake system — fluid level, hose condition, lever feel, and function. Also check at 1,000 km. Every 6,000 km or annually — whichever comes first.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Brake Lock Operation",
        "interval_km": 6000, "interval_months": None, "replace_months": None,
        "notes": "Inspect that the rear brake lock lever engages fully and releases completely with no drag on the rear wheel. Every 6,000 km.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Headlight Aim",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect headlight beam aim and adjust if the beam is too high, too low, or off-centre. Every 6,000 km or annually — whichever comes first.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Clutch Shoes Wear",
        "interval_km": 12000, "interval_months": None, "replace_months": None,
        "notes": "Inspect centrifugal clutch shoe thickness for wear every 12,000 km. Dealer service.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Side Stand",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect the side stand spring and ignition cut-off function every 6,000 km and annually. The engine must not start when the side stand is down.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Suspension",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect front fork for oil leaks and smooth operation; inspect rear suspension for smooth operation and no abnormal play. Every 6,000 km or annually — whichever comes first.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Nuts & Bolts",
        "interval_km": 12000, "interval_months": 12, "replace_months": None,
        "notes": "Check tightness of critical nuts, bolts, and fasteners on the frame, engine, and wheels. Also check at 1,000 km. Every 12,000 km or annually — whichever comes first.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Wheels & Tyres",
        "interval_km": 6000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect tyre condition (cuts, cracks, embedded objects, abnormal wear, tread depth indicators). Check and adjust cold tyre pressure: Front 200 kPa / 29 psi, Rear 225 kPa / 33 psi. Every 6,000 km and annually.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Steering Head Bearings",
        "interval_km": 12000, "interval_months": 12, "replace_months": None,
        "notes": "Inspect steering head bearings for play and rough spots every 12,000 km and annually. Dealer service.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Drive Belt",
        "interval_km": 12000, "interval_months": None, "replace_months": None,
        "notes": "Inspect CVT drive belt for cracks, fraying, and wear every 12,000 km; replace every 24,000 km. Dealer service — requires CVT case removal.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Final Drive Oil",
        "interval_km": None, "interval_months": None, "replace_months": 24,
        "notes": "Replace final drive gear oil every 2 years. Dealer service recommended.",
        "maintenance_level": "Intermediate",
    },
]


def seed_items():
    with Session(engine) as session:
        for item_data in ITEMS:
            existing = session.exec(
                select(MaintenanceItem).where(MaintenanceItem.name == item_data["name"])
            ).first()
            if not existing:
                session.add(MaintenanceItem(**item_data))
            else:
                for k, v in item_data.items():
                    setattr(existing, k, v)
                session.add(existing)

        if not session.exec(select(Motorcycle)).first():
            session.add(Motorcycle())

        for key in ("telegram_bot_token", "telegram_chat_id"):
            if not session.exec(select(Setting).where(Setting.key == key)).first():
                session.add(Setting(key=key, value=None))

        session.commit()
