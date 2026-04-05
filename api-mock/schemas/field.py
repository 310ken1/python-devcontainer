"""型定義."""

from enum import Enum
from typing import Annotated

from pydantic import EmailStr, Field


class Gender(str, Enum):
    """性別."""

    male = "male"
    female = "female"
    unknown = "unknown"


UserIdField = Annotated[
    int,
    Field(
        description="ユーザID",
        examples=[1001],
        ge=0,
        le=9999,
    ),
]

UserNameField = Annotated[
    str,
    Field(
        description="氏名",
        examples=["山田太郎"],
        min_length=1,
        max_length=20,
    ),
]

EmailField = Annotated[
    EmailStr,
    Field(
        description="メールアドレス",
        examples=["yamada@example.com"],
        min_length=6,
        max_length=254,
    ),
]

GenderField = Annotated[
    Gender | None,
    Field(
        description="性別(male=男性, female=女性, unknown=その他)",
        examples=["male"],
    ),
]
