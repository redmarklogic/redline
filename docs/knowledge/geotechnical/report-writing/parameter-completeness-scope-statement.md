# Parameter Completeness Scope Statement

**Status**: draft
**Owner**: Graeme (Principal Geotechnical Engineer)
**Last updated**: 2026-05-04
**Provenance**: Parameter completeness advisory session, 2026-05-04

**Sub-domain**: report-writing
**Confidence**: practitioner-grounded

## Canonical Scope Statement

> Parameter Completeness Checking
>
> Redline shall verify that a geotechnical design report documents all parameters
> required for the specific design type(s) addressed, and flags the presence of
> parameters not relevant to those design types.
>
> This requires:
>
> 1. A design type taxonomy mapping each sub-type to its required input and output
>    parameters
> 2. A regional overlay identifying additional parameters required by local regulatory
>    frameworks
> 3. Awareness of parameter placement -- distinguishing between parameters that must
>    appear in the report body, parameters that may appear in appendices, and parameters
>    that legitimately reside only in calculation files
>
> Pareto-governed: initial coverage targets the five highest-volume design types before
> expanding.
>
> The system checks for presence and relevance, not correctness of values.

## Failure Modes

Parameter completeness checking addresses two distinct failure modes, not one.

### Under-inclusion (missing parameters)

The report omits a parameter required for the design type. This is the obvious failure
mode. A slope stability report that does not state the shear strength parameters used,
or a foundation report that does not document the assumed groundwater level, has a gap
that could lead to errors, rework, or liability exposure.

Case law confirms that omitting information "vital to the integrity" of a structure
constitutes negligence (see parameter-completeness-checking-standard-of-care.md for
the three leading cases).

### Over-inclusion (irrelevant parameters)

The report includes parameters that are not relevant to the design type addressed. This
is a less obvious but equally documented failure mode. Corporate guidance from large
consultancies explicitly states that "many of our reports are too wordy and complex" and
include "information which is not relevant to the reader."

Over-inclusion creates noise. It makes the report harder to review, obscures the
parameters that actually matter, and can mislead downstream parties into thinking
a parameter was considered in the design when it was merely listed.

A complete check flags both: parameters that should be present but are not, and
parameters that are present but should not be.

## The "Teach for Free, Check for Pay" Principle

The design-type taxonomy serves two purposes with different commercial models:

1. **Teaching** (skeleton generation): When a designer starts a new report, the system
   can present the parameter set for their chosen design type as a template or skeleton.
   This teaches less experienced engineers what parameters to include. This is a
   productivity and training function, and may be offered at lower cost or for free
   as a market entry mechanism.

2. **Checking** (pre-review): When a designer submits a completed report, the system
   can verify that all required parameters are present and flag irrelevant parameters.
   This is a quality assurance function that directly reduces risk and liability
   exposure. This is the higher-value service.

The taxonomy is the same in both cases. The commercial distinction is between using
the taxonomy prospectively (before writing) versus retrospectively (after writing).

## Three-Tier Taxonomy Exposure Model

The design-type taxonomy contains commercially sensitive information about the depth
of Redline's domain knowledge. Not all of it should be visible to all audiences:

1. **Public tier** (website, marketing): Top-level categories only.
   Example: "Foundations", "Retaining Structures", "Slope Stability".
   This demonstrates breadth without revealing depth.

2. **Sales tier** (demos, proposals): Category and family/type level.
   Example: "Foundations > Shallow > Pad Footings". This demonstrates structured
   knowledge without exposing the full parameter sets.

3. **Product tier** (paying users only): Full taxonomy including sub-types,
   parameter sets, regional overlays, and input/output classification.
   This is the operational knowledge that powers the checking engine.

## Presence and Relevance, Not Correctness

The scope statement explicitly limits the check to presence and relevance:

- **Presence**: Is the parameter documented somewhere in the report or its appendices?
- **Relevance**: Is the parameter appropriate for the design type(s) addressed?

The system does not check whether the parameter value is correct, reasonable, or
consistent with other values. Value checking (e.g., "is this friction angle realistic
for this soil type?") is a separate, harder problem that requires engineering judgment
and is not in scope for parameter completeness checking.

This boundary is important because it keeps the system in the domain of structured
document analysis (checkable by rules) rather than engineering assessment (requires
professional judgment).

## Open Questions

1. How should the system handle reports that address multiple design types
   simultaneously (e.g., a report covering both foundations and retaining walls)?
   Union of parameter sets? Separate checklists per section?
2. Should the check distinguish between parameters that are explicitly stated versus
   parameters that can be inferred from other stated values?
3. What is the minimum confidence level required before a parameter set can be used
   for checking (as opposed to teaching only)?
