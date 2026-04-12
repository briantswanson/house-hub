# Contributing to House Hub

Welcome! No experience required — Claude Code is here to help at every step.

Before contributing, read [SPEC.md](SPEC.md) (what we're building) and [ARCHITECTURE.md](ARCHITECTURE.md) (how it's structured). Claude can explain any part of either doc if something isn't clear.

---

## How a feature gets built

1. **Write a GitHub Issue** describing what you want (use the feature template)
2. **Create a branch** off main: `git checkout -b feature/your-feature-name`
3. **Implement it** across all three layers (see below)
4. **Write tests** for any new logic
5. **Open a PR** — CI runs automatically (flake8 + pytest)
6. **Brian reviews** and merges

A feature isn't done until it works in all three places:
- Claude can do it (MCP tool in `app/mcp_server.py`)
- The API supports it (Flask endpoint in `app/api/`)
- The dashboard shows it (UI in `static/index.html`)

---

## Where things go

```
app/connectors/      # Talk to external APIs — Hue, SmartThings, Sensibo, Eero, Pi-hole
app/models/          # Data shapes — Light, Lock, HVACUnit, Appliance
app/api/             # Flask REST endpoints — one file per device type
app/mcp_server.py    # Claude tools — @mcp.tool() functions
app/scenes/          # Multi-device scenes (leaving, movie_night, etc.)
app/routines/        # Automated triggers, e.g. garage open at night (P1)
static/index.html    # Dashboard UI — all frontend lives here
tests/               # pytest tests
```

---

## Writing a good Issue

A good spec answers three questions:

- **What** should the system be able to do?
- **Why** is this useful?
- **How do you know it's working?** (what does success look like?)

**Example:**

> **Title:** Movie night scene
>
> **What:** When I tap "Movie Night" on the dashboard or tell Claude "movie night",
> the living room lights should dim to 20% and the AC should set to 72°F.
>
> **Why:** I don't want to adjust four different things every time we watch something.
>
> **Success:** Both happen within 3 seconds. Dashboard reflects the new state.
> Claude confirms in chat.

---

## Getting started with Codespaces

1. Go to the repo on GitHub
2. Click the green **Code** button → **Codespaces** → **Create codespace on main**
3. Wait for it to load — you'll get VS Code in your browser
4. In the terminal:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # fill in any credentials you have in .env
   python main.py
   ```
5. Click the **Ports** tab → open port 5000 in your browser

---

## Running tests

```bash
pytest
```

## Code style

flake8, 120 character line limit. CI catches issues before review.

```bash
flake8 .
```

---

## Questions?

Open an Issue or ask Claude Code — it has full context on the project architecture and can walk you through implementing anything.
