import os
from flask import Blueprint, jsonify
from app.connectors import smartthings, pihole

status_bp = Blueprint("status", __name__, url_prefix="/api/status")


def _configured(result, key, fn):
    """Call fn() and store result under key, or mark as not configured on failure."""
    try:
        data = fn()
        result[key] = {"configured": True, **data}
    except Exception:
        result[key] = {"configured": False}


@status_bp.route("/", methods=["GET"])
def get_status():
    result = {}

    # SmartThings
    if os.getenv("SMARTTHINGS_TOKEN"):
        try:
            devices = smartthings.get_all_status()
            result["smartthings"] = {"configured": True, "devices": devices}
        except Exception:
            result["smartthings"] = {"configured": True, "devices": [], "error": True}
    else:
        result["smartthings"] = {"configured": False}

    # Pi-hole
    if os.getenv("PIHOLE_PASSWORD"):
        _configured(result, "pihole", pihole.get_stats)
    else:
        result["pihole"] = {"configured": False}

    # Platforms not yet configured — always included so the frontend can show them
    result["hue"] = {"configured": bool(os.getenv("HUE_BRIDGE_IP") and os.getenv("HUE_API_KEY"))}
    result["sensibo"] = {"configured": bool(os.getenv("SENSIBO_API_KEY"))}
    result["schlage"] = {"configured": False}  # pending account access
    result["myq"] = {"configured": bool(os.getenv("MYQ_EMAIL") and os.getenv("MYQ_PASSWORD"))}

    return jsonify(result)
