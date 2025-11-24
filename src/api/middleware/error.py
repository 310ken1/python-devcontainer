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


class BadRequestError(Exception):
    """400 エラー例外."""


class UnauthorizedError(Exception):
    """401 エラー例外."""


class InternalServerError(Exception):
    """500 エラー."""


def error_handler(logger: Logger, metrics: Metrics = None) -> Callable:
    """カスタム例外をHTTPレスポンスに変換するデコレータ."""

    def decorator(lambda_handler: Callable) -> Callable:
        """デコレータ関数."""

        @wraps(lambda_handler)
        def wrapper(event: APIGatewayProxyEvent, context: LambdaContext) -> dict[str, Any]:
            try:
                return lambda_handler(event, context)

            except BadRequestError:
                logger.warning("BadRequestError")
                if metrics:
                    metrics.add_metric(name="BadRequestError", unit="Count", value=1)
                return {
                    "statusCode": HTTPStatus.BAD_REQUEST,
                    "body": json.dumps({"error": "Bad Request"}),
                }

            except UnauthorizedError:
                logger.warning("UnauthorizedError")
                if metrics:
                    metrics.add_metric(name="UnauthorizedError", unit="Count", value=1)
                return {
                    "statusCode": HTTPStatus.UNAUTHORIZED,
                    "body": json.dumps({"error": "Unauthorized"}),
                }

            except InternalServerError:
                logger.exception("InternalServerError")
                if metrics:
                    metrics.add_metric(name="InternalServerError", unit="Count", value=1)
                return {
                    "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "body": json.dumps({"error": "Internal Server Error"}),
                }

            except Exception:
                logger.exception("UnhandledException")
                if metrics:
                    metrics.add_metric(name="UnhandledException", unit="Count", value=1)
                return {
                    "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "body": json.dumps({"error": "Internal Server Error"}),
                }

        return wrapper

    return decorator
