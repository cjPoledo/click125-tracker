"""
Migration: correct interval_km / interval_months values per Honda Click 125i 2024
owner's manual pages 55-57.

Run inside the backend container:
  docker exec -it <backend-container> python /app/migrate_intervals.py

Or locally (with venv active, from backend/):
  DATABASE_URL=sqlite:////path/to/click125.db python migrate_intervals.py
"""
import os
import sqlite3

db_url = os.environ.get("DATABASE_URL", "sqlite:////app/data/click125.db")
db_path = db_url.replace("sqlite:////", "/").replace("sqlite:///", "")

print(f"Connecting to: {db_path}\n")
con = sqlite3.connect(db_path)
cur = con.cursor()
updated = 0


def fix(name, interval_km, interval_months):
    global updated
    cur.execute(
        "UPDATE maintenanceitem SET interval_km=?, interval_months=? WHERE name=?",
        (interval_km, interval_months, name),
    )
    if cur.rowcount:
        km_str = f"{interval_km:,} km" if interval_km is not None else "NULL km"
        mo_str = f"{interval_months} months" if interval_months is not None else "NULL months"
        print(f"  ✓ {name}: {km_str} / {mo_str}")
        updated += cur.rowcount
    else:
        print(f"  ! '{name}' not found — skipped")


# Fix 1 — Remove fabricated 24-month intervals
# Manual has no "24-month" column; these are km-only inspect items.
print("Fix 1 — Remove fabricated 24-month intervals:")
fix("Spark Plug",              12000, None)
fix("Valve Clearance",         12000, None)
fix("Engine Idle Speed",       12000, None)
fix("Side Stand",              12000, None)
fix("Suspension",              12000, None)
fix("Nuts & Bolts",            12000, None)
fix("Steering Head Bearings",  12000, None)

# Fix 2 — Correct starting km interval for brake/throttle items
# Manual shows first inspection at 6,000 km, not 12,000 km.
print("\nFix 2 — Correct starting km interval:")
fix("Throttle Operation", 6000, None)
fix("Front Brake Pads",   6000, None)
fix("Rear Brake Shoes",   6000, None)

# Fix 3 — Annual Check-only items should have no km trigger
# Manual places these in the Annual Check column only.
print("\nFix 3 — Remove fabricated km intervals from annual-check-only items:")
fix("Brake System",   None, 12)
fix("Wheels & Tyres", None, 12)

# Fix 4 — Crankcase Breather is Annual, not interval-less
# Manual places it in the Annual Check column.
print("\nFix 4 — Crankcase Breather → Annual (12 months):")
fix("Crankcase Breather", None, 12)

con.commit()
con.close()
print(f"\nMigration complete — {updated} row(s) updated.")
