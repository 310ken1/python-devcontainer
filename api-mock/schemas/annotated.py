"""型定義."""

from enum import Enum
from typing import Annotated

from pydantic import EmailStr, Field


class Gender(str, Enum):
    """性別."""

    male = "男性"
    female = "女性"
    unknown = "その他"


UserId = Annotated[
    int,
    Field(
        description="ユーザID",
        examples=[1001],
        ge=0,
        le=9999,
    ),
]
UserName = Annotated[
    str,
    Field(
        description="氏名",
        examples=["山田太郎"],
        min_length=1,
        max_length=20,
    ),
]

UserEmail = Annotated[
    EmailStr,
    Field(
        description="メールアドレス",
        examples=["yamada@example.com"],
        min_length=6,
        max_length=254,
    ),
]

UserGender = Annotated[
    Gender,
    Field(
        description="性別",
        examples=["男性"],
    ),
]
