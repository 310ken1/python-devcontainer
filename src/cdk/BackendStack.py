"""."""

from typing import Any

from aws_cdk import CfnOutput, Environment, Stack, aws_apigateway, aws_lambda
from constructs import Construct


class BackendStack(Stack):
    """_summary_.

    Args:
        Stack (_type_): _description_
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs: dict[str, Any]) -> None:
        """_summary_.

        Args:
            scope (Construct): _description_
            construct_id (str): _description_
            kwargs (dict[str, Any]): _description_
        """
        super().__init__(
            scope,
            construct_id,
            env=Environment(
                region="ap-northeast-1",
            ),
            **kwargs,
        )

        lambda_sample = aws_lambda.Function(
            self,
            "LambdaSample",
            code=aws_lambda.Code.from_asset("src/api/"),
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="get_user.lambda_handler",
            description="Lambda関数(Amazon API Gateway)サンプル.",
        )

        api = aws_apigateway.RestApi(
            self,
            "PythonDevcontainerAPI",
            rest_api_name="PythonDevcontainerAPI",
            description="CDKで構築されたAPI Gatewayサービス",
        )
        lambda_integration = aws_apigateway.LambdaIntegration(
            lambda_sample,
            proxy=True,
        )

        resource_user = api.root.add_resource("user")
        resource_user.add_method(
            "GET",
            lambda_integration,
            operation_name="GetUser",
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=api.url,
            description="The URL of the API Gateway Endpoint",
        )
