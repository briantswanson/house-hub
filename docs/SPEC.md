# House Hub — Specification

## What is House Hub?

House Hub is a smart home control system that runs on a Raspberry Pi on the home network.
It provides two interfaces to the same backend:

1. **Browser dashboard (PWA)** — view and control devices from any phone or browser on the network
2. **Claude (MCP)** — control and query the house via natural language

Both interfaces talk to the same API. A feature isn't done until it works in both.

---

## User Journeys

### Control devices manually
> Open the dashboard, see which lights are on, tap to turn them off.
> Check the lock state, tap to lock the door.
> See AC temps per room, adjust from the dashboard.

### Ask Claude
> "Are any lights still on?" → status report
> "Lock the door and turn everything off" → executes immediately
> "What's the washer doing?" → reports cycle state

### Run a scene
> Tap "Leaving" on the dashboard or tell Claude "I'm leaving" →
> door locks, garage closes, all lights off, AC to eco mode

### Get notified automatically
> It's 1am and the garage is still open → SMS alert sent
> Washer finishes → SMS notification

### Monitor the network
> "What devices are on the network right now?" → Claude reports via Pi-hole
> Dashboard shows DNS query stats, blocked domains
> Block a domain from the dashboard or by asking Claude

---

## Devices

| Device | Integration | Control |
|---|---|---|
| Smart lock | SmartThings | Lock / unlock |
| Garage door | SmartThings | Open / close |
| Washer, dryer, dishwasher | SmartThings | Status only |
| Range, microwave, TV | SmartThings | Status only |
| Water heater | SmartThings | Status only |
| Lights (all rooms) | Philips Hue | On/off, brightness, color |
| Mini-splits x5 (HVAC) | Sensibo | Mode, temp, fan speed |
| Network / presence | Eero | Who's home, device list |
| DNS / network monitoring | Pi-hole | Stats, block/unblock domains |

---

## Scenes

| Scene | Actions |
|---|---|
| **leaving** | Lock door + close garage + all lights off + AC to eco |
| **arriving** | Unlock door + entry lights on |
| **bedtime** | Lock door + check garage + dim bedroom lights + everything else off |
| **movie_night** | Living room lights to 20% + AC to 72°F |
| **check** | Status report — locked? garage closed? lights left on? |

---

## Notifications

- Delivery: SMS via Twilio
- Triggers defined as routines (see Architecture)
- Examples: garage left open at night, appliance cycle complete, unknown device on network

---

## Success Criteria

- Claude can query and control any supported device
- Dashboard shows live device state (polling)
- Dashboard allows manual control of all devices
- Scenes work from both Claude and the dashboard
- SMS notifications fire on configured triggers
- Pi-hole stats and controls accessible via Claude and dashboard
- App is installable as a PWA on iOS and Android
- Accessible remotely via Tailscale with login required
