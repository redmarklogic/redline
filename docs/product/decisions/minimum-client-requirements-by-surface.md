# Minimum Client Requirements by Product Surface

**Status**: v1 — partial (one of three surfaces fully established).
**Owner**: Mark.
**Strategic anchor**: Bet 1 (The Free Skeleton Wedge) and Bet 5 (NZ + AU Year One beachhead). A minimum-client-requirement floor is a commercial promise that gates who can buy; it must be true before any contract / terms-of-use / website copy states it.
**Trigger**: Spike #185 raised the Word taskpane's declared Office.js floor from WordApi 1.1 to 1.3 to honestly match the code (`ContentControl.getRange()` in the Replace stage needs 1.3). Founder flagged that each surface has its own minimum and only the taskpane's was known.
**Date**: 2026-06-13.
**Project memory**: A directive memo records this flag for durable capture.

---

## Diagnosis

- **Stage**: Pre-launch, pre-revenue. Launch backstop 2026-07-31 (Bet 1). Design budget $100/mo. Runway short (~7 weeks at flag time).
- **Binding constraint now**: No paying subscriber exists yet, but contract / ToS / website copy is about to be written. A wrong or missing minimum-requirement line in that copy becomes a promise we cannot honour and a refund/trust risk the moment the first subscriber's environment fails. The cost of getting this wrong is asymmetric — cheap to state correctly now, expensive to retract after a client has paid.
- **Theoretical-only constraint**: The Email service surface does not exist at launch (launch UX is web page → download DOCX per the #78 stack decision; the Outlook/email add-in is a later phase). Establishing its exact floor today is not on the critical path — but *naming that it is unestablished and who must establish it* is, so the public line is not silently over-promised.

## Surviving the Round test

- **Short runway (3–6 months)**: At launch only TWO surfaces are live — the web app (the Skeleton Generator page) and the Word taskpane add-in. The minimum-requirements line must cover exactly those two. Getting the web app baseline and the taskpane floor right is the whole job for this round.
- **Long runway (2+ years)**: The Email service becomes a third surface with its own floor. Disclosing its requirement now would be over-disclosure of a capability we do not yet sell. **Defer** the email floor to when that surface is built; do not let it inflate the launch-day public statement.

Conclusion: scope the public statement to the two launch surfaces. Hold the email surface as a named, owned gap, not a guess.

---

## 1. Minimum client requirement per surface

### Surface A — Word taskpane add-in (ESTABLISHED)

**Minimum: Word 2019 (perpetual/volume-licensed) OR any Microsoft 365 subscription Word. Word 2016, 2013, 2010 are NOT supported.**

Evidence and correction (this is load-bearing — the founder's framing memo contained a factual error that this decision corrects):

- The code's Office.js floor is **WordApi requirement set 1.3** (spike #185, `docs/research/20260622-185-officejs-spike/evidence.md`, line 23; `snippet.yaml` line 13).
- Per Microsoft's official requirement-set table (`learn.microsoft.com/.../word/word-api-requirement-sets`, doc dated 2026-04-21), the perpetual/volume-licensed Office version that first carries **WordApi 1.3 is Office 2019** (Version 1612, Build 7668.1000). **WordApi 1.1 — not 1.3 — is the set that maps to Office 2016** (Version 1509).
- Therefore raising the floor from 1.1 to 1.3 **drops Word 2016**. The minimum perpetual desktop version is **Word 2019**, not Word 2016. The founder's trigger memo stated "WordApi 1.3 is present from Word 2016 onward" — that is incorrect; 1.3 is present from Word 2019 onward. The spike's own evidence.md is correct: it states the 1.3 floor "drops Word 2016 support."
- **Microsoft 365 subscription Word** is evergreen and always exceeds 1.3, so all M365 users are covered regardless of when they installed. Office on the web, Mac, and iPad all support 1.3.

Net public-facing floor for the taskpane: **Word 2019 or newer (perpetual), or Microsoft 365.**

### Surface B — Web app (ESTABLISHED, low confidence on exact browser list — confirm with Peter)

**Minimum: a current mainstream evergreen browser (Chrome, Edge, Firefox, Safari — recent versions). No legacy Internet Explorer.**

Grounding: The launch web app is Django server-rendered templates + HTMX (issue #78 stack decision, founder-ratified 2026-06-11). Server-rendered HTML with HTMX has a very low browser bar — it works on essentially any browser from the last several years and degrades gracefully. There is **no heavy single-page-app framework** raising the floor.

This surface is **clearly LESS restrictive than the Word taskpane.** A machine that can run Word 2019 / Microsoft 365 can certainly run a current browser. *Evidence still needed*: Peter (Principal Engineer) should confirm the exact supported-browser statement (e.g. "last 2 versions of Chrome/Edge/Firefox/Safari") so the public line is precise rather than my inference. This does not block the conclusion below.

### Surface C — Email service (NOT ESTABLISHED — named gap)

**Minimum: UNKNOWN. Must be established before this surface ships. Does not exist at launch.**

The requirement depends entirely on what "Email service" means, and that is my open question to the founder:

- **If it is an inbound email channel** (client emails us a document, we email back a marked-up version), the client's only requirement is *an email account able to send and receive file attachments* — i.e. essentially **no meaningful floor**, far less restrictive than Word 2019.
- **If it is an Outlook email add-in / taskpane** (analogous to the Word add-in, running Office.js inside Outlook), it carries its **own Office.js MailboxApi requirement-set floor** — which could land at a specific Outlook version and might or might not be less restrictive than Word 2019. This branch must be measured, not assumed.

**Evidence needed and from whom**: Peter (and the spike that builds the email surface) must establish (a) which of the two architectures it is, and (b) if it is an Outlook add-in, the MailboxApi floor and the resulting minimum Outlook/Microsoft 365 version. Until that exists, **the email surface must not be covered by the launch public statement** — because we cannot yet truthfully state its floor.

---

## 2. Is the founder's single-line simplification valid?

**Partly. It is valid for the two surfaces that ship at launch, but the line must be corrected to Word 2019 (not 2016), and it must be explicitly scoped to launch surfaces — it cannot yet speak for the email service.**

- The Word taskpane **is** the binding (most restrictive) constraint among the live launch surfaces. The web app is strictly less restrictive. So a single floor line is sound for launch.
- **But the founder's proposed wording is wrong on the version.** "Minimum: Word 2016" would under-state our true floor and would let a Word 2016 user subscribe and then fail — the exact surprise this flag exists to prevent. The correct collapsed line is **Word 2019 / Microsoft 365**, not Word 2016.
- The simplification is **not yet validated for the email service** because that surface's floor is unestablished. Today this is fine: the email service is not live at launch, so a launch-scoped statement does not need to cover it. When the email surface ships, this decision must be revisited to confirm it remains less restrictive than Word 2019; if an Outlook add-in pushes the floor higher, the single line breaks and requirements become per-surface.

## 3. Recommended public statement and where it must appear

**Recommended launch public statement (for the two live surfaces):**

> **Minimum requirement to use Redline:** Microsoft Word 2019 or newer, or a Microsoft 365 subscription (which always qualifies). The web app works in any current Chrome, Edge, Firefox, or Safari browser. Word 2016 and earlier are not supported.

(Final browser wording pending Peter's confirmation per Surface B.)

**Where it must be disclosed — before purchase, never after:**

1. **Website copy** — a "System requirements" line on or one click from the pricing/signup page, visible *before* a visitor enters the signup flow. (Note: pricing page is currently scope-locked OUT of the minimum viable website per `launch-perimeter-constraints.md` §2 — so this line lands wherever pricing/subscription first appears, which is post-Step-3, not on the waitlist landing page.)
2. **Signup / subscription flow** — a checkpoint or visible note at the point the user commits (the SSO-gated signup), so no one pays without having seen it.
3. **Terms of Use / contract** — a "System Requirements" clause stating the same floor, so it is contractually disclosed and not a hidden condition.

The disclosure principle: the floor must be readable at or before the moment money or a binding commitment is given — so a subscriber cannot discover the requirement after subscribing.

## 4. Does this need Ron's input on positioning?

**Yes — route to Ron.** A minimum-requirement floor is a commercial promise: it defines who is eligible to buy and silently excludes the Word-2016-and-earlier segment. That is positioning and addressable-market territory, not pure engineering. Specifically Ron should weigh:

- Whether excluding perpetual Word 2016/2013 users materially shrinks the NZ+AU beachhead (Bet 5) — geotechnical firms can run older perpetual Office.
- The exact public wording, so the requirement reads as a confident product standard ("built for modern Word / Microsoft 365"), not as an apology.

This is my call to route, and I am routing it: **Ron owns the final wording of this as a commercial claim; I own the factual floor that wording must not contradict.**

---

## Decision log

**Decided**: Launch-scoped minimum-requirement floor = **Word 2019 / Microsoft 365** (most-restrictive live surface = Word taskpane), web app strictly less restrictive, email surface deferred as a named gap.

**Alternatives considered and rejected**:

- *"Minimum: Word 2016" (founder's original line)* — **rejected**: factually wrong. WordApi 1.3 maps to Word 2019, not 2016; this line would let a Word 2016 user subscribe and then fail.
- *Publish a per-surface requirements table now* — **rejected for launch**: over-discloses an email surface that does not yet ship and is not yet measured; adds confusion for no live benefit. Revisit when the email surface ships.
- *Lower the code floor back to 1.1 to keep Word 2016 support* — **rejected / out of my lane**: that is an engineering + product trade-off Peter and the founder already settled in the spike (1.3 needed for `getRange()` in Replace). Re-opening it is a separate decision, not this one. Flagged here only so the option is on record.

**Open items / next evidence owners**:
- Peter — confirm exact supported-browser wording for the web app (Surface B).
- Founder/Peter — define what "Email service" is (inbound channel vs Outlook add-in) and, if an add-in, establish its MailboxApi floor (Surface C). Revisit this decision when that surface is scoped.
- Ron — own the public wording as a commercial claim; confirm the excluded-segment trade-off against Bet 5.
