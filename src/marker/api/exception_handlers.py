"""Global exception handlers for the Marker API.

Registers uniform error envelope handlers on the FastAPI application.
Every non-2xx response uses the shape: {code, message, trace_id, details?}

Module note: the binding of these handlers to routes is a documented placeholder
pending issue #78 (Option B — global handler wiring strategy).
"""

import logging
import uuid

import pydantic
from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def _envelope(
    code: str,
    message: str,
    *,
    details: object = None,
) -> dict[str, object]:
    """Build a standard error envelope dict.

    Args:
        code: Stable machine-readable error code.
        message: Human-readable, display-safe message.
        details: Optional machine-actionable specifics.

    Returns:
        Error envelope mapping.
    """
    envelope: dict[str, object] = {
        "code": code,
        "message": message,
        "trace_id": str(uuid.uuid4()),
    }
    if details is not None:
        envelope["details"] = details
    return envelope


def _sanitize_errors(errors: list[dict]) -> list[dict]:
    """Remove non-JSON-serializable objects from Pydantic error dicts.

    Pydantic v2 includes the original exception object under ``ctx["error"]``.
    JSON cannot serialise Python exceptions, so we replace them with their
    string representation.

    Args:
        errors: Raw error list from ``exc.errors()``.

    Returns:
        A copy of the list with all ``ctx["error"]`` values stringified.
    """
    sanitized = []
    for error in errors:
        entry = dict(error)
        ctx = entry.get("ctx")
        if (
            isinstance(ctx, dict)
            and "error" in ctx
            and isinstance(ctx["error"], Exception)
        ):
            entry["ctx"] = {**ctx, "error": str(ctx["error"])}
        sanitized.append(entry)
    return sanitized


def register_exception_handlers(app: FastAPI) -> None:
    """Attach global exception handlers to app.

    Covers: StarletteHTTPException, RequestValidationError,
    pydantic.ValidationError (defense-in-depth), and bare Exception (catch-all).

    Args:
        app: FastAPI application instance to configure.
    """

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Map StarletteHTTPException to the standard error envelope.

        Args:
            request: Incoming HTTP request.
            exc: The raised HTTP exception.

        Returns:
            JSONResponse with the error envelope.
        """
        status_code = exc.status_code
        if status_code == status.HTTP_401_UNAUTHORIZED:
            code = "HTTP_401"
            message = "Authentication required."
        elif status_code == status.HTTP_403_FORBIDDEN:
            code = "HTTP_403"
            message = "Access denied."
        elif status_code == status.HTTP_404_NOT_FOUND:
            code = "NOT_FOUND"
            message = "Resource not found."
        else:
            code = f"HTTP_{status_code}"
            message = str(exc.detail) if exc.detail else "HTTP error."
        headers: dict[str, str] = dict(exc.headers) if exc.headers else {}
        return JSONResponse(
            status_code=status_code,
            content=_envelope(code, message),
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Map RequestValidationError to the standard error envelope.

        Unparsable bodies (json_invalid) → 400 BAD_REQUEST.
        All other validation failures → 422 VALIDATION_ERROR with details.

        Args:
            request: Incoming HTTP request.
            exc: The raised validation error.

        Returns:
            JSONResponse with the error envelope.
        """
        errors = exc.errors()
        is_json_invalid = any(e.get("type") == "json_invalid" for e in errors)
        if is_json_invalid:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=_envelope("BAD_REQUEST", "Request body could not be parsed."),
            )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=_envelope(
                "VALIDATION_ERROR",
                "Request validation failed.",
                details=_sanitize_errors(errors),
            ),
        )

    @app.exception_handler(pydantic.ValidationError)
    async def pydantic_validation_handler(
        request: Request, exc: pydantic.ValidationError
    ) -> JSONResponse:
        """Map pydantic.ValidationError to the standard error envelope (defense-in-depth).

        Catches domain-model failures raised during DTO→domain translation
        so they never become 500 errors.

        Args:
            request: Incoming HTTP request.
            exc: The raised Pydantic validation error.

        Returns:
            JSONResponse with the error envelope.
        """
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=_envelope(
                "VALIDATION_ERROR",
                "Request validation failed.",
                details=_sanitize_errors(exc.errors()),
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Catch-all handler: log the exception and return a safe 500 envelope.

        No internal detail (stack trace, class name, path) is included in the
        response body.

        Args:
            request: Incoming HTTP request.
            exc: The unhandled exception.

        Returns:
            JSONResponse with a safe INTERNAL_ERROR envelope.
        """
        logger.exception("Unhandled exception on %s %s", request.method, request.url)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_envelope(
                "INTERNAL_ERROR",
                "An unexpected error occurred. Please try again later.",
            ),
        )
