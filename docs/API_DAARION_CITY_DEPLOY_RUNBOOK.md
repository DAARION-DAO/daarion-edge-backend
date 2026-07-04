# api.daarion.city Deploy Runbook

Status: operator runbook, no production database writes. Public ingress is not
approved until the stack audit is reviewed.

This runbook deploys the merged `main` branch of `DAARION-DAO/daarion-edge-backend`
as the local-first runtime target for the MicroDAO Connect Device beta gate.
Public exposure requires a separate ingress/TLS/DNS decision after local smoke.

Preferred production host:

```text
NODA3
```

Fallback host:

```text
NODA4, only if NODA3 is not reachable or unsuitable
```

Excluded host:

```text
NODA1, currently unavailable for this deploy
```

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

Read before any public ingress work:

```text
docs/architecture/DAARION_PLATFORM_MULTINODE_ARCHITECTURE_2026-07.md
docs/operations/NODA3_NODA4_OCTELIUM_STACK_AUDIT_2026-07-03.md
```

## Non-Goals

- No worker mode.
- No DAARWIZZ routing.
- No node federation.
- No Supabase dependency.
- No Supabase Edge Functions.
- No production database writes.
- No Edge Client installer changes.

## Preflight

Run on NODA3 first. Do not continue to NODA4 unless NODA3 fails these checks or
the operator explicitly rejects NODA3 for this role.

```bash
whoami
hostname
uptime
docker --version
docker compose version
sudo -n true
sudo ss -ltnp | grep -E ':80 |:443 |:9413 ' || true
command -v nginx || true
command -v caddy || true
command -v traefik || true
command -v certbot || true
df -h /
```

Confirm the hostname currently resolves to the selected host:

```bash
dig +short api.daarion.city A
```

The current DNS target and the selected host address are operator-verified
values. Re-check them in the DNS provider and on the selected host before any
public ingress work. Do not treat the local Docker deploy as approval to change
DNS.

```text
api.daarion.city A -> <current-dns-target>
NODA3 public IPv4 -> <operator-verified-noda3-ip>
```

If NODA3 remains the selected host in a later public-ingress task, update the
DNS `A` record for `api.daarion.city` to the operator-verified NODA3 public IPv4
and remove the previous target only after ingress, TLS, firewall, and rollback
are approved.

Do not reuse port `80` blindly. The NODA3 audit observed `httpd` listening on
port `80`; preserve existing services and add only an approved virtual host or
reverse-proxy route for `api.daarion.city`.

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

The stack audit found no approved general-purpose public ingress for this API.

Do not assume Apache/httpd is the correct path. On NODA3, `httpd` is owned by
the Nextcloud snap service.

Do not reuse the Ring FileBase Caddy container for this API without a separate
Ring FileBase ingress decision. That Caddy instance is scoped to file gateway
traffic on non-standard host ports.

Do not use MicroK8s/k3s ingress for this beta health endpoint while the cluster
has degraded workloads and no listed ingress resources.

Do not use Octelium for public `api.daarion.city` until Octelium authentication
and service routing are repaired and explicitly designed.

Approved next public-ingress choices must come from an operator decision after
local Docker smoke. Candidate directions are:

- external HTTPS tunnel/CDN/load balancer to `127.0.0.1:9413`;
- a new dedicated host-level reverse proxy with approved TLS and firewall;
- a reviewed integration with an existing ingress only if its service owner
  confirms it is the correct layer.

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

If a later public-ingress task added a route, remove only that route and reload
the approved proxy using that proxy's own validation/reload command. For the
local-only Docker deploy, there is no proxy rollback step.

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
