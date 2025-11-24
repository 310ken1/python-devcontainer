"""Lambda関数(Amazon API Gateway)サンプル."""

from __future__ import annotations

import json
import os
import textwrap
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent, event_source
from aws_lambda_powertools.utilities.parser import BaseModel, ValidationError, parse
from aws_lambda_powertools.utilities.validation import validate

from api.error_middleware import BadRequestError, handle_api_errors

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext

LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
SSM_PATH_PREFIX: str = os.environ.get("SSM_PATH_PREFIX", "/python-devcontainer/dev/")

SERVICE_NAME: str = "python-devcontainer"
NAMESPACE_NAME: str = "lambda_handler"

logger: Logger = Logger(service=SERVICE_NAME, level=LOG_LEVEL)
tracer: Tracer = Tracer(service=SERVICE_NAME)
metrics: Metrics = Metrics(namespace=NAMESPACE_NAME, service=SERVICE_NAME)


def get_psycopg2() -> Any:  # noqa: ANN401
    """psycopg2モジュールを遅延インポートして返す.

    Returns:
        Any: psycopg2モジュール
    """
    # NOTE: Lambdaのコールドスタート時間短縮のため、psycopg2を遅延インポート
    import psycopg2  # noqa: PLC0415

    return psycopg2


class User(BaseModel):
    """リクエストボディのユーザーIDを定義するスキーマ."""

    id: int


@metrics.log_metrics(capture_cold_start_metric=True)
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
@event_source(data_class=APIGatewayProxyEvent)
@handle_api_errors(logger)
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
        validate(
            event=body,
            schema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                },
                "required": ["id"],
            },
        )
        user: User = parse(event=body, model=User)

    except ValidationError as e:
        raise BadRequestError from e

    logger.append_keys(user_id=user.id)

    settings: dict = parameters.get_parameter(f"{SSM_PATH_PREFIX}settings", transform="json")
    db_settings: dict = settings["db"]

    psycopg2_module = get_psycopg2()
    query: str = textwrap.dedent(
        """
                SELECT
                    user_id
                    , email
                    , username
                    , display_name
                FROM
                    users
                WHERE
                    user_id = %s;
            """,
    )

    with (
        psycopg2_module.connect(
            dbname=db_settings["database"],
            user=db_settings["user"],
            password=db_settings["password"],
            host=db_settings["host"],
            port=db_settings["port"],
        ) as conn,
        conn.cursor() as cursor,
    ):
        cursor.execute(query, (user.id,))
        record = cursor.fetchone()

    if record:
        response_body = {
            "user_id": record[0],
            "email": record[1],
            "username": record[2],
            "display_name": record[3],
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
