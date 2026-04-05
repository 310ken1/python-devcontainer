"""ユーザルータ."""

import http

from aws_lambda_powertools.event_handler.api_gateway import Router

from schemas.error_schema import CommonResponses, NotFoundResponse
from schemas.field import Gender
from schemas.user_schema import CreateUserRequest, UpdateUserRequest, User, UserListResponse, UserResponse

router = Router()


@router.get(
    "/users",
    tags=["Users"],
    summary="ユーザー情報リストの取得",
    description="システムに登録されたユーザに関する情報のリストを取得する.",
    responses={
        **CommonResponses,
    },
)
def get_user_list() -> UserListResponse:
    """ユーザー情報リストの取得."""
    return UserListResponse(
        users=[
            User(id=1000, name="テスト1", email="test1@example.com"),
            User(id=1001, name="テスト2", email="test2@example.com"),
        ],
    )


@router.post(
    "/users",
    tags=["Users"],
    summary="ユーザ登録",
    description="システムに新しいユーザを登録する.",
    responses={
        **CommonResponses,
    },
)
def create_user(body: CreateUserRequest) -> UserResponse:
    """ユーザ登録."""
    user = User(
        id=1002,
        name=body.name,
        email=body.email,
        gender=body.gender,
    )

    return UserResponse(user=user)


@router.get(
    "/users/<user_id>",
    tags=["Users"],
    summary="ユーザ情報の取得",
    description="指定したユーザの情報を取得する.",
    responses={
        **CommonResponses,
    },
)
def get_user(user_id: int) -> UserResponse:
    """ユーザ情報の取得."""
    user = User(
        id=user_id,
        name="テストユーザ",
        email="test@example.com",
        gender=Gender.male,
    )

    return UserResponse(user=user)


@router.put(
    "/users/<user_id>",
    tags=["Users"],
    summary="ユーザ更新",
    description="指定したユーザの情報を更新する.",
    responses={
        **CommonResponses,
    },
)
def update_user(user_id: int, body: UpdateUserRequest) -> UserResponse:
    """ユーザ更新."""
    user = User(
        id=user_id,
        name=body.name,
        email=body.email,
        gender=body.gender,
    )

    return UserResponse(user=user)


@router.delete(
    "/users/<user_id>",
    tags=["Users"],
    summary="ユーザ削除",
    description="指定したユーザをシステムから削除する.",
    responses={
        http.HTTPStatus.NOT_FOUND: NotFoundResponse,
        **CommonResponses,
    },
)
def delete_user(user_id: int) -> dict:
    """ユーザ削除."""
    return {
        "message": f"user {user_id} deleted",
    }
