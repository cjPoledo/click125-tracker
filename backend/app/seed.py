from sqlmodel import Session, select
from app.database import engine
from app.models import MaintenanceItem, Motorcycle, Setting

# Honda Click 125i 2024 maintenance schedule — owner's manual pp. 55-57
# interval_km    : km-based trigger (None = no km interval)
# interval_months: time-based trigger (None = no time interval)
# maintenance_level: Standard | Intermediate | Technical
ITEMS = [
    {
        "name": "Engine Oil Change",
        "interval_km": 6000, "interval_months": 12,
        "notes": "Replace engine oil. Use JASO T903 MB, SAE 10W-30, API SJ or higher. First change at 1,000 km, then every 6,000 km or 12 months — whichever comes first. Reset the OIL CHANGE indicator on the dashboard after every change.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Air Cleaner Element",
        "interval_km": None, "interval_months": 12,
        "notes": "Inspect the viscous air filter element for dirt and damage. Do not clean with air blow or any liquid — this permanently degrades the viscous element. Annual inspect; replace if contaminated. Dealer service only.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Spark Plug",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect electrode gap and condition; replace if worn, fouled, or damaged. Every 12,000 km.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Valve Clearance",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect and adjust intake and exhaust valve clearance. Incorrect clearance causes poor performance and engine damage. Every 12,000 km. Dealer service — requires feeler gauges and shop manual procedure.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Engine Idle Speed",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect idle RPM and adjust if outside spec. Rough or unstable idle at low speed is a sign this is needed. Every 12,000 km.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Throttle Operation",
        "interval_km": 6000, "interval_months": None,
        "notes": "Check that the throttle opens smoothly and snaps fully closed in all steering positions. Also check freeplay. Every 6,000 km.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Fuel Line",
        "interval_km": None, "interval_months": 24,
        "notes": "Inspect fuel line for cracks, hardening, leaks, and loose connections. Annual inspect. Dealer service.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Engine Oil Strainer Screen",
        "interval_km": 12000, "interval_months": None,
        "notes": "Clean the oil strainer screen to remove debris and maintain oil flow. Every 12,000 km.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Crankcase Breather",
        "interval_km": None, "interval_months": 12,
        "notes": "Inspect the crankcase breather drain tube for deposits. Service if deposit level is visible in the transparent section of the drain tube. Annual inspect — service more frequently when riding in rain, at full throttle, or after washing or overturning the vehicle.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Radiator Coolant",
        "interval_km": None, "interval_months": 36,
        "notes": "Replace coolant with Honda Pre-Mix Coolant only — do not dilute with water. First replacement at 3 years; every 2 years after that. Dealer service.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Cooling System",
        "interval_km": None, "interval_months": 12,
        "notes": "Inspect coolant hoses and connections for cracks, leaks, and deterioration. Check reserve tank level is between MIN and MAX. Annual inspect.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Brake Fluid",
        "interval_km": None, "interval_months": 24,
        "notes": "Replace brake fluid. Use Honda DOT 3 or DOT 4 brake fluid. Every 2 years. Dealer service — brake fluid absorbs moisture over time, reducing braking effectiveness.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Front Brake Pads",
        "interval_km": 6000, "interval_months": None,
        "notes": "Inspect brake pad thickness through the inspection port. Replace pads before they wear to the wear indicator. Every 6,000 km.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Rear Brake Shoes",
        "interval_km": 6000, "interval_months": None,
        "notes": "Inspect brake shoe thickness and check lever freeplay; adjust if necessary. Every 6,000 km.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Brake System",
        "interval_km": None, "interval_months": 12,
        "notes": "General inspection of the entire brake system — fluid level, hose condition, lever feel, and function. Annual inspect.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Brake Lock Operation",
        "interval_km": None, "interval_months": None,
        "notes": "Inspect that the rear brake lock lever engages fully and releases completely with no drag on the rear wheel before riding. Inspect as needed — check before every ride.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Headlight Aim",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect headlight beam aim and adjust if the beam is too high, too low, or off-centre. Every 12,000 km.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Clutch Shoes Wear",
        "interval_km": None, "interval_months": 12,
        "notes": "Inspect centrifugal clutch shoe thickness for wear. Annual inspect. Dealer service.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Side Stand",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect the side stand spring and ignition cut-off function. The engine must not start when the side stand is down. Every 12,000 km.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Suspension",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect front fork for oil leaks and smooth operation; inspect rear suspension for smooth operation and no abnormal play. Every 12,000 km.",
        "maintenance_level": "Intermediate",
    },
    {
        "name": "Nuts & Bolts",
        "interval_km": 12000, "interval_months": None,
        "notes": "Check tightness of critical nuts, bolts, and fasteners on the frame, engine, and wheels. Every 12,000 km.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Wheels & Tyres",
        "interval_km": None, "interval_months": 12,
        "notes": "Inspect tyre condition (cuts, cracks, embedded objects, abnormal wear, tread depth indicators). Check and adjust cold tyre pressure: Front 200 kPa / 29 psi, Rear 225 kPa / 33 psi. Annual inspect.",
        "maintenance_level": "Standard",
    },
    {
        "name": "Steering Head Bearings",
        "interval_km": 12000, "interval_months": None,
        "notes": "Inspect steering head bearings for play and rough spots by rocking the front wheel forward and back with the front wheel off the ground. Every 12,000 km. Dealer service.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Drive Belt",
        "interval_km": None, "interval_months": 12,
        "notes": "Inspect CVT drive belt for cracks, fraying, and wear. Annual inspect. Dealer service — requires CVT case removal.",
        "maintenance_level": "Technical",
    },
    {
        "name": "Final Drive Oil",
        "interval_km": None, "interval_months": None,
        "notes": "Replace final drive gear oil. Every 2 years. Dealer service recommended.",
        "maintenance_level": "Technical",
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

        if not session.exec(select(Motorcycle)).first():
            session.add(Motorcycle())

        for key in ("telegram_bot_token", "telegram_chat_id"):
            if not session.exec(select(Setting).where(Setting.key == key)).first():
                session.add(Setting(key=key, value=None))

        session.commit()
