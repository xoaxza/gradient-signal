# Gradient Signal

Gradient Signal is an AI-engineer-focused newsletter and launch website built around one editorial promise: cover only the AI changes that materially affect builders. The MVP site ships a strong landing page, an anti-hype methodology page, a curated latest brief, a small JSON API, and a demo-grade waitlist flow.

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

Waitlist submissions are written to `data/waitlist.jsonl` by default. For isolated local testing, override the path with `GRADIENT_SIGNAL_WAITLIST_PATH=/tmp/gradient-signal-waitlist.jsonl`.

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
- `POST /api/waitlist`
- `GET /llms.txt`
- `GET /openapi.json`

### Demo form flow

- `POST /waitlist`

## Render deployment

The repo includes `runtime.txt` for Python 3.12 and `render.yaml` with a simple web-service configuration using:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The waitlist is intentionally file-backed and demo-grade. A Render deployment should treat that storage as ephemeral unless replaced with durable backing services.
