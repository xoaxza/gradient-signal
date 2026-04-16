# Gradient Signal MVP Launch Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Launch a live website for Gradient Signal, an AI-engineer-focused newsletter that filters for important AI changes rather than hype, then email the live URL to team@scottyshelpers.org.

**Architecture:** Build a small FastAPI web app with server-rendered pages and a lightweight JSON API. Ship a strong landing page, an editorial methodology page, a sample latest brief built around important AI-engineering changes, health/docs/llms endpoints, and regression tests. Keep the first launch operationally simple and static-data-backed.

**Tech Stack:** Python 3.12, FastAPI, Jinja2 templates, plain CSS, pytest, Uvicorn, Render web service.

---

## Product requirements
- Brand: Gradient Signal
- Positioning: “What changed in AI, and what it changes for builders.”
- Audience: AI engineers, applied researchers, ML platform teams, and technical founders
- Editorial rule: only cover stories that materially change capability, cost, latency, reliability/evals, security/safety, licensing/access, or deployment/compliance
- Initial pages:
  - `/` landing page with hero, differentiators, sample high-signal stories, and CTA
  - `/methodology` explaining the anti-hype editorial filter and sources
  - `/brief/latest` readable latest issue page
- Initial machine-readable endpoints:
  - `/healthz`
  - `/api/brief/latest`
  - `/openapi.json`
  - `/llms.txt`
- Initial content should include a small curated set of current important AI items with source URLs and why they matter to builders
- No database requirement for v1; content can be file-backed

## Task 1: Scaffold the app
**Objective:** Create the Python app, dependency manifest, routing skeleton, template system, and static file support.

**Files:**
- Create: `app/main.py`
- Create: `app/__init__.py`
- Create: `app/content.py`
- Create: `app/templates/base.html`
- Create: `app/templates/index.html`
- Create: `app/templates/methodology.html`
- Create: `app/templates/brief_latest.html`
- Create: `app/static/styles.css`
- Create: `requirements.txt`
- Create: `runtime.txt`

**Verification:**
- Run: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Run: `uvicorn app.main:app --host 127.0.0.1 --port 8000`
- Expected: `/`, `/methodology`, and `/brief/latest` render without server errors

## Task 2: Add editorial content and product copy
**Objective:** Encode the business thesis directly in the site copy and populate the latest brief with concrete high-signal AI news items and citations.

**Files:**
- Modify: `app/content.py`
- Modify: `app/templates/index.html`
- Modify: `app/templates/methodology.html`
- Modify: `app/templates/brief_latest.html`

**Requirements:**
- Use Gradient Signal branding throughout
- Make the copy explicit about anti-hype filtering and primary-source-first reporting
- Include 4-6 brief items, each with title, impact summary, “why builders should care,” and at least one source URL
- Include a section explaining what Gradient Signal ignores

**Verification:**
- Manually inspect each rendered page locally
- Confirm all source links are present in page markup

## Task 3: Add machine-readable endpoints and docs assets
**Objective:** Support deployment verification and agent/user discoverability with API and llms docs.

**Files:**
- Modify: `app/main.py`
- Create: `app/templates/llms.txt.j2` or equivalent file-backed response logic
- Create: `docs/reference.md`

**Requirements:**
- `/healthz` returns JSON with status and brand
- `/api/brief/latest` returns the same latest brief content in JSON
- `/llms.txt` explains the site, key pages, and API endpoints in plain text/markdown-friendly form
- `docs/reference.md` explains local run, routes, and deployment assumptions

**Verification:**
- `curl -s http://127.0.0.1:8000/healthz`
- `curl -s http://127.0.0.1:8000/api/brief/latest`
- `curl -s http://127.0.0.1:8000/llms.txt`
- `curl -s http://127.0.0.1:8000/openapi.json`

## Task 4: Add regression tests
**Objective:** Meet release gates with parser/schema coverage and endpoint smoke tests.

**Files:**
- Create: `tests/test_app.py`

**Requirements:**
- Test page routes return 200
- Test `/healthz` contract
- Test `/api/brief/latest` schema shape, including item count and required keys
- Test `/llms.txt` contains the brand and key route references

**Verification:**
- Run: `pytest -q`
- Expected: all tests pass

## Task 5: Prepare launch-ready repo state
**Objective:** Make the repository easy to deploy and review.

**Files:**
- Modify: `README.md`
- Optionally create: `render.yaml` if helpful, but deployment may also be API-driven without it

**Requirements:**
- README includes business summary, local run instructions, test command, and route list
- Commit all files to git

**Verification:**
- Run: `git status --short` should be clean after commit
- Run: `pytest -q`
- Run representative curls for `/healthz`, `/api/brief/latest`, `/llms.txt`, `/openapi.json`
