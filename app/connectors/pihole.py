import os
import requests

# Pi-hole v6 API — uses password-based session auth


def _base():
    host = os.getenv("PIHOLE_HOST", "localhost")
    return f"http://{host}/api"


def _get_session():
    """Authenticate and return a session ID."""
    password = os.getenv("PIHOLE_PASSWORD", "")
    resp = requests.post(f"{_base()}/auth", json={"password": password}, timeout=5)
    resp.raise_for_status()
    return resp.json()["session"]["sid"]


def _headers():
    sid = _get_session()
    return {"X-FTL-SID": sid}


def get_stats():
    """Return summary stats for the dashboard."""
    resp = requests.get(f"{_base()}/stats/summary", headers=_headers(), timeout=5)
    resp.raise_for_status()
    data = resp.json()

    queries_today = data.get("queries", {}).get("total", 0)
    blocked = data.get("queries", {}).get("blocked", 0)
    blocked_percent = round((blocked / queries_today * 100), 1) if queries_today else 0

    blocking_resp = requests.get(f"{_base()}/dns/blocking", headers=_headers(), timeout=5)
    blocking_enabled = blocking_resp.json().get("blocking", True) if blocking_resp.ok else True

    return {
        "queries_today": queries_today,
        "blocked": blocked,
        "blocked_percent": blocked_percent,
        "blocking_enabled": blocking_enabled,
    }


def set_blocking(enabled: bool):
    """Enable or disable Pi-hole blocking."""
    resp = requests.post(
        f"{_base()}/dns/blocking",
        headers=_headers(),
        json={"blocking": enabled},
        timeout=5
    )
    return resp.ok
