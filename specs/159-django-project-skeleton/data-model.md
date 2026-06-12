# Data Model: Django Project Skeleton (#159)

**This slice introduces no entities.** That is a deliberate scope boundary, not an
omission (spec Out-of-Scope table; research.md D6):

- No Django ORM model is created. The first platform-state models (user/identity,
  audit log) belong to #165 and #166, after DATABASES wiring in #164.
- No database is provisioned, migrated, or written. The generated settings' default
  DATABASES stanza stays inert — `manage.py check` and the placeholder root view
  require no connection.
- Constitution XVIII guardrail holds vacuously: zero ORM models means zero risk of a
  geotechnical concept appearing as one. The guardrail becomes machine-enforced in
  #160 (import-linter contract).

Anything that looks like a data-model decision encountered during implementation is
out of scope here and escalates to the founder (per the sprint WBS row for #159).
