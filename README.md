# DAARION Edge Backend

Minimal beta backend for DAARION Edge Client health/profile discovery.

This service exists to unblock the MicroDAO Connect Device beta gate by
providing a real backend base URL that can answer:

```text
GET /api/v1/edge/health
```

It is intentionally narrow. It does not register devices, write user data,
dispatch worker jobs, route through DAARWIZZ, or depend on Supabase.

## Status

```text
MVP health/profile target only
```

The health endpoint is public, read-only, and unauthenticated by design. It is
safe to use as the target for a future `device_backend_profiles.backend_url`
only after it is deployed and verified on the production host.

FastAPI interactive docs and OpenAPI JSON are disabled for this health-only
service so the public deployment exposes only the intended read-only endpoints.

## Local Run

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[test]"
uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Smoke:

```bash
curl -fsS http://127.0.0.1:8010/api/v1/edge/health
curl -fsS http://127.0.0.1:8010/healthz
curl -fsS http://127.0.0.1:8010/readyz
```

## Tests

```bash
pytest
```

## Docker

Build:

```bash
docker build -t daarion-edge-backend:local .
```

Run:

```bash
docker run --rm -p 8010:8010 daarion-edge-backend:local
```

Smoke:

```bash
curl -fsS http://127.0.0.1:8010/api/v1/edge/health
```

## Production Host Candidate

Recommended production base URL:

```text
https://api.daarion.city
```

Expected reverse proxy behavior:

```text
https://api.daarion.city/api/v1/edge/health
-> http://127.0.0.1:<service-port>/api/v1/edge/health
```

The endpoint must return HTTP `200` before any `loval-echoes`
`device_backend_profiles` row is inserted.

## Next Step After Deploy

1. Deploy this service behind `https://api.daarion.city`.
2. Verify:

```bash
curl -fsS https://api.daarion.city/api/v1/edge/health
```

3. Insert exactly one active production `device_backend_profiles` row in
   `loval-echoes` through an approved admin/Supabase path.
4. Run Connect Device smoke from `1.daarion.city`.

## Non-Goals

- No worker mode.
- No DAARWIZZ routing.
- No node federation.
- No production DB writes.
- No Supabase Edge Functions.
- No identity bridge.
- No device registration.
- No fake pairing success.
