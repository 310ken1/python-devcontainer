"""検証ミドルウェア."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools.utilities import validation

from api.middleware.error import BadRequestError

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
    from aws_lambda_powertools.utilities.typing import LambdaContext


def validate(query_schema: dict | None = None, body_schema: dict | None = None) -> Callable:
    """クエリパラメータとリクエストボディを検証するデコレータ."""

    def decorator(lambda_handler: Callable) -> Callable:
        """デコレータ関数."""

        @wraps(lambda_handler)
        def wrapper(event: APIGatewayProxyEvent, context: LambdaContext) -> dict[str, Any]:
            try:
                if query_schema:
                    validation.validate(
                        event=event.query_string_parameters or {},
                        schema=query_schema,
                    )
                if body_schema:
                    validation.validate(
                        event=event.json_body or {},
                        schema=body_schema,
                    )
            except validation.SchemaValidationError as e:
                raise BadRequestError from e

            return lambda_handler(event, context)

        return wrapper

    return decorator
