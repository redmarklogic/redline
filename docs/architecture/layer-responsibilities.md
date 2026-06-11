# Layer Responsibilities — Phase 1 Stack

Grounding decision: ADR-024 (Django web stack, single service). Engine boundary:
ADR-002. HTTP contract: ADR-018. Hosting: ADR-022/ADR-023.

Living document: update when a layer gains or loses a responsibility, in the same
change that moves it. Layer *enforcement* (import direction) remains authoritative in
`pyproject.toml` under `[tool.importlinter]`; this table records *ownership*.

## The stack at a glance

```
Browser (server-rendered HTML + vendored HTMX)
    |
Django web shell        views, templates, allauth, sessions, quota middleware,
    |                   ADR-018 error-envelope middleware, contrib.admin
    |__ calls __________ build_skeleton(typed inputs) -> DOCX bytes
    |
Generator core          functions / schemas / domain (plain Python, framework-free)
    |
DocumentFacade          sole owner of python-docx types (ADR-002)
    |
Platform state          Cloud SQL via Django ORM (users, sessions, quota, audit log)
    |
Infrastructure          Cloud Run (single service/env) + Terraform (Brent's domain)
```

## Responsibility table

| Layer | Owns | Must NOT contain | Primary code/config home |
|---|---|---|---|
| **Domain core** (`domain`, `schemas`, `functions`) | Geotechnical concepts, `build_skeleton` orchestration, validation schemas, business rules | Any web-framework import (Django, FastAPI), ORM models, HTTP/session/user concepts, python-docx types | `src/` domain, schemas, and functions packages |
| **Document engine facade** | All python-docx construction; engine swap point | Business logic; knowledge of users, quota, or HTTP | Facade implementation per ADR-002 |
| **Django web shell** | URL routing, plain views serving `POST /skeletons` + health per the ADR-018 envelope, templates + vendored HTMX, request validation (Pydantic carried over from the walking skeleton), error-envelope middleware, sign-in (django-allauth, per ADR-025), sessions, quota enforcement (model + middleware/decorator) | Geotechnical concepts modelled as Django ORM models; any document-engine type; direct python-docx use | Django project package (new in the pivot) |
| **Platform state** | User accounts, sessions, quota counters (configurable cap, default 3, non-renewable), append-only audit log (timestamp, user, parameters, template/model version, output hash). No document blobs. | Geotechnical/domain entities; deployment configuration (env vars stay env vars per ADR-021) | Django ORM models + migrations; Cloud SQL (Sydney) |
| **Back office** | Founder support actions at launch: inspect users/quota, reset a quota, block a user, edit the quota cap | Custom-built admin pages (use `django.contrib.admin` as-is); production SQL-console poking as routine practice | `django.contrib.admin` registration of platform models |
| **Infrastructure** | Single Cloud Run service per environment, Cloud SQL instance + connection strategy, Secret Manager bindings (OAuth client secrets, Sydney-pinned), scale-to-zero with demo-warm flip, budget alerts, load balancer/DNS | Application logic; a second runtime service (requires a new ADR) | Terraform (Brent); manual OAuth registrations documented per ADR-020 exception process |

## The guardrail (ADR-002 / ADR-024, hook-expressible)

1. **No framework leakage into the core:** no module in the domain, schemas, or
   functions packages may import Django (mirror of the prior FastAPI guardrail).
   Enforced via import-linter contracts; violation is a defect, not a style choice.
2. **Django models are platform state only.** A geotechnical concept appearing as a
   Django ORM model is the violation signal — domain stays plain Python.
3. **The web shell never constructs documents.** It calls `build_skeleton` with typed
   inputs and receives bytes; only the facade touches python-docx (ADR-002).
4. **Stateless generator, stateful shell.** The generator layer is pure and
   horizontally indifferent; all per-user state lives in the platform-state layer.
   Anything that breaks this framing is an architectural escalation to Peter.
