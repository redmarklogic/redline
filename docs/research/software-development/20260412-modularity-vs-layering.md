# Modularity vs. Layering: When to Use Sibling Packages vs. Subpackages

**Date**: 2026-04-12
**Research question**: When should a new capability be an independent sibling package rather than a subpackage nested inside an existing package, and how do modularity and layering complement each other?
**Actor**: A senior Python developer designing a modular geotechnical engineering analysis platform with multiple independent tools (skeleton generator, report reviewer, metadata extractor) that may graduate to standalone PyPI packages.
**Redline domains**: Report generation, domain model architecture, package structure

---

## Summary

Modularity and layering are distinct but complementary architectural tools. Layering
enforces dependency direction *within* a component (which layer can import from which).
Modularity decomposes the system into independent, replaceable components at the package
level. When a system will grow multiple independent capabilities that change at different
rates and for different reasons, each capability should be a sibling top-level package --
not a subpackage nested inside an existing one. Each sibling package may then apply its
own internal layered architecture.

## Findings

### Modularity and Layering Are Orthogonal Concerns

Modularity refers to a logical grouping of related code into independent units, known as
components or packages. The goal of modular design is to encapsulate complexity and
minimise dependencies so that a programmer can work on one module without understanding the
details of the others. Modularity divides the system based on *what* the code does from a
business or feature perspective [Source: Software Architecture & DDD notebook, Q1].

Layering is a specific architectural pattern that organises components into logical
horizontal tiers, where each tier performs a specific technical role. The defining rule of
layering is the strict enforcement of dependency direction: an element in one layer can
only depend on elements in the same layer or the layers immediately beneath it. Layering
divides the system based on *how* the code executes its technical responsibilities
[Source: Software Architecture & DDD notebook, Q1].

When combined, they create "Layers of Isolation": because components are modularised, a
change to one feature does not break another feature; because those modules are internally
layered, a change to a low-level detail does not require rewriting higher-level domain
rules [Source: Software Architecture & DDD notebook, Q1].

Modern software architecture increasingly uses "domain partitioning" (modularity), where
the system is divided into separate, independent top-level packages based on workflows.
Within each of those independent packages, a layered architecture separates the business
logic from the infrastructure [Source: Software Architecture & DDD notebook, Q1].

### DDD: Bounded Contexts Map to Top-Level Packages

In Domain-Driven Design (DDD), a Bounded Context establishes a strict semantic boundary
where a specific Ubiquitous Language applies. When multiple Bounded Contexts share a
single codebase, each should be its own top-level package rather than nested as
subpackages underneath a single monolithic application root. This separation represents
modularity at the highest level, while layering is applied *inside* each top-level
package [Source: Software Architecture & DDD notebook, Q2].

**Vaughn Vernon** provides explicit tactical guidance: the top-level package should define
the Bounded Context. He demonstrates naming top-level sibling packages based strictly on
the Bounded Contexts (e.g., `com.saasovation.identityaccess`,
`com.saasovation.collaboration`, `com.saasovation.agilepm`). He specifically advises
against nesting these under a brand or product name, because product names can change and
often have little correlation to the actual Bounded Contexts. Once the Bounded Context is
defined as the top-level package, architectural layers are nested beneath it
[Source: Software Architecture & DDD notebook, Q2].

**Eric Evans** views Modules as a critical communication mechanism that must tell the story
of the system. Regarding Bounded Contexts, Evans states that "it comes naturally to
segregate the code of different CONTEXTS into different MODULES"
[Source: Software Architecture & DDD notebook, Q2].

**Vlad Khononov** emphasises that Bounded Contexts are meant to be physical boundaries
and should ideally be implemented, evolved, and versioned independently. When navigating
this in a monorepo, he stresses that logical boundaries (namespaces, modules, packages)
must be strictly aligned with the Bounded Context/subdomain boundaries. Failing to
separate these contexts at the highest level leads to a "big ball of mud"
[Source: Software Architecture & DDD notebook, Q2].

### Deep vs. Shallow Modules and Domain vs. Technical Partitioning

**John Ousterhout** (A Philosophy of Software Design) evaluates modules based on a
cost-benefit analysis where a module's functionality is the benefit and its interface is
the cost. Deep modules provide powerful functionality behind a simple, minimal interface.
Shallow modules provide very little functionality relative to their interface complexity.
Over-subdividing code leads to "classitis" -- a system overwhelmed by numerous shallow
modules [Source: Software Architecture & DDD notebook, Q4].

Applied to the package decision: you should bring pieces of code together if they share
information, overlap conceptually, or if combining them simplifies the overarching
interface. You must separate general-purpose and special-purpose code -- special-purpose
code should be pulled upward into a separate, independent module to prevent the
general-purpose module's interface from becoming bloated
[Source: Software Architecture & DDD notebook, Q4].

**Neal Ford** contrasts technically-partitioned architectures (organised by technical role)
with domain-partitioned architectures (organised by business domain). There has been a
decided industry trend toward domain partitioning. Domain partitioning models software
closer to how the business actually functions, isolates changes to specific domain
boundaries, and drastically eases migration to distributed architectures. Ford concludes
that "the major lesson of the last decade of architecture design is to model the semantics
of the workflow as closely as possible with the implementation"
[Source: Software Architecture & DDD notebook, Q4].

### Context Mapping Between Sibling Packages

When sibling packages need to share domain concepts, a single massive "common" package
couples all siblings together. Instead, the literature recommends two approaches:
(1) duplicate the concept -- accept that the same real-world concept means something
slightly different in each context and model it separately; (2) use fine-grained shared
libraries -- smaller, functionally partitioned shared packages rather than a "catch-all"
[Source: Software Architecture & DDD notebook, Q3].

The three primary Context Mapping patterns for integrating sibling packages are:

- **Shared Kernel**: An explicit, mutually agreed subset of the domain model shared
  between contexts. Use only when duplication cost significantly exceeds coordination
  cost. Requires cooperative partnership between teams and limits the shared portion to
  highly stable elements [Source: Software Architecture & DDD notebook, Q3].

- **Anti-Corruption Layer (ACL)**: A defensive translation mechanism built by the
  consuming context. Instead of directly importing foreign objects, the ACL translates
  upstream data into its own native language. Use to protect a Core Domain from upstream
  volatility [Source: Software Architecture & DDD notebook, Q3].

- **Published Language**: A standardised exchange format (JSON, schemas) used as a
  communication medium. Use when an upstream context exposes an API to many consumers
  [Source: Software Architecture & DDD notebook, Q3].

### AI System Engineering: Independent Tools as Sibling Packages

In AI engineering, a core best practice is that each tool should be designed as a
self-contained module that can be easily integrated, updated, or replaced without
overhauling the entire system. Building AI-powered tools as independent sibling packages
with a thin orchestrator ensures: reusability and extraction to standalone packages;
simplified orchestration (the orchestrator's job is to sequence tasks, manage state, and
handle failures); and independent testing and evaluation (critical for probabilistic LLM
components) [Source: AI System Engineering notebook, Q1].

Composition patterns for independent tools include: sequential chains (output of one
becomes input of the next), directed acyclic graphs (parallel execution), cyclic graphs
(reflection/error correction loops), and message brokers (event-driven async
communication). The recommendation is to start with simple sequential chains and only
introduce complexity when workflows strictly require it
[Source: AI System Engineering notebook, Q1].

### BPM: Process Decomposition Principles

Business Process Management (BPM) provides four principles for decomposition decisions:

1. **Process Composability and Reusability**: Break apart when components have potential
   to be reused across different parent processes
   [Source: Business Process Management notebook, Q1].

2. **Loose Coupling**: Decouple to reduce the risk that modifying one component creates
   breaking changes in another [Source: Business Process Management notebook, Q1].

3. **Process Autonomy**: Break out a component if it can act autonomously with
   behavioural predictability [Source: Business Process Management notebook, Q1].

4. **Process Granularity**: Group activities into a single process when they form an
   "atomic" unit of work that describes tasks necessary to perform a single capability.
   Break apart when a high-level process becomes too complex
   [Source: Business Process Management notebook, Q1].

### Decision Matrix: Sibling Package vs. Subpackage

The literature converges on five decision criteria (synthesised from Evans, Vernon,
Khononov, Ousterhout, and Ford) [Source: Software Architecture & DDD notebook, Q5]:

| # | Signal | Create Sibling Package | Keep as Subpackage |
|---|--------|------------------------|--------------------|
| 1 | **Language boundary** | New capability introduces a shift in Ubiquitous Language; existing terms take on different meanings | Capability is an intrinsic part of the existing language |
| 2 | **Conceptual cohesion** | Capabilities are fundamentally unrelated and do not share information | Capabilities share information, overlap conceptually, or are frequently used together |
| 3 | **Interface simplicity** | Existing package provides general-purpose mechanism; new capability is special-purpose | Combining simplifies the overall interface and hides complexity (creates a "deep module") |
| 4 | **Rate of change** | New capability exhibits high volatility compared to stable existing package | Both change at similar rates for similar reasons |
| 5 | **Team ownership** | Different team/person will own and maintain the new capability | Same team maintains both; no ownership boundary needed |

Additional signals:

- If a capability may graduate to a standalone PyPI package, start as a sibling
- If a capability requires different architecture characteristics (scalability, security), separate it
- If separating would force excessive inter-service communication for a single workflow, keep together

## Implications for Redline

**Current state**: Redline uses a single top-level package `rl` with an internal layered
architecture (`domain > enrichment > schemas > functions > calculators`). The plan for the
skeleton generator proposes `src/rl/skeleton/` -- a subpackage.

**Assessment against the decision matrix**:

1. **Language boundary**: "Skeleton", "section config", and "project metadata" are new
   domain terms that do not overlap with the existing retaining wall vocabulary. This is a
   new Bounded Context. Signal: **sibling**.

2. **Conceptual cohesion**: The skeleton generator does not share data or concepts with
   the retaining wall reader. They are independent capabilities. Signal: **sibling**.

3. **Interface simplicity**: `rl` provides geotechnical analysis (general-purpose domain);
   skeleton generation is a special-purpose application. Ousterhout says: separate. Signal:
   **sibling**.

4. **Rate of change**: Skeleton generation will evolve rapidly in Phases 0-6 while the
   existing `rl` layers are stable. Signal: **sibling**.

5. **Team ownership**: Same developer for now, but the future reviewer tool will be an
   independent workflow. Signal: **neutral to sibling** (preparing for future separation).

**Recommendation**: `skeleton` should be `src/skeleton/`, not `src/rl/skeleton/`. The same
applies to the future `reviewer` package. The `rl` package becomes a thin integration hub
that composes the independent tools, mirroring the `herne_bay`/`pyzometer`/`sarpy` pattern
from prior projects.

**Structural change required**:

```
src/
  rl/           # integration hub (thin orchestrator)
  skeleton/     # standalone skeleton generator (own bounded context)
  reviewer/     # future: standalone report reviewer
```

**Import-linter implications**: Instead of a single `rl layers` contract with `skeleton`
as a peer layer, define independence contracts between top-level packages. Each package
can have its own internal layer contract if needed. The `rl` hub may import from
`skeleton` and `reviewer`, but they must not import from each other or from `rl`.

**pyproject.toml implications**: The `[tool.hatch] build.targets.wheel.packages` list
must include each sibling package (e.g., `["src/rl", "src/skeleton"]`).

**Context Mapping**: `rl` depends on `skeleton` as a Customer-Supplier relationship.
`skeleton` exposes a public API (`build_skeleton`) and does not know about `rl`. Shared
domain types (if any emerge) should use fine-grained shared libraries or duplication,
never a monolithic "common" package.

## Open Questions

- Should the shared Pydantic models that both `rl` and `skeleton` might need (e.g., a
  generic `ProjectMetadata`) live in a small fine-grained shared kernel package like
  `src/redline_core/`, or should each context define its own version?
- When `reviewer` is introduced, should it consume `skeleton` output via Published
  Language (e.g., a DOCX contract) or via direct Python imports?
- Should `rl` itself retain an internal layered architecture, or does it become thin
  enough that layers are unnecessary?

## Glossary

| Term | Definition |
|---|---|
| Modularity | Decomposing a system into independent, replaceable components (packages) based on business capability |
| Layering | Organising code within a component into horizontal tiers with strict dependency direction (higher layers depend on lower layers, never the reverse) |
| Bounded Context | A DDD concept: a strict semantic boundary where a specific domain vocabulary (Ubiquitous Language) applies consistently |
| Ubiquitous Language | The shared vocabulary between developers and domain experts within a Bounded Context; used consistently in code, docs, and conversation |
| Deep Module | A module that provides powerful functionality behind a simple, minimal interface (Ousterhout) |
| Shallow Module | A module that provides little functionality relative to its interface complexity (Ousterhout) |
| Domain Partitioning | Organising top-level architecture around business domains/workflows rather than technical roles |
| Technical Partitioning | Organising top-level architecture around technical capabilities (presentation, business, persistence) |
| Shared Kernel | A DDD Context Mapping pattern: a small, mutually agreed subset of the domain model shared between two contexts |
| Anti-Corruption Layer | A DDD pattern: a defensive translation layer that converts foreign domain concepts into a context's native language |
| Published Language | A DDD pattern: a standardised exchange format (JSON, XML) used for cross-context communication |
| Context Map | A diagram/document charting the relationships and integration patterns between Bounded Contexts |
| Process Composability | A BPM principle: designing sub-processes so they can be reused in multiple parent processes |

## Sources Consulted

| Notebook | Queries asked | Citations returned |
|---|---|---|
| Software Architecture & Domain-Driven Design | 5 | Evans (Modules, Bounded Contexts), Vernon (top-level BC packages, layer nesting), Khononov (physical boundaries, monorepo alignment), Ousterhout (deep/shallow modules, general/special-purpose separation), Ford (domain vs technical partitioning, architecture quantum) |
| AI System Engineering | 1 | Self-contained AI tool modules, orchestrator patterns (chains, DAGs, cyclic graphs, message brokers), independent testing for probabilistic components |
| Business Process Management | 1 | Process Composability, Loose Coupling, Process Autonomy, Process Granularity, Process-Oriented Architecture (POA) |
