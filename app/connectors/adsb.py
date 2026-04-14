import requests

READSB_URL = "http://localhost:8080/tar1090/data/aircraft.json"
MAX_RANGE_NM = 150


def get_aircraft():
    resp = requests.get(READSB_URL, timeout=3)
    resp.raise_for_status()
    data = resp.json()
    aircraft = []
    for ac in data.get("aircraft", []):
        if "lat" not in ac or "lon" not in ac:
            continue
        if ac.get("r_dst", 999) > MAX_RANGE_NM:
            continue
        aircraft.append({
            "hex": ac.get("hex"),
            "flight": (ac.get("flight") or "").strip() or ac.get("hex"),
            "alt_baro": ac.get("alt_baro"),
            "gs": ac.get("gs"),
            "track": ac.get("track"),
            "baro_rate": ac.get("baro_rate"),
            "r_dst": ac.get("r_dst"),
            "r_dir": ac.get("r_dir"),
            "rssi": ac.get("rssi"),
            "category": ac.get("category"),
        })
    return aircraft
