"""ユーザルータ."""

import http

from aws_lambda_powertools.event_handler.api_gateway import Router

from schemas.error import InternalServerErrorResponse, UnauthorizedResponse
from schemas.user import User

router = Router()


@router.get(
    "/users",
    tags=["Users"],
    summary="ユーザー情報リストの取得",
    description="ユーザリストを取得する.",
    responses={
        http.HTTPStatus.OK: {
            "description": "成功",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": User.model_json_schema(),
                    },
                },
            },
        },
        http.HTTPStatus.UNAUTHORIZED: UnauthorizedResponse,
        http.HTTPStatus.INTERNAL_SERVER_ERROR: InternalServerErrorResponse,
    },
)
def get_list() -> list[User]:
    """."""
    return [
        User(id=1000, name="テスト1", email="test1@example.com"),
        User(id=1001, name="テスト2", email="test2@example.com"),
    ]
