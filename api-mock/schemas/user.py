"""ユーザスキーマ定義."""

from pydantic import BaseModel

from schemas.annotated import UserEmail, UserGender, UserId, UserName


class User(BaseModel):
    """ユーザ情報."""

    id: UserId
    name: UserName
    email: UserEmail
    gender: UserGender | None = None


class UserQuery(BaseModel):
    """ユーザ問い合わせ情報."""

    id: UserId
