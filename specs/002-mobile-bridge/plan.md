# Implementation Plan: Mobile Bridge for Persona Access

**Date**: 2026-04-18 | **Spec**: [spec.md](spec.md)
**Status**: **PARKED** (2026-04-19). GitHub Copilot is accessible via the GitHub
Mobile app, making this custom Telegram bridge unnecessary. See
`docs/product/strategy/decisions/parked-decisions.md` P-025.

## Summary

Build a cloud-hosted FastAPI service that bridges Telegram messages to the GitHub
Copilot SDK, exposing the Ron and Mark personas to the developer's mobile device. The
service runs on Azure Container Apps (Consumption plan), persists conversation state
in Azure Table Storage, and gates sensitive tool calls behind a Human-in-the-Loop
inline-keyboard approval flow.

The implementation is **hands-off**: every Azure resource is provisioned by the agent
via Azure MCP tool calls (or `az` CLI as fallback); every GitHub configuration is
applied via the `gh` CLI. The developer's only manual steps are:
1. Create the Telegram bot via BotFather (one-time, ~30 seconds)
2. Approve HITL prompts that arrive on their phone
3. Type the four answers to `Open Questions` (below)

## Technical Context

**Language**: Python 3.12
**Package manager**: uv
**Web framework**: FastAPI + uvicorn
**Testing**: pytest + httpx + respx (per `python-testing-unit` and `python-testing-api` skills)
**Project layout**: Monorepo (per `.specify/architecture.yml`)
**New package**: `src/mobile_bridge/` -- sibling package alongside `rl` (developer
decision: keep the mobile bridge isolated from the geotechnical domain; different
deployment unit with its own dependency footprint and rate of change)
**Dev OS**: Windows | **Deploy OS**: Linux (container)
**Domain modeling**: Pydantic v2 BaseModel for settings, request/response, table entities
**Key Python deps**: `fastapi`, `uvicorn[standard]`, `httpx`, `pydantic-settings`,
`azure-data-tables`, `azure-identity`, `azure-keyvault-secrets`, `github-copilot-sdk`
(public preview, per the architectural analysis)
**Test deps**: `pytest`, `pytest-asyncio`, `respx`, `pytest-mock`
**Container base**: `python:3.12-slim` multi-stage with `uv` install
**Cloud**: Azure Container Apps (Consumption), Azure Container Registry (Basic),
Azure Table Storage, Azure Key Vault, Log Analytics
**CI/CD**: GitHub Actions with OIDC federated credential (no stored secrets)

## Concept-to-Plan Phase Mapping

No concept doc -- spec was derived from a single architectural analysis conversation.
Phase numbering is plan-native.

## Design Decisions

| # | Decision | Choice | Rationale |
| --- | --- | --- | --- |
| D1 | Service location | `src/mobile_bridge/` sibling package | Developer decision: keep mobile bridge isolated from geotechnical domain. Different deployment unit, dependency footprint, and rate of change. |
| D2 | Hosting | Azure Container Apps Consumption plan | User has existing Azure account; scale-to-zero gives < $1/mo idle cost; supports min-replicas=0. |
| D3 | State store | Azure Table Storage | Cheap, serverless, no Redis instance to manage. Sufficient for K/V conversation state. |
| D4 | Secrets | Azure Key Vault + managed identity | No long-lived secrets in code, GitHub Actions, or env files. |
| D5 | CI/CD auth | GitHub Actions OIDC federated credential | Eliminates stored Azure credentials in GitHub Secrets. |
| D6 | Mobile UI | Telegram Bot API | Native Markdown, inline keyboards, no app-store deployment. |
| D7 | Streaming | Defer -- send complete responses per turn | Telegram lacks native streaming; progressive `editMessage` calls hit rate limits. v2 if needed. |
| D8 | Persona source of truth | `.github/agents/rl.ron.agent.md`, `.github/agents/rl.mark.agent.md` baked into the container image at build time | Single source of truth; same files used by desktop Copilot. |
| D9 | NotebookLM filtering | Strip NotebookLM/`redline-research` tools from Ron's tool list at persona load time when running in mobile mode | Headless OAuth not possible; failing closed prevents broken-tool errors. |
| D10 | HITL classifier | Allowlist of safe tool names (read-only); everything else triggers approval | Fail-closed default; explicit safe-list reviewed by a human. |
| D11 | Provisioning | Azure MCP tool calls preferred; fall back to `az` CLI; Bicep template stored in repo for reproducibility and `what-if` validation | Hands-off requirement; reproducibility for disaster recovery. |
| D12 | GitHub configuration | `gh` CLI for all secrets, OIDC bindings, branch protection | Hands-off requirement; CLI is scriptable and auditable. |
| D13 | Allowlist storage | Comma-separated env var on the Container App | Single-user; full Pydantic settings validation. No need for a DB-backed ACL in v1. |
| D14 | Container hardening | Non-root user, read-only root filesystem, no shell in distroless-equivalent slim image | Security skill compliance; reduces attack surface. |

## Domain Impact

**Modularity assessment**: New top-level sibling package `src/mobile_bridge/`. Signals:
different bounded context (mobile presentation vs. geotechnical analysis), different
deployment unit (container app vs. library), distinct dependency footprint (FastAPI,
Telegram, Azure SDKs), developer-explicit decision to keep packages isolated.

**New packages**: `mobile_bridge` -- new sibling package under `src/`.

**New subpackages**: `src/mobile_bridge/` with internal layers:
- `mobile_bridge/config.py` -- Pydantic settings
- `mobile_bridge/app.py` -- FastAPI factory + lifespan
- `mobile_bridge/telegram/` -- inbound webhook + outbound client
- `mobile_bridge/copilot/` -- session manager, persona loader, HITL hook
- `mobile_bridge/state/` -- Table Storage client and entity models
- `mobile_bridge/security/` -- webhook auth, allowlist authz

**Bounded context changes**: New "Mobile Presentation" bounded context alongside the
existing "Geotechnical Analysis" context in `rl`.

**Import-linter contract updates**:

```toml
[[tool.importlinter.contracts]]
name = "mobile_bridge layers"
type = "layers"
layers = [
  "mobile_bridge.app",
  "mobile_bridge.telegram | mobile_bridge.copilot",
  "mobile_bridge.state | mobile_bridge.security",
  "mobile_bridge.config",
]

[[tool.importlinter.contracts]]
name = "mobile_bridge independence"
type = "independence"
modules = ["rl", "mobile_bridge"]
```

## Phased Delivery

### Phase 0 -- Architecture Decision Records (no code)

Create three ADRs documenting the binding decisions:
- **ADR-010**: Telegram + Azure Container Apps for mobile persona access (records D2, D6)
- **ADR-011**: Session persistence via Azure Table Storage (records D3)
- **ADR-012**: NotebookLM scoped to desktop only -- Ron's mobile tool list filtered (records D9)

### Phase 1 -- FastAPI skeleton, settings, security middleware

Create the package skeleton with `app.py`, `config.py` (Pydantic settings, no defaults
per `AGENTS.md`), and the `/health` and `/telegram/webhook` endpoints. Add webhook
secret-token verification and chat_id allowlist authorization.

TDD per `test-driven-development` skill: failing tests for 401 on bad signature,
silent-200 on non-allowlisted chat, 200 on valid request, 503 on missing required env.

### Phase 2 -- Telegram client + Markdown helpers

Build a thin `httpx.AsyncClient` wrapper for `sendMessage`, `answerCallbackQuery`,
`setWebhook`. Add Markdown V2 escaping helper and a long-message splitter respecting
4096-char limit and code-block boundaries.

TDD with `respx` mocking: send_message happy path, escaping correctness, splitter on
boundary edge cases.

### Phase 3 -- Persona loader

Read `.github/agents/{ron,mark}.agent.md` from the image, parse YAML frontmatter, build
a `Persona` Pydantic model. Apply NotebookLM tool filter to Ron when env flag
`MOBILE_MODE=true` is set. Failing tests first: parse fixture files, assert tool list
filtered, assert system prompt extracted.

### Phase 4 -- State store (Azure Table Storage)

Two tables: `sessions` (PK = `chat_id`, contains `session_id` + active persona) and
`pending_approvals` (PK = `approval_id`, contains pending tool invocation + TTL).

Use `azure-data-tables` SDK + `DefaultAzureCredential`. Failing tests with the local
Azurite emulator (run via `docker run mcr.microsoft.com/azure-storage/azurite`).

### Phase 5 -- Copilot SDK session manager

Wrap `createSession()` / `resumeSession()` from the Copilot SDK. Bind the active
persona's system prompt and tool list. Map `chat_id` to `session_id` via the state
store. Implement `/start`, `/reset`, persona-pick callback, and message-handling flow.

TDD with mocked SDK client: new session creation, resume on follow-up, reset clears
state, persona switch creates new session.

### Phase 6 -- HITL pre-tool-use hook

Register `pre_tool_use` SDK hook. On invocation:
1. Classify tool against `SAFE_TOOLS` allowlist; if safe, allow immediately.
2. Otherwise, persist a `pending_approval` row, send Telegram inline keyboard, and
   suspend the SDK call (await an asyncio Event).
3. `/telegram/callback` resolves the Event with the user's choice.
4. 5-minute timeout defaults to deny.

TDD with mocked SDK and Telegram: approve path, deny path, timeout path, safe-tool
fast-path.

### Phase 7 -- Containerization

Multi-stage `Dockerfile`:
- Stage 1: `python:3.12-slim` + `uv`, install deps to `/opt/venv`
- Stage 2: `python:3.12-slim` runtime, copy venv, copy source, copy `.github/agents/`,
  drop to non-root user, set `read_only_root_filesystem`-compatible paths

Add `.dockerignore`. Local validation: `docker build`, `docker run`, smoke test via
ngrok-forwarded webhook (one-time, before Azure deploy).

### Phase 8 -- Azure provisioning (hands-off via Azure MCP)

The agent invokes Azure MCP tool calls (or `az` CLI as fallback) to:

1. Create resource group `rg-redline-mobile` in the developer's chosen region.
2. Create ACR `crredlinemobile` (Basic SKU).
3. Create storage account `stredlinemobile` + tables `sessions`, `pending_approvals`.
4. Create Key Vault `kv-redline-mobile` with secrets:
   - `telegram-bot-token`
   - `telegram-webhook-secret` (agent generates a 64-char random token)
   - `github-pat` (developer pastes once into a one-time prompt)
5. Create Log Analytics workspace `log-redline-mobile`.
6. Create Container Apps Environment `cae-redline-mobile` linked to the workspace.
7. Create Container App `ca-redline-mobile`:
   - System-assigned managed identity
   - Min replicas: 0, Max replicas: 1
   - Ingress: external, port 8000, HTTPS only
   - Image: placeholder `mcr.microsoft.com/azuredocs/aks-helloworld:v1` (replaced by CI/CD)
   - Env vars: `GITHUB_REPO`, `AZURE_STORAGE_ACCOUNT`, `KEY_VAULT_URI`, `MOBILE_MODE=true`, `LOG_LEVEL=INFO`
   - Secret refs from Key Vault for the three secrets above
8. Grant the managed identity:
   - `Key Vault Secrets User` on the vault
   - `Storage Table Data Contributor` on the storage account
   - `AcrPull` on the registry

A `deploy/mobile_bridge/bicep/main.bicep` template captures the same resources for
reproducibility and disaster recovery. The agent runs `az deployment group what-if`
before any apply.

### Phase 9 -- GitHub configuration (hands-off via `gh` CLI)

The agent invokes `gh` CLI to:

1. Create an Azure AD application + service principal for OIDC federation (via
   Azure MCP).
2. Create a federated credential binding the SP to `repo:harell/redline:ref:refs/heads/master`.
3. Set GitHub repository secrets via `gh secret set`:
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_RESOURCE_GROUP`
   - `AZURE_CONTAINER_APP`
   - `ACR_LOGIN_SERVER`
4. Add the GitHub Actions workflow `.github/workflows/mobile-bridge-deploy.yml`:
   - Trigger: push to `master` affecting `src/rl/mobile_bridge/**`, `deploy/mobile_bridge/**`,
     `.github/agents/{ron,mark}.agent.md`
   - Steps: checkout, login via OIDC, build + push to ACR, update Container App revision
5. Optional: enable branch protection on `master` for the workflow check via
   `gh api` (only if the developer wants it).

### Phase 10 -- Webhook registration + smoke test

After the first successful deploy:
1. The agent fetches the Container App FQDN via Azure MCP.
2. The agent calls Telegram's `setWebhook` with the FQDN + secret token.
3. The agent prompts the developer to send `/start` from their phone.
4. The agent verifies the round-trip via Application Insights logs.

### Phase 11 -- Hardening

- Structured JSON logging (no message bodies, no secrets, redaction filter)
- Per-`chat_id` token-bucket rate limiting (10 messages/min)
- Conversation history pruning (keep last 20 turns; summarize older via Copilot SDK)
- Daily Application Insights alert: cost > $0.50/day, error rate > 5%

## Acceptance Gates

Each phase ends with:
1. `pytest` green for tests added in that phase
2. `ruff check` clean
3. `mypy` clean (strict mode per `python-typing` skill)
4. `import-linter` clean
5. (Phase 7+) `docker build` succeeds
6. (Phase 8+) Azure `what-if` shows only intended deltas
7. (Phase 9+) GitHub Actions workflow run succeeds end-to-end

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Copilot SDK Python bindings not yet stable | Pin to a tested version; abstract behind a thin wrapper so the SDK can be swapped. |
| Telegram webhook flapping during ACA cold start | Cold start ~2-3s; Telegram retries on 5xx. Health-probe warms the container. |
| HITL fatigue (too many approvals) | Curated `SAFE_TOOLS` allowlist for read-only ops; revisit in Phase 11. |
| GitHub PAT scope creep | Explicit `repo:read` scope; rotate quarterly via Key Vault versioning. |
| Cost overrun | Daily Azure budget alert at $5; auto-disable Container App ingress on alert. |
| Telegram bot token leak | Rotate via BotFather + Key Vault new version; old version stays revocable for 30 days. |
| Azure MCP tool unavailable | Fall back to `az` CLI invoked via execution subagent; same Bicep template applies. |

## Open Questions for the Developer

These four answers gate Phase 0 kickoff. The agent will not proceed without them.

1. **GitHub PAT scope**: Confirm `repo:read` only is acceptable, or do you want write
   access (PR comments, issue creation) from mobile? *(Default recommendation: read-only.)*
2. **Allowlist**: Just your personal Telegram `chat_id`, or also a backup chat (e.g.,
   a private group with you only)?
3. **Azure region**: Preferred region? *(Default: `westeurope` for EU latency, `eastus` for US.)*
4. **Streaming**: Wait for full response before sending (simple, slower felt latency)
   or progressively `editMessage` as tokens arrive (complex, hits Telegram rate
   limits)? *(Default: full response.)*

## Skills Applied During Execution

- `spec-kit` -- this plan
- `test-driven-development` + `python-testing-unit` + `python-testing-api` -- Phases 1-6
- `python-style`, `python-typing`, `python-function-design`, `python-class-design`,
  `python-error-handling`, `python-linting`, `python-domain-modeling`,
  `python-module-structure` -- throughout
- `python-paths` -- Phase 3 (persona file resolution via `importlib.resources` or `pathlib` relative to package root)
- `security` -- Phases 1, 4, 6, 7, 8, 9
- `python-static-checks` -- end of every phase
- `version-control` + `git-push-batched` -- at phase boundaries
- `verification-before-completion` -- before claiming each phase done
- `doc-updater` -- Phase 11 (update README, codemap with the new subpackage)
