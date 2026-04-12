# House Hub — Pi Setup Guide

This guide walks you through setting up a Raspberry Pi as the server that runs House Hub.
By the end you'll have the app running on your local network, controllable via browser and Claude.

Claude Code can help you through any step — just describe what you're seeing and it'll guide you.

---

## What you need

**Hardware:**
- Raspberry Pi 4 (2GB RAM minimum, 4GB recommended)
- microSD card (16GB minimum, 32GB recommended) + USB reader
- USB-C power supply (5V/3A — CanaKit includes one)
- Your home WiFi credentials

**Accounts (free):**
- GitHub account
- Tailscale account (tailscale.com — sign in with Google)
- Twilio account (twilio.com — for SMS notifications, P1)
- SmartThings account (if you have Samsung devices)

---

## Step 1 — Flash the SD card

1. Download **Raspberry Pi Imager** from raspberrypi.com/software
2. Open Imager and select:
   - **Device:** Raspberry Pi 4
   - **OS:** Raspberry Pi OS Lite (64-bit) — no desktop needed
   - **Storage:** your SD card
3. Click the **gear icon (⚙)** before writing to configure:
   - Hostname: something memorable (e.g. `your-name-pi`)
   - Enable SSH → password authentication
   - Username: `pi`, set a strong password
   - WiFi: your SSID + password + country (US)
   - Timezone: your local timezone
4. Write the image (~5 min)

---

## Step 2 — Boot and SSH in

1. Insert SD card into the Pi, plug in power — no monitor needed
2. Wait ~90 seconds for first boot
3. Find the Pi's IP in your router app (look for your hostname)
4. From your PC terminal:

```bash
ssh pi@your-hostname.local
# or
ssh pi@<IP from router app>
```

Accept the fingerprint prompt (`yes`) and enter your password.

---

## Step 3 — Set a static IP

Find your router's IP:

```bash
ip route | grep default
```

Note the IP after `via` (your router) and `src` (your Pi's current IP). Then:

```bash
sudo nano /etc/dhcpcd.conf
```

Add at the bottom (replace with your actual IPs):

```
interface wlan0
static ip_address=<your-pi-ip>/24
static routers=<your-router-ip>
static domain_name_servers=<your-router-ip>
```

Save with `Ctrl+X`, `Y`, Enter. Reboot:

```bash
sudo reboot
```

SSH back in at the static IP.

---

## Step 4 — Update and install dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git
python3 --version
```

You should see Python 3.11 or higher.

---

## Step 5 (Optional) — Install Pi-hole

**What it does:** Blocks ads and trackers network-wide for every device on your network — phones, TVs, game consoles, everything. Also gives you a dashboard showing every DNS query from every device so you can see exactly what they're talking to.

**Brian's setup:** Running Pi-hole on his Pi means his household sees ~15-20% of all DNS queries blocked automatically. His Samsung TV alone generates hundreds of tracking requests a day — all silently dropped. He can also see when appliances are phoning home unexpectedly.

**Install:**

```bash
curl -sSL https://install.pi-hole.net | bash
```

During setup:
- Interface: `wlan0`
- Upstream DNS: Cloudflare (1.1.1.1)
- Web admin interface: yes
- Log queries: yes
- Privacy mode: 0 (show everything)

Note the admin password at the end.

**Point your router at the Pi for DNS:**
- Open your router app
- Find DNS settings (usually under Network Settings)
- Set primary DNS to your Pi's static IP
- Set secondary DNS to `1.1.1.1` (fallback if Pi goes offline)

Verify it's working:

```bash
nslookup google.com <your-pi-ip>
```

You should see your Pi's IP as the responding server.

---

## Step 6 (Optional) — Install Tailscale

**What it does:** Creates a private VPN between your devices so you can SSH into the Pi and access the House Hub dashboard from anywhere — not just your home network. Also lets you disable Pi-hole remotely if needed.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Open the URL it gives you, sign in with Google. Then get your Tailscale IP:

```bash
tailscale ip
```

Save that IP — you'll use it for remote SSH and dashboard access. Install Tailscale on your phone and laptop too.

---

## Step 7 — Clone House Hub

```bash
cd ~ && git clone https://github.com/briantswanson/house-hub.git
cd house-hub && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Verify:

```bash
python -m pytest
```

Should show 1 test passing.

---

## Step 8 — Discover your devices

Before filling in credentials, figure out what you have.

**SmartThings** — if you have Samsung appliances:
1. Create a Personal Access Token at account.smartthings.com → Personal Access Tokens
2. Check all permission scopes, generate, copy the token
3. Run this to see your devices (replace YOUR_TOKEN):

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.smartthings.com/v1/devices | python3 -m json.tool | grep '"label"'
```

That'll print just the device names. Note what you have.

**Philips Hue** — if you have Hue lights:
1. Open the Hue app → Settings → My Hue system → Hue Bridges
2. Note the bridge IP address
3. To get an API key, press the button on the bridge then run:

```bash
curl -X POST http://<bridge-ip>/api -d '{"devicetype":"house-hub"}'
```

Copy the `username` value from the response — that's your API key.

**Sensibo** — if you have Sensibo Sky units controlling HVAC:
1. Log into home.sensibo.com
2. Settings → API → Generate API key

---

## Step 9 — Configure credentials

```bash
cp .env.example .env && nano .env
```

Fill in what you have, leave the rest blank:

```
SMARTTHINGS_TOKEN=
HUE_BRIDGE_IP=
HUE_API_KEY=
SENSIBO_API_KEY=
EERO_EMAIL=
EERO_PASSWORD=
PIHOLE_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_FROM_NUMBER=
TWILIO_TO_NUMBER=
FLASK_SECRET_KEY=<make up a long random string>
DASHBOARD_PASSWORD=<make up a password for the dashboard login>
```

Save with `Ctrl+X`, `Y`, Enter.

---

## Step 10 — Run as a service

This makes House Hub start automatically on reboot.

```bash
sudo nano /etc/systemd/system/house-hub.service
```

Paste:

```ini
[Unit]
Description=House Hub
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/house-hub
EnvironmentFile=/home/pi/house-hub/.env
ExecStart=/home/pi/house-hub/.venv/bin/python main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Save, then enable and start:

```bash
sudo systemctl enable house-hub && sudo systemctl start house-hub
```

Verify it's running:

```bash
sudo systemctl status house-hub
curl http://<your-pi-ip>:5000/health
```

You should see `{"status": "ok"}`.

---

## Step 11 — Set up Codespaces for contributing

You don't need to write code on the Pi. The Pi runs the app — you write code in GitHub Codespaces.

1. Go to github.com/briantswanson/house-hub
2. Click the green **Code** button → **Codespaces** → **Create codespace on main**
3. Wait for it to load — you'll get VS Code in your browser
4. In the terminal:

```bash
pip install -r requirements.txt
cp .env.example .env
# fill in your credentials
python main.py
```

5. Click the **Ports** tab → open port 5000 to see the dashboard

Read `docs/CONTRIBUTING.md` before opening your first PR.

---

## Troubleshooting

**Can't SSH in:** Check your router app for the Pi's IP. Try `ssh pi@<IP>` directly instead of the hostname.

**Pi-hole breaking internet:** Open your router app, switch DNS back to automatic. That bypasses Pi-hole immediately.

**House Hub not starting:** Check logs with `sudo journalctl -u house-hub -n 50`.

**Test failing:** Make sure your venv is active (`source .venv/bin/activate`) before running pytest.
