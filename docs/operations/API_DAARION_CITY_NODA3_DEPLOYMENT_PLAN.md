# api.daarion.city NODA3 Deployment Plan

Status: docs-only deployment plan. Do not apply production database writes.

## Executive Decision

Deploy `daarion-edge-backend` to NODA3 first as a local Docker service only.
Do not choose public ingress until the stack audit is reviewed.

Host roles for this beta gate:

```text
NODA3 = preferred api.daarion.city host for minimal Edge Backend health
NODA4 = fallback only if NODA3 becomes unreachable or unsuitable
NODA1 = excluded from this deploy because it is unavailable/offline for this gate
```

This plan only targets:

```text
GET /api/v1/edge/health
GET /healthz
GET /readyz
```

It does not enable worker execution, DAARWIZZ routing, node federation,
Supabase integration, identity bridge, Edge Client installer changes, or
`device_backend_profiles` writes.

## Current Read-Only Evidence

NODA3 read-only checks succeeded from the operator environment:

```text
ssh target: noda3
hostname: llm80-che-1-1
user: zevs
sudo -n: available
uptime: up 4 weeks, 4 days
Docker: Docker version 29.3.1
Docker Compose: v5.1.1
root disk: 3.6T total, 1.7T free, 52% used
observed public IPv4: 212.8.58.133
```

NODA3 ingress facts from read-only checks:

```text
port 80: occupied by httpd
port 443: no confirmed listener in the targeted check
port 9413: free in the targeted check
nginx: missing
caddy: missing
traefik: missing
certbot: missing
ufw: active
ufw 80/tcp allow: not observed
ufw 443/tcp allow: not observed
```

Existing NODA3 services that must not be disturbed:

```text
ring-filebase-auth-gateway-noda3
ring-filebase-api-noda3
ring-filebase-public-gateway-noda3
ring-filebase-minio-noda3
ring-filebase-cdn-noda3
dagi-market-data-node3
noda3-ollama-reasoning-external
noda3-heartbeat-external
noda3-neo4j-graph-external
noda3-qdrant-retrieval-external
noda3-gpu-worker-external
octelium-daemon-noda3
dcgm-exporter
grafana
postgres-daarion
neo4j-daarion
qdrant-daarion
gitlab
```

Historical workspace notes also showed MicroK8s active and `k3s-agent`
problematic on NODA3. Do not install, repair, or change k3s/MicroK8s for this
health backend gate.

NODA4 was considered but is not currently reachable from the operator
environment:

```text
ssh noda4 -> Network is unreachable
```

## Current DNS Truth

Current DNS:

```text
api.daarion.city A -> 144.76.224.179
edge.daarion.city CNAME -> daarion-dao.github.io
```

Observed NODA3 public IPv4:

```text
212.8.58.133
```

Required DNS decision if NODA3 is approved:

```text
api.daarion.city A -> 212.8.58.133
```

Remove or replace the old `144.76.224.179` target. Do not use
`edge.daarion.city` for this backend while it remains a GitHub Pages hostname.

## Required Checks Before Deploy

Run on NODA3:

```bash
whoami
hostname
uptime
sudo -n true
docker --version
docker compose version
sudo ss -ltnp | grep -E ':80 |:443 |:9413 ' || true
sudo ufw status verbose
command -v nginx || true
command -v caddy || true
command -v traefik || true
command -v certbot || true
df -h /
docker ps --format '{{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Stop if:

- NODA3 is unreachable;
- Docker or Docker Compose is unavailable;
- port `9413` is occupied;
- the operator cannot identify the active ingress path for
  `api.daarion.city`;
- TLS for `api.daarion.city` cannot be provided;
- firewall rules for the selected public HTTP/HTTPS route are not explicitly
  approved;
- changing DNS would disrupt an existing production owner of
  `api.daarion.city`.

## Deploy Flow

Use Docker Compose and bind the service only to loopback:

```bash
sudo mkdir -p /opt/daarion-edge-backend
sudo chown "$USER":"$USER" /opt/daarion-edge-backend
cd /opt/daarion-edge-backend

if [ ! -d .git ]; then
  git clone https://github.com/DAARION-DAO/daarion-edge-backend.git .
else
  git fetch origin
fi

git checkout main
git pull --ff-only origin main
```

Create `/opt/daarion-edge-backend/docker-compose.yml`:

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

Start:

```bash
cd /opt/daarion-edge-backend
docker compose config
docker compose up -d --build
docker compose ps
```

Local smoke on NODA3:

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

## Reverse Proxy Decision

NODA3 currently has `httpd` listening on port `80`, active UFW without observed
`80/tcp` or `443/tcp` allow rules, and no confirmed host-level Nginx, Caddy,
Traefik, Certbot, or public `443` listener. Do not stop `httpd`, replace
firewall policy, or move existing services as part of this gate.

Stack audit correction:

- the observed `httpd` is owned by the Nextcloud snap Apache service;
- the observed Caddy process belongs to the Ring FileBase public gateway
  container and is not a general host ingress;
- Octelium is present but currently unauthenticated and not usable as the public
  route;
- MicroK8s has degraded workloads and no listed ingress resources.

Safe operator options after local smoke:

- external HTTPS tunnel/CDN/load balancer to `127.0.0.1:9413`;
- a new dedicated host-level reverse proxy with approved TLS/firewall;
- a reviewed integration with an existing ingress only if its owner confirms it
  is the correct layer.

Only after the approved ingress route exists, add the minimum firewall allow
rule required for that route, for example:

```bash
sudo ufw allow 443/tcp comment 'api.daarion.city HTTPS'
```

Do not open broad additional ports for this health backend.

## DNS And TLS

After NODA3 local smoke passes and the ingress route is ready, repoint DNS:

```text
api.daarion.city A 212.8.58.133
```

Then wait for propagation:

```bash
dig +short api.daarion.city A
```

Do not declare readiness until HTTPS works:

```bash
curl -i https://api.daarion.city/api/v1/edge/health
```

## Public Smoke

Run from outside NODA3:

```bash
curl -i https://api.daarion.city/api/v1/edge/health
curl -i https://api.daarion.city/healthz
curl -i https://api.daarion.city/readyz
curl -i https://api.daarion.city/docs
curl -i https://api.daarion.city/openapi.json
```

Expected:

- health endpoints return HTTP `200`;
- `service` is `daarion-edge-backend`;
- `version` is `0.1.0-beta`;
- `environment` is `production`;
- `status` is `ok`;
- `readiness_status` is `ready`;
- `min_edge_client_version` is `0.2.2-3`;
- `/docs` and `/openapi.json` return `404` or another non-public response;
- no secrets appear in responses or headers.

## Logs And Debug

On NODA3:

```bash
cd /opt/daarion-edge-backend
docker compose ps
docker compose logs --tail=200 daarion-edge-backend
curl -i http://127.0.0.1:9413/api/v1/edge/health
sudo ss -ltnp | grep -E ':80 |:443 |:9413 ' || true
sudo ufw status verbose
```

## Rollback

Stop the backend:

```bash
cd /opt/daarion-edge-backend
docker compose down
```

Remove only the `api.daarion.city` route that was added for this backend, then
reload the approved proxy. Do not touch existing Ring FileBase, GitLab, Qdrant,
Neo4j, Postgres, Grafana, GPU worker, or Octelium containers.

If DNS was changed, revert `api.daarion.city` only after deciding where the API
hostname should point.

## Next Gate After HTTP 200

Only after:

```text
GET https://api.daarion.city/api/v1/edge/health -> HTTP 200
```

prepare a separate `loval-echoes` task to insert one active production backend
profile:

```text
label=DAARION Edge Beta Backend
environment=production
backend_url=https://api.daarion.city
is_active=true
```

Do not insert this row in the deployment-plan task.
