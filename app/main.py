from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, ValidationError

from app.content import BRAND, POSITIONING, get_latest_brief, get_site_context

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

app = FastAPI(
    title=BRAND,
    description=POSITIONING,
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class HealthResponse(BaseModel):
    status: str
    brand: str


class SourceLink(BaseModel):
    label: str
    url: str


class BriefItem(BaseModel):
    slug: str
    headline: str
    announced_on: str
    category: str
    summary: str
    why_it_matters: str
    sources: list[SourceLink]


class BriefResponse(BaseModel):
    brand: str
    positioning: str
    slug: str
    title: str
    published_on: str
    summary: str
    editor_note: str
    items: list[BriefItem]
    what_we_ignore: list[str]
    cta: dict[str, str]


class WaitlistSubmission(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str = Field(
        min_length=5,
        max_length=320,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    company: str | None = Field(default=None, max_length=120)
    note: str | None = Field(default=None, max_length=600)


class WaitlistReceipt(BaseModel):
    status: str
    brand: str
    storage_mode: str
    message: str


@dataclass(frozen=True)
class WaitlistPersistenceResult:
    persisted: bool
    storage_mode: str
    message: str


def build_brief_payload() -> dict:
    brief = get_latest_brief()
    brief["cta"] = {
        **brief["cta"],
        "contact_email": contact_email(),
        "contact_href": contact_href(),
    }
    if not demo_waitlist_enabled():
        brief["cta"].pop("demo_note", None)
    return {
        "brand": BRAND,
        "positioning": POSITIONING,
        **brief,
    }


def parse_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def demo_waitlist_enabled() -> bool:
    return parse_bool_env("GRADIENT_SIGNAL_ENABLE_DEMO_WAITLIST", default=False)


def contact_email() -> str:
    email = os.getenv("GRADIENT_SIGNAL_CONTACT_EMAIL", "team@scottyshelpers.org").strip()
    return email or "team@scottyshelpers.org"


def contact_href() -> str:
    subject = quote("Gradient Signal: send me the next brief")
    body = quote("Name:\nRole:\nWhat I'm tracking:\n")
    return f"mailto:{contact_email()}?subject={subject}&body={body}"


def build_site_context() -> dict:
    context = get_site_context()
    context.update(
        {
            "contact_email": contact_email(),
            "contact_href": contact_href(),
            "demo_waitlist_enabled": demo_waitlist_enabled(),
        }
    )
    return context


def waitlist_path() -> Path:
    override = os.getenv("GRADIENT_SIGNAL_WAITLIST_PATH")
    if override:
        return Path(override)
    return PROJECT_DIR / "data" / "waitlist.jsonl"


def persist_waitlist_submission(
    submission: WaitlistSubmission, source: str
) -> WaitlistPersistenceResult:
    if not demo_waitlist_enabled():
        return WaitlistPersistenceResult(
            persisted=False,
            storage_mode="launch-email-only",
            message=(
                f"Waitlist capture is disabled on this deployment. Email {contact_email()} directly instead."
            ),
        )

    destination = waitlist_path()
    record = {
        "submitted_at": datetime.now(UTC).isoformat(),
        "source": source,
        **submission.model_dump(),
    }

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
    except OSError:
        return WaitlistPersistenceResult(
            persisted=False,
            storage_mode="demo-file-backed-jsonl-unavailable",
            message=(
                f"Local demo waitlist storage is unavailable. Email {contact_email()} directly instead."
            ),
        )

    return WaitlistPersistenceResult(
        persisted=True,
        storage_mode="demo-file-backed-jsonl",
        message="Stored locally for MVP demos only.",
    )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "site": build_site_context(),
        "brief": get_latest_brief(),
        "submitted": request.query_params.get("submitted"),
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/methodology", response_class=HTMLResponse)
async def methodology(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "site": build_site_context(),
        "brief": get_latest_brief(),
    }
    return templates.TemplateResponse(request=request, name="methodology.html", context=context)


@app.get("/brief/latest", response_class=HTMLResponse)
async def brief_latest(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "site": build_site_context(),
        "brief": get_latest_brief(),
    }
    return templates.TemplateResponse(request=request, name="brief_latest.html", context=context)


@app.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    return HealthResponse(status="ok", brand=BRAND)


@app.get("/api/brief/latest", response_model=BriefResponse)
async def api_brief_latest() -> BriefResponse:
    return BriefResponse.model_validate(build_brief_payload())


@app.post(
    "/api/waitlist",
    response_model=WaitlistReceipt,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Launch email-only mode is active on this deployment."},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Demo waitlist storage is temporarily unavailable."},
    },
)
async def api_waitlist(submission: WaitlistSubmission) -> JSONResponse:
    result = persist_waitlist_submission(submission, source="api")
    receipt_status = "accepted" if result.persisted else "disabled"
    response_status = status.HTTP_202_ACCEPTED if result.persisted else status.HTTP_409_CONFLICT
    if not result.persisted and result.storage_mode != "launch-email-only":
        receipt_status = "degraded"
        response_status = status.HTTP_503_SERVICE_UNAVAILABLE

    payload = WaitlistReceipt(
        status=receipt_status,
        brand=BRAND,
        storage_mode=result.storage_mode,
        message=result.message,
    )
    return JSONResponse(status_code=response_status, content=payload.model_dump())


@app.post("/waitlist", status_code=status.HTTP_303_SEE_OTHER)
async def waitlist(
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(default=""),
    note: str = Form(default=""),
) -> RedirectResponse:
    try:
        submission = WaitlistSubmission(
            name=name.strip(),
            email=email.strip(),
            company=company.strip() or None,
            note=note.strip() or None,
        )
    except ValidationError:
        return RedirectResponse(url="/?submitted=error", status_code=status.HTTP_303_SEE_OTHER)

    result = persist_waitlist_submission(submission, source="form")
    redirect_state = "success" if result.persisted else "disabled"
    if not result.persisted and result.storage_mode != "launch-email-only":
        redirect_state = "fallback"

    return RedirectResponse(
        url=f"/?submitted={redirect_state}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.get("/llms.txt", response_class=PlainTextResponse)
async def llms_txt(request: Request) -> PlainTextResponse:
    content = templates.env.get_template("llms.txt.j2").render(
        site=build_site_context(),
        brief=build_brief_payload(),
        request=request,
    )
    return PlainTextResponse(content.strip() + "\n")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
