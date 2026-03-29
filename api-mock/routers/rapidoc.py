"""Rapidocルータ."""

from pathlib import Path

from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.api_gateway import Router

router = Router()


@router.get("/rapidoc", include_in_schema=False)
def rapidoc():  # noqa: ANN201
    """Rapidoc形式のOpenAPI仕様."""
    with Path("rapidoc/index.html").open(encoding="utf-8") as f:
        html = f.read()
    return Response(
        status_code=200,
        content_type="text/html",
        body=html,
    )


@router.get("/rapidoc/<path>", include_in_schema=False)
def rapidoc_assets(path: str):  # noqa: ANN201
    """rapidoc-min.js配信用."""
    with Path(f"rapidoc/{path}").open("r") as f:
        return Response(
            status_code=200,
            content_type="application/javascript",
            body=f.read(),
        )
