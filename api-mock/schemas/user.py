"""ユーザスキーマ定義."""

from pydantic import BaseModel

from schemas.field import EmailField, GenderField, UserIdField, UserNameField


class User(BaseModel):
    """ユーザ情報."""

    id: UserIdField
    name: UserNameField
    email: EmailField
    gender: GenderField


class UserQuery(BaseModel):
    """ユーザ問い合わせ情報."""

    id: UserIdField
