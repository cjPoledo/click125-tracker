# Click125 Tracker

A Progressive Web App for tracking Honda Click 125i (2024, Philippines) maintenance. Installs to your home screen, works offline, and sends Telegram reminders when service is due.

## Features

- Dashboard with odometer and per-item status (OK / Due Soon / Overdue)
- Maintenance log (create, edit, delete entries)
- Odometer history chart
- Pre-ride checklist (14 items from the Click 125i owner's manual)
- Tyre pressure reference card (kPa, kgf/cm², PSI)
- Daily Telegram reminders for overdue or due-soon items
- Offline support via service worker
- Installable PWA (Add to Home Screen)

## Quick Start

### 1. Clone and configure

```bash
git clone <your-repo-url> click125-tracker
cd click125-tracker
cp .env.example .env
```

Edit `.env` — at minimum, fill in your Telegram bot token and chat ID if you want notifications. You can also configure these later via the Settings page in the app.

**To get a Telegram bot:**
1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → follow prompts
2. Copy the token it gives you
3. Message [@userinfobot](https://t.me/userinfobot) to get your chat ID

### 2. Launch

```bash
docker compose up --build -d
```

The app will be available at:
- **App (frontend)**: http://localhost:3000
- **API (Swagger docs)**: http://localhost:8000/docs

### 3. First run

1. Open http://localhost:3000 on your phone
2. Tap the odometer reading to set your current km
3. Tap **+** to log any maintenance you've already done (otherwise all 20 items will show Overdue)
4. Go to **Settings** to confirm your Telegram credentials

### Add to Home Screen

- **iOS**: Safari → Share → Add to Home Screen
- **Android**: Chrome → menu (⋮) → Add to Home Screen (or install prompt will appear automatically)

## Reverse Proxy (nginx)

If you want to serve from a single domain (recommended), see `nginx.conf` for a sample proxy config. Update `your-domain.com` and SSL certificate paths as needed.

```bash
# Example: serve both frontend and backend via nginx on port 80/443
# Place nginx.conf content in /etc/nginx/sites-available/click125
# Then: sudo nginx -t && sudo nginx -s reload
```

## Telegram Reminders

The app checks daily at 7:00 AM (server time) and sends a message for any item that is:
- **Overdue** (km or time interval exceeded)
- **Due soon** (within 500 km or 30 days)

You can trigger a manual test from **Settings → Test Reminders Now**.

## Data Export

Settings → Export Data as JSON — downloads a full JSON dump of your motorcycle profile, maintenance items, and all log entries.

## Updating

```bash
docker compose pull
docker compose up --build -d
```

Your database persists in a Docker named volume (`db_data`) and survives container rebuilds.

## Development

### Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# → API at http://localhost:8000
# → Swagger UI at http://localhost:8000/docs
```

### Frontend (SvelteKit)

```bash
cd frontend
npm install
npm run dev
# → App at http://localhost:5173
# → /api/* proxied to http://localhost:8000
```

## Maintenance Schedule Reference

Pre-loaded from the Honda Click 125i 2024 owner's manual (Philippines spec):

| Item | Interval |
|------|----------|
| Engine Oil Change | 6,000 km or 12 months |
| Air Cleaner Element | 12 months (inspect) |
| Spark Plug | 12,000 km or 24 months |
| Valve Clearance | 12,000 km or 24 months |
| Engine Idle Speed | 12,000 km or 24 months |
| Throttle Operation | 12,000 km or 24 months |
| Radiator Coolant | 36 months |
| Brake Fluid | 24 months |
| Front Brake Pads | 12,000 km |
| Rear Brake Shoes | 12,000 km |
| Brake System | 6,000 km or 12 months |
| Headlight Aim | 12,000 km |
| Clutch System | 12,000 km or 24 months |
| Side Stand | 12,000 km or 24 months |
| Suspension | 12,000 km or 24 months |
| Nuts & Bolts | 12,000 km or 24 months |
| Wheels & Tyres | 6,000 km or 12 months |
| Steering Head Bearings | 12,000 km or 24 months |
| Drive Belt & Rollers (CVT) | 24,000 km |
| Battery | 12 months |

---

*Honda Click 125i 2024 · Single-user personal tool · No auth required*
