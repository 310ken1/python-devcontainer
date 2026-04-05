"""ユーザスキーマ定義."""

from pydantic import BaseModel

from schemas.field import EmailField, GenderField, UserIdField, UserNameField


class User(BaseModel):
    """ユーザ情報."""

    id: UserIdField
    name: UserNameField
    email: EmailField
    gender: GenderField = None


class UserQuery(BaseModel):
    """ユーザ問い合わせ情報."""

    id: UserIdField


class CreateUserRequest(BaseModel):
    """ユーザ作成リクエスト."""

    name: UserNameField
    email: EmailField
    gender: GenderField = None


class UpdateUserRequest(BaseModel):
    """ユーザ更新リクエスト."""

    name: UserNameField
    email: EmailField
    gender: GenderField = None


class UserResponse(BaseModel):
    """ユーザレスポンス."""

    user: User


class UserListResponse(BaseModel):
    """ユーザリストレスポンス."""

    users: list[User]
