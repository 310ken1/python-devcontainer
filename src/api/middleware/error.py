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

    level: str = "exception"
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"
    log_message: str = "UnhandledException"
    metric_name: str = "UnhandledException"


class BadRequestError(APIError):
    """400 エラー例外."""

    level: str = "warning"
    status_code: int = HTTPStatus.BAD_REQUEST
    message: str = "Bad Request"
    log_message: str = "BadRequestError"
    metric_name: str = "BadRequestError"


class UnauthorizedError(APIError):
    """401 エラー例外."""

    level: str = "warning"
    status_code: int = HTTPStatus.UNAUTHORIZED
    message: str = "Unauthorized"
    log_message: str = "UnauthorizedError"
    metric_name: str = "UnauthorizedError"


class InternalServerError(APIError):
    """500 エラー例外."""

    level: str = "exception"
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"
    log_message: str = "InternalServerError"
    metric_name: str = "InternalServerError"


def _error_helper(error: Exception, logger: Logger, metrics: Metrics = None) -> dict[str, Any]:
    """APIErrorをHTTPレスポンスに変換するヘルパー関数."""
    e: APIError = error if isinstance(error, APIError) else InternalServerError()

    if e.level == "warning":
        logger.warning(e.log_message)
    elif e.level == "error":
        logger.error(e.log_message)
    elif e.level == "exception":
        logger.exception(e.log_message)
    else:
        logger.info(e.log_message)
    if metrics:
        metrics.add_metric(name=e.metric_name, unit="Count", value=1)
    return {
        "statusCode": e.status_code,
        "body": json.dumps({"error": e.message}),
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
