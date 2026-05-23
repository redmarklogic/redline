# Tasks: Mobile Bridge for Persona Access

**Input**: [plan.md](plan.md)
**Status**: **PARKED** (2026-04-19). GitHub Copilot is accessible via the GitHub
Mobile app, making this custom Telegram bridge unnecessary. See
`docs/product/strategy/decisions/parked-decisions.md` P-025.

**Prerequisites**: Developer has answered the four Open Questions in `plan.md`. Telegram
bot created via BotFather (token captured). Azure subscription accessible via Azure MCP
or `az login`.
**Testing conventions**: `python-testing-unit` and `python-testing-api` skills.

> **Hands-off rules for the executing agent**
>
> - Use **Azure MCP tools** for all Azure resource operations. Fall back to `az` CLI
>   (invoked via `execution_subagent`) only when no MCP tool covers the operation.
> - Use **`gh` CLI** (invoked via `execution_subagent`) for all GitHub configuration:
>   secrets, OIDC, workflows, branch protection.
> - Never instruct the developer to click in a portal. The only manual steps are: (a)
>   creating the bot via BotFather, (b) pasting the bot token + GitHub PAT into one-time
>   prompts, (c) tapping HITL approvals on their phone during smoke tests.

## Phase 0: Architecture Decision Records

- [ ] T001 [Phase 0] Create `docs/adr/adr-010-telegram-and-azure-container-apps.md`
      recording D2 and D6.
- [ ] T002 [Phase 0] Create `docs/adr/adr-011-session-state-azure-table-storage.md`
      recording D3.
- [ ] T003 [Phase 0] Create `docs/adr/adr-012-notebooklm-desktop-only.md`
      recording D9.
- [ ] T004 [Phase 0] Update `docs/adr/` index in `mkdocs.yml` if applicable.

## Phase 1: FastAPI skeleton + security

### Project setup

- [ ] T010 [Phase 1] Add deps: `uv add fastapi 'uvicorn[standard]' httpx pydantic-settings`
- [ ] T011 [Phase 1] Add test deps: `uv add --dev pytest-asyncio respx`
- [ ] T012 [Phase 1] Update `pyproject.toml`: add `src/mobile_bridge` to
      `tool.hatch.build.targets.wheel.packages`; add `mobile_bridge` to
      `tool.importlinter.root_packages`; add `mobile_bridge layers` and
      `mobile_bridge independence` contracts per plan.md.
- [ ] T013 [Phase 1] Create package skeleton: `src/mobile_bridge/{__init__.py,py.typed,app.py,config.py}`
      and security/telegram/copilot/state subpackages with `__init__.py`.
- [ ] T014 [Phase 1] Create test package skeleton: `tests/mobile_bridge/{__init__.py,conftest.py}`
      with subpackages mirroring source.

### Settings (TDD)

- [ ] T020 [Phase 1] Write failing tests in `tests/mobile_bridge/test_config.py`:
      missing required env raises `ValidationError`; allowlist parses comma-separated
      ints; `MOBILE_MODE` parses to bool.
- [ ] T021 [Phase 1] Confirm fail: `.venv\Scripts\activate; python -m pytest tests/mobile_bridge/test_config.py -v`
- [ ] T022 [Phase 1] Implement `config.py` with `Settings(BaseSettings)`. No defaults
      for any secret or required field.

### Webhook security middleware (TDD)

- [ ] T030 [Phase 1] Write failing tests in `tests/mobile_bridge/security/test_webhook_auth.py`:
      missing/invalid `X-Telegram-Bot-Api-Secret-Token` returns 401; valid token passes.
- [ ] T031 [Phase 1] Implement `security/webhook_auth.py` (FastAPI dependency).
- [ ] T032 [Phase 1] Write failing tests in `tests/mobile_bridge/security/test_authz.py`:
      non-allowlisted chat_id returns silent 200 with no downstream call.
- [ ] T033 [Phase 1] Implement `security/authz.py`.

### App factory + health endpoint (TDD)

- [ ] T040 [Phase 1] Write failing test in `tests/mobile_bridge/test_app.py`: `/health`
      returns 200 with `{"status": "ok"}`.
- [ ] T041 [Phase 1] Implement `app.py` with FastAPI factory and `/health`.

### Acceptance Gate

- [ ] T050 [Phase 1] `pytest tests/mobile_bridge/ -v` -- all green.
- [ ] T051 [Phase 1] `ruff check src/mobile_bridge tests/mobile_bridge` -- clean.
- [ ] T052 [Phase 1] `mypy src/mobile_bridge` -- clean.
- [ ] T053 [Phase 1] `python -m importlinter` -- clean.

## Phase 2: Telegram client

- [ ] T100 [Phase 2] Write failing tests in `tests/mobile_bridge/telegram/test_client.py`
      using `respx`: `send_message` posts correct payload; `answer_callback_query`
      acknowledges callback; long messages split on code-block boundaries.
- [ ] T101 [Phase 2] Implement `telegram/client.py` with `httpx.AsyncClient`.
- [ ] T102 [Phase 2] Implement `telegram/keyboards.py`: persona picker, HITL approve/deny.
- [ ] T103 [Phase 2] Write failing tests in `tests/mobile_bridge/telegram/test_markdown.py`:
      MarkdownV2 escaping for special characters; preserves fenced code blocks.
- [ ] T104 [Phase 2] Implement `telegram/markdown.py`.
- [ ] T110 [Phase 2] Acceptance gate: pytest, ruff, mypy, importlinter all clean.

## Phase 3: Persona loader

- [ ] T200 [Phase 3] Write failing tests in `tests/mobile_bridge/copilot/test_personas.py`:
      parses YAML frontmatter from a fixture `.agent.md`; extracts name, tools, system
      prompt; with `MOBILE_MODE=true`, Ron's tool list excludes any tool whose name
      contains `notebooklm` or `redline_research`.
- [ ] T201 [Phase 3] Create test fixtures `tests/mobile_bridge/fixtures/{ron,mark}.agent.md`
      mirroring real persona structure.
- [ ] T202 [Phase 3] Implement `copilot/personas.py` with `Persona` Pydantic model and
      `load_persona(name)` function. Use `pathlib` only (per `python-paths` skill).
- [ ] T210 [Phase 3] Acceptance gate: pytest, ruff, mypy, importlinter all clean.

## Phase 4: State store (Azure Table Storage)

### Local emulator setup

- [ ] T300 [Phase 4] Document Azurite usage in `tests/mobile_bridge/conftest.py`:
      pytest fixture starts Azurite via `docker run` if not already running, sets
      connection string env var.
- [ ] T301 [Phase 4] Add `azure-data-tables azure-identity` to runtime deps.

### Entity models (TDD)

- [ ] T310 [Phase 4] Write failing tests in `tests/mobile_bridge/state/test_models.py`:
      `SessionEntity` and `PendingApprovalEntity` round-trip through `to_entity()` /
      `from_entity()`; TTL field is set correctly.
- [ ] T311 [Phase 4] Implement `state/models.py` with frozen Pydantic models.

### Store (TDD against Azurite)

- [ ] T320 [Phase 4] Write failing tests in `tests/mobile_bridge/state/test_store.py`:
      `get_or_create_session` returns existing or creates new; `delete_session`
      removes entry; `create_pending_approval` + `resolve_pending_approval` happy path;
      `resolve_pending_approval` on missing/expired returns `None`.
- [ ] T321 [Phase 4] Implement `state/store.py` using `TableServiceClient` +
      `DefaultAzureCredential`.
- [ ] T330 [Phase 4] Acceptance gate: pytest, ruff, mypy, importlinter all clean.

## Phase 5: Copilot SDK session manager

- [ ] T400 [Phase 5] Add `github-copilot-sdk` (Python preview) to runtime deps.
- [ ] T410 [Phase 5] Write failing tests in `tests/mobile_bridge/copilot/test_session.py`
      with a mocked SDK client: new session created on first message; existing session
      resumed on follow-up; `/reset` deletes state; persona switch creates new session.
- [ ] T411 [Phase 5] Implement `copilot/session.py` with `SessionManager` class.
- [ ] T420 [Phase 5] Write failing tests in `tests/mobile_bridge/telegram/test_webhook.py`:
      `/start` returns persona-picker keyboard; persona-pick callback creates session;
      regular message routes to active session and replies.
- [ ] T421 [Phase 5] Implement `telegram/webhook.py` orchestrating settings, store,
      session manager, and client.
- [ ] T430 [Phase 5] Acceptance gate: pytest, ruff, mypy, importlinter all clean.

## Phase 6: HITL pre-tool-use hook

- [ ] T500 [Phase 6] Define `SAFE_TOOLS` allowlist in `copilot/hooks.py` (read-only
      operations only; document each entry).
- [ ] T510 [Phase 6] Write failing tests in `tests/mobile_bridge/copilot/test_hooks.py`:
      safe tool fast-path skips approval; sensitive tool sends inline keyboard, awaits
      Event; approve callback resolves Event with True; deny callback resolves False;
      timeout (mocked) defaults to deny.
- [ ] T511 [Phase 6] Implement `copilot/hooks.py` with `pre_tool_use` registration and
      asyncio.Event-based suspend/resume mechanism.
- [ ] T520 [Phase 6] Write failing tests in `tests/mobile_bridge/telegram/test_callback.py`:
      `/telegram/callback` resolves the matching pending approval; unknown approval_id
      returns 200 with no-op (avoid retry storms).
- [ ] T521 [Phase 6] Implement callback handler in `telegram/webhook.py`.
- [ ] T530 [Phase 6] Acceptance gate: pytest, ruff, mypy, importlinter all clean.

## Phase 7: Containerization

- [ ] T600 [Phase 7] Create `deploy/mobile_bridge/Dockerfile` (multi-stage, slim,
      non-root, copies `.github/agents/` into image).
- [ ] T601 [Phase 7] Create `deploy/mobile_bridge/.dockerignore`.
- [ ] T602 [Phase 7] Local validation (executed by agent via `execution_subagent`):
      `docker build -t redline-mobile-bridge:dev -f deploy/mobile_bridge/Dockerfile .`
- [ ] T603 [Phase 7] Local smoke test: `docker run --env-file .env.local -p 8000:8000 redline-mobile-bridge:dev`,
      hit `/health` from host.

## Phase 8: Azure provisioning (hands-off)

> The executing agent invokes Azure MCP tools for each step. If a specific tool is
> unavailable, fall back to `az` CLI via `execution_subagent`. Capture all resource
> IDs in `deploy/mobile_bridge/.azure-state.json` (gitignored).

- [ ] T700 [Phase 8] Create `deploy/mobile_bridge/bicep/main.bicep` and
      `parameters.json` mirroring all resources below (for reproducibility / DR).
- [ ] T710 [Phase 8] Via Azure MCP: create resource group `rg-redline-mobile` in the
      developer's chosen region (from Open Question 3).
- [ ] T711 [Phase 8] Via Azure MCP: create ACR `crredlinemobile` (Basic SKU,
      admin disabled).
- [ ] T712 [Phase 8] Via Azure MCP: create storage account `stredlinemobile` and
      tables `sessions`, `pending_approvals`.
- [ ] T713 [Phase 8] Via Azure MCP: create Key Vault `kv-redline-mobile` (RBAC mode).
- [ ] T714 [Phase 8] Generate webhook secret (64-char URL-safe random) and store as
      Key Vault secret `telegram-webhook-secret`.
- [ ] T715 [Phase 8] Prompt developer once for the Telegram bot token; store as Key
      Vault secret `telegram-bot-token`. Do NOT log the value.
- [ ] T716 [Phase 8] Prompt developer once for the GitHub PAT (scope per Open Q1);
      store as Key Vault secret `github-pat`.
- [ ] T717 [Phase 8] Via Azure MCP: create Log Analytics workspace `log-redline-mobile`.
- [ ] T718 [Phase 8] Via Azure MCP: create Container Apps Environment `cae-redline-mobile`
      bound to the workspace.
- [ ] T719 [Phase 8] Via Azure MCP: create Container App `ca-redline-mobile`:
      system-assigned managed identity, min=0/max=1 replicas, external HTTPS ingress
      on port 8000, placeholder image, env vars per plan, secret refs from Key Vault.
- [ ] T720 [Phase 8] Via Azure MCP: assign role `Key Vault Secrets User` on the vault
      to the Container App's managed identity.
- [ ] T721 [Phase 8] Via Azure MCP: assign role `Storage Table Data Contributor` on
      the storage account to the managed identity.
- [ ] T722 [Phase 8] Via Azure MCP: assign role `AcrPull` on the registry to the
      managed identity.
- [ ] T730 [Phase 8] Run `az deployment group what-if` against the Bicep template;
      verify it shows zero deltas (the Bicep matches what was actually provisioned).
- [ ] T731 [Phase 8] Set Azure budget alert at $5/month on `rg-redline-mobile` via
      Azure MCP.

## Phase 9: GitHub configuration (hands-off via `gh` CLI)

> All commands invoked by the agent via `execution_subagent`.

- [ ] T800 [Phase 9] Via Azure MCP: create AAD app registration + service principal
      for OIDC (`spn-redline-mobile-deploy`).
- [ ] T801 [Phase 9] Via Azure MCP: create federated credential binding the SP to
      `repo:harell/redline:ref:refs/heads/master`.
- [ ] T802 [Phase 9] Via `gh` CLI: set repo secrets `AZURE_CLIENT_ID`,
      `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`,
      `AZURE_CONTAINER_APP`, `ACR_LOGIN_SERVER`.
- [ ] T810 [Phase 9] Create `.github/workflows/mobile-bridge-deploy.yml`:
      - Trigger on push to `master` affecting `src/rl/mobile_bridge/**`,
        `deploy/mobile_bridge/**`, `.github/agents/{ron,mark}.agent.md`,
        `.github/workflows/mobile-bridge-deploy.yml`.
      - Steps: checkout, `azure/login` via OIDC, `docker build` + `az acr login` +
        push, `az containerapp update` to new image revision.
- [ ] T811 [Phase 9] Trigger first run via `gh workflow run mobile-bridge-deploy.yml`
      and watch with `gh run watch`. Confirm exit 0.
- [ ] T812 [Phase 9] (Optional, ask developer) Enable branch protection on `master`
      requiring the `mobile-bridge-deploy` check via `gh api`.

## Phase 10: Webhook registration + smoke test

- [ ] T900 [Phase 10] Via Azure MCP: fetch Container App FQDN.
- [ ] T901 [Phase 10] Via Telegram Bot API (curl): `setWebhook` with the FQDN +
      secret token. Verify success response.
- [ ] T902 [Phase 10] Prompt developer to send `/start` from their phone. Wait for
      confirmation.
- [ ] T903 [Phase 10] Via Azure MCP / Log Analytics query: confirm the request
      arrived and was authorized.
- [ ] T904 [Phase 10] Prompt developer to pick `Mark`, ask a question, confirm reply.
- [ ] T905 [Phase 10] Repeat with `Ron` (after `/reset`).
- [ ] T906 [Phase 10] Trigger a sensitive-tool path (forced via a test command);
      verify HITL prompt arrives and `Deny` aborts the action.

## Phase 11: Hardening

- [ ] TA00 [Phase 11] Add structured JSON logging with redaction filter (no message
      bodies, no secrets). Tests in `tests/mobile_bridge/test_logging.py`.
- [ ] TA10 [Phase 11] Implement per-`chat_id` token bucket (10 msg/min) in
      `security/rate_limit.py`. Tests cover limit reached and reset.
- [ ] TA20 [Phase 11] Implement conversation history pruning in `copilot/session.py`
      (keep last 20 turns; summarize older via SDK). Tests with mocked SDK.
- [ ] TA30 [Phase 11] Configure App Insights alerts via Azure MCP:
      cost > $0.50/day, error rate > 5% over 15 min.
- [ ] TA40 [Phase 11] Run `doc-updater` skill to refresh `README.md`,
      `docs/CODEMAPS/`, and `docs/architecture/` with the new subpackage.
- [ ] TA50 [Phase 11] Final acceptance gate: full pytest, ruff, mypy, importlinter,
      deptry all clean. `pre-commit run --all-files` clean.

## Definition of Done

- All tasks above checked.
- All acceptance gates passed.
- Developer has successfully completed Scenarios 1-6 from `spec.md` from a real mobile
  device, with screenshots attached to the PR.
- Cost dashboard after 7 days shows < $2 actual spend.
- ADRs 005, 006, 007 merged.
- Final PR merged to `master`; the `mobile-bridge-deploy` workflow has run successfully
  at least twice (initial deploy + one update).
