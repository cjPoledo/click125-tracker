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

---

## Deployment (Portainer + Cloudflare Tunnel)

This setup uses your existing `cloudflared` container for ingress — no host ports are opened. Cloudflare handles SSL. nginx runs as a container inside the stack and routes `/api/` to the FastAPI backend and everything else to the SvelteKit frontend.

### 1. One-time server setup

```bash
# Create the shared Docker network (skip if it already exists)
docker network create cloudflared

# Connect your existing cloudflared container to it
docker network connect cloudflared <your-cloudflared-container-name>
```

### 2. Configure the Cloudflare Tunnel

In the [Cloudflare Zero Trust dashboard](https://one.dash.cloudflare.com/) → Networks → Tunnels → your tunnel → **Public Hostnames** → Add:

| Field | Value |
|-------|-------|
| Subdomain / Domain | `your-domain.com` (or a subdomain) |
| Service type | HTTP |
| URL | `nginx:80` |

Cloudflare resolves `nginx` to the nginx container via the shared `cloudflared` Docker network.

### 3. Deploy via Portainer

1. Portainer → **Stacks** → **Add Stack**
2. Paste the contents of `docker-compose.yml` (or connect your Git repo)
3. Set environment variables:
   - `TELEGRAM_BOT_TOKEN` — from [@BotFather](https://t.me/BotFather) (optional, configurable later in the app)
   - `TELEGRAM_CHAT_ID` — from [@userinfobot](https://t.me/userinfobot) (optional)
4. **Deploy the stack**

The stack starts 3 containers: `backend`, `frontend`, `nginx`. The nginx container joins the `cloudflared` network so your tunnel can reach it.

### 4. First run

1. Open your tunnel URL on your phone (e.g. `https://click125.your-domain.com`)
2. Tap the odometer reading to set your current km
3. Tap **+** to log any maintenance you've already done (otherwise all 20 items will show Overdue)
4. Go to **Settings** to confirm your Telegram credentials

### Add to Home Screen

- **iOS**: Safari → Share → Add to Home Screen
- **Android**: Chrome → menu (⋮) → Add to Home Screen (or install prompt will appear automatically)

### Updating

Rebuild in Portainer (pull latest images / redeploy stack), or:

```bash
docker compose build
docker compose up -d
```

Your database persists in a Docker named volume (`db_data`) and survives container rebuilds.

---

## Access Control (Cloudflare Access)

By default anyone with your tunnel URL can use the app. Lock it to yourself using Cloudflare Access — it gates the entire hostname at the Cloudflare edge before requests reach your server. Free for a single user, no code or Docker changes needed.

**In [Cloudflare Zero Trust](https://one.dash.cloudflare.com/) → Zero Trust:**

1. **Settings → Authentication** — add an identity provider. Google is simplest (OAuth with your Google account).

2. **Access → Applications → Add an application → Self-hosted**
   - Application name: `Click125 Tracker`
   - Application domain: `your-domain.com`
   - Session duration: `1 month` (so your phone stays logged in)

3. **Add a policy:**
   - Policy name: `Owner only`
   - Action: `Allow`
   - Include rule: `Emails` → `your@email.com`

4. Save.

Anyone hitting the URL now sees a Cloudflare login page first. After you authenticate once on your phone, the session lasts a month before requiring re-auth.

---

## Telegram Reminders

The app checks daily at 7:00 AM (server time) and sends a message for any item that is:
- **Overdue** (km or time interval exceeded)
- **Due soon** (within 500 km or 30 days)

You can trigger a manual test from **Settings → Test Reminders Now**.

**To get a Telegram bot:**
1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → follow prompts → copy the token
2. Message [@userinfobot](https://t.me/userinfobot) to get your numeric chat ID

---

## Data Export

Settings → Export Data as JSON — downloads a full JSON dump of your motorcycle profile, maintenance items, and all log entries.

---

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

---

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
