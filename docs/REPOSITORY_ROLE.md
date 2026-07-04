# Repository Role

Status: public sanitized repository role card

This repository is part of the DAARION.city / DAGI / MicroDAO ecosystem.

The full canonical repository ownership map lives in the private operations
repository: `IvanTytar/microdao-daarion`.

This public repository contains only a sanitized local role summary.

## Role

`DAARION-DAO/daarion-edge-backend` is the public service-contract backend repo
for server-side Edge coordination.

It owns the health/readiness contract and future device/node/capability registry
code, while live deployment truth remains private.

## Owns

- `GET /api/v1/edge/health`;
- `GET /healthz`;
- `GET /readyz`;
- generic Docker/K3s-ready backend code;
- public API contracts;
- sanitized deployment examples.

## Does Not Own

- live node-network truth;
- exact NODA/DNS/firewall/Octelium facts;
- Edge Client installer/runtime;
- MicroDAO web UI;
- city frontend;
- Supabase production writes;
- private production runbooks.

Public `api.daarion.city` ingress and production deployment evidence belong in
the private operations repository.

`device_backend_profiles` activation belongs to the MicroDAO app lane only after
public health returns HTTP 200.

## Related Repositories

- `DAARION-DAO/daarion-ai-city` - public city frontend.
- `DAARION-DAO/loval-echoes` - MicroDAO app and Connect Device UI.
- `DAARION-DAO/daarion-edge-client` - user-installed Edge Client.
- `IvanTytar/microdao-daarion` - private operations truth.

## Public / Private Boundary

Public repositories may contain source code, public contracts, sanitized docs,
generic examples, and non-sensitive roadmap notes.

This repository must not contain live NODA/IP/DNS/firewall/Octelium/deployment
truth, private production runbooks, incidents, secrets, operator access details,
or private infrastructure evidence.

Live node-network operations truth belongs in the private
`IvanTytar/microdao-daarion` repository.
