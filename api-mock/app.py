"""APIモック."""

from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.openapi.models import Server
from aws_lambda_powertools.utilities.typing import LambdaContext

from routers.rapidoc import router as rapidoc_router
from routers.users import router as users_router

app = APIGatewayRestResolver()
app.enable_swagger(
    path="/swagger",
    title="APIモック",
    description="開発用APIモック",
    version="1.0.0",
    servers=[Server(url="http://127.0.0.1:3000/", description="APIモック")],
)
app.include_router(users_router)
app.include_router(rapidoc_router)


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """ラムダハンドラ."""
    return app.resolve(event, context)
