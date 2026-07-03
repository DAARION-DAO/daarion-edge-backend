# DAARION Platform Multinode Architecture

## Docker-to-K3s Roadmap for MicroDAO / DAGI / DAARION.city

## 1. Document Status

Status: canonical architecture draft

Date: 2026-07

Owner: SOFIIA / DAARION architecture governance

Scope:

- DAARION.city
- DAGI
- MicroDAO
- Edge Client
- Edge Backend
- NODA infrastructure
- Core 6+1 agents
- models and model/provider bindings
- public and private platforms
- deployment roadmap

Non-goal: this document is not a final implementation specification for every
subsystem. It defines the architecture direction, safety boundaries, and
deployment sequencing that future PRs, operator tasks, Lovable tasks, Codex
tasks, and research work should use as a common reference.

## 2. Executive Verdict

DAARION should use a Docker-first, K3s-later deployment strategy.

The immediate beta blocker is not a lack of city-scale doctrine. It is the
absence of a verified public Edge Backend health endpoint for Connect Device.
The current safe path is:

```text
Docker local service on NODA3
-> local smoke
-> operator decision on ingress/TLS/DNS
-> public smoke
-> device_backend_profiles
-> Connect Device smoke
-> Edge Client smoke
```

Key decisions:

- Docker Compose is the immediate deployment layer.
- K3s is the preferred future lightweight Kubernetes target after the node
  fleet, ingress, DNS/TLS, secrets, observability, and service contracts are
  stable.
- NODA3 is the preferred first host for the local Edge Backend Docker service.
- Public ingress, DNS, TLS, and firewall routing are a separate operator
  decision.
- Edge Client remains required. Edge Backend does not replace it.
- Edge Backend is the coordination endpoint for Connect Device beta and later
  device/node coordination.
- Supabase and Lovable are temporary launch layers, not final canonical
  DAARION infrastructure.
- The platform must be prepared for 10,000 users and many edge clients without
  becoming a chaotic collection of unrelated services.

The beta architecture must stay narrow while the city architecture stays large
enough to grow.

## 3. Why This Document Exists

DAARION is now multidimensional:

- many repositories;
- many platforms;
- many public surfaces;
- many agents;
- many node types;
- user-owned edge runtimes;
- backend coordination services;
- Core 6+1 constitutional systems;
- local, node-local, cloud, and future network-provided models;
- multiple infrastructure layers.

Without a canonical architecture document, each repository can optimize locally
and accidentally create fragmentation:

- one repo invents its own deployment truth;
- another repo invents its own agent authority model;
- another repo treats Supabase as final infrastructure;
- another repo treats a local node as permanent doctrine;
- another repo treats a temporary health endpoint as full city backend.

This document gives the project a shared architectural frame while preserving
evidence discipline. Current deployment reality is evidence, not doctrine.

## 4. Strategic Goals

DAARION must evolve toward:

1. 10,000-user readiness for MicroDAO and DAGI network participation.
2. Many Edge Client installations on user-owned devices.
3. A real City of Agents, not a single chatbot.
4. MicroDAO onboarding and Connect Device flows that fail closed.
5. Core 6+1 agents and their subagents with explicit boundaries.
6. Many platforms and product verticals without siloed architecture.
7. Controlled, observable, scalable, non-chaotic infrastructure.
8. Agent-led operations with human/operator approval gates.
9. Clear authority boundaries between SOFIIA, DAARWIZZ, AISTALK, DAIS,
   SENTINEL, MELISSA, and KILLER.
10. Future node federation without making current node placement permanent.

## 5. Current Architecture

### Repo-local Evidence

This repository, `daarion-edge-backend`, currently contains a minimal FastAPI
health service for Connect Device beta.

Repo-local evidence:

- `GET /api/v1/edge/health`
- `GET /healthz`
- `GET /readyz`
- service name: `daarion-edge-backend`
- default version: `0.1.0-beta`
- default environment: `production`
- default health status: `ok`
- readiness status: `ready`
- minimum Edge Client version: `0.2.2-3`
- FastAPI docs and OpenAPI JSON are disabled for public exposure.
- The service has no Supabase dependency.
- The service does not register devices.
- The service does not dispatch workers.
- The service does not route through DAARWIZZ.
- The service does not implement node federation.

### Current Platform Evidence

Operator-provided current evidence for the wider platform:

- `loval-echoes` is the current public web/Lovable/Supabase entry layer.
- Supabase is a temporary launch layer, not final canonical DAARION
  infrastructure.
- `daarion-edge-client` is the user device runtime and is still required.
- Edge Client is not replaced by Edge Backend.
- `daarion-edge-backend` is the missing coordination/control endpoint for
  Connect Device.
- Connect Device must remain fail-closed until a real public backend health
  endpoint returns HTTP 200.
- `device_backend_profiles` must only be inserted after public
  `https://api.daarion.city/api/v1/edge/health` returns HTTP 200.

### Current Node Evidence

Operator-provided node evidence:

- NODA1 is unavailable/offline for the current beta deployment path.
- NODA2 is a strong control/development/runtime node, especially around
  SOFIIA, but must not be hardcoded as eternal doctrine.
- NODA3 is reachable, has Docker/Compose, has public IP `212.8.58.133`, and is
  the preferred first host for the local Edge Backend service.
- NODA4 is a fallback/future node but is currently unreachable.
- `api.daarion.city` currently points to old IP `144.76.224.179`, not NODA3.

Operator-provided NODA3 infrastructure evidence:

- Docker/Compose available.
- Port `9413` is free.
- Apache/httpd belongs to Nextcloud snap and is not confirmed DAARION ingress.
- Ring FileBase Caddy is scoped to Ring FileBase and must not be reused
  casually.
- Octelium exists but is currently unauthenticated and not usable as public
  route.
- MicroK8s/k3s are not clean deployment targets right now.
- Surrounding infrastructure may include Ring FileBase, Qdrant, Neo4j,
  Postgres, Grafana, GitLab, Ollama, Octelium, and other services that must not
  be disturbed casually.

## 6. Target Architecture

DAARION should be treated as five runtime planes.

### A. Public Experience Plane

This plane contains user-facing surfaces:

- web apps;
- Lovable apps;
- onboarding;
- MicroDAO flows;
- public pages;
- chat UI;
- user dashboards;
- platform-specific apps.

This plane should be allowed to move quickly, but it must not become the
canonical owner of identity, agent truth, device truth, or infrastructure truth.

### B. Edge Sovereignty Plane

This plane contains user-owned and node-owned runtime:

- Edge Client;
- local identity;
- local device capabilities;
- local models;
- local worker readiness;
- device pairing;
- future user-owned compute.

The Edge Client is required because DAARION is not only a cloud app. The user
device is part of the network.

### C. Coordination Plane

This plane coordinates devices, nodes, services, and capability discovery:

- Edge Backend;
- node registration;
- capability registry;
- backend profile registry;
- service health;
- pairing coordination;
- routing contracts;
- future job dispatch.

The current Edge Backend starts as a narrow health/profile endpoint. It should
grow only through reviewed contracts.

### D. Knowledge and State Plane

This plane stores durable truth and history:

- Postgres;
- Neo4j;
- Qdrant;
- object storage / MinIO / FileBase;
- agent memory;
- routing history;
- trust state;
- audit logs;
- governance events;
- model registry.

State must not become trapped in temporary node-local memory unless explicitly
classified as local cache or local session state.

### E. Agent Execution Plane

This plane contains the city intelligence:

- Core 6+1 agents;
- public specialist agents;
- internal crews;
- subagents;
- child specialists;
- agent workers;
- model-routing layer;
- task queues.

Execution must stay bounded by agent identity, model/provider binding,
runtime enablement, tool permissions, authority rules, and auditability.

## 7. Core 6+1 Role in Scaling

Core 6+1 systems are constitutional systems, not just bots.

### SOFIIA

SOFIIA owns architecture truth, build intelligence, system evolution, and CTO
logic. SOFIIA must not become the mayor, universal router, or owner of every
domain.

### DAARWIZZ

DAARWIZZ owns public orchestration, routing, city front-door behavior, and
movement through the city. DAARWIZZ must not absorb all sovereignty, all truth,
or all authority.

### AISTALK

AISTALK owns security, defense, investigation, and red/blue/purple team logic.
Its offensive or invasive capabilities must remain bounded and must not be
connected casually to public runtime.

### DAIS

DAIS owns identity, legitimacy, trust, access boundaries, and revocation
logic. DAIS must not fail open.

### SENTINEL

SENTINEL owns observability, telemetry, anomaly detection, normalized evidence,
and operational signal integrity. Dashboards alone are not enough; evidence
must feed decisions.

### MELISSA

MELISSA owns value, incentives, usefulness, contribution, and circulation
logic. Value logic must not become casual payment or authority execution.

### KILLER

KILLER owns bounded containment, freeze, quarantine, revocation, and
termination only under an explicit authority chain. KILLER must remain blocked
for execution unless a future authority path is proven and approved.

### Core 6+1 Scaling Rules

- Core 6+1 systems may have subagents.
- Subagents do not become sovereign constitutional systems by default.
- DAARWIZZ orchestrates movement but does not own all truth.
- SOFIIA governs architecture truth but does not own every domain.
- DAIS, SENTINEL, and KILLER must never fail open.
- Shared memory and authoritative write paths are required before broad
  automation.

## 8. Many Platforms Layer

DAARION will include many platforms, for example:

- MicroDAO core;
- Energy Union / HELION;
- AgroMatrix;
- NUTRA;
- PRORYV;
- Ring FileBase integration;
- Cosmic Food Systems / GREENFOOD;
- future public and private verticals.

Platform integration rules:

- each platform has its own UX and domain;
- each platform can have specialized agents;
- shared identity/trust should converge through DAIS;
- shared routing should converge through DAARWIZZ;
- shared observability should converge through SENTINEL;
- architecture decisions should converge through SOFIIA;
- platform-specific backends must expose health/readiness and audit
  interfaces;
- platform-specific data must not silently become global city truth;
- shared services must use explicit contracts rather than hidden coupling.

The goal is a city with many districts, not many disconnected silos.

## 9. Node Model

DAARION should distinguish node types:

| Node type | Role |
| --- | --- |
| Control/development node | Architecture, build, operator, local runtime, admin testing. |
| Public gateway node | Public ingress, TLS, API exposure, reverse proxy. |
| GPU/inference node | Model serving and inference capacity. |
| Storage/state node | Databases, object storage, backup, event stores. |
| Edge user node | User-owned Edge Client runtime. |
| Worker node | Bounded job execution and future capability services. |
| Observability node | Logs, metrics, traces, health, evidence normalization. |
| Fallback node | Failover or degraded-mode runtime. |

Current node map:

| Node | Current role |
| --- | --- |
| NODA1 | Excluded/offline for current beta deploy. |
| NODA2 | Strong SOFIIA/control/development/runtime node; not permanent doctrine. |
| NODA3 | Preferred first runtime host for local Edge Backend Docker service. |
| NODA4 | Fallback/future node, currently unreachable. |
| Future nodes | Phones, laptops, servers, sensors, GPU boxes. |

Node placement is transitional evidence. It must not harden into permanent
architecture without review.

## 10. Docker-first Policy

Docker Compose is the immediate deployment layer because it is:

- simple;
- low disruption;
- available on NODA3 now;
- compatible with local health proof;
- independent from public DNS/TLS decisions;
- less risky than using degraded or ambiguous Kubernetes;
- a useful step toward portable service packaging.

Docker requirements for DAARION services:

- Dockerfile;
- docker-compose example;
- explicit service port;
- loopback binding when public ingress is not approved;
- `/healthz`;
- `/readyz`;
- structured JSON health where useful;
- no secrets in the image;
- no hardcoded host paths;
- structured logs to stdout/stderr;
- version/environment config;
- local smoke checklist;
- graceful shutdown where applicable.

For Edge Backend beta, the Docker path should first prove local health on
NODA3 before public ingress is changed.

## 11. K3s-later Policy

K3s should become the future lightweight Kubernetes target after the platform
has stable node and service contracts.

Move to K3s when these conditions are met:

- NODA3 is stable;
- NODA4 is reachable or additional nodes are available;
- one control plane is selected;
- ingress strategy is selected;
- DNS/TLS strategy is selected;
- secrets strategy is selected;
- observability baseline exists;
- CI image build pipeline exists;
- service contracts are stable;
- stateful backup/failover plan exists.

Do not move now because:

- MicroK8s is degraded;
- k3s-agent is problematic;
- clean ingress resources are not established;
- NODA4 is unreachable;
- public DNS still points elsewhere;
- Octelium is unauthenticated;
- Kubernetes would add complexity without solving the current Connect Device
  blocker.

K3s target rules:

- one lightweight Kubernetes path;
- no ambiguous MicroK8s plus K3s competition;
- stateless services first;
- stateful services only after backup strategy;
- Gateway API or ingress controller later;
- service mesh only after basic platform stability.

## 12. What Makes a Service K3s-ready

Every DAARION service should become K3s-ready even when deployed with Docker
Compose first.

Minimum properties:

- OCI image;
- explicit ports;
- `/healthz`;
- `/readyz`;
- structured JSON health;
- environment contract;
- no local-only secrets;
- no hidden local state;
- idempotent startup;
- logs to stdout/stderr;
- metrics endpoint later;
- graceful shutdown;
- resource requests/limits later;
- readiness/liveness semantics;
- no canonical truth trapped in pod memory.

K3s readiness is a packaging and operations discipline. It is not a command to
deploy everything into Kubernetes immediately.

## 13. Ingress / DNS / TLS Strategy

Service runtime must be separate from public ingress.

Rules:

- public ingress must be operator-approved;
- do not reuse Nextcloud Apache casually;
- do not reuse Ring FileBase Caddy casually;
- Octelium is not the current public route;
- public API requires DNS, TLS, firewall, and smoke proof;
- `api.daarion.city` should only move to NODA3 after ingress is ready.

Required public gate:

```text
https://api.daarion.city/api/v1/edge/health -> HTTP 200
```

This must happen before inserting any active production
`device_backend_profiles` row.

## 14. Octelium Role

Octelium may become valuable for:

- private operator access;
- inter-node access;
- internal service mesh-like access;
- private management channels.

It is not currently ready for public `api.daarion.city` because the current
evidence says it is unauthenticated and not usable as a public route.

Octelium needs a separate repair/auth/session/routing design. It should be
evaluated as overlay/private mesh first, not blindly used as public ingress.

## 15. Edge Backend Role

Edge Backend is not the full city backend yet.

Beta role:

- public health endpoint;
- backend profile target;
- pairing coordination foundation;
- deployment proof for Connect Device.

Later roles:

- node registration;
- device pairing;
- capability registry;
- service discovery;
- readiness callbacks;
- controlled worker registration;
- audit;
- policy-aware routing.

The beta service must remain narrow and safe. It must not gain worker mode,
DAARWIZZ routing, node federation, Supabase dependency, or production writes
without separate design and review.

## 16. Edge Client Role

Edge Client is required.

It is the user-owned runtime layer for:

- local identity;
- device pairing;
- local model/runtime capability;
- future worker mode;
- future user-owned compute;
- local readiness and capability reporting.

Edge Client must not be replaced by the web app or backend. Worker mode must
remain gated, sandboxed, auditable, and disabled until policy and security are
ready.

## 17. MicroDAO Onboarding Path

Target flow:

1. User opens public web app.
2. User creates or uses account.
3. User enters MicroDAO flow.
4. User chooses Connect Device.
5. Web app checks active backend profile.
6. Edge Backend health is verified.
7. Device pairing invite is created.
8. User installs Edge Client.
9. Edge Client pairs with backend.
10. Device reports readiness and capabilities.
11. User device becomes a known edge node.
12. Future: device may become local worker under policy.

The current beta must not fake any of these steps. The backend profile must
only be inserted after public backend health returns HTTP 200.

## 18. 10K User Readiness Model

10,000 users is not only a marketing target. It means the platform must handle:

- onboarding;
- sessions;
- chats;
- device pairing;
- backend health checks;
- queueing;
- agent tasks;
- telemetry;
- model routing;
- support loops.

Readiness dimensions:

- frontend scalability;
- auth/session stability;
- backend API health;
- queue/event bus;
- database indexes and RLS;
- device pairing throughput;
- Edge Client release distribution;
- observability;
- support/agent automation;
- abuse prevention;
- rate limiting;
- cost controls;
- model routing;
- fallback modes.

No one subsystem should claim 10K readiness alone.

## 19. Agent Operations Model

Users should not hit all Core 6+1 agents directly for every action.

Operating model:

- DAARWIZZ routes and orchestrates public movement.
- SOFIIA builds, architects, and governs architecture truth.
- SENTINEL observes and normalizes evidence.
- DAIS validates identity, legitimacy, and trust.
- AISTALK handles security and investigation.
- MELISSA interprets value and contribution.
- KILLER enforces containment only under an authority chain.

Agent work should move through:

- fixed contracts;
- queues;
- audit logs;
- explicit delegation;
- bounded execution;
- clear authority class;
- visible result metadata.

Parallel fanout, council behavior, or autonomous swarm behavior requires
separate approval and safety design.

## 20. Model and Inference Strategy

Models may be:

- local;
- node-local;
- server/GPU;
- cloud;
- network-provided;
- fallback-only.

Rules:

- do not hardcode current NODA2 or NODA3 model limits as doctrine;
- each Core 6+1 agent and subagent should have explicit model/provider
  binding;
- bindings can be upgraded as hardware changes;
- model routing should abstract provider, model, weight, placement, and
  fallback policy;
- critical paths need fallback and cost/latency policies;
- binding does not grant runtime permission;
- runtime enablement does not prove binding.

## 21. State, Memory, and Truth

Not all memory is equal.

Truth domains:

- DAARWIZZ needs office/routing continuity.
- SOFIIA needs architecture truth continuity.
- DAIS needs identity/trust truth.
- SENTINEL needs normalized evidence truth.
- KILLER needs sanction/audit trail.
- Platform chats can have user conversation memory.
- Node-local memory can be useful, but must not become canonical truth
  accidentally.

Canonical state should be explicit:

- owner;
- writer;
- reader;
- audit path;
- backup path;
- retention policy;
- recovery plan.

## 22. Observability and SENTINEL

Every service must expose health.

Minimum observability path:

- `/healthz`;
- `/readyz`;
- structured logs;
- version and environment metadata;
- request IDs later;
- metrics endpoint later;
- service dependency status later.

SENTINEL should normalize telemetry and anomaly signals. Dashboards are useful,
but evidence must be routed into decisions, incidents, and operator workflows.

## 23. Security and AISTALK

Security is not an afterthought.

High-risk patterns:

- exposed keys;
- public unauthenticated mutation endpoints;
- fake health;
- Edge Functions that bypass review;
- public worker execution before sandboxing;
- broad CORS or admin APIs;
- using old ingress without ownership proof;
- ambiguous public/private service exposure.

AISTALK should own investigation and defense workflows. Red/blue/purple team
roles must be bounded. Offensive tooling must not be connected casually to
public runtime.

## 24. Identity and DAIS

Identity must cover:

- users;
- devices;
- agents;
- nodes;
- sessions;
- services;
- keys;
- capabilities.

DAIS should own legitimacy, trust, revocation, and access boundaries.

Supabase auth may be a temporary web-layer auth substrate. It is not final DAIS
truth unless a later architecture decision explicitly makes it so.

## 25. Governance / MicroDAO / MELISSA / KILLER

MicroDAO requires governance workflows and audit.

MELISSA handles:

- value;
- usefulness;
- contribution;
- circulation logic;
- incentive interpretation.

KILLER handles:

- freeze;
- quarantine;
- revocation;
- termination;
- containment.

KILLER action must only happen through an explicit authority chain. Governance
sensitive actions must not become casual local fallbacks.

## 26. Repository Strategy

Current repository roles:

| Repository | Role |
| --- | --- |
| `loval-echoes` | Public beta web surface and current Supabase/Lovable entry layer. |
| `daarion-edge-client` | User device runtime and future edge worker base. |
| `daarion-edge-backend` | Coordination/control backend for Connect Device beta and later device/node coordination. |
| Future core service repos | Shared city backend, registries, queues, state, identity, and agent operations. |

Repository rules:

- docs must cross-link or reference canonical architecture consistently;
- each repo should avoid inventing its own doctrine;
- local implementation docs should state whether they are beta, temporary,
  canonical, or experimental;
- public beta surfaces should not become canonical backend truth by accident;
- architecture truth should converge through SOFIIA governance.

## 27. Short-term Roadmap: Beta Gate

Next sequence for Connect Device beta:

1. Merge/update architecture docs.
2. Deploy Edge Backend locally on NODA3 through Docker Compose.
3. Run local smoke.
4. Decide public ingress/TLS/DNS.
5. Configure DNS/TLS/firewall.
6. Run public smoke.
7. Insert one active backend profile.
8. Run Connect Device smoke.
9. Run Edge Client installer smoke.
10. Release `0.2.2-4+` if needed.
11. Add basic operational dashboard.

The immediate unblock remains:

```text
https://api.daarion.city/api/v1/edge/health -> HTTP 200
```

## 28. Medium-term Roadmap: Platformization

Medium-term platform work:

- service contract standard;
- image build pipeline;
- registry/versioning;
- queue/event bus;
- capability registry;
- node registry;
- model registry;
- observability baseline;
- DAIS identity draft;
- SENTINEL telemetry draft;
- DAARWIZZ routing contract;
- SOFIIA architecture write path;
- support for several platforms.

This stage turns beta infrastructure into repeatable platform infrastructure.

## 29. Long-term Roadmap: Distributed City

Long-term city architecture:

- K3s cluster/fleet;
- multiple backend nodes;
- many edge clients;
- agent workloads distributed by capability;
- DAARWIZZ orchestration over shared memory;
- DAIS trust layer;
- SENTINEL monitoring;
- AISTALK security;
- MELISSA value layer;
- KILLER enforcement;
- self-healing operations;
- edge worker marketplace/capability network;
- MicroDAO governance.

Distributed city architecture requires clear ownership of identity, routing,
truth, memory, observability, value, and authority.

## 30. Risk Register

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| False readiness | UI can look ready while backend health is absent. | Require public health 200 before DB profile insert. |
| Split-brain architecture | Repos may invent competing doctrine. | Use canonical docs and explicit ownership. |
| Two equal DAARWIZZ mayors | Orchestration authority can fragment. | Keep DAARWIZZ role singular and contract-bound. |
| Identity fragmentation | Users/devices/nodes/agents can diverge. | Route identity truth through DAIS architecture. |
| Routing truth fragmentation | Multiple routers can conflict. | Define DAARWIZZ routing and backend contracts. |
| Node-local memory as truth | Temporary runtime memory can become accidental canon. | Label local memory and create canonical stores. |
| Wrong ingress reuse | Nextcloud or Ring FileBase ingress may be disturbed. | Separate ingress decision and smoke proof. |
| Kubernetes too early | Adds complexity before blocker is solved. | Docker-first, K3s-later. |
| Supabase as accidental canon | Temporary launch layer can become permanent doctrine. | Treat Supabase as beta substrate unless reviewed. |
| Unauthenticated Octelium | Private mesh may not be safe public ingress. | Separate Octelium repair/design. |
| NODA4 unreachable | Reduces failover confidence. | Restore or replace before cluster claims. |
| Edge worker mode too early | User devices need sandbox and policy. | Keep worker mode disabled until approved. |
| No rate limits for 10K users | Public APIs can overload or be abused. | Add rate limits and queueing before scale. |
| No observability | Failures cannot be diagnosed. | SENTINEL-aligned health/log/metric baseline. |
| No model cost control | Cloud/model use can become expensive. | Model routing policy and cost budgets. |
| Platforms become silos | Vertical apps diverge from city truth. | Shared identity/routing/observability principles. |

## 31. Canonical Decisions

Current canonical decisions:

- Docker Compose now.
- K3s later.
- Edge Client required.
- Edge Backend required.
- Supabase temporary.
- `device_backend_profiles` only after public health 200.
- Public ingress separate from runtime.
- NODA3 local first for current Edge Backend service.
- No NODA1 for current deploy.
- NODA4 fallback/future.
- Octelium later/private until repaired.
- Core 6+1 authority boundaries preserved.
- All services must be K3s-ready.
- Stateful services need backup/failover before cluster migration.
- Many platforms must integrate through shared identity, routing,
  observability, memory, and governance principles.

## 32. Open Questions

Open questions:

1. What final public ingress should serve `api.daarion.city`?
2. Should DNS move to NODA3 directly or to an external proxy?
3. Should Octelium become a private operator mesh?
4. How will NODA4 be restored or replaced?
5. Which service owns the model registry?
6. Where does canonical DAIS identity live?
7. Where does DAARWIZZ office continuity live?
8. How is SOFIIA architecture truth persisted?
9. When should Docker Compose migrate to K3s?
10. What minimum telemetry is required before a 10K-user beta?
11. How many platforms are included in the first public beta?
12. Which stateful services need backup before cluster migration?
13. Which queues/events are required before agent task distribution?
14. What rate-limit and abuse-prevention policy is needed for public Edge
    Backend endpoints?

## 33. Immediate Next Implementation Sequence

Recommended next implementation sequence:

1. Finish and merge the current deploy runbook PR.
2. Deploy Edge Backend locally on NODA3 via Docker Compose.
3. Run local smoke.
4. Decide public ingress/TLS/DNS.
5. Make `api.daarion.city` return health 200.
6. Insert one active `device_backend_profiles` row.
7. Run Connect Device smoke.
8. Run Edge Client installer smoke.
9. Define service standard for all future backends.
10. Prepare K3s migration plan only after NODA3, NODA4, and node fleet state
    are stable.

## 34. Explicit Non-Goals For This Document

This document does not:

- deploy Edge Backend;
- change DNS;
- change firewall rules;
- change TLS;
- add Supabase migrations;
- insert `device_backend_profiles`;
- write production data;
- add worker mode;
- add DAARWIZZ routing implementation;
- add node federation implementation;
- change Edge Client;
- change `loval-echoes`;
- define a final implementation spec for every subsystem;
- claim NODA3 public readiness before public smoke;
- claim 10K-user readiness today.

## 35. Validation Expectations

This document should be maintained through docs-only PRs unless a future phase
explicitly opens implementation.

Minimum validation for this PR:

- `git diff --check`
- local-path and secret-like scan
- no deploy
- no DNS changes
- no firewall changes
- no Supabase changes
- no production DB writes
- no `device_backend_profiles` insert
- no worker mode
- no DAARWIZZ routing implementation
- no node federation implementation
