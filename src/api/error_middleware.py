"""APIエラーミドルウェア."""

from __future__ import annotations

import json
from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools import Logger
    from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
    from aws_lambda_powertools.utilities.typing import LambdaContext


class BadRequestError(Exception):
    """400 エラー例外."""


class UnauthorizedError(Exception):
    """401 エラー例外."""


class InternalServerError(Exception):
    """500 エラー."""


def handle_api_errors(logger: Logger) -> Callable:
    """カスタム例外をHTTPレスポンスに変換するデコレータ."""

    def decorator(func: Callable) -> Callable:
        """デコレータ関数."""

        @wraps(func)
        def wrapper(event: APIGatewayProxyEvent, context: LambdaContext) -> dict[str, Any]:
            try:
                return func(event, context)

            except BadRequestError as e:
                logger.exception("BadRequestError", message=str(e))
                return {
                    "statusCode": HTTPStatus.BAD_REQUEST,
                    "body": json.dumps({"error": "Bad Request"}),
                }

            except UnauthorizedError as e:
                logger.exception("UnauthorizedError", message=str(e))
                return {
                    "statusCode": HTTPStatus.UNAUTHORIZED,
                    "body": json.dumps({"error": "Unauthorized"}),
                }

            except InternalServerError as e:
                logger.exception("InternalServerError", message=str(e))
                return {
                    "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "body": json.dumps({"error": "Internal Server Error"}),
                }

            except Exception as e:
                logger.exception("UnhandledException", message=str(e))
                return {
                    "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "body": json.dumps({"error": "Internal Server Error"}),
                }

        return wrapper

    return decorator
