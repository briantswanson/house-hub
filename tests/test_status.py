import pytest
from unittest.mock import patch
from app.server import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_status_no_credentials(client):
    """All platforms unconfigured when no env vars set."""
    with patch.dict("os.environ", {}, clear=True):
        resp = client.get("/api/status/")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["smartthings"]["configured"] is False
        assert data["pihole"]["configured"] is False
        assert data["hue"]["configured"] is False
        assert data["sensibo"]["configured"] is False


def test_status_smartthings_configured(client):
    """SmartThings shows as configured when token is set."""
    with patch.dict("os.environ", {"SMARTTHINGS_TOKEN": "fake-token"}):
        with patch("app.connectors.smartthings.get_all_status", return_value=[]):
            resp = client.get("/api/status/")
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["smartthings"]["configured"] is True
            assert "devices" in data["smartthings"]


def test_status_pihole_configured(client):
    """Pi-hole shows as configured when password is set."""
    mock_stats = {
        "queries_today": 1000,
        "blocked": 150,
        "blocked_percent": 15.0,
        "blocking_enabled": True,
    }
    with patch.dict("os.environ", {"PIHOLE_PASSWORD": "test-pass"}):
        with patch("app.connectors.pihole.get_stats", return_value=mock_stats):
            resp = client.get("/api/status/")
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["pihole"]["configured"] is True
            assert data["pihole"]["queries_today"] == 1000
            assert data["pihole"]["blocked_percent"] == 15.0


def test_status_hue_configured(client):
    """Hue shows as configured when both env vars are set."""
    with patch.dict("os.environ", {"HUE_BRIDGE_IP": "192.168.1.2", "HUE_API_KEY": "abc123"}):
        resp = client.get("/api/status/")
        data = resp.get_json()
        assert data["hue"]["configured"] is True


def test_status_always_includes_all_platforms(client):
    """All known platforms are always present in the response."""
    with patch.dict("os.environ", {}, clear=True):
        resp = client.get("/api/status/")
        data = resp.get_json()
        for platform in ["smartthings", "pihole", "hue", "sensibo", "schlage", "myq"]:
            assert platform in data
