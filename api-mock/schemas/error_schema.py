"""エラースキーマ定義."""

import http

from aws_lambda_powertools.event_handler.openapi.types import (
    OpenAPIResponse,
)
from pydantic import BaseModel


class ApiError(BaseModel):
    """APIエラー."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """APIエラーレスポンス."""

    error: ApiError


# 400 Bad Request
BadRequestResponse: OpenAPIResponse = {
    "description": "リクエスト不正",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "リクエスト不正": {
                    "value": {
                        "error": {
                            "code": "400",
                            "message": "Bad Request",
                        },
                    },
                },
            },
        },
    },
}

# 401 Unauthorized
UnauthorizedResponse: OpenAPIResponse = {
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

# 403 Forbidden
ForbiddenResponse: OpenAPIResponse = {
    "description": "アクセス権限エラー",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "アクセス権限エラー": {
                    "value": {
                        "error": {
                            "code": "403",
                            "message": "Forbidden",
                        },
                    },
                },
            },
        },
    },
}

# 404 Not Found
NotFoundResponse: OpenAPIResponse = {
    "description": "リソースが存在しない",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "リソース未存在": {
                    "value": {
                        "error": {
                            "code": "404",
                            "message": "Not Found",
                        },
                    },
                },
            },
        },
    },
}

# 409 Conflict
ConflictResponse: OpenAPIResponse = {
    "description": "リソース競合",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "リソース競合": {
                    "value": {
                        "error": {
                            "code": "409",
                            "message": "Conflict",
                        },
                    },
                },
            },
        },
    },
}

# 422 Unprocessable Entity
UnprocessableEntityResponse: OpenAPIResponse = {
    "description": "バリデーションエラー",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "バリデーションエラー": {
                    "value": {
                        "error": {
                            "code": "422",
                            "message": "Unprocessable Entity",
                        },
                    },
                },
            },
        },
    },
}

# 429 Too Many Requests
TooManyRequestsResponse: OpenAPIResponse = {
    "description": "リクエスト過多",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "リクエスト過多": {
                    "value": {
                        "error": {
                            "code": "429",
                            "message": "Too Many Requests",
                        },
                    },
                },
            },
        },
    },
}

# 500 Internal Server Error
InternalServerErrorResponse: OpenAPIResponse = {
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

# 503 Service Unavailable
ServiceUnavailableResponse: OpenAPIResponse = {
    "description": "サービス利用不可",
    "content": {
        "application/json": {
            "model": ErrorResponse,
            "examples": {
                "サービス利用不可": {
                    "value": {
                        "error": {
                            "code": "503",
                            "message": "Service Unavailable",
                        },
                    },
                },
            },
        },
    },
}

# 共通エラーレスポンス
CommonResponses: dict[http.HTTPStatus, OpenAPIResponse] = {
    http.HTTPStatus.BAD_REQUEST: BadRequestResponse,
    http.HTTPStatus.UNAUTHORIZED: UnauthorizedResponse,
    http.HTTPStatus.FORBIDDEN: ForbiddenResponse,
    http.HTTPStatus.UNPROCESSABLE_ENTITY: UnprocessableEntityResponse,
    http.HTTPStatus.INTERNAL_SERVER_ERROR: InternalServerErrorResponse,
    http.HTTPStatus.SERVICE_UNAVAILABLE: ServiceUnavailableResponse,
}
