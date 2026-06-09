"""Health check router -- infrastructure liveness probe (US1, FR-001 to FR-006)."""

from fastapi import APIRouter

health_router = APIRouter()


# NOTE: exempt from rate limiting (FR-006) — infrastructure probes call this continuously.
@health_router.get("/health", include_in_schema=False)
def get_health() -> dict[str, str]:
    """Return service liveness signal.

    No authentication required. No response model — body is fixed by contract.
    No per-route error handling — the global exception handler covers failures.
    """
    return {"status": "healthy"}
