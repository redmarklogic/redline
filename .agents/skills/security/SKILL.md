---
name: security
description: Secure coding rules for secrets, configuration, and logging in this repo.
---

# Security

This skill defines security rules for day-to-day development in this repo.

## Boundary Contract

### Applies To
- Secrets handling, configuration, and logging across all code

### Produces
- Code free from hardcoded secrets, safe logging, and secure configuration patterns

### Does Not Cover
- General style (`python-style`)
- Error handling (`python-error-handling`)
- Authentication and authorization architecture

## Context & Guidelines

### Secrets

- Never hardcode real secrets (API keys, passwords, tokens) in code.
- Prefer environment variables for sensitive configuration.
- If a config file needs a value, prefer referencing an environment variable (e.g., `$FOO_API_KEY`).

### Local Configuration

- Keep `.env` out of version control.
- Use `.env.template` for documenting required environment variables.

### Logging

- Never print or log secrets.
- Avoid logging URLs if they contain API keys or other credentials.
- Avoid logging sensitive information (passwords, tokens, PII).

## Procedure

1. Treat any credential as sensitive.
2. Store secrets in environment variables or the deployment secret store.
3. Keep logs safe: redact or omit sensitive values.
