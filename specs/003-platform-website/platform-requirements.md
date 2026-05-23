# Platform & Website Requirements

**Status**: Captured (raw founder input). **Owner**: Mark.
**Captured**: 2026-04-19. **Source**: Founder specification notes.

> These requirements define the architectural constraints for the Redline web
> platform. They are NOT Sprint 1 scope -- they are the guardrails that Sprint 1's
> architecture must respect so that future sprints do not require an overhaul.

---

## Table of Contents

1. [Security-by-Design: SOC 2 "Shadow" Compliance](#security-by-design-soc-2-shadow-compliance)
2. [API-First Architecture: Headless Core and Multi-Interface Extensibility](#api-first-architecture-headless-core-and-multi-interface-extensibility)
3. [Geo-Aware Regulatory Localization](#geo-aware-regulatory-localization)
4. [Unified Telemetry: PostHog](#unified-telemetry-posthog)
5. [Deep-Stack AI Observability: Langfuse](#deep-stack-ai-observability-langfuse)
6. [Communicating the Impact of Redline](#communicating-the-impact-of-redline)

---

## Security-by-Design: SOC 2 "Shadow" Compliance

To future-proof our platform for enterprise adoption, we are adopting a
"Compliance-First" engineering approach. Rather than treating security and compliance
as an afterthought to be bolted on later, they are core functional requirements baked
into our Minimum Viable Product (MVP).

By operating in a state of SOC 2 "Shadow" compliance, we design our architecture to
automatically collect evidence, maintain tamper-proof logs, and follow strict access
control protocols as if we were already under formal audit. This "Security-by-Design"
strategy prevents the expensive, time-consuming architectural rewrites commonly faced
by startups, allows us to legitimately claim we are "Audit-Ready" to early prospects,
and ensures the eventual formal SOC 2 certification is merely a procedural "switch-flip"
rather than a massive engineering hurdle.

### Architectural Requirements

- **Infrastructure as Code (IaC)**: All infrastructure must be provisioned and managed
  using IaC (e.g., Terraform, AWS CloudFormation). Manual configuration via cloud console
  is strictly prohibited to ensure all environments are reproducible, version-controlled,
  and fully auditable.
- **Principle of Least Privilege (PoLP)**: All internal systems, API endpoints, and
  databases must enforce strict Role-Based Access Control (RBAC). Default access across
  the entire platform must be set to "deny."
- **Encryption Everywhere**: All data must be encrypted in transit (using TLS 1.2 or
  higher) and at rest (using AES-256 or equivalent) without exception. This includes
  databases, backups, and temporary storage.
- **Centralized Audit Logging**: Every system change, API access, authentication event,
  and administrative action must be automatically logged to a centralized, tamper-evident
  log management system.

### Compliance and Audit Constraints

- **Separation of Duties**: Production environments must be strictly segregated from
  development and staging environments. Developers must not have direct write access to
  production databases; any emergency access must be handled via audited "break-glass"
  procedures.
- **Continuous Monitoring Readiness**: The architecture, APIs, and cloud environments
  must be structured in a way that is immediately compatible with automated compliance
  monitoring platforms (e.g., Vanta, Drata, Thoropass) to continuously ingest and verify
  our security posture.
- **Vulnerability Management**: Automated vulnerability scanning (e.g., Dependency
  tracking, SAST/DAST) must be integrated into the CI/CD pipeline, blocking deployments
  that contain critical or high-severity vulnerabilities.

### Acceptance Criteria

1. Infrastructure changes are deployed exclusively via automated CI/CD pipelines using
   version-controlled IaC.
2. Centralized logging captures all authentication attempts, data modifications, and
   administrative actions with corresponding timestamps and user IDs.
3. An automated scan (or manual architectural review) confirms that 100% of data stores
   and backups are encrypted at rest.
4. Production access requires MFA (Multi-Factor Authentication) and is gated behind SSO
   (Single Sign-On) or strict identity management.
5. A simulated "shadow audit" demonstrates that an engineer can quickly retrieve an
   immutable log of who deployed what code to production, and when.

---

## API-First Architecture: Headless Core and Multi-Interface Extensibility

To ensure maximum reach and flexibility, our core tools are being built exclusively as an
independent backend API using Python. Rather than tightly coupling these tools to a
specific web interface, we are building an "engine" first.

> **Discovery-phase note (2026-04-20):** The backend framework is TBD. Django and
> FastAPI are both under consideration. Django offers a batteries-included stack
> (ORM, admin, auth, sessions) which may reduce Sprint 1 surface area; FastAPI
> offers async-native performance and auto-generated OpenAPI docs. This decision
> will be locked in ADR-010 during discovery Week 1 (June 1--5).

By treating the API as the primary product, we guarantee ultimate extensibility. These
engineering tools can be seamlessly embedded into no-code automation workflows (like n8n),
queried dynamically by AI agents (via the Model Context Protocol / MCP), or integrated
directly into client enterprise systems. Any web-based User Interface we develop will
simply act as one of many "clients" that consumes this tools API via standard RESTful
HTTP requests.

### Architectural Requirements

- **API as the Primary Product**: The backend tools and business logic must exist
  completely independently of any User Interface. The API is the product; any frontend
  application is strictly an external consumer of this API.
- **Technology Stack and Protocol**: The tools API must be built in Python using either
  Django (with Django REST Framework) or FastAPI (decision TBD -- see ADR-010). All
  communication between clients and the tools must occur via RESTful HTTP requests
  (GET, POST, PUT, DELETE).
- **Core Logic Encapsulation**: All engineering mathematics, standards evaluations, and
  data retrieval must live exclusively within the API. There must be absolutely no
  proprietary engineering logic or calculation formulas written into any future frontend
  client code.
- **Standardized Contracts and Auto-Documentation**: The API must follow strict RESTful
  standards and utilize FastAPI's native capabilities to auto-generate OpenAPI (Swagger)
  documentation. The schema for every tool must be instantly readable by both human
  developers and machines.
- **AI and Automation Readiness**: The API structure, JSON payload responses, and
  authentication methods must be designed to be easily digestible by no-code orchestrators
  (like n8n) and LLM-driven applications using the Model Context Protocol (MCP).

### Integration Constraints

- **Statelessness and Predictability**: API responses for engineering standards and
  calculations must be strictly stateless. Every request must return a highly structured,
  predictable JSON payload (enforced via Pydantic) to ensure third-party automation tools
  do not break when parsing the outputs.
- **Rate Limiting and Security**: Because the API is the primary execution environment
  for our tools, robust rate limiting, payload validation, and scoped authentication must
  be implemented at the gateway level to prevent abuse from automated scripts or heavy
  programmatic usage.

### Acceptance Criteria

1. A core engineering tool or calculation can be successfully executed via a raw RESTful
   HTTP request (e.g., using Postman or cURL).
2. FastAPI successfully auto-generates an accessible OpenAPI (Swagger) documentation page
   detailing the inputs and outputs for all available engineering tools.

---

## Geo-Aware Regulatory Localization

Because civil engineering standards and compliance claims are legally binding and vary
strictly by region, our platform is being built with a "Global-Ready Architecture" from
day one. Rather than hardcoding rules for a single country into our software, the system
is designed to act as a smart container that automatically displays the correct, localized
regulations based on the user's web address (such as /nz/ for New Zealand or /us/ for the
United States). Even though we are launching in just one market initially, establishing
this regionalized foundation now ensures we completely avoid the legal risk of displaying
incorrect standards to international users in the future. More importantly, it turns our
future global expansion into a simple, fast content-entry task rather than an expensive,
slow software rewrite.

### Architectural Requirements

- **URL-Based Routing**: The application must utilize localized subdirectories (e.g.,
  x.com/us/, x.com/nz/) to determine the user's active region. The core application logic
  remains shared, but the region state is dictated by the URL path.
- **Decoupled Content Model**: Hardcoding engineering standards, compliance claims, or
  static text into the frontend codebase is strictly prohibited. All region-specific
  variables (measurements, legal standards, certifications) and locale-specific strings
  (e.g., US vs. UK English spelling variations like "aluminum" vs. "aluminium") must be
  abstracted into a localized database or Content Management System (CMS).
- **Configuration over Code**: Launching a new country (e.g., adding x.com/au/) should be
  a content and configuration task, requiring zero structural code changes or new
  deployments.
- **Fallback Logic**: If a user lands on the root domain (x.com), the system should either
  use IP geolocation to redirect them to the correct regional subdirectory or prompt them
  to select their region via a modal before displaying engineering standards.

### SEO and Metadata Constraints

- **Hreflang Implementation**: The `<head>` of all localized pages must include dynamically
  generated hreflang tags mapping the relationship between the regional variants to prevent
  Google from penalizing the site for duplicate content.

### Acceptance Criteria

1. A user visiting x.com/nz/ sees New Zealand structural standards loaded dynamically.
2. A user visiting x.com/us/ sees US structural standards loaded dynamically on the exact
   same page template.
3. The engineering team can demonstrate adding a dummy region (x.com/test/) solely through
   the CMS/Database without pushing new frontend code.

---

## Unified Telemetry: PostHog

To ensure our development is driven by empirical usage data rather than assumption, we are
implementing PostHog as our unified product telemetry engine. Rather than relying on
superficial marketing analytics, this event-based architecture focuses on capturing
granular user workflows, feature adoption rates, and interaction friction points within
the AI interface.

By centralising event tracking, session replays, and feature flag management into a single
platform, we establish a tight, actionable feedback loop that accelerates our iteration
cycles without inflating our technical debt or fragmenting our tool stack.

This integrated telemetry approach ensures we are measuring the actual value delivered at
the consultancy level, utilising robust Group Analytics to track engagement and resource
consumption across entire engineering firms. By embedding this tracking infrastructure
seamlessly across both our API core and client interfaces from day one, we lay a stable
foundation for future usage-based billing and data-driven product decisions.

Furthermore, PostHog's open-source pedigree provides a vital architectural fail-safe,
granting us the flexibility to eventually self-host our analytics infrastructure should
future enterprise clients mandate strict data sovereignty and on-premises isolation.

---

## Deep-Stack AI Observability: Langfuse

To maintain rigorous quality control and unit economics over our AI core, we are
implementing Langfuse as our dedicated LLM observability layer. Standard product analytics
cannot interrogate the "black box" of generative AI. By instrumenting our FastAPI backend
with Langfuse via its OpenTelemetry-based SDK, we achieve deterministic traceability of
every model invocation. This allows us to monitor generation latency, measure granular
token consumption, and evaluate output quality in real-time, ensuring that the underlying
AI models driving our engineering reviews operate efficiently and within strict cost
margins.

Crucially, this observability layer acts as a vital component of our "Compliance-First"
architecture. Langfuse provides a tamper-proof audit trail of system prompts, user inputs,
and AI outputs, natively satisfying the rigorous data lineage and auditing requirements of
SOC 2. Furthermore, by establishing a telemetry pipeline that automatically batches these
AI-specific metrics directly into PostHog, we bridge the gap between backend AI
performance and frontend user engagement. This dual-stack approach allows us to
dynamically version prompts, aggressively optimise API costs, and guarantee that our AI
infrastructure remains scalable, transparent, and audit-ready from day one.

---

## Communicating the Impact of Redline

To effectively demonstrate value to users, especially those in a risk-averse field like
geotechnical engineering, we need to shift from "what the tool does" to "what the tool
saved."

### Option 1: Executive Summary (Direct and Professional)

For monthly email or dashboard notification for managers.

> **Subject: Monthly Performance Insights: Risk Mitigation and Efficiency**
>
> Risk Mitigation: Successfully identified [X] critical liability clauses that required
> revision.
> Time Savings: Recovered approximately [X] man-hours by automating the quality-gate
> process.
> Quality Assurance: Processed [X] documents through our automated "checker" protocol,
> ensuring 100% compliance with internal standards.

### Option 2: Immediate Impact (Action-Oriented)

For a "Last Run" summary that appears immediately after a user finishes a session.

> **Review Complete: Your Impact Summary**
>
> Liability Alerts: Found [X] high-risk clauses that may have otherwise gone unnoticed.
> Efficiency Gain: You saved [X] minutes of manual review time, allowing you to focus on
> high-level engineering decisions.
> Consistency: This run ensures your reporting remains aligned with the firm's latest
> geotechnical standards.

### Option 3: Startup/Visionary (Bold and Objective)

Strictly metrics-focused.

> **Redline Value Metrics: April 2026**
>
> Liability Catch-Rate: Identified an average of [X] problematic clauses per report,
> directly reducing legal exposure.
> Resource Allocation: Saved a total of [X] man-hours across the team -- the equivalent
> of [X] full working days.
> Error Reduction: Flagged [X] inconsistencies in technical specifications before they
> reached the client.
