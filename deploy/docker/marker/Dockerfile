# syntax=docker/dockerfile:1

# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.14-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project --link-mode=copy

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.14-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

RUN addgroup --gid 1000 appgroup \
 && adduser --uid 1000 --gid 1000 --disabled-password --gecos "" appuser

COPY src/ /app/src/

ENV PYTHONPATH=/app/src
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --retries=3 --start-period=15s \
  CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\", \"8080\")}/health')"

CMD ["sh", "-c", "exec python -m uvicorn marker.api.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8080} --timeout-graceful-shutdown 10"]
