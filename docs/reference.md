# Gradient Signal Reference

Gradient Signal is a small FastAPI application that serves a launch website for an AI-engineer-focused newsletter. The initial release is intentionally simple: server-rendered Jinja pages, static curated content, a JSON brief endpoint, and a demo-grade file-backed waitlist.

## Local run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The app defaults to writing waitlist submissions to `data/waitlist.jsonl`. Override that path in local testing with `GRADIENT_SIGNAL_WAITLIST_PATH=/tmp/gradient-signal-waitlist.jsonl`.

## Routes

- `GET /` landing page with positioning, sample stories, and waitlist CTA
- `GET /methodology` editorial filter and sourcing approach
- `GET /brief/latest` latest curated issue
- `GET /healthz` JSON health check
- `GET /api/brief/latest` JSON payload for the latest issue
- `POST /api/waitlist` JSON waitlist intake for MVP demos
- `POST /waitlist` HTML form intake that redirects back to `/`
- `GET /llms.txt` plain-text machine-readable overview
- `GET /openapi.json` FastAPI-generated schema

## Deployment assumptions

- Python runtime: `3.12`
- ASGI server: `uvicorn`
- Static assets are served directly by FastAPI for MVP simplicity
- Waitlist storage is file-backed and demo-grade only; Render deployments should treat it as ephemeral unless replaced with durable storage
