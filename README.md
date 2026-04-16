# Gradient Signal

Gradient Signal is an AI-engineer-focused newsletter and launch website built around one editorial promise: cover only the AI changes that materially affect builders. The MVP site ships a strong landing page, an anti-hype methodology page, a curated latest brief, a small JSON API, and a launch-safe email CTA. An optional file-backed waitlist remains available for local demos only.

## Business summary

- Brand: Gradient Signal
- Positioning: "What changed in AI, and what it changes for builders."
- Audience: AI engineers, applied researchers, ML platform teams, and technical founders
- Editorial rule: filter for changes in capability, cost, latency, reliability, evals, security, licensing/access, or deployment/compliance

## Local run

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Configuration

- `GRADIENT_SIGNAL_CONTACT_EMAIL`
  - Direct-email CTA target.
  - Defaults to `team@scottyshelpers.org`.
- `GRADIENT_SIGNAL_ENABLE_DEMO_WAITLIST`
  - Enables the JSONL-backed waitlist form and POST handling for local demos.
  - Defaults to `false` so public deploys do not rely on ephemeral disk.
- `GRADIENT_SIGNAL_WAITLIST_PATH`
  - Optional override for local demo storage.
  - Only used when `GRADIENT_SIGNAL_ENABLE_DEMO_WAITLIST=true`.
  - Example: `/tmp/gradient-signal-waitlist.jsonl`.

## Test command

```bash
pytest -q
```

## Routes

### Human pages

- `GET /`
- `GET /methodology`
- `GET /brief/latest`

### Machine endpoints

- `GET /healthz`
- `GET /api/brief/latest`
- `POST /api/waitlist` (optional local demo flow, disabled by default)
- `GET /llms.txt`
- `GET /openapi.json`

### Demo form flow

- `POST /waitlist` (optional local demo flow, disabled by default)

## Render deployment

The repo includes `runtime.txt` for Python 3.12 and `render.yaml` with a simple web-service configuration using:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The launch configuration defaults to direct email intake and keeps the demo waitlist disabled so the public CTA does not depend on Render's ephemeral filesystem.
