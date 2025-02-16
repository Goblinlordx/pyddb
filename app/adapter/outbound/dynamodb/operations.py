from abc import ABC

from adapter.outbound.dynamodb.serialize import python_to_dynamo
from domain.external.transactional import ReversableOperation
from domain.user.model import User
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_dynamodb.type_defs import TransactWriteItemTypeDef


class DynamoDBOp(ABC):
    def up(self) -> list[TransactWriteItemTypeDef]: ...
    def down(self) -> list[TransactWriteItemTypeDef]: ...


class DynamoDBTransactOps(ReversableOperation):
    def __init__(self, client: DynamoDBClient, ops: list[DynamoDBOp]):
        self._client = client
        self._ops = ops

    def up(self):
        if self._ops:
            self._client.transact_write_items(
                TransactItems=[item for op in self._ops for item in op.up()]
            )

    def down(self):
        if self._ops:
            self._client.transact_write_items(
                TransactItems=[item for op in reversed(self._ops) for item in op.down()]
            )


class DynamoDBUserCreateOp(DynamoDBOp):
    def __init__(self, user: User) -> None:
        self._user = user

    def up(self) -> list[TransactWriteItemTypeDef]:
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
            }
        ]

    def down(self) -> list[TransactWriteItemTypeDef]:
        return [
            {
                "Delete": {
                    "TableName": "test-tx-st",
                    "Key": {
                        "PK": {"S": f"USER#{self._user.id}"},
                        "SK": {"S": f"USER#{self._user.id}"},
                    },
                }
            }
        ]


class DynamoDBUserDeleteOp(DynamoDBOp):
    def __init__(self, user: User) -> None:
        self._user = user

    def up(self) -> list[TransactWriteItemTypeDef]:
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
            }
        ]

    def down(self) -> list[TransactWriteItemTypeDef]:
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
            }
        ]
