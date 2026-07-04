# DAARION Edge Repository Boundary Decision

Date: 2026-07

Status: decision record, docs-only

Repository: `DAARION-DAO/daarion-edge-backend`

Related repositories:

- `DAARION-DAO/loval-echoes`
- `DAARION-DAO/daarion-edge-client`
- `DAARION-DAO/daarion-edge-backend`
- `IvanTytar/microdao-daarion`

## 1. Executive Verdict

Keep `daarion-edge-backend` as a separate public repository for now.

Treat it as a public, generic, service-contract backend for DAARION Edge
coordination. Do not move it into `daarion-edge-client` during the Connect
Device beta gate.

The current boundary is:

```text
loval-echoes
-> public MicroDAO web and temporary Supabase/Lovable launch layer

daarion-edge-client
-> user-installed Edge Client, Tauri/Rust device runtime, local identity,
   pairing client, local capability detection, future local worker runtime

daarion-edge-backend
-> server-side Edge coordination service, public API contract, health/readiness,
   future pairing/node/device/capability registry

IvanTytar/microdao-daarion
-> private node-network operations truth, exact NODA inventory, DNS, firewall,
   ingress, Octelium, incidents, and production runbooks
```

This decision can be revisited after beta. If the backend remains tiny,
client-coupled, and never becomes an independently deployed service, a future
`daarion-edge` monorepo may become reasonable. That is not the right move now.

## 2. Why This Document Exists

DAARION now has multiple public repositories and at least one private operations
repository. That is acceptable only if each repository has a clear lifecycle and
does not duplicate another repository's authority.

The immediate risk is not "too many repos" by itself. The risk is boundary
confusion:

- a client installer repo starts carrying server deployment truth;
- a public backend repo starts carrying private NODA operational truth;
- a Lovable/Supabase web repo starts becoming canonical infrastructure;
- a private node-network repo becomes invisible to public service contracts;
- Codex tasks and maintainers accidentally mix docs-only, runtime, deployment,
  and production-write lanes.

This document records the intended boundary so future PRs can be reviewed
against it.

## 3. Evidence Inspected

This decision is based on current repository evidence, not only naming.

### `daarion-edge-backend`

Repo-local evidence:

- `README.md` describes a minimal beta backend for Edge Client health/profile
  discovery.
- `docs/EDGE_BACKEND_HEALTH_CONTRACT.md` defines the public
  `GET /api/v1/edge/health` contract.
- `app/main.py` implements a small FastAPI service.
- `pyproject.toml` packages a Python backend service.
- `Dockerfile` and deploy docs make this a server-deployed runtime.
- The service exposes `/api/v1/edge/health`, `/healthz`, and `/readyz`.
- The service intentionally does not register devices, dispatch workers, route
  through DAARWIZZ, depend on Supabase, or implement node federation.
- `docs/architecture/DAARION_PLATFORM_MULTINODE_ARCHITECTURE_2026-07.md`
  states that Edge Client remains required and Edge Backend does not replace it.

### `loval-echoes`

Repo-local evidence:

- `README.md` identifies the project as a Lovable-managed public web app.
- `docs/product/CONNECT_DEVICE_CONTRACT.md` makes `loval-echoes` the owner repo
  for the product journey.
- The same contract identifies `daarion-edge-client` as the related runtime
  repo.
- `docs/operations/DAARION_EDGE_BACKEND_HEALTH_TRUTH_2026-07-03.md` states that
  `loval-echoes` contains the frontend Connect Device flow and Supabase device
  pairing tables/RPCs, but not a deployable service for
  `GET /api/v1/edge/health`.
- The Supabase `device_backend_profiles` row must not be inserted before a real
  backend URL returns HTTP 200.

### `daarion-edge-client`

Public repo evidence:

- GitHub describes it as `DAARION Sovereign Agent Edge Client - Tauri desktop
  app for birthing autonomous AI agents`.
- `README.md` describes a public desktop/mobile gateway and Edge Client runtime.
- `package.json` identifies a Vite/Tauri app at version `0.2.2-4`.
- `src-tauri/Cargo.toml` identifies a Rust/Tauri package named
  `daarion-edge-client`.
- `src-tauri/src/pairing.rs` owns persisted local backend pairing state.
- `src-tauri/src/backend_health.rs` calls `GET /api/v1/edge/health` against the
  paired backend and validates service, schema, protocol, environment, status,
  and minimum client version.
- `src/lib/backendConfig.ts` reads the effective paired backend URL through a
  Tauri command.
- The client repo contains installer/runtime concerns, local identity, local
  capability detection, Genesis, pairing, backend health diagnostics, and
  gated future worker functionality.

This is client/runtime evidence, not server deployment evidence.

### `IvanTytar/microdao-daarion`

Repository metadata evidence:

- The repository is private.
- It is described as `MicroDAO & DAARION.city - Agent-based community platform`.

Boundary inference:

- Exact node inventory, operational NODA facts, IP/DNS/firewall state,
  Octelium state, production runbooks, incidents, and telemetry belong in a
  private operations repository, not in a public service-contract repository.
- Public repositories may refer to the private repo as the private operations
  source of truth, but must not expose its private contents.

## 4. Why `daarion-edge-backend` Was Created

`daarion-edge-backend` was created to fill a missing layer between the public
web product and the user-installed Edge Client.

The missing layer was:

```text
loval-echoes Connect Device UI
-> needs a verified backend profile
-> Edge Client needs a backend health contract
-> no live backend existed for /api/v1/edge/health
```

The backend is required because:

- `loval-echoes` must remain fail-closed until a backend URL is verified.
- `device_backend_profiles.backend_url` must point to a real service.
- Edge Client pairing and health diagnostics require a backend base URL.
- Connect Device beta needs `GET /api/v1/edge/health` to return HTTP 200 before
  any production profile row is inserted.
- Future pairing coordination, readiness callbacks, node/device registry, and
  capability registry are server-side responsibilities.

This backend was not created to replace `daarion-edge-client`. It was created
because `daarion-edge-client` needs something real to connect to.

## 5. Repository Ownership Boundaries

### `DAARION-DAO/loval-echoes`

Owns:

- public MicroDAO web UI;
- onboarding and Dashboard product flows;
- Connect Device entry point and product language;
- Supabase/Lovable temporary launch layer;
- browser session and current product auth integration;
- MicroDAO-facing presentation of device readiness;
- device pairing table/RPC integration in the current beta substrate.

Does not own:

- native installer builds;
- local device identity;
- local worker runtime;
- public Edge backend uptime;
- NODA operations truth;
- canonical DAARION infrastructure.

### `DAARION-DAO/daarion-edge-client`

Owns:

- user-installed client application;
- Tauri/Rust desktop runtime;
- installer/release artifacts for macOS, Windows, Linux, and later mobile;
- local identity generation and secure local storage;
- persisted pairing state;
- backend health client;
- local device capability detection;
- local model/runtime surfaces;
- future local worker runtime, gated and disabled until security is proven.

Does not own:

- public backend deployment;
- public DNS/TLS/firewall;
- NODA inventory;
- central backend registry state;
- Supabase production profile writes.

### `DAARION-DAO/daarion-edge-backend`

Owns:

- server-side Edge coordination endpoint;
- public backend API contracts;
- `GET /api/v1/edge/health`;
- `/healthz` and `/readyz`;
- Docker/K3s-ready backend packaging;
- future pairing coordination;
- future node/device/capability registry;
- future signed readiness callback contract;
- generic, sanitized deployment examples.

Does not own:

- installer artifacts;
- local user device identity;
- live node-network truth;
- exact NODA IP/DNS/firewall state;
- private operational incidents;
- production database writes;
- Supabase Edge Functions;
- worker dispatch in the beta phase.

### `IvanTytar/microdao-daarion`

Owns:

- private live node-network truth;
- exact NODA inventory;
- exact IP/DNS/firewall/Octelium/deployment facts;
- private production runbooks;
- operational incidents and telemetry;
- private node-network experiments and recovery notes;
- sensitive deployment context that could become an attack map if public.

Does not need to own:

- generic public health contract documentation;
- sanitized open-source service code;
- generic Docker/K3s readiness examples;
- public Edge Client installer source.

## 6. Options Compared

### Option A: Keep Three Public Repositories

Shape:

```text
DAARION-DAO/loval-echoes
DAARION-DAO/daarion-edge-client
DAARION-DAO/daarion-edge-backend
```

Pros:

- Clear lifecycle separation between web UI, client installer, and backend
  service.
- Backend can deploy independently from desktop/mobile installer releases.
- Edge Client can release native artifacts without inheriting server CI/CD.
- Backend can stay Docker/K3s-ready without turning the client repo into an ops
  repo.
- Security boundaries are easier to review.
- Public API contracts remain visible and reusable.
- Server-side contribution model stays different from client/runtime
  contribution model.
- Reduced risk that client installer docs start exposing live node operations.

Cons:

- More repositories to coordinate.
- Cross-repo PR sequencing must be explicit.
- Shared contracts need disciplined docs and versioning.
- Small backend may feel oversized as a separate repo during early beta.

### Option B: Move Backend Into `daarion-edge-client`

Possible shape:

```text
DAARION-DAO/daarion-edge-client/
  apps/client/
  services/edge-backend/
  docs/contracts/
```

Pros:

- Pairing and health contract can live near client code.
- Fewer public repositories.
- Easier local full-stack development for one maintainer.
- One issue tracker for Edge Client plus backend pairing work.

Cons:

- Repository name says `client` but would contain a server.
- Desktop/mobile release lifecycle mixes with server deploy lifecycle.
- Tauri/Rust/Vite CI mixes with Python/FastAPI/Docker/K3s CI.
- Security review surface becomes less clear.
- Backend deploy cadence can become blocked by installer release work.
- Installer release notes may become entangled with public API uptime.
- Greater risk of live node-network details drifting into the public client
  repo.

This option is not recommended now.

### Option C: Create Or Rename Into A Future `daarion-edge` Monorepo

Possible shape:

```text
DAARION-DAO/daarion-edge/
  apps/client/
  services/backend/
  packages/contracts/
  docs/
```

Pros:

- Name matches the broader domain better than `daarion-edge-client`.
- Shared contracts can become first-class packages.
- One repo can coordinate client/backend compatibility tests.
- Good future shape if Edge becomes a single product family.

Cons:

- Migration cost now would slow the beta gate.
- Release complexity increases.
- CI and ownership rules need more design.
- A monorepo can still leak operational truth if boundaries are not enforced.
- Does not solve the immediate public health endpoint gate.
- Premature consolidation can hide useful lifecycle differences.

This option may be worth revisiting after Connect Device beta if the client and
backend evolve as one tightly coupled product family.

## 7. Evaluation Matrix

| Criterion | Option A: keep separate | Option B: move into client | Option C: future monorepo |
| --- | --- | --- | --- |
| Clarity | High | Medium/low because repo name says client | High if renamed and governed |
| Public open-source usefulness | High for service contract reuse | Medium | High later |
| Release lifecycle | Clean separation | Mixed | Mixed but governable |
| CI/CD | Simple per repo | Mixed stacks | Requires monorepo discipline |
| Security boundary | Strong | Weaker | Depends on governance |
| Deployment boundary | Strong | Blurred | Depends on layout |
| Docker/K3s readiness | Strong | Possible but less natural | Strong if designed |
| Edge Client installer cadence | Independent | Entangled | Entangled unless carefully isolated |
| Backend deploy cadence | Independent | Entangled | Entangled unless carefully isolated |
| Contribution model | Clear | Blurred | Good later with ownership rules |
| Risk of leaking private ops truth | Lower if docs are sanitized | Higher | Medium |
| Convenience for Codex/maintainers | Good with explicit PR sequence | Convenient short-term, risky long-term | Good later, costly now |

## 8. Recommended Decision

Decision:

```text
Keep daarion-edge-backend separate for now.
```

Reasoning:

- The backend has a different deployment lifecycle from the Edge Client.
- The Edge Client is an installed Tauri/Rust runtime, not a server.
- The backend is Docker/K3s-ready server infrastructure.
- Connect Device beta requires an independently verified backend URL before
  `device_backend_profiles` can be activated.
- Future pairing coordination, readiness callbacks, node/device registry, and
  capability registry are server-side coordination concerns.
- Keeping the backend separate makes it easier to keep public contracts generic
  and private node operations private.

Secondary decision:

```text
Do not move backend into daarion-edge-client during beta.
```

Future revisit condition:

```text
Revisit a daarion-edge monorepo only after beta if backend remains tiny,
client-coupled, and not independently deployed.
```

## 9. Required Public/Private Boundary

Public repositories may contain:

- source code;
- public API contracts;
- sanitized architecture docs;
- generic Docker examples;
- generic K3s readiness guidance;
- generic health checks;
- compatibility matrices;
- release notes;
- test fixtures without secrets or private topology.

Public repositories must not become:

- live NODA inventory;
- exact DNS/firewall/IP map;
- Octelium session/auth state;
- private runbook archive;
- incident log;
- operator credential map;
- production database write log;
- attack map for DAARION infrastructure.

Private operations repository owns:

- exact node names and current reachability;
- exact public and private IPs;
- firewall rules;
- DNS provider state;
- TLS provider state;
- reverse proxy configs;
- Octelium auth/session state;
- private operational logs;
- production incidents;
- production rollback details;
- sensitive deploy commands tied to live topology.

Public docs may say:

```text
Private node-network operations truth lives in IvanTytar/microdao-daarion.
```

Public docs must not expose the private contents of that repo.

## 10. Immediate Follow-Up Actions

Completed or current actions:

- `daarion-edge-backend` exists as a separate public service-contract repo.
- The minimal backend health service exists.
- The canonical platform roadmap states that Edge Client remains required and
  Edge Backend does not replace it.
- Public deploy docs have been sanitized to avoid exact live NODA/IP/path
  details.
- The NODA3 local Docker proof is separate from public ingress/DNS/TLS.

Required next actions:

1. Keep backend code public only while it remains generic and non-sensitive.
2. Keep exact NODA operational truth in `IvanTytar/microdao-daarion`.
3. If public docs need node context, use sanitized placeholders and point to the
   private operations source of truth without exposing it.
4. Do not add worker mode, DAARWIZZ routing, node federation, or production
   profile writes to `daarion-edge-backend` without separate design review.
5. Add or maintain compatibility notes between `daarion-edge-client` health
   parsing and `daarion-edge-backend` health responses.
6. Revisit monorepo consolidation after beta only if there is evidence that the
   backend is permanently small, tightly coupled to Edge Client, and not useful
   as an independently deployed server.

## 11. Non-Goals

This decision does not:

- move repositories;
- rename repositories;
- change CI/CD;
- change Edge Client code;
- change `loval-echoes`;
- change private operations repositories;
- deploy public ingress;
- change DNS;
- change firewall rules;
- insert `device_backend_profiles`;
- enable worker mode;
- implement DAARWIZZ routing;
- implement node federation.

## 12. Final Decision Statement

For the Connect Device beta phase:

```text
Keep DAARION-DAO/daarion-edge-backend separate.
Use it as the public Edge coordination backend and health contract repo.
Keep DAARION-DAO/daarion-edge-client focused on user-installed runtime.
Keep DAARION-DAO/loval-echoes focused on MicroDAO web and temporary launch UI.
Keep IvanTytar/microdao-daarion as private live node-network operations truth.
```

This is the smallest safe boundary that preserves beta momentum without
collapsing client release, backend deployment, web UI, and private operations
into one confused repository.
