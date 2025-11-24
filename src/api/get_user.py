"""Lambda関数(Amazon API Gateway)サンプル."""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent, event_source
from aws_lambda_powertools.utilities.parser import BaseModel, ValidationError, parse

from api.middleware.error import BadRequestError, error_handler
from api.middleware.validate import validate
from api.repository.db_connector import DBConnector
from api.repository.user_repository import UserRecord, UserRepository

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext

LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
SSM_PATH: str = os.environ.get("SSM_PATH", "/python-devcontainer/dev/settings")

SERVICE_NAME: str = "python-devcontainer"
NAMESPACE_NAME: str = "lambda_handler"

logger: Logger = Logger(service=SERVICE_NAME, level=LOG_LEVEL)
tracer: Tracer = Tracer(service=SERVICE_NAME)
metrics: Metrics = Metrics(namespace=NAMESPACE_NAME, service=SERVICE_NAME)


class User(BaseModel):
    """リクエストボディのユーザーIDを定義するスキーマ."""

    id: int


body_schema: dict = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
    },
    "required": ["id"],
}


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
@event_source(data_class=APIGatewayProxyEvent)
@error_handler(logger, metrics)
@validate(body_schema=body_schema)
def lambda_handler(event: APIGatewayProxyEvent, _: LambdaContext) -> dict[str, Any]:
    """APIGatewayからのリクエストを処理し、DBからユーザー情報を取得して返す.

    Args:
        event (APIGatewayProxyEvent): API Gatewayからのイベントデータ.
        _ (LambdaContext): Lambda実行コンテキスト (未使用).

    Returns:
        dict[str, Any]: API Gatewayへのレスポンス.
    """
    try:
        body: dict[str, Any] = event.json_body
        user: User = parse(event=body, model=User)

    except ValidationError as e:
        raise BadRequestError from e

    logger.append_keys(user_id=user.id)

    repository: UserRepository = UserRepository(DBConnector(SSM_PATH), metrics)
    record: UserRecord | None = repository.get_user_by_id(user.id)
    if record:
        response_body = {
            "user_id": record.user_id,
            "email": record.email,
            "username": record.username,
            "display_name": record.display_name,
        }
    else:
        response_body = {}

    response = {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {"Content-Type": "application/json"},
    }

    logger.info("Successfully processed request.")
    return response
