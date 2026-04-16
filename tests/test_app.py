import json

from fastapi.testclient import TestClient

from app.main import app


def test_page_routes_render() -> None:
    client = TestClient(app)

    expectations = {
        "/": ["Gradient Signal", "Ignore the hype", "Join the waitlist"],
        "/methodology": ["The filter is the product", "Primary-source-first", "What we ignore"],
        "/brief/latest": ["Latest Brief", "Why it matters:", "GitHub Copilot gets US/EU data residency"],
    }

    for path, fragments in expectations.items():
        response = client.get(path)
        assert response.status_code == 200
        for fragment in fragments:
            assert fragment in response.text


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
    assert "demo_note" in payload["cta"]

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


def test_api_waitlist_persists_demo_submission(monkeypatch, tmp_path) -> None:
    storage_path = tmp_path / "waitlist.jsonl"
    monkeypatch.setenv("GRADIENT_SIGNAL_WAITLIST_PATH", str(storage_path))
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
    assert response.json()["storage_mode"] == "demo-file-backed-jsonl"

    lines = storage_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["source"] == "api"
    assert record["email"] == "ada@example.com"


def test_waitlist_form_redirects_and_persists(monkeypatch, tmp_path) -> None:
    storage_path = tmp_path / "waitlist.jsonl"
    monkeypatch.setenv("GRADIENT_SIGNAL_WAITLIST_PATH", str(storage_path))
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
