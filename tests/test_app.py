import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def enable_demo_waitlist(monkeypatch, storage_path: Path) -> None:
    monkeypatch.setenv("GRADIENT_SIGNAL_ENABLE_DEMO_WAITLIST", "true")
    monkeypatch.setenv("GRADIENT_SIGNAL_WAITLIST_PATH", str(storage_path))


def test_page_routes_render() -> None:
    client = TestClient(app)

    expectations = {
        "/": ["Gradient Signal", "Ignore the hype", "Email the team"],
        "/methodology": ["The filter is the product", "Primary-source-first", "What we ignore"],
        "/brief/latest": ["Latest Brief", "Why it matters:", "Launch contact"],
    }

    for path, fragments in expectations.items():
        response = client.get(path)
        assert response.status_code == 200
        for fragment in fragments:
            assert fragment in response.text


def test_homepage_uses_launch_safe_email_cta_by_default() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert "mailto:team@scottyshelpers.org" in response.text
    assert 'action="/waitlist"' not in response.text



def test_healthz_contract() -> None:
    client = TestClient(app)

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "brand": "Gradient Signal"}



def test_latest_brief_api_shape_and_content() -> None:
    client = TestClient(app)

    response = client.get("/api/brief/latest")
    payload = response.json()

    assert response.status_code == 200
    assert payload["brand"] == "Gradient Signal"
    assert payload["slug"] == "2026-04-16-launch-brief"
    assert payload["published_on"] == "2026-04-16"
    assert len(payload["items"]) == 6
    assert "Ignore the hype" not in payload["summary"]
    assert "launch_note" in payload["cta"]
    assert "demo_note" not in payload["cta"]
    assert payload["cta"]["contact_email"] == "team@scottyshelpers.org"

    required_item_keys = {
        "slug",
        "headline",
        "announced_on",
        "category",
        "summary",
        "why_it_matters",
        "sources",
    }
    first_item = payload["items"][0]
    assert required_item_keys.issubset(first_item.keys())
    assert first_item["headline"] == "OpenAI adds native sandbox execution to the Agents SDK"
    assert first_item["sources"][0]["url"] == "https://openai.com/index/the-next-evolution-of-the-agents-sdk/"
    assert any("Viral demos" in item for item in payload["what_we_ignore"])
    assert payload["items"][1]["announced_on"] == "2026-04-09"



def test_llms_txt_contains_brand_and_route_references() -> None:
    client = TestClient(app)

    response = client.get("/llms.txt")
    text = response.text

    assert response.status_code == 200
    assert "Gradient Signal" in text
    assert "Ignore the hype / What we ignore" in text
    assert "/brief/latest" in text
    assert "/api/brief/latest" in text
    assert "/openapi.json" in text
    assert "team@scottyshelpers.org" in text
    assert "Demo note:" not in text


def test_openapi_includes_waitlist_failure_response() -> None:
    client = TestClient(app)

    response = client.get("/openapi.json")
    payload = response.json()

    assert response.status_code == 200
    post_responses = payload["paths"]["/api/waitlist"]["post"]["responses"]
    assert "202" in post_responses
    assert "409" in post_responses
    assert "503" in post_responses
    assert post_responses["409"]["description"] == "Launch email-only mode is active on this deployment."
    assert post_responses["503"]["description"] == "Demo waitlist storage is temporarily unavailable."


def test_api_waitlist_returns_launch_safe_response_by_default() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/waitlist",
        json={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "company": "Analytical Engines",
            "note": "Tracking model routing and compliance changes.",
        },
    )

    assert response.status_code == 409
    assert response.json()["status"] == "disabled"
    assert response.json()["storage_mode"] == "launch-email-only"
    assert "team@scottyshelpers.org" in response.json()["message"]



def test_api_waitlist_persists_demo_submission(monkeypatch, tmp_path) -> None:
    storage_path = tmp_path / "waitlist.jsonl"
    enable_demo_waitlist(monkeypatch, storage_path)
    client = TestClient(app)

    response = client.post(
        "/api/waitlist",
        json={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "company": "Analytical Engines",
            "note": "Tracking model routing and compliance changes.",
        },
    )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
    assert response.json()["storage_mode"] == "demo-file-backed-jsonl"

    lines = storage_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["source"] == "api"
    assert record["email"] == "ada@example.com"



def test_waitlist_form_redirects_and_persists(monkeypatch, tmp_path) -> None:
    storage_path = tmp_path / "waitlist.jsonl"
    enable_demo_waitlist(monkeypatch, storage_path)
    client = TestClient(app)

    response = client.post(
        "/waitlist",
        data={
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "company": "Compiler Corps",
            "note": "Watching agent runtimes.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/?submitted=success"

    lines = storage_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["source"] == "form"
    assert record["name"] == "Grace Hopper"



def test_api_waitlist_persistence_failure_returns_degraded_receipt(monkeypatch, tmp_path) -> None:
    storage_path = tmp_path / "waitlist.jsonl"
    enable_demo_waitlist(monkeypatch, storage_path)

    def broken_open(self, *args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(Path, "open", broken_open)
    client = TestClient(app)

    response = client.post(
        "/api/waitlist",
        json={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "company": "Analytical Engines",
            "note": "Tracking model routing and compliance changes.",
        },
    )

    assert response.status_code == 503
    assert response.json()["status"] == "degraded"
    assert response.json()["storage_mode"] == "demo-file-backed-jsonl-unavailable"
    assert "team@scottyshelpers.org" in response.json()["message"]



def test_waitlist_form_falls_back_to_email_when_storage_fails(monkeypatch, tmp_path) -> None:
    storage_path = tmp_path / "waitlist.jsonl"
    enable_demo_waitlist(monkeypatch, storage_path)

    def broken_open(self, *args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(Path, "open", broken_open)
    client = TestClient(app)

    response = client.post(
        "/waitlist",
        data={
            "name": "Grace Hopper",
            "email": "grace@example.com",
            "company": "Compiler Corps",
            "note": "Watching agent runtimes.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/?submitted=fallback"
