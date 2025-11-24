"""Lambda関数(Amazon API Gateway)サンプルテスト."""

import importlib
import json
import os
from dataclasses import dataclass
from unittest import mock

import boto3
import pytest
from aws_lambda_powertools.utilities import parameters
from moto import mock_aws


@dataclass
class LambdaContext:
    function_name: str = "test"
    memory_limit_in_mb: int = 128
    invoked_function_arn: str = "test"
    aws_request_id: str = "test"


mock_template: dict = {
    "ssm": {
        "db": {
            "user": "postgres",
            "host": "postgres",
            "database": "postgres",
            "port": 5432,
            "password": "postgres",
        },
    },
}
event_template: dict = {
    "headers": {},
    "multiValueHeaders": {},
    "isBase64Encoded": False,
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "body": {"id": 1},
}
expected_template: dict = {
    "response": {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {
            "user_id": 1,
            "email": "user_a@example.com",
            "username": "User A",
            "display_name": "User A",
        },
    },
}
excepted_400_template: dict = {
    "response": {
        "statusCode": 400,
        "body": {"error": "Bad Request"},
    },
}
excepted_500_template: dict = {
    "response": {
        "statusCode": 500,
        "body": {"error": "Internal Server Error"},
    },
}

test_cases: dict = {
    "正常": [
        # mock
        mock_template,
        # event
        event_template,
        # expected
        expected_template,
    ],
    "異常 400": [
        # mock
        mock_template,
        # event
        event_template | {"body": {"id": "invalid"}},
        # expected
        excepted_400_template,
    ],
    "異常 500": [
        # mock
        mock_template | {"ssm": {"db": None}},
        # event
        event_template,
        # expected
        excepted_500_template,
    ],
}


@pytest.mark.parametrize(
    ("mock", "event", "expected"),
    list(test_cases.values()),
    ids=list(test_cases.keys()),
)
@mock.patch.dict(
    os.environ,
    {
        "POWERTOOLS_TRACE_DISABLED": "true",
        "AWS_REGION": "ap-northeast-1",
        "AWS_DEFAULT_REGION": "ap-northeast-1",
    },
    clear=False,
)
def test_user(mock: dict, event: dict, expected: dict) -> None:
    """lambda_handlerの単体テスト."""
    lambda_event = event.copy()
    if isinstance(event["body"], dict):
        lambda_event["body"] = json.dumps(event["body"])
    lambda_exception = expected.copy()
    if isinstance(expected["response"]["body"], dict):
        lambda_exception["response"]["body"] = json.dumps(expected["response"]["body"])

    parameters.clear_caches()
    with mock_aws():
        ssm = boto3.client("ssm")
        ssm.put_parameter(
            Name="/python-devcontainer/dev/settings",
            Value=json.dumps(mock["ssm"]),
            Type="String",
            Overwrite=True,
        )

        import api.get_user  # noqa: PLC0415

        importlib.reload(api.get_user)

        response = api.get_user.lambda_handler(lambda_event, LambdaContext())
        assert response == lambda_exception["response"]
