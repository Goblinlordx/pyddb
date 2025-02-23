from typing import Any

from adapter.outbound.dynamodb.serialize import python_to_dynamo
from adapter.outbound.dynamodb.transaction import DynamoDBOp
from domain.user.model import User

# from mypy_boto3_dynamodb.type_defs import TransactWriteItemTypeDef


class DynamoDBUserCreateOp(DynamoDBOp):
    def __init__(self, user: User) -> None:
        self._user = user

    def up(self) -> list[Any]:
        return [
            {
                "Put": {
                    "TableName": "test-tx-st",
                    "Item": python_to_dynamo(
                        {
                            "PK": f"USER#{self._user.id}",
                            "SK": f"USER#{self._user.id}",
                            **self._user.__dict__,
                        }
                    ),
                    "ConditionExpression": "(attribute_not_exists(PK) AND attribute_not_exists(SK))",
                }
            },
            {
                "Put": {
                    "TableName": "test-tx-st",
                    "Item": python_to_dynamo(
                        {
                            "PK": "USER#CONSTRAINT#BY_EMAIL",
                            "SK": f"{self._user.email}",
                        }
                    ),
                    "ConditionExpression": "(attribute_not_exists(PK) AND attribute_not_exists(SK))",
                }
            },
        ]

    def down(self) -> list[Any]:
        return [
            {
                "Delete": {
                    "TableName": "test-tx-st",
                    "Key": python_to_dynamo(
                        {
                            "PK": f"USER#{self._user.id}",
                            "SK": f"USER#{self._user.id}",
                        }
                    ),
                }
            },
            {
                "Delete": {
                    "TableName": "test-tx-st",
                    "Key": python_to_dynamo(
                        {
                            "PK": "USER#CONSTRAINT#BY_EMAIL",
                            "SK": f"{self._user.email}",
                        }
                    ),
                }
            },
        ]


class DynamoDBUserDeleteOp(DynamoDBOp):
    def __init__(self, user: User) -> None:
        self._user = user

    def up(self) -> list[Any]:
        return [
            {
                "Delete": {
                    "TableName": "test-tx-st",
                    "Key": python_to_dynamo(
                        {
                            "PK": f"USER#{self._user.id}",
                            "SK": f"USER#{self._user.id}",
                        }
                    ),
                }
            },
            {
                "Delete": {
                    "TableName": "test-tx-st",
                    "Key": python_to_dynamo(
                        {
                            "PK": "USER#CONSTRAINT#BY_EMAIL",
                            "SK": f"{self._user.email}",
                        }
                    ),
                }
            },
        ]

    def down(self) -> list[Any]:
        return [
            {
                "Put": {
                    "TableName": "test-tx-st",
                    "Item": python_to_dynamo(
                        {
                            "PK": f"USER#{self._user.id}",
                            "SK": f"USER#{self._user.id}",
                            **self._user.__dict__,
                        }
                    ),
                    "ConditionExpression": "(attribute_not_exists(PK) AND attribute_not_exists(SK))",
                }
            },
            {
                "Put": {
                    "TableName": "test-tx-st",
                    "Item": python_to_dynamo(
                        {
                            "PK": "USER#CONSTRAINT#BY_EMAIL",
                            "SK": f"{self._user.email}",
                        }
                    ),
                    "ConditionExpression": "(attribute_not_exists(PK) AND attribute_not_exists(SK))",
                }
            },
        ]
