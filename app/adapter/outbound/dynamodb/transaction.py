from abc import ABC

from domain.external.transactional import ReversableOperation
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
