"""エラースキーマ定義."""

from pydantic import BaseModel


class ApiError(BaseModel):
    """APIエラー."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """APIエラーレスポンス."""

    error: ApiError


UnauthorizedResponse = {
    "description": "認証エラー",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "認証エラー": {
                    "value": {
                        "error": {
                            "code": "401",
                            "message": "Unauthorized",
                        },
                    },
                },
            },
        },
    },
}

InternalServerErrorResponse = {
    "description": "内部サーバエラー",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "内部サーバエラー": {
                    "value": {
                        "error": {
                            "code": "500",
                            "message": "Internal Server Error",
                        },
                    },
                },
            },
        },
    },
}
