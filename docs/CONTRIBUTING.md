# Contributing to House Hub

Welcome! No experience required — Claude Code is here to help at every step.

## How it works

1. **Write an Issue** describing a feature you want
2. **Implement it** in a branch (Claude Code will help)
3. **Open a PR** — CI runs automatically
4. **Brian reviews** and merges

A feature isn't done until it works in all three places: Claude can do it, the dashboard shows it, and the API supports it.

## Getting started with Codespaces

1. Go to the repo on GitHub
2. Click the green **Code** button → **Codespaces** → **Create codespace on main**
3. Wait for it to load — you'll get a full VS Code environment in your browser
4. Open the terminal and run:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```
5. Click the **Ports** tab to open the app in your browser

## Writing a good Issue

A good spec answers:
- **What** should the system be able to do?
- **Why** is this useful?
- **How do you know it's working?** (what does success look like?)

Example:
> **Title:** Movie night scene
>
> When I tell Claude "movie night" or tap it on the dashboard, the living room lights should dim to 20% and the AC should set to 72°F.
>
> Success: Both happen within 3 seconds, dashboard reflects the new state.

## Running tests

```bash
pytest
```

## Code style

We use flake8 with a 120 character line limit. CI will catch any issues.
