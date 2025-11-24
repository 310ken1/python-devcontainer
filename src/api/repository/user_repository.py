"""UserRepositoryモジュール."""

import textwrap
import time
from typing import TYPE_CHECKING

from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
from pydantic import BaseModel

from api.repository.db_connector import DBConnector

if TYPE_CHECKING:
    from psycopg2.extras import DictRow


class UserRecord(BaseModel):
    """DBから取得したユーザーレコードのスキーマ."""

    user_id: int
    email: str
    username: str | None
    display_name: str | None


class UserRepository:
    """UserRepositoryクラス."""

    def __init__(self, connector: DBConnector, metrics: Metrics | None) -> None:
        """初期化."""
        self.connector = connector
        self.metrics = metrics

    def get_user_by_id(self, user_id: int) -> UserRecord | None:
        """ユーザーIDに基づいてユーザー情報を取得する."""
        psycopg2 = self.connector.get_psycopg2()
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

        start_time = time.perf_counter()

        with (
            self.connector.connect() as conn,
            conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor,
        ):
            cursor.execute(query, (user_id,))
            record: DictRow = cursor.fetchone()

        end_time = time.perf_counter()
        if self.metrics:
            self.metrics.add_metric(  # メトリクス計測は引き続きここで行う
                name="DatabaseQueryLatency",
                unit=MetricUnit.Milliseconds,
                value=(end_time - start_time) * 1000,
            )

        return UserRecord.model_validate(dict(record)) if record else None
