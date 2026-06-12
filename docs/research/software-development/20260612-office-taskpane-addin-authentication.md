# Office Word Task-Pane Add-in Authentication — Discovery Report

**Date:** 2026-06-12
**Status:** Durable research record (filed by Peter from the 2026-06-12 API-standards
revisit working notes; content preserved verbatim, all sources fetched/verified
2026-06-12).
**Decisions grounded in this research:**
[ADR-025 Amendment 1](../../adr/adr-025-launch-sign-in-google-microsoft-oauth-only.md)
(dual-track authentication) and §7 of
[`http-api-standard.md` v0.2](../../architecture/api/http-api-standard.md).
**Future consumer:** the Word add-in epic — cite this document rather than
re-researching.

**Context:** Redline API uses session-cookie OAuth (ADR-025, Google/Microsoft
sign-in). A Word task-pane add-in will later consume this API. Question: what
constrains the backend API auth design *now* vs what can be deferred until the
add-in is built.

---

## Q1 — Do cookies work in Office Add-in task panes?

**Short answer: not reliably, and on two of three platforms they are effectively broken for cross-site session auth. Cookie-only session auth is not viable for task-pane → API calls.**

The task pane is a web page loaded in an embedded runtime that differs per platform:

| Platform | Runtime | Cookie situation (2025–2026) |
|---|---|---|
| Word on Windows (M365, current) | Edge **WebView2** | Task pane page is top-level in the webview, so *first-party* cookies on the add-in's own domain mostly work. But the API is on a different domain → cookies on `fetch()` are *cross-site*: require `SameSite=None; Secure` + CORS `credentials: include`, and are subject to Chromium third-party-cookie phase-out and CHIPS partitioning behaviour inherited by WebView2. Chromium ≥115 also enables **storage partitioning** (localStorage etc. keyed by top-level site). Microsoft's own docs note `Office.context.partitionKey` is `undefined` on Windows webviews (no partitioning there *today*), but this is runtime behaviour Microsoft can change, not a contract. |
| Word on Mac | Safari **WKWebView** | **All third-party cookies are blocked.** ITP (Intelligent Tracking Prevention) is enabled by default in WKWebView and *cannot be disabled* for the embedded control in Office on Mac (unlike desktop Safari where the user can toggle it). Microsoft's guidance: don't rely on third-party cookies; use OAuth token handoff to establish a first-party session, or the Storage Access API. |
| Word on the web | Browser iframe inside office.com | The task pane is an **iframe on a different origin than the top-level page** → every cookie your API sets is by definition a third-party cookie. Safari blocks them outright (ITP); Chrome/Edge are phasing them out / partitioning them; Edge policy `DefaultThirdPartyStoragePartitioningSetting` governs partitioning. The Storage Access API (`document.requestStorageAccess()`) is the sanctioned escape hatch but requires a user gesture, prior first-party interaction with your domain, and is supported only on Office on the web and Mac — a fragile UX. |

Microsoft's own published mitigation for add-ins that "need third-party cookies for authentication" is telling: **do OAuth 2.0, forward an authorization token, and only then establish a server-set first-party session** — i.e. token-first, cookie-second ([ITP and third-party cookies doc, ms.date 2025-09-24](https://learn.microsoft.com/en-us/office/dev/add-ins/develop/itp-and-third-party-cookies)).

**Verdict:** a session cookie set by the Redline API origin for a task pane served from another origin will fail on Mac and Office-on-web (Safari especially), and is on a deprecation path on Chromium. The dependable cross-platform channel is an **`Authorization: Bearer <token>` header** on fetch, with the token held in (partitioned) localStorage or memory.

Sources:

- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/itp-and-third-party-cookies> (ms.date 2025-09-24)
- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/persisting-add-in-state-and-settings> (partitioned storage, `Office.context.partitionKey`)
- <https://developer.chrome.com/docs/privacy-sandbox/storage-partitioning/> (Chromium ≥115 storage partitioning)
- <https://privacysandbox.com/news/privacy-sandbox-update> (Chrome third-party cookie direction)

---

## Q2 — Recommended auth pattern for Office Add-ins, 2025–2026

Microsoft's current ladder (overview doc ms.date **2025-12-25**):

1. **Nested App Authentication (NAA) with MSAL.js — the current recommendation for SSO.**
   - `createNestablePublicClientApplication` from `@azure/msal-browser`; the Office host (Word/Excel/PowerPoint/Outlook/Teams, the `brk-multihub` broker group) brokers token acquisition for the signed-in Office account.
   - Requires an **Entra ID app registration** with SPA redirect `brk-multihub://<add-in-domain>` (+ a normal SPA redirect for Office on the web).
   - **Account types: Microsoft Entra ID (work/school) and personal Microsoft accounts (MSA) only. No Azure AD B2C, and no non-Microsoft IdPs.** Tokens are Microsoft-identity-platform access tokens (for Graph or for your own Entra-registered API).
   - Pattern: `acquireTokenSilent`/`ssoSilent` → fall back to `acquireTokenPopup`; call APIs with `Authorization: Bearer`. Note the doc's own sample calls the API via **bearer header on fetch** — the canonical add-in→API call shape.
   - Constraints: must request ≥1 scope beyond openid/profile/offline_access; several MSAL APIs throw under NAA (`loginRedirect`, `logout*`, `acquireTokenRedirect`); older Office builds don't support NAA → feature-detect `Office.context.requirements.isSetSupported("NestedAppAuth", "1.1")` and keep a fallback; known gaps on Outlook Mobile (falsely reports support, GitHub issue #6275).
2. **Legacy Office SSO (`Office.auth.getAccessToken`)** — still supported but explicitly labelled **legacy**; only for maintaining existing add-ins. (Separately, Outlook's *Exchange legacy tokens* were deprecated Feb 2025 and turned off across tenants by ~Aug 2025 — different mechanism, but it shows the migration pressure toward NAA.)
3. **Office Dialog API (`displayDialogAsync`)** — the universal fallback and the *only* route for **non-Microsoft identity providers** or when SSO is unavailable/undesired ("sign in to the add-in with a different ID from the one signed in to Office" is an explicitly documented scenario).

Sources:

- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/overview-authn-authz> (ms.date 2025-12-25)
- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/enable-nested-app-authentication-in-your-add-in> (ms.date 2025-12-15)
- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/sso-in-office-add-ins> (legacy SSO)
- <https://devblogs.microsoft.com/microsoft365dev/naa-and-deprecation-of-legacy-tokens/> and <https://devblogs.microsoft.com/microsoft365dev/updates-on-deprecating-legacy-exchange-online-tokens-for-outlook-add-ins/> (legacy-token shutdown timeline)
- <https://github.com/OfficeDev/office-js/issues/6275> (Outlook Mobile NAA gap)

---

## Q3 — Can a user sign in with Google from inside the task pane?

**Yes — via the Office Dialog API. This is a documented, first-class pattern** (auth-with-office-dialog-api doc, ms.date **2026-01-08**, literally titled "…enable users to sign in to Google, Facebook, Microsoft 365…").

Mechanics and limitations:

- Google (like most IdPs) **refuses to render its sign-in page in an iframe**, and webview security features can break sign-in pages in the task pane itself → the flow must run in `Office.context.ui.displayDialogAsync`, which opens a **separate browser/webview instance** (not an iframe).
- The dialog's **first page must be on the same domain as the task pane**; it then redirects to Google OAuth; Google redirects back to your domain; that page calls `messageParent(...)` to hand the result (token / session handle / success flag) back to the task pane, which closes the dialog.
- **The dialog shares nothing with the task pane**: separate window object, separate sessionStorage; on Safari/Office-web even localStorage is not shared, and Chromium ≥115 storage partitioning further restricts sharing. Microsoft's recommendation: pass data via `messageParent`/`messageChild`, not via storage or library token caches.
- Consequence for auth libraries: a library's in-memory token cache or "auth context" object created in the dialog is unusable in the task pane — you must explicitly extract the token/string result and message it across. (This is exactly why Redline's *web* OAuth code can't be reused blindly; the redirect landing page needs a `messageParent` variant.)
- UX cost: a visible popup dialog on first sign-in (and on session expiry); silent renewal needs your own refresh-token/long-lived-session design on the API side, since the dialog's silent flows aren't reachable from the task pane.
- Multiple providers: documented pattern is a provider-picker first page in the dialog → so "Sign in with Google *or* Microsoft" inside the add-in is fully supported, independent of the Word-logged-in account.

Sources:

- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/auth-with-office-dialog-api> (ms.date 2026-01-08)
- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/auth-external-add-ins> (non-Microsoft IdPs)
- <https://community.auth0.com/t/using-auth0-in-office-web-add-ins/58915> (real-world third-party-IdP-in-add-in experience)

---

## Q4 — The identity-mismatch problem (Google email X vs Microsoft email Y)

If the add-in uses NAA/Office SSO, the API receives a **Microsoft token for identity Y** with no inherent link to the SaaS account created via Google as X. Standard patterns, in rough order of robustness:

1. **In-add-in independent login (recommended for Redline's shape).** The add-in ignores the Office identity entirely and runs *the product's own* sign-in (Google or Microsoft) in the Office dialog (Q3). The API sees the same identity it saw on the web. Identity mismatch never arises; one auth model serves web + add-in. Cost: one dialog page pair (launcher + redirect-landing with `messageParent`) and a bearer-token issuance path on the API. This is what most cross-platform SaaS add-ins (e.g. Grammarly's Word add-in, which offers Google/Apple/Facebook/email sign-in from the task pane) do — they treat the add-in as just another client of their own auth, not as a Microsoft-identity app.
2. **Account linking.** User signs in once with each provider (or confirms the second from a signed-in session); backend stores `(provider, subject-id)` pairs against one account. Google Cloud Identity Platform formalises this model (one internal UID, N federated providers). Gold standard, but real product surface: linking UI, unlink, collision handling.
3. **Email matching.** Match Microsoft token's email claim to the existing Google-created account. **Security caveat is load-bearing:** match only on *verified* email claims. Entra ID's `email` claim can be user-mutable/unverified in some tenant configurations — auto-linking on it enables account takeover (the documented "nOAuth" misconfiguration class, Descope 2023; Microsoft's mitigation guidance says key on `tid`+`oid`, treat email as a hint). If used, gate it: match → require one-time proof (login via original provider, or email OTP) → then link.
4. **Do nothing / segment users** (founder's simplification): rely on emails matching; mismatched users use web only. Works mechanically, but silently strands an unknown % of users (personal MSA in Word + Google Workspace at work is common), and *still* requires email-claim matching with caveat 3 for the "matching" majority.

**Evaluation of the founder's simplification:** the escape hatch already exists and is cheap — option 1 *is* the "in-task-pane independent login" the founder hypothesised, it is Microsoft-documented, and it costs roughly two small pages plus token plumbing the API needs anyway (Q1). Since it must be built for Mac/web cookie reasons regardless, the email-match assumption becomes unnecessary: **independent login dissolves the mismatch problem at near-zero marginal cost.** NAA can be layered on later as a *convenience* accelerator ("you're already signed into Word as Y — use that?") for users whose emails do match, with email-verification guardrails.

Sources:

- <https://docs.cloud.google.com/identity-platform/docs/link-accounts> (account-linking model)
- <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/overview-authn-authz> ("sign in to the add-in with a different ID" scenario)
- <https://www.descope.com/blog/post/noauth> (nOAuth email-claim account-takeover; 2023, still the canonical reference)
- <https://learn.microsoft.com/en-us/samples/officedev/office-add-in-samples/outlook-add-in-sso-naa-identity/> (Microsoft's sample for sending NAA identity claims to your own backend)
- <https://www.grammarly.com/signin> + <https://support.grammarly.com/hc/en-us/sections/115000022252-Sign-in-Help> (Grammarly add-in uses own multi-provider login)

---

## Q5 — What constrains the API design NOW vs what can be deferred

### Decide / build NOW (constrains ADR-025)

1. **The API must accept `Authorization: Bearer <token>` — cookies cannot be the only session mechanism.** This is the single load-bearing constraint. Every viable add-in auth path (NAA, Dialog-API Google login, legacy SSO) terminates in "task pane calls API with a bearer header"; cookies fail on Mac WKWebView and Office-on-web iframes (Q1). Concretely: the auth layer should be able to *issue* a token (e.g. short-lived JWT/opaque token minted at OAuth completion) and *validate* it on requests, alongside the existing cookie path for browsers. Designing this in now is cheap; retrofitting a cookie-coupled session model later is not.
2. **Keep OAuth completion decoupled from "set cookie".** The OAuth callback should end in a step that can either set a cookie (web) or hand a token to a `messageParent` page (add-in). I.e. structure the flow as *authorization-code → session-establishment primitive*, not *authorization-code → Set-Cookie inline*. This is a design-shape decision, near-free now.
3. **Stable internal user ID with `(provider, subject)` identity rows** (even if only one row per user today). One-time schema decision that makes future account linking and a future Microsoft-identity row additive instead of a migration.
4. **CORS posture awareness:** bearer-header CORS (no `credentials: include`) is simpler and safer than cookie CORS; another nudge toward tokens for non-browser-page clients.

### Defer until the add-in is built (with triggers)

| Deferred item | Trigger to decide |
|---|---|
| NAA vs Dialog-only; Entra app registration; `brk-multihub` redirect | Add-in project kickoff |
| Office SSO → Redline account convenience linking (email-match UX + verification guardrails) | Only if/when NAA adopted **and** users complain about double sign-in |
| Account-linking UI (multi-provider per account) | First real support cases of mismatched emails; not before |
| Token storage in partitioned localStorage / `Office.context.partitionKey` handling, dialog `messageParent` plumbing | Add-in implementation detail |
| Storage Access API usage | Probably never — bearer tokens make it moot |
| Office-on-web vs desktop platform matrix testing | Add-in beta |

### On the founder's simplification

Acceptable as a *non-blocking* assumption, but it shouldn't drive the API design — because the bearer-token requirement (item 1) is forced by cookie/webview mechanics *regardless of whose emails match*. Once bearer issuance exists, the in-dialog independent Google/Microsoft login is the cheap path Microsoft documents, and the mismatched-email cohort is served for marginal cost ≈ two dialog pages. Recommend: adopt simplification as a *roadmap sequencing* statement ("no account-linking UI in v1"), not as an API architecture input.

---

## Source list (all fetched/verified 2026-06-12)

- Microsoft Learn, *Overview of authentication and authorization in Office Add-ins*, ms.date 2025-12-25 — <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/overview-authn-authz>
- Microsoft Learn, *Enable SSO in an Office Add-in with nested app authentication*, ms.date 2025-12-15 — <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/enable-nested-app-authentication-in-your-add-in>
- Microsoft Learn, *Authenticate and authorize with the Office dialog API*, ms.date 2026-01-08 — <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/auth-with-office-dialog-api>
- Microsoft Learn, *Develop your Office Add-in to work with ITP when using third-party cookies*, ms.date 2025-09-24 — <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/itp-and-third-party-cookies>
- Microsoft Learn, *Persist add-in state and settings* — <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/persisting-add-in-state-and-settings>
- Microsoft Learn, *Enable legacy Office SSO* — <https://learn.microsoft.com/en-us/office/dev/add-ins/develop/sso-in-office-add-ins>
- Microsoft Learn, *Nested app authentication FAQ (Outlook legacy tokens)* — <https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/faq-nested-app-auth-outlook-legacy-tokens>
- Microsoft 365 Dev Blog, *NAA and deprecation of legacy tokens* — <https://devblogs.microsoft.com/microsoft365dev/naa-and-deprecation-of-legacy-tokens/>
- Microsoft 365 Dev Blog, *Updates on deprecating legacy Exchange Online tokens* — <https://devblogs.microsoft.com/microsoft365dev/updates-on-deprecating-legacy-exchange-online-tokens-for-outlook-add-ins/>
- OfficeDev/office-js issue #6275 (Outlook Mobile NAA false-positive) — <https://github.com/OfficeDev/office-js/issues/6275>
- Microsoft sample, *Send identity claims to resources using NAA and SSO* — <https://learn.microsoft.com/en-us/samples/officedev/office-add-in-samples/outlook-add-in-sso-naa-identity/>
- Chrome Developers, *Storage partitioning* — <https://developer.chrome.com/docs/privacy-sandbox/storage-partitioning/>
- Privacy Sandbox, *A new path for Privacy Sandbox on the web* — <https://privacysandbox.com/news/privacy-sandbox-update>
- Google Cloud Identity Platform, *Linking multiple providers to an account* — <https://docs.cloud.google.com/identity-platform/docs/link-accounts>
- Descope, *nOAuth: how a misconfiguration in Entra ID OAuth led to account takeover* (2023) — <https://www.descope.com/blog/post/noauth>
- Auth0 Community, *Using Auth0 in Office Web Add-ins* — <https://community.auth0.com/t/using-auth0-in-office-web-add-ins/58915>
- Grammarly sign-in help (multi-provider login in add-in) — <https://support.grammarly.com/hc/en-us/sections/115000022252-Sign-in-Help>

*Caveat on comparable products (Q4): direct technical write-ups of how Grammarly/DocuSign implement Word add-in login are not published; the claim that they use own-account multi-provider login is grounded in their public sign-in surfaces and support docs, not engineering blogs.*
