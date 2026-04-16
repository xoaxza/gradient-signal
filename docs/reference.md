# Gradient Signal Reference

Gradient Signal is a small FastAPI application that serves a launch website for an AI-engineer-focused newsletter. The initial release is intentionally simple: server-rendered Jinja pages, static curated content, a JSON brief endpoint, a launch-safe direct-email CTA, and an optional demo-only file-backed waitlist.

## Local run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Configuration

- `GRADIENT_SIGNAL_CONTACT_EMAIL`
  - Direct-email CTA target.
  - Defaults to `team@scottyshelpers.org`.
- `GRADIENT_SIGNAL_ENABLE_DEMO_WAITLIST`
  - Enables the JSONL-backed waitlist for local demos.
  - Defaults to `false`.
- `GRADIENT_SIGNAL_WAITLIST_PATH`
  - Overrides the JSONL path used by the local demo waitlist.
  - Example: `/tmp/gradient-signal-waitlist.jsonl`.

## Routes

- `GET /` landing page with positioning, sample stories, and launch contact CTA
- `GET /methodology` editorial filter and sourcing approach
- `GET /brief/latest` latest curated issue
- `GET /healthz` JSON health check
- `GET /api/brief/latest` JSON payload for the latest issue
- `POST /api/waitlist` JSON intake for the optional local demo waitlist
- `POST /waitlist` HTML form intake for the optional local demo waitlist that redirects back to `/`
- `GET /llms.txt` plain-text machine-readable overview
- `GET /openapi.json` FastAPI-generated schema

## Deployment assumptions

- Python runtime: `3.12`
- ASGI server: `uvicorn`
- Static assets are served directly by FastAPI for MVP simplicity
- Public deploys should use the direct-email CTA and leave the demo waitlist disabled unless durable storage is added
- If demo waitlist storage fails, endpoints degrade gracefully instead of returning 500 responses
