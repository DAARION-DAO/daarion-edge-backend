# DAARION Edge Backend Health Contract

Status: beta MVP contract

Canonical endpoint:

```text
GET /api/v1/edge/health
```

This endpoint is public, read-only, unauthenticated, and cache-resistant. It is
the first deploy target required before `loval-echoes` can safely insert an
active `device_backend_profiles` row for Connect Device beta.

## Response

Example:

```json
{
  "schema_version": 1,
  "ok": true,
  "service": "daarion-edge-backend",
  "version": "0.1.0-beta",
  "backend_version": "0.1.0-beta",
  "environment": "production",
  "status": "ok",
  "readiness_status": "ready",
  "edge_protocol_version": "1.0.0",
  "min_edge_client_version": "0.2.2-3",
  "server_time": "2026-07-03T00:00:00Z",
  "capabilities": {
    "pairing": true,
    "readiness_callback": false,
    "worker_dispatch": false,
    "daarwizz_routing": false,
    "genesis": false,
    "registry": false,
    "model_registry": false,
    "voice_ceremony": false,
    "worker_relay": false
  }
}
```

## Compatibility Note

Current `daarion-edge-client` source expects `status` to be one of:

- `ok`
- `degraded`
- `maintenance`

The prompt-level MVP wording used `status: "ready"`, but that value would be
rejected by the current Edge Client health parser. This backend therefore uses
`status: "ok"` for client compatibility and exposes `readiness_status: "ready"`
as additive metadata.

## Additional Endpoints

```text
GET /healthz
GET /readyz
```

These endpoints are intended for process and reverse-proxy checks. They do not
replace the canonical Edge Client endpoint.

FastAPI interactive docs and OpenAPI JSON are disabled for this health-only
public service. Public deployments should return `404` for `/docs`, `/redoc`,
and `/openapi.json`.

## Production Reverse Proxy

Candidate production base URL:

```text
https://api.daarion.city
```

Expected route:

```text
https://api.daarion.city/api/v1/edge/health
-> http://127.0.0.1:<service-port>/api/v1/edge/health
```

## Non-Goals

- No worker mode.
- No DAARWIZZ routing.
- No node federation.
- No Supabase Edge Functions.
- No production database writes.
- No identity bridge.
- No device registration.
- No readiness callback until a separate signed trust contract exists.
