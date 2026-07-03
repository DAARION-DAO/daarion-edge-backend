from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_edge_health_contract() -> None:
    response = client.get("/api/v1/edge/health")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"

    payload = response.json()
    assert payload["schema_version"] == 1
    assert payload["ok"] is True
    assert payload["service"] == "daarion-edge-backend"
    assert payload["version"] == "0.1.0-beta"
    assert payload["backend_version"] == "0.1.0-beta"
    assert payload["environment"] == "production"
    assert payload["status"] == "ok"
    assert payload["readiness_status"] == "ready"
    assert payload["edge_protocol_version"] == "1.0.0"
    assert payload["min_edge_client_version"] == "0.2.2-3"
    assert payload["server_time"].endswith("Z")

    capabilities = payload["capabilities"]
    assert capabilities["pairing"] is True
    assert capabilities["readiness_callback"] is False
    assert capabilities["worker_dispatch"] is False
    assert capabilities["daarwizz_routing"] is False
    assert capabilities["worker_relay"] is False


def test_healthz() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == {
        "ok": True,
        "service": "daarion-edge-backend",
        "status": "ok",
        "version": "0.1.0-beta",
    }


def test_readyz() -> None:
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["ok"] is True


def test_invalid_env_values_fall_back(monkeypatch) -> None:
    monkeypatch.setenv("EDGE_BACKEND_ENVIRONMENT", "invalid")
    monkeypatch.setenv("EDGE_BACKEND_STATUS", "ready")

    response = client.get("/api/v1/edge/health")
    payload = response.json()

    assert payload["environment"] == "production"
    assert payload["status"] == "ok"


def test_public_docs_are_not_exposed() -> None:
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404
