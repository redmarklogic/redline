# Feature Specification: Mobile Bridge for Persona Access

**Branch**: `feature/mobile-bridge`
**Created**: 2026-04-18
**Status**: **PARKED** (2026-04-19). GitHub Copilot is accessible via the GitHub
Mobile app, making this custom Telegram bridge unnecessary. See
`docs/product/strategy/decisions/parked-decisions.md` P-025.

## Source Document Reconciliation

| Source | Authority | Status |
| --- | --- | --- |
| Conversation context (architectural analysis report, 2026-04-18) | Primary -- problem framing | Captured below |
| `.github/agents/rl.ron.agent.md` (existing) | Binding -- persona definition | No conflicts |
| `.github/agents/rl.mark.agent.md` (existing) | Binding -- persona definition | No conflicts |
| `.agents/skills/notebooklm-mcp/SKILL.md` | Supporting -- auth model constraint | No conflicts |
| `.agents/skills/security/SKILL.md` | Binding -- secrets handling | No conflicts |
| `AGENTS.md` (Python/uv/env-var conventions) | Binding -- coding standards | No conflicts |

### Resolved Conflicts

None.

### Resolved Ambiguities

| Question | Answer |
| --- | --- |
| Which agents to expose on mobile? | Ron and Mark (both) |
| Local uncommitted file access required? | No -- pushed GitHub repo state is sufficient |
| Hosting platform? | Azure Container Apps (Consumption plan) -- existing Azure account |
| NotebookLM via mobile? | Out of scope -- headless auth not possible (browser-only OAuth) |

## Scope

This spec covers the **Mobile Bridge service** that allows the developer to chat with
the Ron and Mark personas from a mobile device (Telegram) when away from a desktop IDE.

In scope:
- Telegram bot front-end with persona picker
- Cloud-hosted FastAPI service backed by GitHub Copilot SDK
- Persistent session state (conversation continuity across messages and devices)
- Human-in-the-Loop (HITL) approval gate for any tool that mutates state
- Hands-off provisioning via `gh` CLI and Azure MCP tools (no manual portal clicks)

Out of scope (explicitly):
- Ron's NotebookLM-backed research (browser auth incompatible with cloud hosting)
- Multi-user support (single-user allowlist only)
- Voice/image multimodal input (text only in v1)
- Agent write access to the repo (read-only PAT in v1)
- Custom mobile app (Telegram is the UI)

## Scenarios (mandatory)

### Scenario 1 -- Send `/start` and pick a persona

The developer opens the Telegram bot from their phone and sends `/start`. The bot
replies with a message offering two inline-keyboard buttons: `Ron` and `Mark`. Tapping
`Mark` creates a new Copilot session bound to the Mark persona and replies confirming
the active persona.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| --- | --- | --- | --- | --- |
| 1 | 3 | 95 | 2 | 1.4 |

**Independent test**: From Telegram, send `/start`, tap `Mark`, observe a confirmation
message naming the persona within 5 seconds.

**Acceptance criteria**:
1. **Given** an authorized `chat_id`, **when** `/start` is sent, **then** the bot replies
   with an inline keyboard containing `Ron` and `Mark` within 3 seconds.
2. **Given** a `Mark` selection callback, **when** processed, **then** a new session is
   created, persisted in storage with the `chat_id`, and the bot confirms the active
   persona.
3. **Given** an unauthorized `chat_id`, **when** any message is sent, **then** the bot
   does not respond and the request is logged as rejected.

### Scenario 2 -- Hold a multi-turn conversation with Mark

The developer asks Mark a product question (e.g., "What's the current PRD for the
skeleton generator?"). Mark replies with a repo-grounded answer. The developer asks a
follow-up. Mark's reply demonstrates memory of the previous turn.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| --- | --- | --- | --- | --- |
| 1 | 3 | 90 | 3 | 0.9 |

**Independent test**: Send two related questions in sequence; verify the second answer
references context from the first without re-stating it.

**Acceptance criteria**:
1. **Given** an active session, **when** a question is sent, **then** the bot replies
   with a Markdown-formatted answer within 30 seconds.
2. **Given** a follow-up question on the same session, **when** processed, **then** the
   Copilot SDK is invoked with the resumed `session_id` (no new session).
3. **Given** a reply exceeding Telegram's 4096-char message limit, **when** sending,
   **then** the response is split across multiple messages preserving Markdown blocks.

### Scenario 3 -- Resume the same conversation from a second device

The developer chats with Mark on their phone, then opens Telegram Web on a borrowed
laptop. The conversation history is identical and the next message continues the same
session.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| --- | --- | --- | --- | --- |
| 1 | 2 | 90 | 1 | 1.8 |

**Independent test**: Send messages from one client, switch to another Telegram client
on the same account, verify the next message resumes the same session.

**Acceptance criteria**:
1. **Given** Telegram clients share a `chat_id` per account, **when** a message arrives
   from any client, **then** the same `session_id` is loaded from storage.

### Scenario 4 -- HITL gate blocks an unapproved sensitive tool call

The agent attempts to invoke a tool classified as sensitive. The bot sends an inline
keyboard with `Approve` and `Deny`. The developer taps `Deny`. The agent reports it
cannot proceed and offers an alternative.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| --- | --- | --- | --- | --- |
| 1 | 3 | 85 | 4 | 0.6 |

**Independent test**: Force the agent to attempt a sensitive tool; confirm the prompt
appears, tap `Deny`, verify the agent does not execute the tool.

**Acceptance criteria**:
1. **Given** a sensitive tool invocation, **when** the pre-tool-use hook fires,
   **then** SDK execution is paused and an inline-keyboard prompt is sent.
2. **Given** a `Deny` callback, **when** processed, **then** the SDK call is aborted
   and the agent is informed of the denial.
3. **Given** an `Approve` callback, **when** processed, **then** the SDK call resumes
   and the tool executes.
4. **Given** no callback within 5 minutes, **when** the timeout fires, **then** the
   pending action is denied by default and the user is notified.

### Scenario 5 -- Reset the session

The developer sends `/reset`. The bot drops the current session and confirms a clean
slate. The next message starts a fresh session.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| --- | --- | --- | --- | --- |
| 1 | 1 | 95 | 0.5 | 1.9 |

**Independent test**: Send `/reset`, then ask a question; verify the agent has no
memory of prior turns.

**Acceptance criteria**:
1. **Given** an active session, **when** `/reset` is sent, **then** the session entry
   is deleted from storage and the bot confirms the reset.
2. **Given** a reset session, **when** the next message arrives, **then** a new
   `session_id` is created.

### Scenario 6 -- Unauthorized actor is silently ignored

A third party discovers the bot and sends a message. The bot does not reply. The
event is logged with the `chat_id`, timestamp, and "unauthorized" reason. No Copilot
SDK call is made.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| --- | --- | --- | --- | --- |
| 1 | 3 | 95 | 1 | 2.9 |

**Independent test**: Send a message from a different Telegram account; verify silence
from the bot and a structured log entry recording the rejection.

**Acceptance criteria**:
1. **Given** a `chat_id` not in the allowlist, **when** any update arrives, **then**
   the request returns 200 to Telegram (avoid retry storms) and no further action is
   taken.
2. **Given** a request with an invalid `X-Telegram-Bot-Api-Secret-Token`, **when**
   received, **then** the response is `401` and the request is logged.

## Constraints

- **Python 3.12 only** (per `AGENTS.md`).
- **No defaults for env vars** (per `AGENTS.md`); fail fast on missing config.
- **No `argparse`**; configuration is env-driven only.
- **Read-only repo access** in v1: GitHub PAT scoped to `repo:read`.
- **Single-user allowlist**: `TELEGRAM_ALLOWED_CHAT_IDS` env var, comma-separated.
- **Hands-off deployment**: all Azure resources provisioned via Azure MCP tool calls
  or Bicep `what-if`/`deploy` commands invoked by the agent. All GitHub configuration
  (Actions secrets, OIDC federated credential, branch protection) provisioned via
  `gh` CLI invoked by the agent. Manual portal use is forbidden except for one-time
  Telegram bot creation via BotFather.
- **NotebookLM is desktop-only**: Ron's mobile persona MUST have NotebookLM tools
  filtered out at load time.

## Non-Functional Requirements

| ID | Requirement |
| --- | --- |
| NFR1 | Cold start to first token: < 5 seconds (warm), < 15 seconds (cold) |
| NFR2 | Monthly cost: < $10 USD steady state |
| NFR3 | All secrets stored in Azure Key Vault; none in code or GitHub Actions YAML |
| NFR4 | All inbound webhooks authenticated via Telegram secret token |
| NFR5 | All sensitive tool invocations gated by HITL approval |
| NFR6 | Container runs as non-root with read-only root filesystem |
| NFR7 | Structured JSON logging; no message bodies or secrets in logs |
| NFR8 | Session TTL: 30 days (auto-pruned from Table Storage) |

## Glossary

- **Persona**: A `.github/agents/<name>.agent.md` file defining a named AI agent.
- **HITL**: Human-In-The-Loop -- a mandatory user approval before a sensitive action.
- **Session**: A Copilot SDK conversation thread identified by `session_id`.
- **Allowlist**: Set of Telegram `chat_id` values permitted to interact with the bot.
- **Sensitive tool**: Any Copilot tool that writes, executes, or mutates external state.
