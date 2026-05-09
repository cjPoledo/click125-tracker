"""
One-shot migration: correct maintenance schedule per Honda Click 125i 2024 manual.

Run inside the backend container:
  docker exec -it <backend-container> python /app/migrate_schedule.py

Or locally (with venv active, from backend/):
  DATABASE_URL=sqlite:////path/to/click125.db python migrate_schedule.py
"""
import os
import sqlite3

db_url = os.environ.get("DATABASE_URL", "sqlite:////app/data/click125.db")
db_path = db_url.replace("sqlite:////", "/").replace("sqlite:///", "")

print(f"Connecting to: {db_path}")
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Delete Battery (maintenance-free — no schedule applies)
cur.execute("SELECT id FROM maintenanceitem WHERE name = 'Battery'")
row = cur.fetchone()
if row:
    battery_id = row[0]
    cur.execute("DELETE FROM maintenancelog WHERE item_id = ?", (battery_id,))
    cur.execute("DELETE FROM maintenanceitem WHERE id = ?", (battery_id,))
    print(f"Deleted Battery (id={battery_id}) and its log entries.")
else:
    print("Battery not found — skipping delete.")

# 2. Rename Clutch System → Clutch Shoes Wear, fix intervals
cur.execute(
    "UPDATE maintenanceitem SET name=?, interval_km=?, interval_months=?, notes=? WHERE name=?",
    ("Clutch Shoes Wear", None, 12, "Inspect for wear.", "Clutch System"),
)
if cur.rowcount:
    print("Renamed 'Clutch System' → 'Clutch Shoes Wear' (NULL km, 12 months).")
else:
    print("'Clutch System' not found — skipping rename.")

# 3. Rename Drive Belt & Rollers (CVT) → Drive Belt, fix intervals
cur.execute(
    "UPDATE maintenanceitem SET name=?, interval_km=?, interval_months=?, notes=? WHERE name=?",
    ("Drive Belt", None, 12, "Inspect condition and tension.", "Drive Belt & Rollers (CVT)"),
)
if cur.rowcount:
    print("Renamed 'Drive Belt & Rollers (CVT)' → 'Drive Belt' (NULL km, 12 months).")
else:
    print("'Drive Belt & Rollers (CVT)' not found — skipping rename.")

# 4. Insert missing items (idempotent — skip if name already exists)
new_items = [
    ("Fuel Line",               None,  24,   "Inspect; replace every 6 years."),
    ("Engine Oil Strainer Screen", 12000, None, "Clean at first 1,000 km, then every 12,000 km."),
    ("Crankcase Breather",      None,  None, "Inspect periodically."),
    ("Cooling System",          None,  12,   "Check coolant level and hoses."),
    ("Final Drive Oil",         None,  None, "Consult dealer — dealer service recommended."),
    ("Brake Lock Operation",    None,  None, "Inspect periodically."),
]

for name, km, months, notes in new_items:
    cur.execute("SELECT id FROM maintenanceitem WHERE name = ?", (name,))
    if cur.fetchone():
        print(f"'{name}' already exists — skipping insert.")
    else:
        cur.execute(
            "INSERT INTO maintenanceitem (name, interval_km, interval_months, notes) VALUES (?,?,?,?)",
            (name, km, months, notes),
        )
        print(f"Inserted '{name}'.")

con.commit()
con.close()
print("Migration complete.")
