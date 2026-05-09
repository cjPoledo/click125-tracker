"""
Migration: add maintenance_level column and populate per Honda Click 125i 2024
owner's manual pages 55-57 legend.

Run inside the backend container:
  docker exec -it <backend-container> python /app/migrate_levels.py

Or locally (with venv active, from backend/):
  DATABASE_URL=sqlite:////path/to/click125.db python migrate_levels.py
"""
import os
import sqlite3

db_url = os.environ.get("DATABASE_URL", "sqlite:////app/data/click125.db")
db_path = db_url.replace("sqlite:////", "/").replace("sqlite:///", "")

print(f"Connecting to: {db_path}\n")
con = sqlite3.connect(db_path)
cur = con.cursor()

# Add column — silently skip if it already exists
try:
    cur.execute(
        "ALTER TABLE maintenanceitem ADD COLUMN maintenance_level TEXT "
        "CHECK(maintenance_level IN ('Standard', 'Intermediate', 'Technical'))"
    )
    print("Added maintenance_level column.\n")
except sqlite3.OperationalError as e:
    if "duplicate column" in str(e).lower():
        print("maintenance_level column already exists — skipping ALTER.\n")
    else:
        raise

# Name → level mapping (manual pp. 55-57)
LEVELS = {
    "Fuel Line":                  "Technical",
    "Fuel Level":                 "Standard",
    "Throttle Operation":         "Standard",
    "Air Cleaner":                "Technical",
    "Crankcase Breather":         "Intermediate",
    "Spark Plug":                 "Intermediate",
    "Valve Clearance":            "Technical",
    "Engine Oil":                 "Standard",
    "Engine Oil Change":          "Standard",    # DB name variant
    "Engine Oil Strainer Screen": "Intermediate",
    "Engine Idle Speed":          "Intermediate",
    "Radiator Coolant":           "Technical",
    "Cooling System":             "Intermediate",
    "Drive Belt":                 "Technical",
    "Final Drive Oil":            "Technical",
    "Brake Fluid":                "Technical",
    "Brake Shoes / Pads Wear":    "Standard",
    "Front Brake Pads":           "Standard",    # DB name variant
    "Rear Brake Shoes":           "Standard",    # DB name variant
    "Brake System":               "Standard",
    "Brake Lock Operation":       "Standard",
    "Headlight Aim":              "Intermediate",
    "Lights & Horn":              "Standard",
    "Clutch Shoes Wear":          "Technical",
    "Side Stand":                 "Standard",
    "Suspension":                 "Intermediate",
    "Nuts & Bolts":               "Standard",    # DB name
    "Nuts, Bolts & Fasteners":    "Standard",    # reference name
    "Wheels & Tyres":             "Standard",
    "Steering Head Bearings":     "Technical",
}

rows = cur.execute("SELECT id, name FROM maintenanceitem ORDER BY id").fetchall()
updated = 0
skipped = []

print("Assigning maintenance levels:")
for item_id, name in rows:
    level = LEVELS.get(name)
    if level:
        cur.execute(
            "UPDATE maintenanceitem SET maintenance_level=? WHERE id=?",
            (level, item_id),
        )
        print(f"  {level:<14} {name}")
        updated += 1
    else:
        skipped.append(name)

if skipped:
    print(f"\n  ! No level defined for: {', '.join(skipped)}")

con.commit()
con.close()
print(f"\nMigration complete — {updated} row(s) updated.")
