"""DB接続用モジュール."""

from contextlib import contextmanager
from typing import Any

from aws_lambda_powertools.utilities import parameters


class DBConnector:
    """DB接続を管理するクラス."""

    def __init__(self, settings_path: str) -> None:
        """初期化."""
        self.settings_path = settings_path
        self._db_settings = self._load_db_settings()

    def _load_db_settings(self) -> dict:
        settings: dict = parameters.get_parameter(self.settings_path, transform="json")
        return settings["db"]

    def get_psycopg2(self) -> Any:  # noqa: ANN401
        """psycopg2モジュールを遅延インポートして返す.

        Returns:
            Any: psycopg2モジュール
        """
        import psycopg2  # noqa: PLC0415
        import psycopg2.extras  # noqa: PLC0415

        return psycopg2

    @contextmanager
    def connect(self) -> Any:  # noqa: ANN401
        """DB接続コンテキストマネージャ."""
        psycopg2 = self.get_psycopg2()
        conn = psycopg2.connect(
            dbname=self._db_settings["database"],
            user=self._db_settings["user"],
            password=self._db_settings["password"],
            host=self._db_settings["host"],
            port=self._db_settings["port"],
        )
        try:
            yield conn
        finally:
            conn.close()
