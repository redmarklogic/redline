# 0011 --- Point solution vs quality layer

**Date**: 2026-04-26

**Skill**: `pm-product-strategist` (link: `.agents/skills/pm-product-strategist/SKILL.md`)

**Context**: Analysing Leya (leya.law, legal AI startup, $675M valuation, YC W24;
note: original notebook source transcribed the name as "Legora" — corrected 2026-04-27),
as an adjacent-market signal for Redline's geotechnical AI positioning.

**Observation**: In legal tech, fragmented point solutions (templating, translation,
redlining, contract research) became obsolete when generative AI could cover all
text-processing workflows from a single interface. Leya succeeded by positioning as
a firm-wide legal workspace with playbook-driven review, audit trail, and Word-native
integration --- not as a feature that does one thing.

**Root Cause**: Point solutions in document-heavy, high-liability professions are
vulnerable because their surface-level task (e.g., "flag missing clauses") can be
replicated by any sufficiently capable LLM. What cannot be replicated quickly is
domain-specific curation (playbooks, standards corpora, firm-specific rules) and the
trust infrastructure (audit trails, version history, explainability) that wraps it.

**Principle**: In document-heavy, high-liability professions, do not build AI point
solutions where the durable value is a domain-specific quality layer with audit trail.
The defensible asset is the curated knowledge corpus and the firm-specific
configuration layered on top --- not the AI text-processing capability itself.

**Refinement (2026-05-03)**: Microsoft Word Legal Agent and actual Legora strengthen the
same principle from a platform-risk angle. Once a platform owner makes document-native
review, redlining, citations, and tracked changes native to the workflow surface, the
moat moves even more decisively to domain corpus, firm rules, audit trail, and adoption
context. Redline should treat generic Word review as table stakes and defend the
geotechnical quality layer.

**Source**: `docs/research/20260426-legal-ai-adjacent-market-signal.md`
**Additional source**: `docs/research/20260503-microsoft-word-legal-agent-robin-ai-legora-signal.md`
