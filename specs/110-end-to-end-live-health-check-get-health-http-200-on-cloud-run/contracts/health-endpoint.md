# Contract: Health Endpoint (live acceptance surface)

**Source of truth**: `src/marker/api/health.py` ("body is fixed by contract";
the module docstring cites its spec's US1/FR-001–FR-006). This feature consumes
the contract; it must not change it.

## Request

```text
GET <service-url>/health
```

- No authentication.
- No rate limiting (exempt by design — probes call continuously).
- `<service-url>`: Terraform output `staging_url` (Stage 1) or
  `gcloud run services describe staging-redline-api --region australia-southeast1 --format 'value(status.url)'` (CI).

## Response

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"healthy"}
```

- Status code: exactly `200`.
- Body: the JSON object `{"status": "healthy"}` — founder ruling 2026-06-11
  supersedes issue #110's `{"status": "ok"}` wording.
- **Comparison rule**: assert JSON-equality (parse, then compare), never
  byte-equality — FastAPI serializes compact (`{"status":"healthy"}`, no space),
  so a literal string match against the spec's pretty form fails.
- Port inside the container: 8080 (startup probe and Dockerfile agree).

## Consumers and tolerances

| Consumer | Tolerance |
|---|---|
| Cloud Run startup probe | 10 s initial delay, 3 failures × 5 s timeout |
| CI health-check step | Wait for service Ready condition, then poll with retry up to ~120 s (cold start on scale-to-zero), then assert code + JSON-equal body |
| Manual Stage 1 curl | Single request after service reports Ready |
