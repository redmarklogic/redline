---
id: P-027
type: strategic
date_deferred: 2026-05-31
status: open
deferred_by: Ron
owner_at_retrieval: "Founder / Engineering (produces list); Founder (signs off before trust document publishes)."
unfreeze_condition: >-
  Exhaustive sub-processor list produced (covering all services touching customer data: infrastructure, logging, error tra.
---

# Sub-processor audit required before publishing Principal-facing trust document

## Why deferred

The trust document (required before first quota-exhaustion event per `gtm/2026-launch-plan.md`) must name every service that touches customer data and accurately represent their certifications. No exhaustive sub-processor list has been produced or audited. Publishing SOC 2 sub-processor claims before the audit is complete risks a false trust claim — GTM non-goal #7.

## Unfreeze condition

Exhaustive sub-processor list produced (covering all services touching customer data: infrastructure, logging, error tracking, analytics, email, CI/CD) and every item verified against its SOC 2 scope.

## Owner at retrieval

Founder / Engineering (produces list); Founder (signs off before trust document publishes).
