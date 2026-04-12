import os
import requests

BASE_URL = "https://api.smartthings.com/v1"

# Map SmartThings category names to friendly labels
CATEGORY_LABELS = {
    "Washer": "Washer",
    "Dryer": "Dryer",
    "Refrigerator": "Refrigerator",
    "Range": "Range",
    "Dishwasher": "Dishwasher",
    "Microwave": "Microwave",
    "Television": "TV",
    "WaterHeater": "Water Heater",
}

# Devices that support on/off via the switch capability
SWITCHABLE = {"Television"}


def _headers():
    return {"Authorization": f"Bearer {os.getenv('SMARTTHINGS_TOKEN')}"}


def _primary_category(device):
    try:
        return device["components"][0]["categories"][0]["name"]
    except (KeyError, IndexError):
        return "Other"


def _device_state(device_id, category):
    """Fetch simplified state for a device based on its category."""
    url = f"{BASE_URL}/devices/{device_id}/status"
    resp = requests.get(url, headers=_headers(), timeout=5)
    if not resp.ok:
        return "unknown"

    components = resp.json().get("components", {}).get("main", {})

    if category == "Washer":
        state = components.get("washerOperatingState", {})
        return state.get("machineState", {}).get("value", "unknown")

    if category == "Dryer":
        state = components.get("dryerOperatingState", {})
        return state.get("machineState", {}).get("value", "unknown")

    if category == "Television":
        state = components.get("switch", {})
        return state.get("switch", {}).get("value", "unknown")

    if category == "Refrigerator":
        door = components.get("contactSensor", {}).get("contact", {}).get("value", "unknown")
        temp = components.get("temperatureMeasurement", {}).get("temperature", {}).get("value")
        if temp:
            return f"door {door} · {round(temp)}°F"
        return f"door {door}"

    if category == "Range":
        oven = components.get("ovenOperatingState", {})
        phase = oven.get("operationPhase", {}).get("value", "")
        mode = oven.get("ovenJobState", {}).get("value", "")
        if phase and phase != "unknown":
            return phase
        if mode and mode != "unknown":
            return mode
        return "off"

    return "unknown"


def send_command(device_id, capability, command):
    """Send a command to a SmartThings device."""
    url = f"{BASE_URL}/devices/{device_id}/commands"
    body = {"commands": [{"component": "main", "capability": capability, "command": command}]}
    resp = requests.post(url, headers=_headers(), json=body, timeout=5)
    return resp.ok


def get_all_status():
    """Return a list of device dicts for the dashboard."""
    resp = requests.get(f"{BASE_URL}/devices", headers=_headers(), timeout=5)
    if not resp.ok:
        return []

    devices = []
    for item in resp.json().get("items", []):
        category = _primary_category(item)
        if category not in CATEGORY_LABELS:
            continue

        device_id = item["deviceId"]
        label = item.get("label") or CATEGORY_LABELS[category]
        state = _device_state(device_id, category)
        actions = ["turn_on", "turn_off"] if category in SWITCHABLE else []

        devices.append({
            "id": device_id,
            "name": label,
            "category": category,
            "state": state,
            "actions": actions,
        })

    return devices
