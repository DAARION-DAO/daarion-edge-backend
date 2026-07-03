# api.daarion.city Deploy Runbook

Status: operator runbook, no production database writes.

This runbook deploys the merged `main` branch of `DAARION-DAO/daarion-edge-backend`
as the public beta health target for MicroDAO Connect Device.

Canonical public endpoint:

```text
GET https://api.daarion.city/api/v1/edge/health
```

Expected production facts:

```text
service=daarion-edge-backend
version=0.1.0-beta
environment=production
status=ok
readiness_status=ready
min_edge_client_version=0.2.2-3
```

Do not insert a `device_backend_profiles` row until the public smoke checks in
this runbook return HTTP `200` with the expected JSON.

## Non-Goals

- No worker mode.
- No DAARWIZZ routing.
- No node federation.
- No Supabase dependency.
- No Supabase Edge Functions.
- No production database writes.
- No Edge Client installer changes.

## Preflight

Run on the selected production host:

```bash
whoami
hostname
docker --version
docker compose version
sudo -n true
```

Confirm the hostname currently resolves to the selected host:

```bash
dig +short api.daarion.city A
```

As of the deployment prep audit, `api.daarion.city` resolves to:

```text
144.76.224.179
```

If the selected host is different, update DNS first and wait for propagation.

## Deploy With Docker Compose

Use a dedicated service directory:

```bash
sudo mkdir -p /opt/daarion-edge-backend
sudo chown "$USER":"$USER" /opt/daarion-edge-backend
cd /opt/daarion-edge-backend
```

Clone or refresh the repository:

```bash
if [ ! -d .git ]; then
  git clone https://github.com/DAARION-DAO/daarion-edge-backend.git .
else
  git fetch origin
fi
git checkout main
git pull --ff-only origin main
```

Create `docker-compose.yml`:

```yaml
services:
  daarion-edge-backend:
    build: .
    container_name: daarion-edge-backend
    restart: unless-stopped
    environment:
      EDGE_BACKEND_ENVIRONMENT: production
      EDGE_BACKEND_VERSION: 0.1.0-beta
      EDGE_BACKEND_STATUS: ok
      EDGE_PROTOCOL_VERSION: 1.0.0
      MIN_EDGE_CLIENT_VERSION: 0.2.2-3
    ports:
      - "127.0.0.1:9413:8010"
```

Check that host port `9413` is free before starting:

```bash
sudo ss -ltnp | grep ':9413' || true
```

Build and start:

```bash
docker compose config
docker compose up -d --build
docker compose ps
```

Local host smoke:

```bash
curl -i http://127.0.0.1:9413/api/v1/edge/health
curl -i http://127.0.0.1:9413/healthz
curl -i http://127.0.0.1:9413/readyz
curl -i http://127.0.0.1:9413/docs
curl -i http://127.0.0.1:9413/openapi.json
```

Expected:

- `/api/v1/edge/health`: HTTP `200`
- `/healthz`: HTTP `200`
- `/readyz`: HTTP `200`
- `/docs`: HTTP `404`
- `/openapi.json`: HTTP `404`

## Reverse Proxy

If the host uses Nginx, add a narrowly scoped `api.daarion.city` server block or
merge these locations into the existing `api.daarion.city` HTTPS server block.

Proxy only the health endpoints required for this beta gate:

```nginx
location = /api/v1/edge/health {
    proxy_pass http://127.0.0.1:9413/api/v1/edge/health;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy no-referrer always;
}

location = /healthz {
    proxy_pass http://127.0.0.1:9413/healthz;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy no-referrer always;
}

location = /readyz {
    proxy_pass http://127.0.0.1:9413/readyz;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy no-referrer always;
}
```

Validate and reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

If TLS is not already configured for `api.daarion.city`, configure HTTPS before
declaring the backend ready.

## Public Smoke

Run from outside the server:

```bash
curl -i https://api.daarion.city/api/v1/edge/health
curl -i https://api.daarion.city/healthz
curl -i https://api.daarion.city/readyz
curl -i https://api.daarion.city/docs
curl -i https://api.daarion.city/openapi.json
```

Required before unblocking Connect Device:

- `/api/v1/edge/health`: HTTP `200`
- `/healthz`: HTTP `200`
- `/readyz`: HTTP `200`
- `/docs`: HTTP `404`
- `/openapi.json`: HTTP `404`
- no secrets in any response body or headers
- `Cache-Control: no-store` on successful health responses

## Rollback

Stop the container:

```bash
cd /opt/daarion-edge-backend
docker compose down
```

Remove or comment out the Nginx locations, then reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Next Gate

Only after public smoke returns valid HTTP `200`:

```text
backend_url=https://api.daarion.city
```

Prepare the next `loval-echoes` task:

- insert exactly one active production `device_backend_profiles` row;
- `label`: `DAARION Edge Beta Backend`;
- `environment`: `production`;
- `backend_url`: `https://api.daarion.city`;
- `is_active`: `true`;
- then run Connect Device smoke;
- then run Edge Client installer smoke.
