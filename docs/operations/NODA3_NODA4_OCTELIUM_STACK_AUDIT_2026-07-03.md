# NODA3/NODA4/Octelium Stack Audit

Status: evidence-first audit. No deployment, DNS change, firewall change, proxy
change, Supabase write, or `device_backend_profiles` write was performed.

## Executive Verdict

Do not deploy `daarion-edge-backend` through Apache/httpd, Caddy, Nginx,
Kubernetes, or Octelium yet.

Recommended next path:

```text
Docker local service on NODA3 first -> local health smoke -> operator decision on
public ingress/TLS/DNS -> public smoke -> only then device_backend_profiles
```

Reason:

- NODA3 is reachable and suitable for a local Docker service.
- `api.daarion.city` still resolves away from the verified NODA3 target.
- NODA3 public IPv4 was operator-verified and is intentionally redacted from
  this public audit.
- The host has multiple existing services and ingress surfaces.
- `httpd` is a Nextcloud snap Apache process, not a confirmed DAARION ingress.
- Caddy exists only inside the Ring FileBase public gateway container on
  non-standard host ports, not as a general host ingress for `api.daarion.city`.
- MicroK8s is present but workloads are degraded; do not add this beta health
  service to Kubernetes now.
- Octelium is installed as a container but currently fails unauthenticated and
  is not usable as the route for a public health endpoint.

## What Was Inspected

Repository and workspace docs were searched for:

```text
NODA3, NODA4, NODA1, Octelium, k3s, Kubernetes, ingress, nginx, apache,
httpd, caddy, traefik, certbot, api.daarion.city, edge.daarion.city,
daarion-edge-backend, device_backend_profiles, /api/v1/edge/health,
Vault, ESO, Postgres, Redis, Qdrant, MinIO, NATS, Supabase mirror,
service mesh, reverse proxy, DNS
```

NODA3 was audited with read-only commands only. Sensitive config values,
environment variables, private keys, and tokens were not printed.

NODA4 was checked only for safe reachability.

## Repo/Doc Evidence

Relevant docs found:

- `docs/operations/API_DAARION_CITY_NODA3_DEPLOYMENT_PLAN.md`
- `docs/API_DAARION_CITY_DEPLOY_RUNBOOK.md`
- `docs/EDGE_BACKEND_HEALTH_CONTRACT.md`
- `loval-echoes/docs/operations/DAARION_EDGE_BACKEND_HEALTH_TRUTH_2026-07-03.md`
- `agrowise-nexus/docs/ops/noda3-agromatrix-runtime-data-mirror-plan.md`

Prior NODA3 planning already recommended Docker Compose first and warned not to
install or change k3s for the immediate gate because MicroK8s was active while
k3s-agent was problematic.

The Edge backend health truth report already established:

- `api.daarion.city` timed out for `/api/v1/edge/health`;
- `edge.daarion.city` served GitHub Pages for that path;
- no `device_backend_profiles` row should be created before a real HTTP `200`
  backend health response exists.

## NODA3 Live Evidence

Read-only NODA3 host facts:

```text
ssh target: noda3
hostname: operator-verified
user: redacted
sudo -n: available
OS: Ubuntu 24.04.4 LTS
kernel: 6.8.0-111-generic
uptime: up 4 weeks, 4 days
public IPv4: operator-verified, redacted from public docs
memory: 125Gi total
root disk: 3.6T total, 1.7T free, 52% used
```

DNS resolution from NODA3:

```text
api.daarion.city -> current target is not the verified NODA3 backend target
edge.daarion.city -> GitHub Pages addresses through daarion-dao.github.io
```

Docker:

```text
Docker version 29.3.1
Docker Compose version v5.1.1
```

Observed Docker networks and containers confirmed that NODA3 already runs
several unrelated service groups, including Ring FileBase, DAGI market data,
external worker services, Octelium, observability, databases, retrieval/graph
services, and GitLab. Exact network names, container names, and operator paths
are intentionally omitted from this public audit.

Do not disturb those services or paths during the Edge health beta gate.

## NODA4 Reachability Evidence

Safe reachability check:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 noda4 'set -e; hostname; uptime; docker --version || true'
```

Result:

```text
Network is unreachable
```

NODA4 remains fallback-only and is not currently usable for this deployment.

## Octelium Evidence

Octelium daemon container exists:

```text
image: ghcr.io/octelium/octelium:0.30.0
status: running
network: host
```

No host `octelium` binary was found in `PATH`.

Recent Octelium container logs show unauthenticated failures, with sensitive
phrases redacted during collection:

```text
rpc error: code = Unauthenticated desc = Unauthenticated User
gRPC error Unauthenticated Unauthenticated User
```

Interpretation:

- Octelium is present on NODA3, but not proven healthy or authenticated.
- There is no evidence from this audit that Octelium can currently expose
  `daarion-edge-backend`.
- Octelium may still be appropriate later for private operator or inter-node
  access, but it is not currently a viable public `api.daarion.city` route.
- Using Octelium would require a separate authentication/session repair and
  route/service design.

## Current Ingress/Proxy Evidence

Observed listeners:

```text
*:80 -> httpd from snap.nextcloud.apache.service
non-standard HTTP/HTTPS ports -> existing Ring FileBase public gateway
non-standard HTTPS port -> existing GitLab container
```

No standard host `*:443` listener was confirmed.

Host proxy binaries:

```text
nginx: missing
apache2/apachectl/httpd: missing from host PATH
caddy: missing from host PATH
traefik: missing
certbot: missing
```

Apache/httpd truth:

```text
systemd unit: snap.nextcloud.apache.service
snap nextcloud ports: http=80, https=443
```

This means the observed `httpd` is Nextcloud-owned. It is not confirmed as an
intended DAARION or `api.daarion.city` ingress layer.

Caddy truth:

```text
image: caddy:2.8.4-alpine
scope: Ring FileBase public gateway
```

The Caddyfile is scoped to Ring FileBase (`{$FILES_DOMAIN}`, `/files/*`, upload
API paths, and `/health`). It should not be modified for `api.daarion.city`
without a separate Ring FileBase ingress decision.

## Current DNS/TLS/Firewall Evidence

Current public DNS:

```text
api.daarion.city A -> <current-dns-target>
edge.daarion.city CNAME -> daarion-dao.github.io
```

NODA3 public IPv4:

```text
<operator-verified-noda3-ip>
```

Firewall:

```text
ufw: active
default incoming: deny
80/tcp allow: not observed
443/tcp allow: not observed
existing non-standard Ring FileBase public ports: present
```

TLS tooling:

```text
certbot: missing
/etc/letsencrypt: missing
```

Current public smoke remains blocked because `api.daarion.city` still points to
a target that does not serve the verified Edge Backend health endpoint.

## Existing DAARION Services On NODA3

Docker-based services already present include market-data, external worker,
Qdrant, Neo4j, Postgres, Grafana, Ollama, Ring FileBase, GitLab, and Octelium.

MicroK8s contains DAARION-related resources:

```text
namespace: daarion-edge
comfy-agent: Running
dagi-router: ContainerCreating
swapper-service: Pending / ContainerStatusUnknown
```

The MicroK8s cluster is not a clean deployment target for this health service
right now.

## Kubernetes/k3s Evidence

Tools:

```text
kubectl: present
microk8s: present
k3s: present
helm: missing
```

Systemd:

```text
k3s.service: inactive
k3s-agent.service: activating for about one month
microk8s kubelite: active
```

MicroK8s:

```text
node: Ready
multiple kube-system/gpu/daarion-edge pods are ContainerCreating, Pending,
ContainerStatusUnknown, or PodInitializing
no ingress resources were listed
```

Conclusion: do not use Kubernetes/k3s ingress for this beta health endpoint.

## Deployment Options Comparison

| Option | Safety | Disruption Risk | Speed | TLS Complexity | Rollback | Fit |
| --- | --- | --- | --- | --- | --- | --- |
| Docker local service only on `127.0.0.1:9413` | High | Low | Fast | None for local smoke | Simple `docker compose down` | Best first step |
| Existing Nextcloud snap Apache/httpd | Low until owner/intent confirmed | High | Medium | Entangled with Nextcloud snap | Risky | Not recommended now |
| Existing Ring FileBase Caddy container | Low for this API | Medium/high | Medium | Bound to Ring FileBase domain/config | Risky | Not recommended now |
| Install new Nginx/Caddy on host | Medium only after operator ingress decision | Medium | Medium | Requires cert/DNS/firewall | Manageable | Possible later |
| MicroK8s/k3s ingress | Low now | High | Slow | Cluster-dependent | Harder | Not recommended now |
| Octelium route/service | Low now | Medium | Unknown | Private overlay design first | Unknown | Later private/admin path |
| External DNS/CDN/tunnel to NODA3 local service | Medium/high after approval | Medium | Medium | External provider handles TLS | Manageable | Good public option if approved |
| Leave public API blocked | High | None | Immediate | None | N/A | Valid until ingress owner is clear |

## Recommended Deployment Route

1. Keep PR #2 docs-only until this audit is reviewed.
2. Do not edit Nextcloud Apache/httpd, Ring FileBase Caddy, firewall, DNS, or
   MicroK8s.
3. If approved, deploy only the Docker service on NODA3 bound to
   `127.0.0.1:9413` and run local smoke.
4. After local smoke, make an explicit operator ingress decision:
   - external HTTPS tunnel/CDN/load balancer to `127.0.0.1:9413`; or
   - a new dedicated host-level reverse proxy with approved TLS/firewall; or
   - a carefully reviewed Apache/Caddy integration only if the current service
     owner confirms it is the right ingress.
5. Repoint `api.daarion.city` to the operator-verified NODA3 target only after
   ingress/TLS is ready.
6. Run public smoke.
7. Only after HTTP `200`, open the separate `loval-echoes`
   `device_backend_profiles` task.

## Exact Next Safe Step

Run a local-only Docker deployment on NODA3 after operator approval:

```bash
ssh noda3
sudo mkdir -p /opt/daarion-edge-backend
sudo chown "$USER":"$USER" /opt/daarion-edge-backend
cd /opt/daarion-edge-backend
git clone https://github.com/DAARION-DAO/daarion-edge-backend.git . || git fetch origin
git checkout main
git pull --ff-only origin main
```

Then create Docker Compose binding only to loopback:

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

Local smoke:

```bash
docker compose config
docker compose up -d --build
curl -i http://127.0.0.1:9413/api/v1/edge/health
curl -i http://127.0.0.1:9413/healthz
curl -i http://127.0.0.1:9413/readyz
curl -i http://127.0.0.1:9413/docs
curl -i http://127.0.0.1:9413/openapi.json
```

This still does not make `api.daarion.city` public. A separate ingress/DNS/TLS
decision remains required.

## What Must Not Be Touched

- Do not deploy through Nextcloud Apache/httpd yet.
- Do not modify Ring FileBase Caddy.
- Do not change DNS.
- Do not open firewall ports.
- Do not install Nginx/Caddy/Traefik/Certbot.
- Do not alter MicroK8s/k3s.
- Do not stop or restart existing services.
- Do not touch Supabase.
- Do not insert `device_backend_profiles`.
- Do not modify `loval-echoes`.
- Do not enable worker mode, DAARWIZZ routing, or node federation.

## Unknowns That Remain

- Who owns `api.daarion.city` DNS and where the record should live long-term.
- Whether public `api.daarion.city` should be direct-to-NODA3, CDN/tunnel, or
  another gateway.
- Whether NODA3 should run a new dedicated public ingress service.
- Whether Octelium should be repaired for private/operator routing later.
- Whether Nextcloud snap Apache should remain on standard port 80.
- Whether a standard 443 listener should be created on NODA3 or terminated
  externally.
