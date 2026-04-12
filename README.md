# house-hub

Smart home control via Claude (MCP) + browser dashboard.

Runs on a Raspberry Pi. Controls SmartThings, Philips Hue, Sensibo (HVAC), and Eero devices.

## Architecture

```
Claude Code
    ↕ MCP protocol
                   \
                    → house-hub (Pi 4) ← shared backend
                   /      ↕ REST API
Browser / PWA ----
```

## Setup

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) to get started.

## Stack

- Python 3.11+
- Flask (REST API + PWA)
- FastMCP (MCP server)
- pytest
