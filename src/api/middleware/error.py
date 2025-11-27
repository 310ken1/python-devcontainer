"""APIエラーミドルウェア."""

from __future__ import annotations

import json
from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools import Logger, Metrics
    from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
    from aws_lambda_powertools.utilities.typing import LambdaContext


class APIError(Exception):
    """APIエラーの基底クラス."""


class APIFatalError(APIError):
    """復旧不可能なAPIエラー."""


class UnhandledError(APIError):
    """予期しない例外."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"
    id: str = "UnhandledException"


class InternalServerError(APIFatalError):
    """500 Internal Server Error (サーバー内部エラー)."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"
    id: str = "InternalServerError"


class APITransientError(APIError):
    """一時的な(復旧可能な)APIエラー."""


class ServiceUnavailableError(APITransientError):
    """503 Service Unavailable (サービス利用不可)."""

    status_code: int = HTTPStatus.SERVICE_UNAVAILABLE
    message: str = "Service Unavailable"
    id: str = "ServiceUnavailableError"


class ClientError(APIError):
    """クライアント要因の警告."""


class BadRequestError(ClientError):
    """400 Bad Request (不正なリクエスト構文)."""

    status_code: int = HTTPStatus.BAD_REQUEST
    message: str = "Bad Request"
    id: str = "BadRequestError"


class UnauthorizedError(ClientError):
    """401 Unauthorized (認証エラー)."""

    status_code: int = HTTPStatus.UNAUTHORIZED
    message: str = "Unauthorized"
    id: str = "UnauthorizedError"


class ForbiddenError(ClientError):
    """403 Forbidden (認可エラー)."""

    status_code: int = HTTPStatus.FORBIDDEN
    message: str = "Forbidden"
    id: str = "ForbiddenError"


class NotFoundError(ClientError):
    """404 Not Found (リソース未発見)."""

    status_code: int = HTTPStatus.NOT_FOUND
    message: str = "Not Found"
    id: str = "NotFoundError"


def _error_helper(error: Exception, logger: Logger, metrics: Metrics = None) -> dict[str, Any]:
    """APIErrorをHTTPレスポンスに変換するヘルパー関数."""
    if isinstance(error, APIFatalError):
        logger.exception(error.id)
    elif isinstance(error, APITransientError):
        logger.error(error.id)
    elif isinstance(error, ClientError):
        logger.warning(error.id)
    else:
        error = UnhandledError()
        logger.exception(error.id)

    if metrics:
        metrics.add_metric(name=error.id, unit="Count", value=1)

    return {
        "statusCode": error.status_code,
        "body": json.dumps({"message": error.message}),
        "headers": {"Content-Type": "application/json"},
        "isBase64Encoded": False,
    }


def error_handler(logger: Logger, metrics: Metrics = None) -> Callable:
    """カスタム例外をHTTPレスポンスに変換するデコレータ."""

    def decorator(lambda_handler: Callable) -> Callable:
        """デコレータ関数."""

        @wraps(lambda_handler)
        def wrapper(event: APIGatewayProxyEvent, context: LambdaContext) -> dict[str, Any]:
            try:
                return lambda_handler(event, context)

            except Exception as e:  # noqa: BLE001
                return _error_helper(e, logger, metrics)

        return wrapper

    return decorator
