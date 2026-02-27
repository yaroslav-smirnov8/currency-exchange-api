from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aiohttp import web


@dataclass(frozen=True, slots=True)
class AppError(Exception):
    code: str
    message: str
    http_status: int = 400
    details: dict[str, Any] | None = None


class ValidationError(AppError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(code="validation_error", message=message, http_status=400, details=details)


class ProviderError(AppError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(code="provider_error", message=message, http_status=502, details=details)


class NotFoundError(AppError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(code="not_found", message=message, http_status=404, details=details)


def json_response(data: Any, status: int = 200) -> web.Response:
    return web.json_response({"data": data}, status=status)


def json_error_response(error: AppError) -> web.Response:
    payload: dict[str, Any] = {
        "error": {
            "code": error.code,
            "message": error.message,
        }
    }
    if error.details:
        payload["error"]["details"] = error.details
    return web.json_response(payload, status=error.http_status)

