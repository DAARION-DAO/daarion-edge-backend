from datetime import datetime, timezone
import os
from typing import Literal

from fastapi import FastAPI, Response
from pydantic import BaseModel, Field


SERVICE_NAME = "daarion-edge-backend"
DEFAULT_BACKEND_VERSION = "0.1.0-beta"
DEFAULT_ENVIRONMENT = "production"
DEFAULT_EDGE_PROTOCOL_VERSION = "1.0.0"
DEFAULT_MIN_EDGE_CLIENT_VERSION = "0.2.2-3"

HealthStatus = Literal["ok", "degraded", "maintenance"]
Environment = Literal["production", "staging", "development"]


class HealthCapabilities(BaseModel):
    pairing: bool = True
    readiness_callback: bool = False
    worker_dispatch: bool = False
    daarwizz_routing: bool = False
    genesis: bool = False
    registry: bool = False
    model_registry: bool = False
    voice_ceremony: bool = False
    worker_relay: bool = False


class EdgeHealthResponse(BaseModel):
    schema_version: int = 1
    ok: bool = True
    service: str = SERVICE_NAME
    version: str
    backend_version: str
    environment: Environment
    status: HealthStatus
    readiness_status: Literal["ready", "degraded", "maintenance"]
    edge_protocol_version: str
    min_edge_client_version: str
    server_time: str
    capabilities: HealthCapabilities = Field(default_factory=HealthCapabilities)


class SimpleHealthResponse(BaseModel):
    ok: bool
    service: str
    status: HealthStatus
    version: str


def _environment() -> Environment:
    value = os.getenv("EDGE_BACKEND_ENVIRONMENT", DEFAULT_ENVIRONMENT).strip().lower()
    if value in {"production", "staging", "development"}:
        return value  # type: ignore[return-value]
    return DEFAULT_ENVIRONMENT


def _status() -> HealthStatus:
    value = os.getenv("EDGE_BACKEND_STATUS", "ok").strip().lower()
    if value in {"ok", "degraded", "maintenance"}:
        return value  # type: ignore[return-value]
    return "ok"


def _version() -> str:
    return os.getenv("EDGE_BACKEND_VERSION", DEFAULT_BACKEND_VERSION).strip() or DEFAULT_BACKEND_VERSION


def _edge_protocol_version() -> str:
    value = os.getenv("EDGE_PROTOCOL_VERSION", DEFAULT_EDGE_PROTOCOL_VERSION).strip()
    return value or DEFAULT_EDGE_PROTOCOL_VERSION


def _min_edge_client_version() -> str:
    value = os.getenv("MIN_EDGE_CLIENT_VERSION", DEFAULT_MIN_EDGE_CLIENT_VERSION).strip()
    return value or DEFAULT_MIN_EDGE_CLIENT_VERSION


def _server_time() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _readiness_status(status: HealthStatus) -> Literal["ready", "degraded", "maintenance"]:
    if status == "ok":
        return "ready"
    return status


def build_edge_health_response() -> EdgeHealthResponse:
    status = _status()
    version = _version()
    return EdgeHealthResponse(
        version=version,
        backend_version=version,
        environment=_environment(),
        status=status,
        readiness_status=_readiness_status(status),
        edge_protocol_version=_edge_protocol_version(),
        min_edge_client_version=_min_edge_client_version(),
        server_time=_server_time(),
    )


app = FastAPI(
    title="DAARION Edge Backend",
    version=DEFAULT_BACKEND_VERSION,
    description="Minimal DAARION Edge health backend for Connect Device beta.",
)


@app.get("/api/v1/edge/health", response_model=EdgeHealthResponse)
def edge_health(response: Response) -> EdgeHealthResponse:
    response.headers["Cache-Control"] = "no-store"
    return build_edge_health_response()


@app.get("/healthz", response_model=SimpleHealthResponse)
def healthz(response: Response) -> SimpleHealthResponse:
    response.headers["Cache-Control"] = "no-store"
    health = build_edge_health_response()
    return SimpleHealthResponse(
        ok=health.ok,
        service=health.service,
        status=health.status,
        version=health.version,
    )


@app.get("/readyz", response_model=SimpleHealthResponse)
def readyz(response: Response) -> SimpleHealthResponse:
    response.headers["Cache-Control"] = "no-store"
    health = build_edge_health_response()
    return SimpleHealthResponse(
        ok=health.ok,
        service=health.service,
        status=health.status,
        version=health.version,
    )
