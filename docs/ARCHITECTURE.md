# House Hub — Architecture

## Overview

House Hub is a Python/Flask application that runs on a Raspberry Pi.
It exposes a REST API consumed by both the browser dashboard and the MCP server (Claude).

```
Claude Code
    ↕ MCP protocol
                   \
                    → house-hub (Pi 4) ← shared backend
                   /      ↕ REST API
Browser / PWA ----
```

---

## Stack

| Layer | Technology | Notes |
|---|---|---|
| Backend | Python 3.11+, Flask | REST API + serves PWA |
| MCP server | FastMCP | Claude tools, runs in same process |
| Scheduler | APScheduler | Automated routines, runs in same process |
| Database | SQLite | State history, logs, routine config |
| Frontend | HTMX + vanilla JS | No build step, served by Flask |
| Notifications | Twilio SMS | Routine alerts |
| Remote access | Tailscale | VPN, no port forwarding |
| Auth | Flask session | Login required for dashboard |
| DNS monitoring | Pi-hole API | Local, runs on same Pi |

---

## Folder Structure

```
house-hub/
├── main.py                  # Entry point — starts Flask + MCP + scheduler
├── app/
│   ├── __init__.py
│   ├── server.py            # Flask app factory, registers blueprints
│   ├── auth.py              # Session login / logout
│   ├── mcp_server.py        # MCP server — all Claude tools defined here
│   ├── scheduler.py         # APScheduler — loads and runs routines
│   ├── notifications.py     # Twilio SMS wrapper
│   ├── connectors/          # One file per external integration
│   │   ├── __init__.py
│   │   ├── hue.py           # Philips Hue (local REST API)
│   │   ├── smartthings.py   # SmartThings (cloud REST API)
│   │   ├── sensibo.py       # Sensibo HVAC (cloud REST API)
│   │   ├── eero.py          # Eero presence (unofficial Python lib)
│   │   └── pihole.py        # Pi-hole (local REST API)
│   ├── models/              # Dataclasses representing devices
│   │   ├── __init__.py
│   │   ├── light.py         # Light(id, name, room, on, brightness, color)
│   │   ├── lock.py          # Lock(id, name, state)
│   │   ├── hvac.py          # HVACUnit(id, name, room, mode, temp, fan)
│   │   ├── appliance.py     # Appliance(id, name, type, state)
│   │   └── scene.py         # Scene(name, actions)
│   ├── api/                 # Flask blueprints — one per device type
│   │   ├── __init__.py
│   │   ├── lights.py        # GET/POST /api/lights
│   │   ├── locks.py         # GET/POST /api/locks
│   │   ├── hvac.py          # GET/POST /api/hvac
│   │   ├── appliances.py    # GET /api/appliances
│   │   ├── scenes.py        # POST /api/scenes/<name>
│   │   ├── network.py       # GET /api/network (Eero + Pi-hole)
│   │   └── status.py        # GET /api/status (full home snapshot)
│   ├── routines/            # Automated routine definitions (P1)
│   │   ├── __init__.py
│   │   └── examples.py      # garage_open_at_night, appliance_done, etc.
│   └── scenes/              # Scene definitions and runner
│       ├── __init__.py
│       └── definitions.py   # leaving, arriving, bedtime, movie_night, check
├── static/
│   ├── index.html           # PWA shell
│   ├── manifest.json        # PWA install metadata
│   └── sw.js                # Service worker (offline support)
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_connectors/
│   └── test_api/
├── data/                    # Gitignored — SQLite DB lives here
├── .env                     # Gitignored — all credentials
└── docs/
    ├── SPEC.md
    ├── ARCHITECTURE.md
    └── CONTRIBUTING.md
```

---

## Layer Responsibilities

### connectors/
Talk to external APIs. Return model objects. Never return raw API responses.
Each connector is a class initialized with credentials from the environment.

```python
# Example
class HueConnector:
    def get_lights(self) -> list[Light]: ...
    def set_light(self, id: str, on: bool, brightness: int) -> Light: ...
```

### models/
Python dataclasses. The shared language between connectors, API, and MCP tools.
No business logic — just data shapes.

### api/
Flask blueprints. Call connectors, return JSON. One blueprint per device type.
All routes require login (enforced via decorator).

```
GET  /api/status              # full home snapshot
GET  /api/lights              # list all lights + state
POST /api/lights/<id>         # set light state
GET  /api/locks               # list locks + state
POST /api/locks/<id>          # lock or unlock
GET  /api/hvac                # list HVAC units + state
POST /api/hvac/<id>           # set mode/temp/fan
GET  /api/appliances          # list appliances + state
POST /api/scenes/<name>       # run a scene
GET  /api/network             # presence + Pi-hole stats
POST /api/network/block       # block a domain
POST /api/network/unblock     # unblock a domain
```

### mcp_server.py
FastMCP tools. Call connectors directly (not the REST API).
Claude talks to this via the MCP protocol.

```python
# Example tools
@mcp.tool()
def get_home_status() -> str: ...

@mcp.tool()
def set_light(room: str, on: bool, brightness: int = 100) -> str: ...

@mcp.tool()
def run_scene(name: str) -> str: ...
```

### scenes/
Scene definitions map a name to a list of actions across connectors.
Called from both `api/scenes.py` and MCP tools.

### scheduler.py
APScheduler runs routines on a schedule or condition check interval.
Each routine checks a condition and fires a notification + optional action.

### notifications.py
Thin wrapper around Twilio. Single function: `send_sms(message: str)`.

---

## Data Flow — Example: "movie night"

```
User taps dashboard  →  POST /api/scenes/movie_night
                     →  scenes/definitions.py runs movie_night()
                     →  HueConnector.set_light(living_room, brightness=20)
                     →  SensiboConnector.set_hvac(living_room, temp=72)
                     →  returns updated state
                     →  dashboard reflects new state on next poll
```

```
User tells Claude "movie night"  →  MCP tool run_scene("movie_night")
                                 →  same scene runner
                                 →  Claude confirms result in chat
```

---

## Credentials (.env)

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
FLASK_SECRET_KEY=
DASHBOARD_PASSWORD=
```

---

## Priority

**P0 — Core (build first)**
- All connectors
- Models
- REST API
- MCP tools
- Dashboard (view + control)
- Auth
- Scenes

**P1 — Next**
- Automated routines
- SMS notifications
- Pi-hole dashboard integration
- PWA install (manifest + service worker)

---

## Adding a New Feature

1. Write a GitHub Issue (see CONTRIBUTING.md)
2. Add or update the model in `models/` if needed
3. Add or update the connector method
4. Add the API endpoint in `api/`
5. Add the MCP tool in `mcp_server.py`
6. Add the dashboard UI in `static/index.html`
7. Write tests
8. Open a PR — CI must pass, Brian reviews
